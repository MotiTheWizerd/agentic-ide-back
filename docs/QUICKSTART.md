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
│       │   ├── users.py             # POST/GET/DELETE /api/v1/users
│       │   └── projects.py          # POST/GET/DELETE /api/v1/projects
│       └── schemas/
│           ├── auth.py              # LoginRequest, TokenResponse, RefreshRequest
│           ├── user.py              # UserCreate, UserResponse
│           └── project.py           # ProjectCreate, ProjectResponse
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
│   └── project.py                   # Project SQLAlchemy model (FK → users)
└── modules/
    ├── users/
    │   └── manager.py               # User business logic
    └── projects/
        ├── manager.py               # Project business logic
        └── dependency.py            # get_project_manager DI
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

## API Endpoints

| Method   | Path                      | Auth     | Description                          |
|----------|---------------------------|----------|--------------------------------------|
| `GET`    | `/api/v1/health`          | No       | Health check                         |
| `POST`   | `/api/v1/auth/login`      | No       | Login → access + refresh tokens + user |
| `POST`   | `/api/v1/auth/refresh`    | No       | Refresh token → new token pair + user  |
| `POST`   | `/api/v1/users`           | No       | Create user                          |
| `GET`    | `/api/v1/users/{id}`      | No       | Get user by ID                       |
| `DELETE` | `/api/v1/users/{id}`      | No       | Delete user                          |
| `POST`   | `/api/v1/projects`        | No       | Create project                       |
| `GET`    | `/api/v1/projects/{id}`   | No       | Get project by ID                    |
| `DELETE` | `/api/v1/projects/{id}`   | No       | Delete project                       |

## Authentication

JWT-based with refresh tokens:
- **Access token**: 30 min expiry
- **Refresh token**: 7 day expiry
- Protect any route with: `current_user: User = Depends(get_current_user)`

## Key Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlalchemy + aiosqlite** - Async ORM + SQLite driver
- **alembic** - Database migrations
- **bcrypt** - Password hashing
- **python-jose[cryptography]** - JWT tokens
- **google-adk** - Google ADK (reserved for future use)
