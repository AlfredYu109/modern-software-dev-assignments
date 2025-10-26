"""Frontend integration tests - lightweight API integration tests."""


def test_frontend_root_endpoint(client):
    """Test that the root endpoint serves the frontend."""
    r = client.get("/")
    assert r.status_code == 200
    # Should be HTML content
    assert b"<!doctype html>" in r.content or b"<!DOCTYPE html>" in r.content


def test_api_endpoints_cors_and_json(client):
    """Test that API endpoints return proper JSON responses."""
    # Notes endpoint
    r = client.get("/notes/")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/json")

    # Action items endpoint
    r = client.get("/action-items/")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/json")


def test_search_integration_workflow(client):
    """Test the full search workflow as frontend would use it."""
    # Create some notes
    notes_data = [
        {"title": "Project Planning", "content": "Discuss requirements and timeline"},
        {"title": "Meeting Notes", "content": "Team sync on project progress"},
        {"title": "Budget Review", "content": "Quarterly financial planning"},
    ]

    for note in notes_data:
        r = client.post("/notes/", json=note)
        assert r.status_code == 201

    # Search for "project" (should match 2 notes)
    r = client.get("/notes/search/", params={"q": "project"})
    assert r.status_code == 200
    results = r.json()["data"]
    assert len(results) >= 2

    # Search for "budget" (should match 1 note)
    r = client.get("/notes/search/", params={"q": "budget"})
    assert r.status_code == 200
    results = r.json()["data"]
    assert len(results) >= 1

    # Search with no query (should return all)
    r = client.get("/notes/search/")
    assert r.status_code == 200
    results = r.json()["data"]
    assert len(results) >= 3


def test_action_items_complete_workflow(client):
    """Test the complete action item workflow as frontend would use it."""
    # Create action items
    tasks = [
        {"description": "Review pull request"},
        {"description": "Update documentation"},
        {"description": "Fix bug #123"},
    ]

    created_ids = []
    for task in tasks:
        r = client.post("/action-items/", json=task)
        assert r.status_code == 201
        created_ids.append(r.json()["data"]["id"])

    # List all items (all should be incomplete)
    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()["data"]
    assert len(items) == 3
    assert all(not item["completed"] for item in items)

    # Complete first two items
    for item_id in created_ids[:2]:
        r = client.put(f"/action-items/{item_id}/complete")
        assert r.status_code == 200
        assert r.json()["data"]["completed"] is True

    # List again - 2 should be completed
    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()["data"]
    completed = [item for item in items if item["completed"]]
    incomplete = [item for item in items if not item["completed"]]
    assert len(completed) == 2
    assert len(incomplete) == 1


def test_optimistic_update_scenario(client):
    """
    Test scenario simulating optimistic UI updates.
    Frontend would show immediate feedback, then verify with server.
    """
    # Create a note
    payload = {"title": "Test Note", "content": "Original content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["data"]["id"]

    # Simulate frontend optimistically displaying the note
    # Then verify it exists on server
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    note = r.json()["data"]
    assert note["title"] == "Test Note"
    assert note["content"] == "Original content"

    # Simulate optimistic completion of action item
    payload = {"description": "Quick task"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201
    item_id = r.json()["data"]["id"]

    # Frontend shows it as complete immediately
    # Then syncs with server
    r = client.put(f"/action-items/{item_id}/complete")
    assert r.status_code == 200
    assert r.json()["data"]["completed"] is True


def test_error_handling_for_frontend(client):
    """Test that frontend receives proper error responses."""
    # Try to get non-existent note
    r = client.get("/notes/99999")
    assert r.status_code == 404
    error = r.json()
    assert error["ok"] is False
    assert "error" in error
    assert "message" in error["error"]

    # Try to create invalid note
    r = client.post("/notes/", json={"title": "", "content": "test"})
    assert r.status_code == 422
    error = r.json()
    assert error["ok"] is False
    assert error["error"]["code"] == "VALIDATION_ERROR"


def test_pagination_placeholder(client):
    """
    Test placeholder for pagination (not yet implemented).
    This tests current behavior - when pagination is added, update this test.
    """
    # Create many notes
    for i in range(15):
        payload = {"title": f"Note {i}", "content": f"Content {i}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201

    # Currently returns all notes
    r = client.get("/notes/")
    assert r.status_code == 200
    notes = r.json()["data"]
    assert len(notes) >= 15

    # When pagination is added, this test should verify:
    # - page parameter works
    # - page_size parameter works
    # - total count is returned
    # - items array has correct length
