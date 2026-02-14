# Quickstart

## Prerequisites

- Python 3.11+
- Poetry
- PostgreSQL

## Install

```bash
poetry install
```

## Environment

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/agentic-ai-db
AUTH_SECRET_KEY=secret-me
PORT=8000
MISTRAL_API_KEY=your-key
GLM_API_KEY=your-key
OPENROUTER_API_KEY=your-key
HF_API_KEY=your-key
ANTHROPIC_API_KEY=your-key      # Optional — only needed if using Claude provider
FIREWORKS_API_KEY=your-key      # Required for Black Forest Labs Flux image generation
```

## Run

```bash
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Project Structure

```
app/
├── main.py                          # FastAPI app + lifespan + CORS + boot sequence
├── api/
│   └── v1/
│       ├── router.py                # v1 router (auto-discovers all endpoint routers)
│       ├── endpoints/               # Drop a file here → auto-discovered
│       │   ├── auth.py              # POST /auth/login, POST /auth/refresh
│       │   ├── backoffice_auth.py   # POST /auth/backoffice/create, POST /auth/backoffice/login
│       │   ├── users.py             # POST/GET/DELETE /api/v1/users
│       │   ├── projects.py          # POST/POST-select/GET/DELETE /api/v1/projects
│       │   ├── execution.py         # POST /api/v1/execution/run — trigger graph execution
│       │   └── ws.py                # WebSocket /api/v1/ws — global real-time tunnel
│       └── schemas/
│           ├── auth.py              # LoginRequest, TokenResponse, RefreshRequest
│           ├── backoffice_auth.py   # BackofficeLoginRequest, BackofficeTokenResponse, BackofficeUserCreate, BackofficeUserResponse
│           ├── user.py              # UserCreate, UserResponse
│           └── project.py           # ProjectCreate, ProjectSelectByUser, ProjectResponse
├── core/
│   ├── security.py                  # bcrypt hashing + JWT token create/decode
│   ├── auth.py                      # get_current_user dependency (Bearer token)
│   ├── db/
│   │   ├── base.py                  # SQLAlchemy async engine + Base (reads DATABASE_URL from .env)
│   │   └── dependency.py            # get_db FastAPI dependency
│   ├── di/
│   │   ├── registry.py              # ServiceRegistry — singleton DI container
│   │   └── discovery.py             # Auto-discovery: routers, managers, event handlers
│   ├── events/
│   │   ├── base.py                  # Event base model (pydantic)
│   │   ├── types.py                 # EventTypes — single source of truth for all event names
│   │   └── subscribe.py             # @subscribe decorator for event handlers
│   ├── bus/
│   │   └── event_bus.py             # Async event bus (on/off/emit) + auto-persist to event_logs
│   ├── ws/
│   │   ├── models.py                # WSMessage pydantic model (type + data envelope)
│   │   └── manager.py              # ConnectionManager — track connections, send_to_user, broadcast
│   └── logger/
│       └── setup.py                 # Logging configuration
├── models/
│   ├── user.py                      # User SQLAlchemy model
│   ├── backoffice_user.py           # BackofficeUser SQLAlchemy model
│   ├── project.py                   # Project SQLAlchemy model (FK → users)
│   ├── agentic_component.py         # AgenticComponent model (node type blueprints)
│   ├── component_field.py           # ComponentField model (configurable fields per component)
│   ├── component_port.py            # ComponentPort model (input/output handles)
│   ├── component_api_config.py      # ComponentApiConfig model (execution/API mapping)
│   ├── component_output_schema.py   # ComponentOutputSchema model (what each node produces)
│   ├── flow.py                      # Flow model (user pipelines with graph_data JSON)
│   ├── consistent_character.py      # ConsistentCharacter model (persona data)
│   └── event_log.py                 # EventLog model (persisted event audit trail)
└── modules/                         # Drop a module here → manager + handlers auto-discovered
    ├── users/
    │   ├── manager.py               # User business logic
    │   └── handlers.py              # @subscribe handlers for user events
    ├── projects/
    │   ├── manager.py               # Project business logic
    │   └── handlers.py              # @subscribe handlers for project events
    └── execution/                   # Graph execution engine (event-driven)
        ├── manager.py               # ExecutionManager — entry point, fire-and-forget via asyncio.create_task
        ├── handlers.py              # 8 @subscribe handlers → bridge events to WebSocket
        ├── models.py                # ExecutionStep, NodeOutput, NodeExecutionContext, ResolvedModel
        ├── runner.py                # Orchestration: topo sort → level grouping → parallel exec → event emit
        ├── graph/
        │   ├── topological_sort.py  # Kahn's algorithm + group_by_levels() for parallel branches
        │   ├── edge_classification.py # Text vs adapter edge filtering
        │   └── traversal.py         # BFS upstream/downstream
        ├── executors/
        │   ├── registry.py          # EXECUTORS dict: node_type → async executor function (9 registered)
        │   ├── base.py              # ExecutorFn type alias
        │   ├── utils.py             # merge_input_text, extract_personas, LANGUAGE_NAMES
        │   ├── data_sources.py      # consistent_character, scene_builder
        │   ├── text_processing.py   # initialPrompt, promptEnhancer, translator, storyTeller, grammarFix, compressor
        │   └── output.py            # textOutput
        ├── providers/
        │   ├── base.py              # TextProvider protocol
        │   ├── openai_compat.py     # AsyncOpenAI (Mistral, GLM, OpenRouter, HuggingFace)
        │   ├── claude.py            # AsyncAnthropic
        │   └── registry.py          # get_text_provider() lazy factory
        ├── prompts/
        │   ├── enhance.py           # Prompt enhancement (with/without notes)
        │   ├── translate.py         # Translation
        │   ├── storyteller.py       # Creative narrative (temp 0.95)
        │   ├── grammar_fix.py       # Grammar correction (optional style)
        │   ├── compress.py          # Text compression
        │   └── inject_persona.py    # Character persona injection
        └── config/
            ├── model_defaults.py    # NODE_MODEL_DEFAULTS + resolve_model_for_node()
            └── scene_prompts.py     # SCENE_PROMPT_BLOCKS + compose_scene_prompt()
scripts/
└── seed_components.py               # Seed script for all 13 component types + related data
```

## Boot Sequence

On startup, the app automatically:
1. Configures logging
2. Auto-discovers routers from `app/api/v1/endpoints/`
3. Auto-discovers and registers managers from `app/modules/*/manager.py` as singletons
4. Auto-discovers and subscribes event handlers from `app/modules/*/handlers.py`

## Adding a New Module (Zero Wiring)

1. Create `app/api/v1/endpoints/flows.py` with `router = APIRouter(prefix="/flows", tags=["flows"])` — auto-discovered
2. Create `app/modules/flows/manager.py` with `class FlowManager` — auto-registered as singleton
3. Create `app/modules/flows/handlers.py` with `@subscribe` handlers — auto-subscribed
4. Done. No manual imports or registration needed.

To use a manager in an endpoint:
```python
from app.core.di import registry
from app.modules.flows.manager import FlowManager

manager: FlowManager = Depends(registry.get(FlowManager))
```

## Database

PostgreSQL (async via asyncpg). Connection string read from `.env`.

### Migrations

```bash
# Generate a migration
alembic revision --autogenerate -m "describe change"

# Apply migrations
alembic upgrade head
```

### Seeding

```bash
# Seed all 13 agentic component types (idempotent — safe to re-run)
python -m scripts.seed_components
```

## Database Schema

### Core Tables

| Table | PK | Description |
|-------|-----|-------------|
| `users` | int | App users |
| `projects` | int | User projects (FK → users) |
| `backoffice_users` | int | Admin users |

### Agentic Components Tables

| Table | PK | Description |
|-------|-----|-------------|
| `agentic_components` | UUID | Node type blueprints (13 types seeded) |
| `component_fields` | UUID | Configurable fields per component (FK → agentic_components) |
| `component_ports` | UUID | Input/output handles per component (FK → agentic_components) |
| `component_api_config` | UUID | Execution/API mapping per component (FK → agentic_components) |
| `component_output_schema` | UUID | Output schema per component (FK → agentic_components) |

### Flow & Character Tables

| Table | PK | Description |
|-------|-----|-------------|
| `flows` | UUID | User pipelines — graph_data JSON holds nodes + edges + viewport (FK → users, projects) |
| `consistent_characters` | UUID | Reusable character personas (FK → users, projects) |

### Event Tables

| Table | PK | Description |
|-------|-----|-------------|
| `event_logs` | UUID | Persisted event audit trail (event_name, payload JSON, user_id FK, project_id FK nullable, session_id nullable) |

## Event System

Events use typed constants and auto-discovered handlers:

```python
# Define event type (app/core/events/types.py)
class EventTypes:
    PROJECT_CREATED = "project.created"

# Emit from a manager
await event_bus.emit(Event(type=EventTypes.PROJECT_CREATED, payload={...}))

# Handle with @subscribe (app/modules/projects/handlers.py)
@subscribe(EventTypes.PROJECT_CREATED)
async def on_project_created(event: Event) -> None:
    ...
```

Every emitted event is automatically persisted to the `event_logs` table.

## WebSocket Tunnel

Global persistent WebSocket connection for all real-time communication.

### Connection

```
ws://localhost:8000/api/v1/ws?token=<JWT_ACCESS_TOKEN>
```

- One connection per client session
- JWT passed as query param (validated on connect, rejected with 4001 if invalid)
- Auto-reconnect is the client's responsibility

### Message Envelope (both directions)

```json
{ "type": "domain.action", "data": { ... } }
```

### Current Messages

| Direction | type | data | Description |
|-----------|------|------|-------------|
| Server → Client | `connection.ready` | `{ "user_id": int }` | Sent after successful auth |
| Client → Server | `ping` | `{}` | Keep-alive |
| Server → Client | `pong` | `{}` | Keep-alive response |

### Execution Messages

| Direction | type | data | Description |
|-----------|------|------|-------------|
| Client → Server | `execution.start` | `{ flow_id, nodes, edges, provider_id, trigger_node_id?, cached_outputs? }` | Trigger graph execution |
| Server → Client | `execution.started` | `{ run_id }` | Run accepted |
| Server → Client | `execution.node.status` | `{ run_id, node_id, status }` | Node pending/running/skipped |
| Server → Client | `execution.node.completed` | `{ run_id, node_id, output }` | Node finished with output |
| Server → Client | `execution.node.failed` | `{ run_id, node_id, error }` | Node errored |
| Server → Client | `execution.completed` | `{ run_id, outputs }` | All nodes done |
| Server → Client | `execution.failed` | `{ run_id, error }` | Fatal error (cycle, etc.) |

### Sending from anywhere in the backend

```python
from app.core.ws import ws_manager, WSMessage

# Send to a specific user
await ws_manager.send_to_user(user_id, WSMessage(type="some.event", data={...}))

# Broadcast to all connected clients
await ws_manager.broadcast(WSMessage(type="system.notification", data={...}))
```

## Execution Engine

The execution engine runs graph workflows server-side with event-driven status updates.

### Architecture

```
Frontend → WS: execution.start → ExecutionManager.run() → asyncio.create_task
                                    |
                                    runner.py:
                                      topo sort → group by levels → asyncio.gather per level
                                      emit(NODE_PENDING/RUNNING/COMPLETED/FAILED) via EventBus
                                    |
                                  handlers.py (@subscribe):
                                    on_node_* → ws_manager.send_to_user()
                                    |
Frontend ← WS: execution.node.* ← Server
```

**Key principle**: `runner.py` never imports WebSocket. It only emits domain events. Handlers bridge to WS.

### Features

- **Parallel execution** — independent branches run concurrently via topological level grouping
- **Error propagation** — failed node → all downstream nodes skipped
- **Partial re-execution** — send `trigger_node_id` + `cached_outputs` to re-run from a specific node
- **Model resolution** — node override → node-type default → flow-level provider

### Registered Executors (9)

| Executor | Category | Makes API Call |
|----------|----------|----------------|
| `consistentCharacter` | Data Source | No |
| `sceneBuilder` | Data Source | No |
| `initialPrompt` | Text Processing | Yes (if adapters) |
| `promptEnhancer` | Text Processing | Yes |
| `translator` | Text Processing | Yes |
| `storyTeller` | Text Processing | Yes |
| `grammarFix` | Text Processing | Yes |
| `compressor` | Text Processing | Yes (if >2500 chars) |
| `textOutput` | Output | No |

### Text Providers

| Provider | SDK | Base URL |
|----------|-----|----------|
| Mistral | AsyncOpenAI | `https://api.mistral.ai/v1` |
| GLM | AsyncOpenAI | `https://api.z.ai/api/coding/paas/v4` |
| OpenRouter | AsyncOpenAI | `https://openrouter.ai/api/v1` |
| HuggingFace | AsyncOpenAI | `https://router.huggingface.co/v1` |
| Claude | AsyncAnthropic | Direct API |

## API Endpoints

| Method   | Path                              | Auth     | Description                                  |
|----------|-----------------------------------|----------|----------------------------------------------|
| `GET`    | `/api/v1/health`                  | No       | Health check                                 |
| `POST`   | `/api/v1/auth/login`             | No       | Login (email or username) → tokens + user    |
| `POST`   | `/api/v1/auth/refresh`           | No       | Refresh token → new token pair + user        |
| `POST`   | `/api/v1/auth/backoffice/create` | No       | Create backoffice user                       |
| `POST`   | `/api/v1/auth/backoffice/login`  | No       | Backoffice login (email or username) → tokens|
| `POST`   | `/api/v1/users`                  | No       | Create user                                  |
| `GET`    | `/api/v1/users/{id}`             | No       | Get user by ID                               |
| `DELETE` | `/api/v1/users/{id}`             | No       | Delete user                                  |
| `POST`   | `/api/v1/projects`               | No       | Create project                               |
| `POST`   | `/api/v1/projects/select`        | No       | Get projects by user_id                      |
| `GET`    | `/api/v1/projects/{id}`          | No       | Get project by ID                            |
| `DELETE` | `/api/v1/projects/{id}`          | No       | Delete project                               |
| `POST`   | `/api/v1/execution/run`          | Yes      | Trigger graph execution → returns run_id     |
| `WS`     | `/api/v1/ws?token=<JWT>`         | Yes      | WebSocket global tunnel                      |

## Authentication

JWT-based with refresh tokens:
- **Access token**: 30 min expiry
- **Refresh token**: 7 day expiry
- Login accepts `identifier` (email or username) + `password`
- Protect any route with: `current_user: User = Depends(get_current_user)`

## Key Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlalchemy + asyncpg** - Async ORM + PostgreSQL driver
- **alembic** - Database migrations
- **bcrypt** - Password hashing
- **python-jose[cryptography]** - JWT tokens
- **python-dotenv** - Environment variable loading
- **openai** - AsyncOpenAI client for Mistral, GLM, OpenRouter, HuggingFace
- **anthropic** - AsyncAnthropic client for Claude
- **google-adk** - Google ADK (reserved for future use)
