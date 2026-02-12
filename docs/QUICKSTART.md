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
├── main.py                          # FastAPI app + lifespan
├── api/
│   └── v1/
│       ├── router.py                # v1 router aggregator
│       ├── endpoints/
│       │   └── users.py             # POST/GET/DELETE /api/v1/users
│       └── schemas/
│           └── user.py              # Pydantic request/response schemas
├── core/
│   ├── security.py                  # bcrypt password hashing
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
│   └── user.py                      # User SQLAlchemy model
└── modules/
    └── users/
        └── manager.py               # User business logic
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

| Method   | Path                   | Description     |
|----------|------------------------|-----------------|
| `GET`    | `/api/v1/health`       | Health check    |
| `POST`   | `/api/v1/users`        | Create user     |
| `GET`    | `/api/v1/users/{id}`   | Get user by ID  |
| `DELETE` | `/api/v1/users/{id}`   | Delete user     |

## Key Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlalchemy + aiosqlite** - Async ORM + SQLite driver
- **alembic** - Database migrations
- **bcrypt** - Password hashing
- **google-adk** - Google ADK (reserved for future use)
