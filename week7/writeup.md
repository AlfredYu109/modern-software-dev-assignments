# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Alfred Yu** \
SUNet ID: **ayu1001** \
Citations: **Claude Code and Graphite**

This assignment took me about **5** hours to do.


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> https://app.graphite.com/github/pr/AlfredYu109/modern-software-dev-assignments/3/Task-1-Claude-Try

b. PR Description
Description of the problem: There are limited API endpoints, which means that there is limited API functionality. The approach done here was to prompt Claude to add additional API endpoints, such as bulk operations for notes, and endpoints htat keep track of statistics on the notes. Specifically, Claude Code implemented: DELETE `/notes/{id}` and `/action-items/{id}`, POST `/notes/bulk` and `/notes/bulk/delete` (max 100 items), PUT `/action-items/bulk/complete`, GET `/notes/stats/summary` and `/action-items/stats/summary`, plus Pydantic validators with `@field_validator` for whitespace trimming and length constraints.

Testing: Claude Code ran `make test` which executed 36 pytest tests (all passing), and manually tested with `curl -X POST http://localhost:8000/notes/bulk -d '{"notes":[{"title":"Test","content":"Content"}]}'` which successfully created bulk notes.

Limitations: There is still limited functionality on some endpoints - these endpoints are not exhaustive.

Follow-up:  More features could be added, and API efficiency can be further improved on.



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
Description of the problem: The extraction logic is currently limited. We want more sophisticated pattern recognition, so we enhance the Regex coverage including additional action markers and more detailed action item extraction.

The testing that can be done is via make test or attempted action items from the various text formats.

make test
# or
poetry run pytest backend/tests/test_extract.py -v
Try extracting action items from various text formats:

from backend.app.services.extract import extract_action_items, extract_action_items_detailed


Limitations may be that the Regex coverage is not necessarily perfect. False positives may be possible, and the numbers of len > 10 and len > 5 may be arbitrary.

Follow-up: It may be wiser to implement parsing with ML rather than hard-coding. Tokenization and NLP parsing may be a better way of doing this.


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

Description of the problem: There didn't exist database models with relationships. The code added a new Tag mjodel and implemented relationships between the Tags and Action items.

Testing: You can run the test suite generated at pytest backend/tests/test_tags.py.

Limitations: There isn't filtering on tags, and there are no limits on tags per note, which may be harmful in causing relational overloads.

Follow-up: A limitation should be added. Bulk tag operations to immediately operate on a series of tags may be helpful as well.

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
> https://app.graphite.com/github/pr/AlfredYu109/modern-software-dev-assignments/6/Task-4

b. PR Description
Problem: The tests for pagination and sorting functionality were not comprehensive.

What changed:  Added comprehensive test suite for pagination and sorting functionality across Notes and Action Items endpoints.


Testing: Run the test suite with pytest backend/tests/test_pagination_sorting.py
We can test specific test classes with commands like:
pytest backend/tests/test_pagination_sorting.py::TestNotesPagination
pytest backend/tests/test_pagination_sorting.py::TestNotesSorting
pytest backend/tests/test_pagination_sorting.py::TestActionItemsPagination
pytest backend/tests/test_pagination_sorting.py::TestActionItemsSorting
pytest backend/tests/test_pagination_sorting.py::TestEdgeCases

Tradeoffs:

Tests use time.sleep() to ensure different timestamps, which slows down test execution
Tests create actual database records that require cleanup via fixtures
Some tests depend on sorting order which could be fragile if default sort changes
Limitations:
Tests don't cover all possible combinations of sort fields with each other
No tests for concurrent pagination scenarios (race conditions)
Tests rely on database state isolation between test methods
No performance/load tests for pagination with large datasets (1000+ items)
Tests assume consistent database ordering within same timestamp

Follow-ups:

Add performance benchmarks for pagination with large datasets (10K+ items)
Test concurrent access patterns to verify pagination consistency under load
Add tests for additional sort fields if new sortable columns are added
Consider replacing time.sleep() with mocked/controlled timestamps for faster tests
Add tests for pagination cursor patterns if implemented in the future
Test behavior with different database backends (PostgreSQL vs SQLite

c. Graphite Diamond generated code review
> Graphite Diamond didn't have direct comments, but when prompted further, suggested the following:
"1. Remove code duplication with fixtures and helpers
Lines 14-124 and 256-327 have nearly identical tests for Notes and Action Items.

# Add to conftest.py or top of file
import pytest

@pytest.fixture
def created_notes(client):
    """Factory fixture for creating test notes."""
    def _create(count, **kwargs):
        ids = []
        for i in range(count):
            response = client.post("/notes/", json={
                "title": kwargs.get("title", f"Note {i}"),
                "content": kwargs.get("content", f"Content {i}")
            })
            ids.append(response.json()["id"])
        return ids
    return _create

# Then use: created_notes(10) instead of loops
2. Replace time.sleep() with controlled timestamps
Lines 137, 153, 204, etc. use time.sleep() which is slow and flaky.

from freezegun import freeze_time
from datetime import datetime, timedelta

def test_sort_by_created_at_descending(self, client):
    base_time = datetime(2024, 1, 1)
    for i in range(5):
        with freeze_time(base_time + timedelta(seconds=i)):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
3. Use parametrization for similar tests
TestNotesPagination and TestActionItemsPagination are duplicates.

@pytest.mark.parametrize("endpoint,payload", [
    ("/notes/", {"title": "Note {}", "content": "Content {}"}),
    ("/action-items/", {"description": "Task {}"}),
])
class TestPagination:
    def test_basic_pagination(self, client, endpoint, payload):
        # Create 10 items
        for i in range(10):
            client.post(endpoint, json={k: v.format(i) for k, v in payload.items()})
        # ... rest of test
4. Fix weak assertions
Line 74: assert len(notes) >= 3 should be exact.

assert len(notes) == 3  # We created exactly 3, should get exactly 3
5. Extract constants
Magic numbers throughout should be constants:

MAX_LIMIT = 200
DEFAULT_PAGE_SIZE = 5
6. Better test isolation
Lines 175-179: Filtering "our notes" suggests data leakage.

# Either use database transactions that rollback, or:
@pytest.fixture(autouse=True)
def isolate_db(db):
    yield
    db.query(Note).delete()
    db.query(ActionItem).delete()
    db.commit()
7. Test negative limit
Missing test for limit=-1 which should likely return validation error.

8. More specific error assertions
Line 291: Should verify the error message too.

response = client.get("/action-items/", params={"limit": 201})
assert response.status_code == 422
assert "limit" in response.json()["detail"][0]["loc"]
These changes would make tests faster, more maintainable, and more reliable."

## Brief Reflection
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> I generally had trouble making comments. I thought the code Claude generated was pretty well-thought out and comprehensive (Graphite seemingly did too, given that there was only one action item where it had comments on the code, and even then, the comments were on things that I completely did not catch and was not aware of). I think one area that I noted was relative security - I was concerned that there was no rate limitations or authentications, which would be something that Semgrep would likely flag. I think the comments that I ended up making were generally more related to security than anything else.

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> Graphite's AI generated comments were generally more comprehensive. To be fair, full-stack programming isn't something I have much expertise in and would consider myself a thorough expert in either. I think Graphite generally didn't comment as much on security, but I think that's because it was a bit more focused on the code itself, and I think I just happened to have that heuristic because of the previous Semgrep assignment.

c. When the AI reviews were better/worse than yours (cite specific examples)
> I didn't have comments on specific lines like Grpahite did. For example, this comment: ""The delete-orphan cascade is incompatible with nullable note_id. When an ActionItem is removed from note.action_items or has its note_id set to None, it will be deleted from the database instead of just being disassociated. This breaks the expected behavior where action items can exist independently without a note (as shown in tests at lines 271-276)." was something I would not have noticed, but Graphite did. I think being able to parse massive PRs, like the ones generated by Claude, was effective as well. Another example is this comment: "Missing validation that note_id exists before creating the ActionItem. If a non-existent note_id is provided, this will cause a foreign key constraint violation at the database level." I did not catch this at all, and given how long the PRs were, I found that I glossed over them and didn't look terribly in depth.

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
> I actually think AI reviews were fairly trustworthy (this is also as someone who has very limited experience with these technologies and is not a master coder by any means), especially in this situation when the PRs generated were massive. It reminded me of what was mentioned in class, specifically about how AI reviews will be important because of the sheer amount of code being generated.  One thing to note is that it may be troublesome to try and force things without a clear direction, for example, forcing Graphite to find code errors where there aren't any may result in hallucinations that actually harm your code instead of helping. I think generally, it's always best to manually look over the code errors that were highlighted to see if they are valid.
