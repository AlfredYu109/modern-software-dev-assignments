# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

#### Prompt 1: "Test Coverage Booster"

**a. Design of each automation, including goals, inputs/outputs, steps**

**Goal:** Automate the generation of comprehensive test coverage for API endpoints following project standards.

**Inputs:**
- `endpoint_path`: The API endpoint path (e.g., `/notes/`, `/action-items/{id}/complete`)
- `module`: Test module name without `test_` prefix (e.g., `notes`, `action_items`)

**Outputs:**
- Complete test file with 4 categories of tests:
  1. Success scenarios (validates `ok: true`, `data` field structure)
  2. Error scenarios (404 NOT_FOUND, 422 VALIDATION_ERROR)
  3. Edge cases (empty database, special characters, idempotent operations)
  4. Integration scenarios (create → retrieve workflows)
- All tests follow the response envelope pattern
- Automated test execution via `make test`

**Steps:**
1. Agent reads existing endpoint implementation
2. Generates test cases covering all success paths
3. Generates test cases for all error paths (404, validation errors)
4. Adds edge case tests (empty lists, special characters, boundary conditions)
5. Adds integration tests simulating real user workflows
6. Ensures all assertions check envelope structure (`ok`, `data`, `error` fields)
7. Runs `make test` to verify all tests pass

---

**b. Before vs. after (i.e. manual workflow vs. automated workflow)**

**Before (Manual):**
1. Manually review endpoint code to understand behavior (~5 min)
2. Write success test case (~5 min)
3. Write 404 test case (~3 min)
4. Write validation error tests for each field (~10 min)
5. Write edge case tests (~8 min)
6. Write integration tests (~7 min)
7. Run tests, fix issues (~5 min)
8. **Total: ~43 minutes per endpoint**

**After (Automated with Warp Prompt):**
1. Open Command Palette (`Cmd + P`)
2. Type "Test Coverage Booster"
3. Fill in 2 arguments: `endpoint_path`, `module` (~30 seconds)
4. Press Enter, agent generates all tests (~2 min)
5. Review generated tests (~3 min)
6. **Total: ~5.5 minutes per endpoint**

**Time saved: ~37.5 minutes per endpoint (87% reduction)**

---

**c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)**

**Autonomy Level:** High autonomy with file write permissions

**Permissions granted:**
- Read access to existing endpoint code and schemas
- Write access to test files (`backend/tests/test_*.py`)
- Execute permissions to run `make test`

**Why:** Test generation is low-risk because:
- Tests don't affect production code
- Failed tests are immediately visible
- Easy to review and modify generated tests

**Supervision approach:**
1. Review generated test names to ensure coverage breadth
2. Spot-check 2-3 test implementations for correctness
3. Verify test execution output (all pass, no false positives)
4. Manual review of edge cases to ensure they match expected behavior

---

**d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures**

N/A - This is a single-agent automation (Warp Drive saved prompt).

---

**e. How you used the automation (what pain point it resolves or accelerates)**

**Pain point resolved:** Writing comprehensive test coverage is tedious and time-consuming, especially when following strict patterns like response envelopes.

**How used:**
- Applied to Tasks #7 and #10 to generate test coverage for notes and action items endpoints
- Generated 30+ test cases across multiple test files
- Ensured consistency in test structure (all tests check envelope format)
- Reduced cognitive load by automating repetitive assertion patterns

**Real example:** After implementing Task #7 (error handling), I used this prompt to generate validation tests:
```
endpoint_path: /notes/
module: notes
```
Agent generated tests for:
- Empty title/content validation
- Whitespace-only validation
- Missing field validation
- Max length boundary testing
- 404 not found scenarios

This would have taken ~40 minutes manually but took ~5 minutes with the automation.

---

#### Prompt 2: "Add CRUD Endpoint with Full Coverage"

**a. Design of each automation, including goals, inputs/outputs, steps**

**Goal:** Scaffold a complete REST resource from scratch with models, schemas, routes, and tests following project architecture.

**Inputs:**
- `RESOURCE_NAME`: PascalCase model name (e.g., `Tag`, `Category`, `Comment`)
- `resource_name`: snake_case route/file name (e.g., `tags`, `categories`, `comments`)

**Outputs:**
- SQLAlchemy model in `backend/app/models.py`
- Pydantic schemas in `backend/app/schemas.py` (Create and Read models with validation)
- Complete router in `backend/app/routers/{resource_name}.py` with 5 endpoints:
  - `GET /{resource_name}/` (list all)
  - `POST /{resource_name}/` (create)
  - `GET /{resource_name}/{id}` (get one)
  - `PUT /{resource_name}/{id}` (update)
  - `DELETE /{resource_name}/{id}` (delete)
- Router registration in `backend/app/main.py`
- Test file `backend/tests/test_{resource_name}.py` with comprehensive coverage
- All responses wrapped in `SuccessResponse` envelopes
- Passing `make test` and `make lint`

**Steps:**
1. Create SQLAlchemy model with appropriate columns and indexes
2. Create Pydantic schemas with Field validators and whitespace checks
3. Generate router file with all 5 CRUD endpoints
4. Wrap all responses in SuccessResponse envelopes
5. Add proper 404 error handling
6. Register router in main.py
7. Generate comprehensive tests (CRUD operations, validation, 404s, edge cases)
8. Run `make test && make lint` to verify

---

**b. Before vs. after (i.e. manual workflow vs. automated workflow)**

**Before (Manual):**
1. Create SQLAlchemy model (~10 min)
2. Create Pydantic schemas with validators (~8 min)
3. Create router file with 5 endpoints (~25 min)
4. Wrap all responses in envelopes (~5 min)
5. Add router to main.py (~2 min)
6. Write tests for all endpoints (~35 min)
7. Debug and fix issues (~10 min)
8. Run lint, fix formatting (~3 min)
9. **Total: ~98 minutes (1 hour 38 min) per resource**

**After (Automated with Warp Prompt):**
1. Open Command Palette (`Cmd + P`)
2. Type "Add CRUD Endpoint"
3. Fill in 2 arguments: `RESOURCE_NAME`, `resource_name` (~30 seconds)
4. Press Enter, agent generates all files (~5 min)
5. Review generated code (~5 min)
6. Make minor adjustments if needed (~3 min)
7. **Total: ~13.5 minutes per resource**

**Time saved: ~84.5 minutes per resource (86% reduction)**

---

**c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)**

**Autonomy Level:** High autonomy with full write permissions

**Permissions granted:**
- Read access to existing codebase patterns
- Write access to models, schemas, routers, tests
- Execute permissions for `make test && make lint`

**Why:** CRUD scaffolding follows well-established patterns in the codebase. High autonomy is appropriate because:
- The structure is highly standardized
- Tests immediately validate correctness
- Lint catches formatting issues
- Easy to iterate if adjustments needed

**Supervision approach:**
1. Review model schema (columns, types, constraints)
2. Verify schema validation logic (min_length, whitespace checks)
3. Spot-check 1-2 endpoints for proper envelope wrapping
4. Review test coverage breadth
5. Verify `make test` passes with no failures
6. Verify `make lint` passes

---

**d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures**

N/A - This is a single-agent automation (Warp Drive saved prompt).

---

**e. How you used the automation (what pain point it resolves or accelerates)**

**Pain point resolved:** Scaffolding new REST resources is highly repetitive. Every resource needs the same boilerplate: model, schemas, 5 CRUD endpoints, envelope wrapping, tests. Manually writing this is error-prone and time-consuming.

**How used:**
- Can be used to quickly add new features like Tags (Task #5), Categories, Comments, etc.
- Ensures consistency across all resources (same validation patterns, same envelope structure)
- Reduces context-switching between files (agent handles all 6 files)
- Eliminates copy-paste errors from duplicating existing resources

**Example use case:** If I wanted to add a "Tag" feature:
```
RESOURCE_NAME: Tag
resource_name: tags
```
Agent would generate:
- Tag model with `id`, `name` columns
- TagCreate/TagRead schemas with validation
- Complete tags router with 5 endpoints
- ~15 test cases
- All in ~13 minutes vs ~98 minutes manually

**Key benefit:** Freed up mental energy to focus on business logic and unique features rather than boilerplate scaffolding.



### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
> TODO

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> TODO

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> TODO

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> TODO

e. How you used the automation (what pain point it resolves or accelerates)
> TODO


### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps
> TODO

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> TODO

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> TODO

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> TODO

e. How you used the automation (what pain point it resolves or accelerates)
> TODO

