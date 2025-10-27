# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Alfred Yu** \
SUNet ID: **ayu1001* \
Citations: I used Warp to provide the initial scaffolding for this file. 

This assignment took me about 1.5 hours to do. 


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
1. Manually review endpoint code to understand behavior 
2. Write success test case 
3. Write 404 test case 
4. Write validation error tests for each field 
5. Write edge case tests
6. Write integration tests 
7. Run tests, fix issues 

**After (Automated with Warp Prompt):**
1. Open Command Palette (`Cmd + P`)
2. Type "Test Coverage Booster"
3. Fill in 2 arguments: `endpoint_path`, `module` 
4. Press Enter, agent generates all tests
5. Review generated tests 



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

**How I used this:**
The agent was able to generate extensive tests for: 
- Empty title/content validation
- Whitespace-only validation
- Missing field validation
- Max length boundary testing
- 404 not found scenarios

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
1. Create SQLAlchemy model 
2. Create Pydantic schemas with validators 
3. Create router file with 5 endpoints 
4. Wrap all responses in envelopes 
5. Add router to main.py 
6. Write tests for all endpoints 
7. Debug and fix issues 
8. Run lint, fix formatting 


**After (Automated with Warp Prompt):**
1. Open Command Palette (`Cmd + P`)
2. Type "Add CRUD Endpoint"
3. Fill in 2 arguments: `RESOURCE_NAME`, `resource_name`
4. Press Enter, agent generates all files
5. Review generated code 
6. Make minor adjustments if needed 

---

**c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)**

**Autonomy Level:** High autonomy was granted with full write permissions

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
3. Review test coverage breadth

---

**d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures**

N/A - This is a single-agent automation (Warp Drive saved prompt).

---

**e. How you used the automation (what pain point it resolves or accelerates)**

**Pain point resolved:** Scaffolding new REST resources is highly repetitive. Every resource needs the same boilerplate: model, schemas, 5 CRUD endpoints, envelope wrapping, tests. Manually writing this is error-prone and time-consuming.

**How I used it:**
I was able to implement a CRUD enpoint fairly painlessly and without much labor on my end - significantly saving time. 
This can be used for future tasks as well to free-up time. 

**Key benefit:** This allowed for freed up mental energy to focus on business logic and unique features rather than boilerplate scaffolding.



### Automation B: Multi‑agent workflows in Warp 

#### Task 8: List Endpoint Pagination (Multi-Agent Implementation)

**a. Design of each automation, including goals, inputs/outputs, steps**

**Goal:** Implement pagination for all collection endpoints (`/notes` and `/action-items`) using concurrent agents working on separate sub-tasks.

**Task Decomposition:**
- **Agent 1 - Backend Notes Pagination**: Add `page` and `page_size` parameters to `GET /notes`, return `{"items": [...], "total": count}`
- **Agent 2 - Backend Action Items Pagination**: Add `page` and `page_size` parameters to `GET /action-items`, return `{"items": [...], "total": count}`
- **Agent 3 - Frontend Pagination UI**: Update frontend to handle paginated responses, add prev/next controls
- **Agent 4 - Pagination Tests**: Add comprehensive tests for pagination edge cases (empty pages, large page_size, boundaries)
I split up the tasks among 4 agents, to test out how agents can work in conjunction and synergistically with one another. 


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
Each agent had their own working copy of the repository, and each agent focused on different actions. 
No merge conflicts because agents worked on different files. Backend agents (1 & 2) worked on separate routers. 
Frontend agent (3) worked on separate files from backend. 
Test agent (4) worked on separate test files

**Concurrency Wins:**
Agents were able to work synchronously, in parallel, without waiting for other agents and 
by running independently. 

**Concurrency Risks**
Some agents both modified the same file. 
Some agents also had to assume the work from the other agents was complete. 

**Failures/Challenges:**
Both backend agents modified `schemas.py` simultaneously, causing merge conflicts. 
I had to commit all changes together after copying files to main worktree
---

**e. How you used the automation (what pain point it resolves or accelerates)**

**Pain point resolved:** Large tasks like pagination require changes across multiple layers (backend, frontend, tests). Working sequentially is slow and requires constant context switching between concerns.

**How I used the automation:**
- Decomposed Task #8 (pagination) into 4 parallel sub-tasks
- Created isolated environments for each agent using git worktrees
- Let agents work independently and simultaneously
- Merged results at the end for integrated solution

Key benefits and pain points eliminated include: 
- Eliminated context switching 
- Faster iteration 
- Scalability


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

