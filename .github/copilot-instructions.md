# AI Coding Agent Instructions

## Architecture Overview

This is a **multi-database full-stack application** with:
- **Backend**: FastAPI with SQLModel supporting 3 databases (PostgreSQL, DuckDB, ScyllaDB)
- **Frontend**: Vue 3 + TypeScript with DaisyUI + Tailwind CSS
- **Database Strategy**: Single codebase, multiple database backends via connector pattern

## Multi-Database Architecture

### Database Connector Pattern (`backend/app/db/connector.py`)
- **Unified Interface**: `Connector` class abstracts database operations
- **Engine-Specific Classes**: `SQLConnector` (Postgres/DuckDB), `ScyllaConnector` (Cassandra CQL)
- **Runtime Selection**: Database chosen via URL path parameter (`/{db_type}/endpoint`)

**Key Pattern**: All CRUD operations return Pydantic models, not raw database objects:
```python
def all_users(self, db_type: DatabaseType) -> List[schemas.UserResponse]:
    # Returns validated Pydantic objects, not SQLModel instances
```

### Database-Agnostic Endpoints (`backend/app/endpoint/__init__.py`)
- **Path Parameters**: `/{db_type}/users` where `db_type` ∈ {postgres, duckdb, scylla}
- **Dependency Injection**: `get_db_connector()` provides correct database interface
- **Unified Schemas**: Same Pydantic models work across all databases

## Frontend Architecture

### Vue 3 + TypeScript Patterns
- **Composition API**: Always use `<script setup lang="ts">`
- **Props Definition**: Use object syntax, not `withDefaults`:
```typescript
const props = defineProps({
  data: {
    type: Array as PropType<User[]>,
    required: true,
  },
})
```
- **Emits Definition**: Use function signature syntax:
```typescript
const emit = defineEmits<{
  (e: "edit", item: User): void;
}>()
```

### DaisyUI + Tailwind Integration
- **Component Library**: DaisyUI 5.x with Tailwind CSS 4.x
- **Color System**: Use daisyUI semantic colors (`primary`, `secondary`) over Tailwind colors
- **Proper Structure**: Follow daisyUI component patterns (see `.github/instructions/daisyui.instructions.md`)

## Development Workflows

### Backend Development
- **Environment**: Uses `uv` for dependency management
- **Database**: Local DuckDB (`duck.db`), Docker containers for Postgres/Scylla
- **Start Backend**: `cd backend && uvicorn main:app --reload`

### Frontend Development
- **Start Frontend**: `cd frontend && npm run dev`
- **Build**: `npm run build` (includes TypeScript compilation)

### Database Setup
- **Docker**: `docker-compose up -d` (Postgres + ScyllaDB)
- **Seeds**: SQL files in `db_seed/` for schema initialization
- **DuckDB**: Initialized automatically via SQLModel

## Critical Patterns

### Schema Consistency
- **Backend Schemas** (`app/schemas.py`): Define `*Response`, `*Create`, `*Update` models
- **Frontend Interfaces**: Mirror backend Response schemas exactly
- **Database Models** (`app/db/models.py`): SQLModel classes with proper relationships

### Error Handling
- **Backend**: FastAPI automatic validation + custom error responses
- **Frontend**: TypeScript strict mode + Vue error boundaries

## Project-Specific Conventions

### File Organization
- **Backend**: Feature-based (`app/db/`, `app/endpoint/`, `app/schemas.py`)
- **Frontend**: Component-based (`src/components/`, `src/api/`)
- **Database**: Separate files per database type (`postgres.py`, `scylla.py`, `duck.py`)

### Naming Conventions
- **Database Types**: Lowercase enum values (`"postgres"`, `"duckdb"`, `"scylla"`)
- **API Endpoints**: RESTful with database prefix (`GET /{db_type}/users`)
- **Vue Components**: PascalCase files, kebab-case in templates