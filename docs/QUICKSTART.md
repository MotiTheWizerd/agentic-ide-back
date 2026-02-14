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
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/agentic-ide
AUTH_SECRET_KEY=secret-me
PORT=8000
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
│       │   └── projects.py          # POST/POST-select/GET/DELETE /api/v1/projects
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
    └── projects/
        ├── manager.py               # Project business logic
        └── handlers.py              # @subscribe handlers for project events
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
- **google-adk** - Google ADK (reserved for future use)
