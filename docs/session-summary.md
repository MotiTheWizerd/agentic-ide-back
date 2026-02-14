# Session Summary — 2026-02-14 (Session 3)

## What was done

### 1. Auto-Discovery DI System
- Created `app/core/di/registry.py` — `ServiceRegistry` singleton container with `register()`, `resolve()`, `get()` (Depends-compatible)
- Created `app/core/di/discovery.py` — auto-discovery engine with `discover_routers()`, `discover_managers()`, `discover_handlers()`
- Created `app/core/di/__init__.py` — clean export of `registry`
- **Routers**: `app/api/v1/router.py` no longer manually imports endpoints — all routers in `app/api/v1/endpoints/` are auto-discovered via `pkgutil`
- **Managers**: all `*Manager` classes in `app/modules/*/manager.py` are auto-instantiated as singletons and registered on boot
- Deleted `app/modules/projects/dependency.py` — no longer needed
- Removed module-level singleton instances from manager files
- Updated `app/api/v1/endpoints/projects.py` to use `registry.get(ProjectManager)` instead of manual factory

### 2. Event System Overhaul
- Created `app/core/events/types.py` — `EventTypes` class as single source of truth for all event type constants
- Created `app/core/events/subscribe.py` — `@subscribe` decorator to mark async functions as event handlers
- Updated `app/core/events/__init__.py` to export `Event`, `EventTypes`, `subscribe`
- Added `discover_handlers()` to auto-discovery engine — scans `app/modules/*/handlers.py` for `@subscribe`-decorated functions and registers them on the event bus
- Created `app/modules/projects/handlers.py` — handlers for `project.created`, `project.deleted`
- Created `app/modules/users/handlers.py` — handlers for `user.registered`, `user.deactivated`
- Updated both managers to use `EventTypes` constants instead of magic strings
- All handlers auto-discovered and subscribed on boot

### 3. Event Logging (Persistence)
- Created `app/models/event_log.py` — `EventLog` model (UUID PK, event_name, payload JSON, user_id FK, project_id FK nullable, session_id nullable, created_at)
- Updated `app/core/bus/event_bus.py` — every `emit()` now auto-persists to `event_logs` table via fire-and-forget background task
- Registered `EventLog` in `app/models/__init__.py`

### 4. PostgreSQL Migration
- Switched from SQLite to PostgreSQL (`postgresql+asyncpg://`)
- Updated `app/core/db/base.py` to read `DATABASE_URL` from `.env` via `python-dotenv`
- Updated `alembic/env.py` to use the same `.env`-driven URL + added `EventLog` to model imports
- Deleted all old SQLite migration files
- Generated fresh single migration for all 11 tables against PostgreSQL
- Added `asyncpg` and `python-dotenv` to dependencies

## New files created this session
- `app/core/di/__init__.py`
- `app/core/di/registry.py`
- `app/core/di/discovery.py`
- `app/core/events/types.py`
- `app/core/events/subscribe.py`
- `app/modules/projects/handlers.py`
- `app/modules/users/handlers.py`
- `app/models/event_log.py`

## Files deleted this session
- `app/modules/projects/dependency.py`
- All old SQLite migrations in `alembic/versions/`

## Boot sequence (what happens on startup)
1. Logging configured
2. Routers auto-discovered from `app/api/v1/endpoints/`
3. Managers auto-discovered and registered as singletons from `app/modules/*/manager.py`
4. Event handlers auto-discovered and subscribed from `app/modules/*/handlers.py`
5. Every event emission auto-persists to `event_logs` table

## Conventions updated
- Database: PostgreSQL via asyncpg (was SQLite)
- Config: `.env` file with `python-dotenv` (was hardcoded)
- DI: auto-discovery, no manual wiring — drop files in convention directories
- Events: `EventTypes` constants (no magic strings), `@subscribe` decorator for handlers
- Adding a new module = create endpoint + manager + handlers files, zero wiring needed
