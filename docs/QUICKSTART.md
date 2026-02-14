# Quickstart

## Prerequisites

- Python 3.11+
- Poetry

## Install

```bash
poetry install
```

## Run

```bash
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

## Project Structure

```
app/
├── main.py                          # FastAPI app + lifespan + CORS
├── api/
│   └── v1/
│       ├── router.py                # v1 router aggregator
│       ├── endpoints/
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
│   │   ├── base.py                  # SQLAlchemy async engine + Base
│   │   └── dependency.py            # get_db FastAPI dependency
│   ├── events/
│   │   └── base.py                  # Event base model (pydantic)
│   ├── bus/
│   │   └── event_bus.py             # Async event bus (on/off/emit)
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
│   └── consistent_character.py      # ConsistentCharacter model (persona data)
└── modules/
    ├── users/
    │   └── manager.py               # User business logic
    └── projects/
        ├── manager.py               # Project business logic
        └── dependency.py            # get_project_manager DI
scripts/
└── seed_components.py               # Seed script for all 13 component types + related data
```

## Database

SQLite (async via aiosqlite). DB file: `app.db`

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
- **sqlalchemy + aiosqlite** - Async ORM + SQLite driver
- **alembic** - Database migrations
- **bcrypt** - Password hashing
- **python-jose[cryptography]** - JWT tokens
- **google-adk** - Google ADK (reserved for future use)
