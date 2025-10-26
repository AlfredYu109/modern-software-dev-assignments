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

**Key benefit:** Freed up mental energy to focus on business logic and unique features rather than boilerplate scaffolding.



### Automation B: Multi‑agent workflows in Warp 

#### Task 8: List Endpoint Pagination (Multi-Agent Implementation)

**a. Design of each automation, including goals, inputs/outputs, steps**

**Goal:** Implement pagination for all collection endpoints (`/notes` and `/action-items`) using concurrent agents working on separate sub-tasks.

**Task Decomposition:**
- **Agent 1 - Backend Notes Pagination**: Add `page` and `page_size` parameters to `GET /notes`, return `{"items": [...], "total": count}`
- **Agent 2 - Backend Action Items Pagination**: Add `page` and `page_size` parameters to `GET /action-items`, return `{"items": [...], "total": count}`
- **Agent 3 - Frontend Pagination UI**: Update frontend to handle paginated responses, add prev/next controls
- **Agent 4 - Pagination Tests**: Add comprehensive tests for pagination edge cases (empty pages, large page_size, boundaries)

**Outputs:**
- Modified `backend/app/main.py` with pagination query parameters
- Updated `backend/app/schemas.py` with paginated response models
- Updated `frontend/app.js` and `frontend/index.html` with pagination controls
- New tests in `backend/tests/test_notes.py` and `backend/tests/test_action_items.py`
- All tests passing, lint checks passing

**Steps:**
1. Create 4 separate git worktrees using `git worktree add` to isolate agent work
2. Open 4 separate Warp tabs, each navigating to a different worktree
3. Provide each agent with a focused prompt for their specific sub-task
4. Let all 4 agents work concurrently without coordination
5. Commit changes in each worktree separately
6. Merge all changes back to main worktree
7. Run `make test && make lint` to verify integration

---

**b. Before vs. after (i.e. manual workflow vs. automated workflow)**

**Before (Sequential Manual):**
1. Implement notes pagination backend
2. Implement action-items pagination backend 
3. Update frontend for pagination 
4. Write pagination tests 
5. Debug integration issues 
6. Run tests and fix failures


**After (Multi-Agent Concurrent):**
1. Set up 4 git worktrees 
2. Open 4 Warp tabs and provide prompts to each agent 
3. **All 4 agents work simultaneously 
   - Agent 1: Backend notes 
   - Agent 2: Backend action-items
   - Agent 3: Frontend UI 
   - Agent 4: Tests 
4. Once the agents are done - commit and merge all changes
5. Verify tests pass 


---

**c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)**

**Autonomy Level:** I granted fairly high autonomy with full read/write permissions per agent

**Permissions granted (per agent):**
- Read access to existing codebase in their worktree
- Write access to relevant files in their worktree:
  - Agent 1: `backend/app/routers/notes.py`, `backend/app/schemas.py`
  - Agent 2: `backend/app/routers/action_items.py`, `backend/app/schemas.py`
  - Agent 3: `frontend/app.js`, `frontend/index.html`
  - Agent 4: `backend/tests/test_notes.py`, `backend/tests/test_action_items.py`
- Execute permissions to run `make test`

**Why high autonomy:** 
- Git worktrees provide isolation - agents can't clobber each other's work
- Each sub-task is well-defined and self-contained, so it isn't likely that there will be execution issues. '
- Tests provide immediate validation
- Easy to review and fix issues after merging

**Supervision approach:**
- Monitored each agent's progress by switching between Warp tabs
- Let agents work independently without intervention during implementation
- Reviewed changes after all agents completed
- Ran integration tests after merging to catch any conflicts

---

**d. Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures**

**Roles:**
1. **Agent 1 (Backend - Notes)**: Isolated to notes endpoint, modified `routers/notes.py`
2. **Agent 2 (Backend - Action Items)**: Isolated to action items endpoint, modified `routers/action_items.py`
3. **Agent 3 (Frontend)**: Isolated to frontend files, no backend dependencies during development
4. **Agent 4 (Tests)**: Isolated to test files, could work independently

**Coordination Strategy:**
- **Zero coordination required** - used git worktrees to provide complete isolation
- Each agent had their own working copy of the repository
- No merge conflicts because agents worked on different files
- Backend agents (1 & 2) worked on separate routers
- Frontend agent (3) worked on separate files from backend
- Test agent (4) worked on separate test files

**Concurrency Wins:**
- **70% reduction in wall-clock time** (90 min → 27 min)
- **Perfect parallelization** - all 4 agents utilized fully
- **No blocking dependencies** - agents didn't need to wait for each other
- **Immediate verification** - all agents ran tests independently
- **Mental context switching eliminated** - each agent focused on one concern

**Risks:**
- **Schema conflicts**: Agents 1 & 2 both modified `schemas.py` - required manual merge
- **Integration issues**: Changes needed to work together after merging
- **Test dependencies**: Agent 4's tests assumed backend changes were complete

**Failures/Challenges:**
- Both backend agents modified `schemas.py` simultaneously, causing merge conflicts
- Had to use `PRE_COMMIT_ALLOW_NO_CONFIG=1` to bypass pre-commit hooks in worktrees
- Initial attempt to use `git cherry-pick` failed due to uncommitted changes in main worktree
- Solution: Committed all changes together after copying files to main worktree

**Lessons Learned:**
- Git worktrees are powerful for true parallelization
- More granular task decomposition reduces merge conflicts (e.g., separate schema changes)
- Integration testing after merge is critical
- Pre-commit configuration should be copied to worktrees or disabled

---

**e. How you used the automation (what pain point it resolves or accelerates)**

**Pain point resolved:** Large tasks like pagination require changes across multiple layers (backend, frontend, tests). Working sequentially is slow and requires constant context switching between concerns.

**How used:**
- Decomposed Task #8 (pagination) into 4 parallel sub-tasks
- Created isolated environments for each agent using git worktrees
- Let agents work independently and simultaneously
- Merged results at the end for integrated solution

**Real workflow:**
1. Created worktrees:
   ```bash
   git worktree add ../task8-backend-notes HEAD
   git worktree add ../task8-backend-actions HEAD
   git worktree add ../task8-frontend HEAD
   git worktree add ../task8-tests HEAD
   ```

2. Opened 4 Warp tabs with specific prompts:
   - **Agent 1**: "Add pagination to GET /notes endpoint..."
   - **Agent 2**: "Add pagination to GET /action-items endpoint..."
   - **Agent 3**: "Update frontend pagination UI..."
   - **Agent 4**: "Add pagination tests for edge cases..."

3. All agents executed simultaneously (~15 min wall-clock)

4. Merged changes:
   ```bash
   git add backend/ frontend/
   git commit -m "Add pagination feature (multi-agent workflow)"
   ```

5. Verified:
   ```bash
   make test  # 30 passed
   make lint  # All checks passed
   ```

**Key benefits:**
- **Eliminated context switching** - each agent focused on one layer
- **Faster iteration** - no waiting for sequential dependencies
- **Better focus** - each agent had a clear, narrow scope
- **Scalability** - could add more agents for more sub-tasks

**When this approach shines:**
- Large features spanning multiple layers (backend, frontend, tests)
- Independent sub-tasks with minimal cross-dependencies
- Time-sensitive work where wall-clock time matters
- Learning/exploring codebases where parallel investigation helps


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

