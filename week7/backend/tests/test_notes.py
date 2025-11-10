def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_delete_note(client):
    # Create a note
    r = client.post("/notes/", json={"title": "To Delete", "content": "Will be deleted"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Delete the note
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    # Verify it's gone
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_nonexistent_note(client):
    r = client.delete("/notes/99999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_validation_empty_title(client):
    r = client.post("/notes/", json={"title": "", "content": "Content"})
    assert r.status_code == 422


def test_validation_whitespace_only_title(client):
    r = client.post("/notes/", json={"title": "   ", "content": "Content"})
    assert r.status_code == 422


def test_validation_title_too_long(client):
    r = client.post("/notes/", json={"title": "x" * 201, "content": "Content"})
    assert r.status_code == 422


def test_validation_empty_content(client):
    r = client.post("/notes/", json={"title": "Title", "content": ""})
    assert r.status_code == 422


def test_validation_whitespace_trimming(client):
    r = client.post("/notes/", json={"title": "  Trimmed  ", "content": "  Content  "})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Trimmed"
    assert data["content"] == "Content"


def test_bulk_create_notes(client):
    payload = {
        "notes": [
            {"title": "Note 1", "content": "Content 1"},
            {"title": "Note 2", "content": "Content 2"},
            {"title": "Note 3", "content": "Content 3"},
        ]
    }
    r = client.post("/notes/bulk", json=payload)
    assert r.status_code == 201
    notes = r.json()
    assert len(notes) == 3
    assert notes[0]["title"] == "Note 1"
    assert notes[1]["title"] == "Note 2"
    assert notes[2]["title"] == "Note 3"


def test_bulk_create_empty_list(client):
    r = client.post("/notes/bulk", json={"notes": []})
    assert r.status_code == 422


def test_bulk_create_too_many(client):
    payload = {"notes": [{"title": f"Note {i}", "content": f"Content {i}"} for i in range(101)]}
    r = client.post("/notes/bulk", json=payload)
    assert r.status_code == 422


def test_bulk_delete_notes(client):
    # Create three notes
    ids = []
    for i in range(3):
        r = client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
        assert r.status_code == 201
        ids.append(r.json()["id"])

    # Bulk delete
    r = client.post("/notes/bulk/delete", json={"ids": ids})
    assert r.status_code == 200
    assert r.json()["deleted_count"] == 3

    # Verify all are deleted
    for note_id in ids:
        r = client.get(f"/notes/{note_id}")
        assert r.status_code == 404


def test_bulk_delete_partial_missing(client):
    # Create one note
    r = client.post("/notes/", json={"title": "Note", "content": "Content"})
    note_id = r.json()["id"]

    # Try to delete it plus a nonexistent one
    r = client.post("/notes/bulk/delete", json={"ids": [note_id, 99999]})
    assert r.status_code == 404
    assert "Missing IDs" in r.json()["detail"]


def test_bulk_delete_empty_list(client):
    r = client.post("/notes/bulk/delete", json={"ids": []})
    assert r.status_code == 422


def test_notes_stats(client):
    # Create some notes
    client.post("/notes/", json={"title": "Note 1", "content": "Short"})
    client.post("/notes/", json={"title": "Note 2", "content": "Medium length"})
    client.post("/notes/", json={"title": "Note 3", "content": "Very long content here"})

    r = client.get("/notes/stats/summary")
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_count"] >= 3
    assert stats["total_characters"] > 0
    assert stats["average_content_length"] > 0


def test_notes_stats_empty_db(client):
    r = client.get("/notes/stats/summary")
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_count"] == 0
    assert stats["total_characters"] == 0
    assert stats["average_content_length"] == 0.0
