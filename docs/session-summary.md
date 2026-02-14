# Session Summary — 2026-02-14 (Session 2)

## What was done

### 1. Agentic Components Table
- Created `agentic_components` table with UUID PK, unique `type`, `name`, `description`, category/provider_type enums, icon, color, LLM settings, version, is_active, created_at, updated_at
- Created `AgenticComponent` SQLAlchemy model with `ComponentCategory` and `ProviderType` string enums
- Generated and applied Alembic migration

### 2. Component Sub-Tables (4 tables)
- **`component_fields`** — configurable fields per component (field_key, label, field_type enum, placeholder, default_value, required, options JSON, validation JSON, sort_order)
- **`component_ports`** — input/output handles (direction enum in/out, port_type enum text/adapter, handle_id, max_connections, is_dynamic, max_dynamic, sort_order)
- **`component_api_config`** — execution/API mapping (api_route, request_mapping JSON, response_mapping JSON, pass_through_condition JSON, compression_threshold, executor_type enum)
- **`component_output_schema`** — what each node produces (output_key, output_type enum, source DSL string)
- All use UUID PKs with FK → agentic_components
- Generated and applied single Alembic migration for all 4 tables

### 3. Flows Table
- Created `flows` table: UUID PK, name, user_id (int FK → users), project_id (int FK → projects, nullable), graph_data JSON, created_at, updated_at
- Stores serialized nodes + edges + viewport as a single JSON blob

### 4. Consistent Characters Table
- Created `consistent_characters` table: UUID PK, user_id (int FK → users), project_id (int FK → projects, nullable), name, description (TEXT), image_path (nullable), created_at, updated_at

### 5. Seed Script — All 13 Component Types
- Created `scripts/seed_components.py` — idempotent seed script
- Seeds 13 component types: initialPrompt, promptEnhancer, translator, storyTeller, grammarFix, compressor, imageDescriber, imageGenerator, personasReplacer, textOutput, consistentCharacter, sceneBuilder, group
- Seeds all related data: 23 fields, 23 ports, 13 API configs, 18 output schemas
- Includes full dropdown options (28 languages, writing styles, image styles, lighting, time of day, weather, camera angles, camera lenses, moods, group colors)
- Run with: `python -m scripts.seed_components`

### 6. Cleanup
- Cleared all data from the `projects` table

## New models added this session
- `app/models/agentic_component.py` — AgenticComponent
- `app/models/component_field.py` — ComponentField
- `app/models/component_port.py` — ComponentPort
- `app/models/component_api_config.py` — ComponentApiConfig
- `app/models/component_output_schema.py` — ComponentOutputSchema
- `app/models/flow.py` — Flow
- `app/models/consistent_character.py` — ConsistentCharacter

## Convention established
- All endpoints use POST with JSON body — avoid GET with query/path params
- New tables use UUID primary keys (core user/project tables remain int)
- Enums stored as varchar strings (native_enum=False) for SQLite compatibility
- JSON columns for flexible data (options, mappings, graph_data)
- Component seed script is idempotent (deletes + re-inserts)
