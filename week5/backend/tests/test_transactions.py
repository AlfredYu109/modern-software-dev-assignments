"""Tests for transaction behavior and database integrity."""


def test_transaction_rollback_on_error(client):
    """Test that database transactions rollback on errors."""
    # Create a valid note
    payload = {"title": "Valid note", "content": "Content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201

    # Get initial count
    r = client.get("/notes/")
    initial_count = len(r.json()["data"])

    # Try to create an invalid note (should fail validation)
    invalid_payload = {"title": "", "content": "Content"}
    r = client.post("/notes/", json=invalid_payload)
    assert r.status_code == 422

    # Count should remain the same (transaction rolled back)
    r = client.get("/notes/")
    final_count = len(r.json()["data"])
    assert final_count == initial_count


def test_concurrent_note_creation(client):
    """Test creating multiple notes doesn't cause conflicts."""
    notes = []
    for i in range(10):
        payload = {"title": f"Note {i}", "content": f"Content {i}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201
        notes.append(r.json()["data"])

    # All notes should have unique IDs
    ids = [note["id"] for note in notes]
    assert len(ids) == len(set(ids)), "IDs should be unique"

    # Verify all notes are in the database
    r = client.get("/notes/")
    assert r.status_code == 200
    all_notes = r.json()["data"]
    assert len(all_notes) >= 10


def test_action_item_completion_consistency(client):
    """Test that action item completion maintains consistency."""
    # Create multiple action items
    items = []
    for i in range(5):
        payload = {"description": f"Task {i}"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201
        items.append(r.json()["data"])

    # Complete some of them
    for i in range(3):
        r = client.put(f"/action-items/{items[i]['id']}/complete")
        assert r.status_code == 200

    # Verify state is consistent
    r = client.get("/action-items/")
    all_items = r.json()["data"]

    completed_count = sum(1 for item in all_items if item["completed"])
    assert completed_count == 3

    incomplete_count = sum(1 for item in all_items if not item["completed"])
    assert incomplete_count == 2


def test_note_creation_with_special_characters(client):
    """Test that special characters are handled correctly."""
    special_chars_title = "Title with 'quotes' and \"double quotes\""
    special_chars_content = "Content with <html>, & ampersand, and unicode: 你好"

    payload = {"title": special_chars_title, "content": special_chars_content}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201

    note_id = r.json()["data"]["id"]

    # Retrieve and verify
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    note = r.json()["data"]
    assert note["title"] == special_chars_title
    assert note["content"] == special_chars_content


def test_database_integrity_after_multiple_operations(client):
    """Test database integrity after a mix of operations."""
    # Create notes
    created_notes = []
    for i in range(5):
        payload = {"title": f"Note {i}", "content": f"Content {i}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201
        created_notes.append(r.json()["data"]["id"])

    # Create action items
    created_items = []
    for i in range(5):
        payload = {"description": f"Task {i}"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201
        created_items.append(r.json()["data"]["id"])

    # Search notes
    r = client.get("/notes/search/", params={"q": "Note"})
    assert r.status_code == 200
    assert len(r.json()["data"]) >= 5

    # Complete some items
    for item_id in created_items[:3]:
        r = client.put(f"/action-items/{item_id}/complete")
        assert r.status_code == 200

    # Verify everything is still consistent
    r = client.get("/notes/")
    assert r.status_code == 200
    assert len(r.json()["data"]) >= 5

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()["data"]
    assert len(items) >= 5
    completed = [item for item in items if item["completed"]]
    assert len(completed) == 3
