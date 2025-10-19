Run the Week 4 backend tests (optional pytest selector: `$ARGUMENTS`).

1. From repo root, run `cd week4` to access the folder.
2. Execute:
   - `make test` when no arguments are provided, or
   - `pytest -q backend/tests $ARGUMENTS` when a selector is supplied.
3. If any test fails, capture the failing test names, relevant traceback snippets, and suggest concrete follow-up steps (rerun with `-k`, inspect file X, etc.).
4. When all tests pass, confirm success and note any additional actions (e.g., run coverage or lint if applicable).
5. Do not modify or create test files unless explicitly instructed elsewhere in the conversation.
