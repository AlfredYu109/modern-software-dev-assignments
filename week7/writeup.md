# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: Alfred Yu \
SUNet ID: ayu1001 \
Citations: Windsurf + Graphite

This assignment took me about **TODO** hours to do.


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> https://app.graphite.com/github/pr/AlfredYu109/modern-software-dev-assignments/1/Add-activity-feed-API

b. PR Description
> Hardened week7’s notes/action-items APIs with stricter Pydantic validators, bounded pagination, and explicit sort allowlists to block malformed input and unsafe column access.

Added missing resource endpoints (GET/DELETE for action items, DELETE for notes) plus consistent 404 helpers and 204 responses, and fixed FastAPI’s static-path resolution so the app runs inside the test harness.

Extended the week7 backend tests to cover all new validation paths and destructive endpoints.

c. Graphite Diamond generated code review
> See PR
"The file is missing a newline at the end, which will trigger the end-of-file-fixer pre-commit hook that's being added in this PR. Please add a newline character at the end of the file to ensure compatibility with the pre-commit configuration and follow standard file formatting conventions."

"The PR title mentions "Add activity feed API", but there's no router for activity feed included in the FastAPI application. The code imports routers for notes and action items, but is missing an import and router inclusion for the activity feed functionality. Consider adding:

from .routers import activity_feed as activity_feed_router
And then including it in the app:

app.include_router(activity_feed_router.router)
This would align the implementation with the PR title's stated purpose."

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> https://app.graphite.com/github/pr/AlfredYu109/modern-software-dev-assignments/2/Task-2

b. PR Description
> "TL;DR
Enhanced action item extraction with advanced pattern recognition and deduplication logic

What changed?
Implemented a more sophisticated action item extraction system in extract.py that recognizes various patterns:
TODO/action item prefixes
Checkbox items
Bullet points with action verbs
Assignments (e.g., "Alice: follow up...")
Phrases with modal verbs ("should", "need to")
Lines with due dates or urgency indicators
Added deduplication to prevent duplicate action items
Created comprehensive test cases in test_extract.py to verify extraction logic
Preserved backward compatibility with existing extraction patterns
How to test?
Run the new test suite to verify extraction functionality:

pytest backend/tests/test_extract.py
The tests validate:

Recognition of various action item formats (TODOs, checkboxes, assignments, etc.)
Proper deduplication of similar items
Filtering out non-action content
Why make this change?
The previous extraction logic was overly simplistic, only recognizing items with "todo:" or "action:" prefixes, or those ending with exclamation marks. This enhancement significantly improves the system's ability to identify action items in real-world meeting notes that use diverse formats and linguistic patterns, making the feature more useful and accurate for end users."

c. Graphite Diamond generated code review
> "Graphite Agent found no issues"

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
