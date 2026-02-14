# Session Summary — 2026-02-14 (Session 4)

## What was done

### 1. New Machine Database Setup
- Database name changed to `agentic-ai-db` (was `agentic-ide`)
- Cleared stale `alembic_version` referencing deleted migration `3934f0046cba`
- Reset public schema (`DROP SCHEMA public CASCADE; CREATE SCHEMA public`)
- Ran `alembic upgrade head` — all 11 tables created via `76ab156db31b_initial_postgres_migration.py`
- Ran `python -m scripts.seed_components` — 13 components, 23 fields, 23 ports, 13 API configs, 18 output schemas seeded

### 2. Execution Engine Architecture Design
- Reviewed `execution_orchestration.md` — the full client-side pipeline documentation
- Decided against 1:1 port (for-loop on server) — chose **event-driven architecture** instead
- Key design decisions:
  - **Event-driven DAG execution**: edges define event subscriptions, pending counter per node, fire when all deps met
  - **Three decoupled layers**: Coordinator (brain) → Event Bus (nervous system) → Request Manager (I/O)
  - **Fire-and-poll pattern**: don't await API calls — fire request, poll for completion in batches
  - **Parallel branches are free**: independent nodes fire concurrently via concurrent `node.ready` events
  - All AI calls are external API providers (Mistral, Claude, HuggingFace, GLM) — server is pure I/O orchestration

### 3. WebSocket Global Tunnel
- Built a persistent, bidirectional WebSocket connection between client and server
- Serves as a **typed message bus** — all real-time communication flows through one tunnel
- Message envelope: `{ "type": "domain.action", "data": { ... } }` with dot-notation namespacing
- JWT authentication via query param on connect
- Connection manager tracks connections by user_id, supports `send_to_user` and `broadcast`
- Ping/pong keep-alive working end-to-end
- Auto-discovered by existing router discovery — zero wiring

## New files created this session
- `app/core/ws/__init__.py` — exports `ws_manager` + `WSMessage`
- `app/core/ws/models.py` — `WSMessage` pydantic model (type + data envelope)
- `app/core/ws/manager.py` — `ConnectionManager` (connect, disconnect, send_to_user, broadcast)
- `app/api/v1/endpoints/ws.py` — WebSocket endpoint with JWT auth + receive loop

## Files modified this session
- None (all new files)

## WebSocket Protocol

### Connection
```
ws://localhost:8000/api/v1/ws?token=<JWT>
```

### Message Envelope (both directions)
```json
{ "type": "string", "data": { } }
```

### Current Messages
| Direction | type | data |
|-----------|------|------|
| Server → Client | `connection.ready` | `{ "user_id": int }` |
| Client → Server | `ping` | `{}` |
| Server → Client | `pong` | `{}` |
| Server → Client | `error` | `{ "message": string }` |

### Future Messages (execution engine)
| Direction | type | data |
|-----------|------|------|
| Client → Server | `execution.start` | `{ flow_id, nodes, edges, ... }` |
| Client → Server | `execution.cancel` | `{ run_id }` |
| Server → Client | `execution.node.completed` | `{ run_id, node_id, output }` |
| Server → Client | `execution.node.failed` | `{ run_id, node_id, error }` |
| Server → Client | `execution.completed` | `{ run_id, outputs }` |

## Technical notes
- `receive_json()` hangs on Starlette/Windows — use raw `ws.receive()` + manual `json.loads()` instead
- WebSocket endpoint uses `APIRouter()` (no prefix) — auto-discovered and mounted under `/api/v1/ws`
- `ConnectionManager` is a module-level singleton (`ws_manager`), not registered in DI registry

## Next steps
- Build execution engine Phase 1: graph analysis (topo sort, edge classification, BFS traversal)
- Build `ExecutionRun` coordinator with event-driven node scheduling
- Build `RequestManager` for fire-and-poll pattern with external AI providers
- Wire execution events through the WebSocket tunnel
