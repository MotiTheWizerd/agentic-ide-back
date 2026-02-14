# Session Summary — 2026-02-14 (Session 5)

## What Was Done

### Event-Driven Execution Engine (Phases 1–4)

Ported the graph execution pipeline from the browser (`runner.ts`) to the FastAPI backend using an **event-driven architecture**. The runner emits domain events via the existing `EventBus`; separate `@subscribe` handlers bridge those events to WebSocket for real-time frontend updates.

**Key design decisions:**
- **Runner is transport-agnostic** — `runner.py` never imports WebSocket. It only emits events via `EventBus`. Handlers in `handlers.py` catch those events and push `WSMessage` to the user's WS connection.
- **Level-based parallel execution** — nodes are grouped by topological level; all nodes at the same level run concurrently via `asyncio.gather`.
- **Fire-and-forget** — `ExecutionManager.run()` spawns a background `asyncio.create_task` and returns `run_id` immediately.
- **Executors are plain async functions** — `async def(ctx: NodeExecutionContext) -> NodeOutput`, registered in a dict.
- **Prompt templates return message lists** — `list[dict]` in OpenAI chat format so providers can handle system messages differently (e.g., Claude separates system from user messages).
- **Lazy provider init** — providers initialize on first call, not at boot time.

### What Was Implemented

1. **Graph Engine** — Kahn's topological sort with cycle detection, edge classification (text vs adapter by `targetHandle` prefix), BFS upstream/downstream traversal, level grouping for parallel execution
2. **9 Executors** — `consistentCharacter`, `sceneBuilder`, `textOutput` (data/output, no API), `initialPrompt`, `promptEnhancer`, `translator`, `storyTeller`, `grammarFix`, `compressor` (text processing, calls LLM providers)
3. **5 Text Provider Clients** — Mistral, GLM, OpenRouter, HuggingFace (all via single `AsyncOpenAI` compat client) + Claude (via `AsyncAnthropic`)
4. **6 Prompt Templates** — enhance, translate, storyteller, grammar_fix, compress, inject_persona
5. **8 Event Types** — `execution.started/completed/failed`, `node.pending/running/completed/failed/skipped`
6. **8 WS Handlers** — one `@subscribe` handler per event type, auto-discovered at boot
7. **2 Trigger Mechanisms** — REST `POST /api/v1/execution/run` + WS `execution.start` message

## Files Created (25 new + 1 endpoint)

```
app/modules/execution/
├── __init__.py
├── manager.py                  # ExecutionManager — auto-discovered singleton
├── handlers.py                 # @subscribe → ws_manager.send_to_user() (8 handlers)
├── models.py                   # ExecutionStep, NodeOutput, NodeExecutionContext, ResolvedModel, etc.
├── runner.py                   # topo sort → level grouping → asyncio.gather → event emit
├── graph/
│   ├── __init__.py
│   ├── topological_sort.py     # Kahn's algorithm + group_by_levels()
│   ├── edge_classification.py  # get_text_input_node_ids / get_adapter_input_node_ids
│   └── traversal.py            # get_upstream_nodes / get_downstream_nodes (BFS)
├── executors/
│   ├── __init__.py
│   ├── registry.py             # EXECUTORS dict with 9 entries
│   ├── base.py                 # ExecutorFn type alias
│   ├── utils.py                # merge_input_text, extract_personas, LANGUAGE_NAMES (28 langs)
│   ├── data_sources.py         # consistent_character, scene_builder
│   ├── text_processing.py      # initial_prompt, prompt_enhancer, translator, story_teller, grammar_fix, compressor
│   └── output.py               # text_output
├── providers/
│   ├── __init__.py
│   ├── base.py                 # TextProvider protocol
│   ├── openai_compat.py        # Single AsyncOpenAI client for Mistral/GLM/OpenRouter/HF
│   ├── claude.py               # AsyncAnthropic client
│   └── registry.py             # get_text_provider() with lazy init
├── prompts/
│   ├── __init__.py
│   ├── enhance.py              # build_enhance_messages(text, notes?)
│   ├── translate.py            # build_translate_messages(text, language)
│   ├── storyteller.py          # build_storyteller_messages(text, tags?)
│   ├── grammar_fix.py          # build_grammar_fix_messages(text, style?)
│   ├── compress.py             # build_compress_messages(text)
│   └── inject_persona.py       # build_inject_persona_messages(personas, prompt_text)
└── config/
    ├── __init__.py
    ├── model_defaults.py       # NODE_MODEL_DEFAULTS + resolve_model_for_node()
    └── scene_prompts.py        # SCENE_PROMPT_BLOCKS + compose_scene_prompt()

app/api/v1/endpoints/
└── execution.py                # POST /api/v1/execution/run (auto-discovered)
```

## Files Modified (3)

| File | Change |
|------|--------|
| `app/core/events/types.py` | Added 8 execution event constants (EXECUTION_STARTED/COMPLETED/FAILED, NODE_PENDING/RUNNING/COMPLETED/FAILED/SKIPPED) |
| `app/api/v1/endpoints/ws.py` | Added `execution.start` WS message handler + imports for ExecutionManager and registry |
| `pyproject.toml` | Added `openai (>=1.0.0,<2.0.0)` and `anthropic (>=0.40.0,<1.0.0)` dependencies |

## WebSocket Protocol (Execution)

### Trigger

```json
{ "type": "execution.start", "data": { "flow_id": "...", "nodes": [...], "edges": [...], "provider_id": "mistral", "trigger_node_id": null, "cached_outputs": null } }
```

### Events

| Direction | type | data |
|-----------|------|------|
| Server → Client | `execution.started` | `{ run_id }` |
| Server → Client | `execution.node.status` | `{ run_id, node_id, status: "pending"/"running"/"skipped" }` |
| Server → Client | `execution.node.completed` | `{ run_id, node_id, output: NodeOutput }` |
| Server → Client | `execution.node.failed` | `{ run_id, node_id, error }` |
| Server → Client | `execution.completed` | `{ run_id, outputs: Record<nodeId, NodeOutput> }` |
| Server → Client | `execution.failed` | `{ run_id, error }` |

## Model Resolution Priority

1. Node-level override (`node_data.providerId` + `node_data.model`)
2. Node-type default (`NODE_MODEL_DEFAULTS[nodeType]`)
3. Flow-level provider (`provider_id` from request)

## New Dependencies

- `openai >= 1.0.0` — AsyncOpenAI for Mistral, GLM, OpenRouter, HuggingFace
- `anthropic >= 0.40.0` — AsyncAnthropic for Claude

## Not Built Yet (Deferred to Future Sessions)

- Image processing executors (`imageDescriber`, `imageGenerator`, `personasReplacer`)
- Image provider clients (HuggingFace FLUX, GLM-Image)
- Image prompt templates (`describe.py`, `replace.py`, `generate_image.py`)
- Image utilities (Pillow-based resize/compress)
- Server-side caching by input hash
- Per-user rate limiting
- `execution.cancel` support
