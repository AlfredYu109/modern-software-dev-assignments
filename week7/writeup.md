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
> https://app.graphite.com/github/pr/AlfredYu109/modern-software-dev-assignments/5/Week-3-No-Whitespace

b. PR Description
> TL;DR
Added a tagging system for notes and action items with many-to-many relationships.

What changed?
Created a new Tag model with name and color fields
Implemented many-to-many relationships between Tags and Notes/ActionItems
Added bidirectional relationships between Notes and ActionItems
Created a new /tags API router with CRUD operations
Added endpoints for associating/disassociating tags with notes and action items
Implemented tag statistics endpoint to track usage
Added comprehensive test suite for all tag functionality
How to test?
Create tags with POST /tags/ endpoint
Associate tags with notes using POST /tags/notes/{note_id}/tags
Associate tags with action items using POST /tags/action-items/{item_id}/tags
View tag statistics with GET /tags/stats/summary
Run the test suite with pytest backend/tests/test_tags.py
Why make this change?
Enables better organization of notes and action items through categorization
Provides a flexible way to filter and group related items
Allows tracking usage patterns through tag statistics
Creates a foundation for more advanced filtering and organization features
Tradeoffs:
Increased data model complexity with many-to-many relationships and cascade deletes
Additional N+1 query concerns when loading tags with notes/action items (consider eager loading for production)

Limitations:
No filtering by tags on /notes/ or /action-items/ list endpoints
Tag names are case-sensitive (can create both "urgent" and "Urgent")
No limit on tags per note/action item
Tag stats endpoint may be slow with large datasets (no caching/indexing strategy)
Cascade deletes are permanent (no soft delete option)

Follow-ups:
Add ?tags= filter parameter to notes and action items list endpoints
Implement tag name normalization (e.g., lowercase, trim whitespace)
Add endpoint to retrieve all notes/action items by tag ID
Consider adding pagination to tag statistics
Add bulk tag operations (associate/disassociate tags from multiple items at once)
Performance optimization for stats with caching or materialized views

c. Graphite Diamond generated code review
> Graphite had 3 comments:
1. The delete-orphan cascade is incompatible with nullable note_id. When an ActionItem is removed from note.action_items or has its note_id set to None, it will be deleted from the database instead of just being disassociated. This breaks the expected behavior where action items can exist independently without a note (as shown in tests at lines 271-276).

Fix: Remove delete-orphan from the cascade:

action_items = relationship(
    "ActionItem",
    back_populates="note",
    cascade="all, delete",  # Remove delete-orphan
    foreign_keys="ActionItem.note_id",

2. Missing validation that note_id exists before creating the ActionItem. If a non-existent note_id is provided, this will cause a foreign key constraint violation at the database level.

Fix: Add validation:

def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    if payload.note_id is not None:
        note = db.get(Note, payload.note_id)
        if not note:
            raise HTTPException(status_code=404, detail=f"Note with id {payload.note_id} not found")
    item = ActionItem(description=payload.description, completed=False, note_id=payload.note_id)
    # ...

Suggested change
    item = ActionItem(description=payload.description, completed=False, note_id=payload.note_id)
    if payload.note_id is not None:
        note = db.get(Note, payload.note_id)
        if not note:
            raise HTTPException(status_code=404, detail=f"Note with id {payload.note_id} not found")
    item = ActionItem(description=payload.description, completed=False, note_id=payload.note_id)

3. Missing validation when updating note_id. If a non-existent note_id is provided, this will cause a foreign key constraint violation.

Fix: Add validation:

if payload.note_id is not None:
    note = db.get(Note, payload.note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id {payload.note_id} not found")
    item.note_id = payload.note_id

Suggested change
    if payload.note_id is not None:
        item.note_id = payload.note_id
    if payload.note_id is not None:
        note = db.get(Note, payload.note_id)
        if not note:
            raise HTTPException(status_code=404, detail=f"Note with id {payload.note_id} not found")
        item.note_id = payload.note_id

"1. N+1 Query Problem
Lines 21-48 in notes.py and tag endpoints don't eager-load relationships:

# In notes.py list_notes():
from sqlalchemy.orm import selectinload

stmt = select(Note).options(selectinload(Note.tags))
2. Duplicate Code in Tag Association
Lines 170-245 have nearly identical logic:

# Create a generic helper function
def _associate_tags(entity, tag_ids: list[int], db: Session):
    for tag_id in tag_ids:
        tag = db.get(Tag, tag_id)
        if not tag:
            raise HTTPException(404, f"Tag with id {tag_id} not found")
        if tag not in entity.tags:
            entity.tags.append(tag)
3. Transaction Atomicity
Tag association can fail partway through. Either all tags should be added or none:

# Validate all tags exist first, then add them
tags = [db.get(Tag, tid) for tid in tag_association.tag_ids]
if any(t is None for t in tags):
    raise HTTPException(404, "One or more tags not found")

for tag in tags:
    if tag not in note.tags:
        note.tags.append(tag)
4. Stats Query Efficiency
Lines 20-88 runs multiple queries. Combine into a single CTE:

# Use a single query with CTEs instead of multiple queries
5. Case-Insensitive Tag Names
Line 123 allows "urgent" and "Urgent":

# In TagCreate validator:
return v.strip().lower()

# In models.py:
name = Column(String(50), nullable=False, unique=True, index=True)
# Add a check constraint for lowercase
6. Missing Limit on List Endpoint
Line 94 has limit: int = 100 with no max:

limit: int = Query(100, le=200)  # Like notes endpoint
7. Stats Response Model
Line 178 in schemas.py uses generic dict:

class TagUsage(BaseModel):
    id: int
    name: str
    usage_count: int

class TagStats(BaseModel):
    most_used_tags: list[TagUsage]
8. No Filtering by Tags
Add query params to notes/action items endpoints:

def list_notes(
    ...
    tag_ids: list[int] | None = Query(None),
):
    if tag_ids:
        stmt = stmt.join(Note.tags).where(Tag.id.in_(tag_ids))
9. Missing Commits
No db.commit() anywhere - you're using db.flush(). If using auto-commit, document it. Otherwise add commits."

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
