# Week 7 - AI Code Review Reference Guide

## Project Overview

This is a FastAPI-based REST API for managing Notes and Action Items with SQLite database backend. The project demonstrates modern Python web development with comprehensive testing and validation.

## Tech Stack

- **Framework**: FastAPI 0.116.1 (async-capable Python web framework)
- **Database**: SQLite with SQLAlchemy 2.0+ ORM
- **Validation**: Pydantic 2.0+ for request/response schemas
- **Server**: Uvicorn (ASGI server)
- **Testing**: Pytest with TestClient
- **Code Quality**: Black (formatter) + Ruff (linter) + pre-commit hooks

## Project Structure

```
week7/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app initialization & routers
│   │   ├── models.py            # SQLAlchemy ORM models (Note, ActionItem)
│   │   ├── schemas.py           # Pydantic validation schemas
│   │   ├── db.py                # Database configuration & session management
│   │   ├── routers/
│   │   │   ├── notes.py         # Notes CRUD endpoints
│   │   │   └── action_items.py  # Action items CRUD endpoints
│   │   └── services/
│   │       └── extract.py       # Action item extraction logic
│   └── tests/
│       ├── conftest.py          # Pytest fixtures (client, temp DB)
│       ├── test_notes.py        # Notes endpoint tests (18 tests)
│       ├── test_action_items.py # Action items endpoint tests (17 tests)
│       └── test_extract.py      # Extract service tests (1 test)
├── frontend/                    # Static HTML/CSS/JS frontend
├── data/                        # SQLite database & seed.sql
├── docs/
│   ├── assignment.md           # Assignment instructions
│   └── TASKS.md                # Task descriptions
├── Makefile                     # Build/run commands
├── pyproject.toml              # Poetry dependencies & config
├── writeup.md                   # PR documentation (TO BE FILLED)
└── CLAUDE.md                    # This file
```

## Database Models

### Note Model
```python
- id: Integer (primary key)
- title: String(200) - required
- content: Text - required
- created_at: DateTime - auto-set
- updated_at: DateTime - auto-updated
```

### ActionItem Model
```python
- id: Integer (primary key)
- description: Text - required
- completed: Boolean - default False
- created_at: DateTime - auto-set
- updated_at: DateTime - auto-updated
```

## Task 1 Status: ✅ COMPLETED

### Implemented Endpoints

#### Notes Endpoints (`/notes`)
- `GET /notes/` - List with filtering, pagination, sorting
- `GET /notes/{note_id}` - Get single note
- `POST /notes/` - Create note
- `PATCH /notes/{note_id}` - Update note
- `DELETE /notes/{note_id}` - Delete note ✨ NEW
- `POST /notes/bulk` - Bulk create notes (max 100) ✨ NEW
- `POST /notes/bulk/delete` - Bulk delete notes ✨ NEW
- `GET /notes/stats/summary` - Get statistics ✨ NEW

#### Action Items Endpoints (`/action-items`)
- `GET /action-items/` - List with filtering, pagination, sorting
- `POST /action-items/` - Create action item
- `PUT /action-items/{item_id}/complete` - Mark as complete
- `PATCH /action-items/{item_id}` - Update action item
- `DELETE /action-items/{item_id}` - Delete action item ✨ NEW
- `POST /action-items/bulk` - Bulk create items (max 100) ✨ NEW
- `POST /action-items/bulk/delete` - Bulk delete items ✨ NEW
- `PUT /action-items/bulk/complete` - Bulk complete items ✨ NEW
- `GET /action-items/stats/summary` - Get statistics ✨ NEW

### Enhanced Validations

All schemas now include:
- **Field constraints**: `max_length` (200 for titles, 500 for descriptions)
- **Custom validators**: Prevent empty/whitespace-only strings
- **Automatic trimming**: Leading/trailing whitespace removed
- **Bulk limits**: 1-100 items per bulk operation

### Error Handling Improvements

- Specific error messages with IDs in 404 responses
- Partial failure detection in bulk operations
- Detailed validation errors (422 status)
- Empty input prevention (400 status for empty bulk requests)

### Test Coverage

- **Total Tests**: 36 tests (all passing ✓)
- **New Tests**: 27 tests added for Task 1
- Coverage includes DELETE, bulk operations, validation, stats, edge cases

## Remaining Tasks

### Task 2: Extend extraction logic
**File**: `backend/app/services/extract.py`

Current implementation:
- Extracts lines starting with "TODO:" or "ACTION:"
- Extracts lines ending with "!"

Needs enhancement with more sophisticated pattern recognition.

### Task 3: Try adding a new model and relationships
**Files**: `backend/app/models.py`, new router files, schemas

Need to:
- Create new database model(s)
- Add relationships (e.g., Notes ↔ ActionItems)
- Update/create routers
- Add schemas and tests

### Task 4: Improve tests for pagination and sorting
**Files**: `backend/tests/test_notes.py`, `backend/tests/test_action_items.py`

Current pagination/sorting tests are basic. Need:
- Edge case testing (offset beyond data, invalid sort fields)
- Boundary testing (limit=0, limit>200)
- Complex sorting scenarios

## Common Commands

```bash
# Development
make run          # Start server (http://localhost:8000)
make test         # Run pytest
make format       # Format with Black + Ruff
make lint         # Check code with Ruff
make seed         # Apply seed.sql to database

# Using Poetry directly
poetry install                    # Install dependencies
poetry run uvicorn app.main:app   # Run server
poetry run pytest                 # Run tests
poetry run black .                # Format code
poetry run ruff check --fix .     # Lint and fix
```

## API Documentation

When server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Important Notes for Future Tasks

### Route Ordering in FastAPI
**CRITICAL**: More specific routes must come before parameterized routes!

✅ Correct order:
```python
@router.post("/bulk/delete")      # Specific path first
@router.delete("/{item_id}")      # Parameterized path second
```

❌ Wrong order:
```python
@router.delete("/{item_id}")      # This catches /bulk/delete!
@router.post("/bulk/delete")      # Never reached
```

### Validation Best Practices

1. **Use Pydantic Field constraints**: `min_length`, `max_length`, descriptions
2. **Add custom validators**: Use `@field_validator` for complex logic
3. **Trim whitespace**: Always clean user input
4. **Provide clear error messages**: Include IDs and specific details

### Testing Considerations

1. Each test uses a fresh temporary database (see `conftest.py`)
2. Tests should be independent and can run in any order
3. TestClient doesn't support `json` parameter for DELETE - use POST instead
4. Use descriptive test names: `test_<action>_<scenario>`

### Database Session Management

```python
# Pattern used in get_db() dependency:
try:
    yield session
    session.commit()    # Auto-commit on success
except Exception:
    session.rollback()  # Rollback on error
    raise
finally:
    session.close()     # Always close
```

## Assignment Workflow

### For Each Task (2, 3, 4):

1. **Create branch**: `git checkout -b task-<number>-<description>`
2. **Implement with AI**: Use 1-shot prompt describing the task
3. **Manual review**: Check every line, fix issues, add explanatory commits
4. **Write tests**: Ensure comprehensive test coverage
5. **Run all tests**: `make test` - must pass ✓
6. **Format code**: `poetry run black . && poetry run ruff check --fix .`
7. **Create PR**:
   - Description of problem and approach
   - Testing summary (commands + results)
   - Tradeoffs/limitations/follow-ups
8. **Graphite Diamond review**: Generate AI code review on PR
9. **Document in writeup.md**: Record PR details and review comparison

### PR Guidelines

Each PR should include:
- **Title**: Clear and descriptive (e.g., "Task 2: Enhanced action item extraction with regex patterns")
- **Description**:
  - Problem statement
  - Approach taken
  - Key design decisions
- **Testing section**:
  - Commands run: `make test`, `make lint`
  - Test results: number of tests, coverage
  - Manual testing performed
- **Notes**:
  - Tradeoffs made
  - Known limitations
  - Potential follow-ups

## Debugging Tips

1. **Check API docs**: Visit `/docs` to see all endpoints and schemas
2. **View SQL**: Enable SQLAlchemy echo in `db.py`
3. **Test in isolation**: Use pytest `-k` to run specific tests
4. **Inspect database**: Use `sqlite3 ./data/app.db` to query directly
5. **Check FastAPI logs**: Uvicorn shows detailed request/response info

## Code Quality Standards

- **Black**: Line length 100, automatic formatting
- **Ruff**: Import sorting, linting
- **Pre-commit**: Runs on every commit (black, ruff, end-of-file-fixer, trailing-whitespace)
- **Type hints**: Use modern Python 3.10+ syntax (`str | None` not `Optional[str]`)

## Current Git Status

- **Branch**: master
- **Untracked**: `../.pre-commit-config.yaml`
- **Clean**: All Task 1 changes committed

## Next Steps

1. Read Task 2 requirements carefully
2. Create new branch: `task-2-extraction-logic`
3. Implement enhanced extraction in `extract.py`
4. Add comprehensive tests
5. Create PR with Graphite Diamond review
6. Document in writeup.md

---

**Last Updated**: Task 1 completed
**Test Status**: 36/36 passing ✓
**Code Quality**: Formatted with Black + Ruff ✓
