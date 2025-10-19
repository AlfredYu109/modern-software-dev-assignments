# Claude Guide

## Quick Start
- Activate local env (`conda activate cs146s` or equivalent) before running commands.
- Work from the `week4/` directory: `cd week4`.
- Launch the app with `make run` → FastAPI on `http://127.0.0.1:8000` and docs at `/docs`.
- Run unit tests via `make test`; use `PYTHONPATH=.` implicitly through the Makefile.
- Format/lint with `make format` (black + autofix ruff) and `make lint` (ruff check only).
- Install pre-commit hooks once: `pre-commit install`; run `pre-commit run --all-files` before commits.

## Repo Layout
- `backend/app/main.py` boots FastAPI, mounts the static frontend, and registers routers.
- `backend/app/routers/` contains feature endpoints (`notes.py`, `action_items.py`); keep new routes modular.
- `backend/app/services/` hosts helper logic (e.g., `extract.py`); prefer extending services over bloating routers.
- `backend/app/schemas.py` defines Pydantic models; add validation rules here.
- `backend/app/db.py` exposes `get_db` dependency, SQLAlchemy `engine`, and seeding utilities.
- `backend/tests/` contains pytest suites; each feature has focused coverage and a shared `client` fixture.
- `frontend/` is a static bundle served by FastAPI (`index.html`, `static/app.js`, `static/styles.css`).
- `data/seed.sql` seeds the SQLite DB on first run; `data/app.db` is the local database file.
- `docs/TASKS.md` lists suggested enhancements; keep automation notes synced with it.
- `writeup.md` documents the automations you build—update as features evolve.

## Database & Seeding
- SQLite file path defaults to `./data/app.db`; override with `DATABASE_PATH` env var if needed.
- `apply_seed_if_needed()` runs on startup via `main.py` to populate the DB from `data/seed.sql`.
- When writing tests, rely on the pytest `client` fixture (`backend/tests/conftest.py`) which swaps in a temp DB.
- To force reseeding locally, delete `data/app.db` (only if you understand the impact) and restart the app.

## Frontend Notes
- The UI is pure static assets—no Node toolchain. Modify `frontend/static/app.js` for UI logic.
- Any API shape changes require parallel updates in the frontend fetch calls and DOM helpers.
- Keep styling adjustments confined to `frontend/static/styles.css`.

## Code Style & Tooling
- Python formatting: black (line length 100) and ruff (`select = E,F,I,UP,B`; ignores `E501`, `B008`).
- Favor type hints across new Python code; match existing pattern in models/routers.
- Handle DB sessions with `Depends(get_db)`; commit/rollback is centralized, avoid manual commits in routes.
- When adding CLI or scripts, document them here and prefer idempotent commands.
- Keep docs, tests, and implementation changes in sync—mention in commit/writeup if automation handled it.

## Testing & QA
- Default to targeted pytest runs: `pytest backend/tests/test_notes.py -k "case"` when iterating.
- Verify frontend changes in the browser after adjusting API responses; smoke test the happy path manually.
- For additions to extraction logic (`services/extract.py`), add unit tests in `backend/tests/test_extract.py`.
- Ensure new endpoints include FastAPI response model annotations and have matching pytest coverage.

## Automation & Collaboration Tips
- Track new slash commands or sub-agent prompts inside `.claude/commands/` (create directory if missing).
- When adding automations, log usage and safety notes in `writeup.md` under the relevant sections.
- Respect existing git history—branch naming up to you; keep commits scoped and run hooks before pushing.
- Avoid destructive shell commands (`rm -rf`, `git reset --hard`) unless explicitly instructed.
- If you introduce environment flags or new Makefile tasks, document invocation steps here.
