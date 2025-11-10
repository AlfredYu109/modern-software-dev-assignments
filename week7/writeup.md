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
> https://app.graphite.com/github/pr/AlfredYu109/modern-software-dev-assignments/4/Task-2-Whitespace-Fixed

b. PR Description
> TL;DR
Enhanced action item extraction with sophisticated pattern recognition and added detailed metadata extraction capabilities.

What changed?
Implemented advanced pattern recognition for action items including:
Additional action markers (FIXME, BUG, HACK, NOTE, XXX, OPTIMIZE, REFACTOR)
Imperative phrases (Need to, Must, Should, Remember to, etc.)
Checkbox patterns ([ ], [x])
Priority markers ([HIGH], [URGENT], [P1], etc.)
Question marks as potential action items
Common imperative verbs (Add, Fix, Update, etc.)
Added new extract_action_items_detailed() function that extracts structured metadata:
Priority information (HIGH, URGENT, P1, etc.)
Assignees from @mentions
Categories based on action markers (bug, todo, optimization, etc.)
Expanded test suite with comprehensive test cases:
Basic extraction patterns
Edge cases and special scenarios
Detailed metadata extraction
Real-world usage scenarios (meeting notes, code reviews, project planning)
How to test?
Run the expanded test suite:

make test
# or
poetry run pytest backend/tests/test_extract.py -v
Try extracting action items from various text formats:

from backend.app.services.extract import extract_action_items, extract_action_items_detailed

# Basic extraction
items = extract_action_items("TODO: Fix bug\nNeed to update docs\n[HIGH] Critical issue!")
print(items)

# Detailed extraction with metadata
detailed = extract_action_items_detailed("BUG: [P1] @alice Fix authentication issue")
print(detailed)
Why make this change?
Improves action item detection with more sophisticated pattern recognition
Provides structured metadata extraction for better organization and prioritization
Enables more intelligent processing of notes by identifying priorities, assignees, and categories
Supports real-world note-taking scenarios like meeting notes, code reviews, and project planning

c. Graphite Diamond generated code review
> Graphite didn't make any direct comments, but noted the following: "Performance & Structure
Compile regex patterns once - Move regex compilation to module level:
_PRIORITY_PATTERN = re.compile(r"^\[(?:HIGH|URGENT|LOW|P[1-5]|CRITICAL)\]\s+", re.IGNORECASE)
_CHECKBOX_PATTERN = re.compile(r"^\[[ xX]?\]\s+")
# ... other patterns
Combine pattern checks - Use a single compiled regex instead of checking multiple patterns in loops:
_IMPERATIVE_VERBS = re.compile(
    r"^(?:add|fix|update|remove|create|implement|...)\s+",
    re.IGNORECASE
)
Logic Issues
Clean extracted descriptions - Remove priority markers and other metadata from the description in extract_action_items_detailed():
# Strip priority markers, checkboxes from description
cleaned = re.sub(priority_pattern, "", item)
cleaned = re.sub(checkbox_pattern, "", cleaned).strip()
Arbitrary thresholds - The len(line) > 10 for questions and len(line) > 5 for verbs are questionable. Consider removing or documenting why these exist.
Type Safety
Fix TypedDict - description should always be present:
class ActionItemExtract(TypedDict):
    description: str
    priority: NotRequired[str]
    assignee: NotRequired[str]
    category: NotRequired[str]
Testing
Missing test coverage - No tests verify that patterns are actually stripped from descriptions (#lines-week7/backend/tests/test_extract.py-R208-R232)

Test the question length threshold - Current test doesn't verify the 10-char threshold is correct" when prompted.

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
