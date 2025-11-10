# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do.


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> https://app.graphite.com/github/pr/AlfredYu109/modern-software-dev-assignments/3/Task-1-Claude-Try

b. PR Description
> TL;DR
Added pre-commit hooks and enhanced the API with bulk operations, validation, and statistics endpoints.

What changed?
Added a .pre-commit-config.yaml file with Black, Ruff, and basic file formatting hooks
Enhanced input validation for notes and action items with field validators
Added bulk operations for notes and action items:
Bulk create
Bulk delete
Bulk complete (for action items)
Added statistics endpoints:
/notes/stats/summary - provides total count, character count, and average content length
/action-items/stats/summary - provides total, completed, pending counts and completion rate
Added individual delete endpoints for notes and action items
Fixed code formatting and removed trailing whitespace/newlines
How to test?
Test bulk operations:

# Bulk create notes
curl -X POST http://localhost:8000/notes/bulk -H "Content-Type: application/json" -d '{"notes":[{"title":"Note 1","content":"Content 1"},{"title":"Note 2","content":"Content 2"}]}'

# Bulk delete notes
curl -X POST http://localhost:8000/notes/bulk/delete -H "Content-Type: application/json" -d '{"ids":[1,2,3]}'

# Bulk complete action items
curl -X PUT http://localhost:8000/action-items/bulk/complete -H "Content-Type: application/json" -d '{"ids":[1,2,3]}'
Test statistics endpoints:

# Get notes statistics
curl http://localhost:8000/notes/stats/summary

# Get action items statistics
curl http://localhost:8000/action-items/stats/summary
Run pre-commit hooks:

pip install pre-commit
pre-commit install
pre-commit run --all-files
Why make this change?
Pre-commit hooks ensure consistent code formatting and quality
Bulk operations improve API efficiency for clients needing to perform multiple operations
Statistics endpoints provide valuable insights into the application data
Input validation ensures data integrity and prevents invalid entries
Individual delete endpoints complete the CRUD functionality

c. Graphite Diamond generated code review
> Graphite Diamond actually did not have direct comments, but when the agent was prompted further, suggested this:
"1. Transaction Management
Using db.flush() without db.commit() may not persist changes. Consider adding commits or relying on FastAPI's dependency cleanup:

db.commit()  # After flush operations
2. Reduce Code Duplication
The bulk operations are nearly identical between notes and action items. Extract common logic:

# Create a generic bulk delete function
def bulk_delete_entities(db, model, ids):
    ...
3. Optimize Stats Queries
Action items stats makes 2 separate queries. Combine them:

stmt = select(
    func.count(ActionItem.id),
    func.count(ActionItem.id).filter(ActionItem.completed.is_(True))
)
4. Use Response Models
Bulk delete returns a dict. Create a proper schema:

class BulkDeleteResponse(BaseModel):
    deleted_count: int
5. Consider Partial Success
Current bulk operations are all-or-nothing. For better UX, consider returning which operations succeeded/failed.

6. Add Rate Limiting
Bulk operations could be abused. Consider adding rate limits or stricter validation.

7. Database Indexes
Add indexes for frequently queried fields (completed status, filtering/sorting columns).

8. Remove Input Stripping
Automatic stripping modifies user input. Consider validating without modifying, or make it explicit.

9. Update Pre-commit Versions
Pinned versions from 2024 may be outdated. Use rev: main or update to latest."

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Brief Reflection
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> TODO

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> TODO

c. When the AI reviews were better/worse than yours (cite specific examples)
> TODO

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
>TODO
