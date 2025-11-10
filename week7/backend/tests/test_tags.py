from fastapi.testclient import TestClient


def test_create_and_list_tags(client: TestClient):
    """Test creating and listing tags."""
    # Create tags
    response1 = client.post("/tags/", json={"name": "urgent", "color": "#FF0000"})
    assert response1.status_code == 201
    tag1 = response1.json()
    assert tag1["name"] == "urgent"
    assert tag1["color"] == "#FF0000"

    response2 = client.post("/tags/", json={"name": "bug"})
    assert response2.status_code == 201
    tag2 = response2.json()
    assert tag2["name"] == "bug"
    assert tag2["color"] is None

    # List tags
    response = client.get("/tags/")
    assert response.status_code == 200
    tags = response.json()
    assert len(tags) == 2
    assert any(t["name"] == "urgent" for t in tags)
    assert any(t["name"] == "bug" for t in tags)


def test_get_tag_by_id(client: TestClient):
    """Test getting a single tag by ID."""
    # Create tag
    create_response = client.post("/tags/", json={"name": "feature", "color": "#00FF00"})
    tag_id = create_response.json()["id"]

    # Get tag
    response = client.get(f"/tags/{tag_id}")
    assert response.status_code == 200
    tag = response.json()
    assert tag["id"] == tag_id
    assert tag["name"] == "feature"
    assert tag["color"] == "#00FF00"


def test_get_nonexistent_tag(client: TestClient):
    """Test getting a tag that doesn't exist."""
    response = client.get("/tags/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_tag(client: TestClient):
    """Test updating a tag."""
    # Create tag
    create_response = client.post("/tags/", json={"name": "old-name", "color": "#000000"})
    tag_id = create_response.json()["id"]

    # Update tag
    response = client.patch(f"/tags/{tag_id}", json={"name": "new-name", "color": "#FFFFFF"})
    assert response.status_code == 200
    updated_tag = response.json()
    assert updated_tag["name"] == "new-name"
    assert updated_tag["color"] == "#FFFFFF"


def test_update_nonexistent_tag(client: TestClient):
    """Test updating a tag that doesn't exist."""
    response = client.patch("/tags/999", json={"name": "nonexistent"})
    assert response.status_code == 404


def test_delete_tag(client: TestClient):
    """Test deleting a tag."""
    # Create tag
    create_response = client.post("/tags/", json={"name": "to-delete"})
    tag_id = create_response.json()["id"]

    # Delete tag
    response = client.delete(f"/tags/{tag_id}")
    assert response.status_code == 204

    # Verify tag is gone
    get_response = client.get(f"/tags/{tag_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_tag(client: TestClient):
    """Test deleting a tag that doesn't exist."""
    response = client.delete("/tags/999")
    assert response.status_code == 404


def test_duplicate_tag_name(client: TestClient):
    """Test that duplicate tag names are rejected."""
    # Create first tag
    client.post("/tags/", json={"name": "duplicate"})

    # Try to create duplicate
    response = client.post("/tags/", json={"name": "duplicate"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_tag_validation_empty_name(client: TestClient):
    """Test that empty tag names are rejected."""
    response = client.post("/tags/", json={"name": ""})
    assert response.status_code == 422


def test_tag_validation_whitespace_only_name(client: TestClient):
    """Test that whitespace-only tag names are rejected."""
    response = client.post("/tags/", json={"name": "   "})
    assert response.status_code == 422


def test_tag_validation_name_too_long(client: TestClient):
    """Test that tag names exceeding max length are rejected."""
    long_name = "a" * 51  # Max is 50
    response = client.post("/tags/", json={"name": long_name})
    assert response.status_code == 422


def test_tag_validation_invalid_color(client: TestClient):
    """Test that invalid color codes are rejected."""
    # Invalid hex codes
    invalid_colors = ["#FFF", "#GGGGGG", "FF0000", "#FF00", "#FFFFFFF"]

    for color in invalid_colors:
        response = client.post("/tags/", json={"name": f"test-{color}", "color": color})
        assert response.status_code == 422


def test_tag_validation_valid_color(client: TestClient):
    """Test that valid color codes are accepted."""
    valid_colors = ["#FF0000", "#00ff00", "#0000FF", "#A1B2C3"]

    for color in valid_colors:
        response = client.post("/tags/", json={"name": f"test-{color}", "color": color})
        assert response.status_code == 201


def test_search_tags(client: TestClient):
    """Test searching tags by name."""
    # Create tags
    client.post("/tags/", json={"name": "python-bug"})
    client.post("/tags/", json={"name": "javascript-bug"})
    client.post("/tags/", json={"name": "feature-request"})

    # Search for tags containing "bug"
    response = client.get("/tags/?search=bug")
    assert response.status_code == 200
    tags = response.json()
    assert len(tags) == 2
    assert all("bug" in t["name"] for t in tags)


def test_associate_tag_with_note(client: TestClient):
    """Test associating a tag with a note."""
    # Create note and tag
    note_response = client.post("/notes/", json={"title": "Test Note", "content": "Test content"})
    note_id = note_response.json()["id"]

    tag_response = client.post("/tags/", json={"name": "important"})
    tag_id = tag_response.json()["id"]

    # Associate tag with note
    response = client.post(f"/tags/notes/{note_id}/tags", json={"tag_ids": [tag_id]})
    assert response.status_code == 201

    # Verify tag is associated
    note_get_response = client.get(f"/notes/{note_id}")
    note = note_get_response.json()
    assert len(note["tags"]) == 1
    assert note["tags"][0]["id"] == tag_id


def test_associate_multiple_tags_with_note(client: TestClient):
    """Test associating multiple tags with a note."""
    # Create note and tags
    note_response = client.post("/notes/", json={"title": "Test Note", "content": "Test content"})
    note_id = note_response.json()["id"]

    tag1 = client.post("/tags/", json={"name": "tag1"}).json()
    tag2 = client.post("/tags/", json={"name": "tag2"}).json()

    # Associate multiple tags
    response = client.post(
        f"/tags/notes/{note_id}/tags", json={"tag_ids": [tag1["id"], tag2["id"]]}
    )
    assert response.status_code == 201

    # Verify both tags are associated
    note = client.get(f"/notes/{note_id}").json()
    assert len(note["tags"]) == 2


def test_disassociate_tag_from_note(client: TestClient):
    """Test removing a tag association from a note."""
    # Create note and tag
    note_response = client.post("/notes/", json={"title": "Test Note", "content": "Test content"})
    note_id = note_response.json()["id"]

    tag_response = client.post("/tags/", json={"name": "removable"})
    tag_id = tag_response.json()["id"]

    # Associate tag
    client.post(f"/tags/notes/{note_id}/tags", json={"tag_ids": [tag_id]})

    # Disassociate tag
    response = client.delete(f"/tags/notes/{note_id}/tags/{tag_id}")
    assert response.status_code == 204

    # Verify tag is removed
    note = client.get(f"/notes/{note_id}").json()
    assert len(note["tags"]) == 0


def test_associate_tag_with_action_item(client: TestClient):
    """Test associating a tag with an action item."""
    # Create action item and tag
    action_item_response = client.post("/action-items/", json={"description": "Test action"})
    item_id = action_item_response.json()["id"]

    tag_response = client.post("/tags/", json={"name": "high-priority"})
    tag_id = tag_response.json()["id"]

    # Associate tag with action item
    response = client.post(f"/tags/action-items/{item_id}/tags", json={"tag_ids": [tag_id]})
    assert response.status_code == 201

    # Verify tag is associated
    item = client.get("/action-items/?skip=0&limit=100").json()[0]
    assert len(item["tags"]) == 1
    assert item["tags"][0]["id"] == tag_id


def test_disassociate_tag_from_action_item(client: TestClient):
    """Test removing a tag association from an action item."""
    # Create action item and tag
    action_item_response = client.post("/action-items/", json={"description": "Test action"})
    item_id = action_item_response.json()["id"]

    tag_response = client.post("/tags/", json={"name": "removable"})
    tag_id = tag_response.json()["id"]

    # Associate tag
    client.post(f"/tags/action-items/{item_id}/tags", json={"tag_ids": [tag_id]})

    # Disassociate tag
    response = client.delete(f"/tags/action-items/{item_id}/tags/{tag_id}")
    assert response.status_code == 204

    # Verify tag is removed
    item = client.get("/action-items/?skip=0&limit=100").json()[0]
    assert len(item["tags"]) == 0


def test_action_item_with_note_id(client: TestClient):
    """Test creating an action item associated with a note."""
    # Create note
    note_response = client.post("/notes/", json={"title": "Test Note", "content": "Test content"})
    note_id = note_response.json()["id"]

    # Create action item associated with note
    response = client.post(
        "/action-items/", json={"description": "Test action", "note_id": note_id}
    )
    assert response.status_code == 201
    action_item = response.json()
    assert action_item["note_id"] == note_id


def test_action_item_without_note_id(client: TestClient):
    """Test creating an action item without a note association."""
    response = client.post("/action-items/", json={"description": "Standalone action"})
    assert response.status_code == 201
    action_item = response.json()
    assert action_item["note_id"] is None


def test_update_action_item_note_id(client: TestClient):
    """Test updating an action item's note association."""
    # Create note and action item
    note_response = client.post("/notes/", json={"title": "Test Note", "content": "Test content"})
    note_id = note_response.json()["id"]

    action_item_response = client.post("/action-items/", json={"description": "Test action"})
    item_id = action_item_response.json()["id"]

    # Update action item to associate with note
    response = client.patch(f"/action-items/{item_id}", json={"note_id": note_id})
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["note_id"] == note_id


def test_delete_note_cascades_to_action_items(client: TestClient):
    """Test that deleting a note also deletes associated action items."""
    # Create note with associated action items
    note_response = client.post("/notes/", json={"title": "Test Note", "content": "Test content"})
    note_id = note_response.json()["id"]

    # Create action items associated with note
    item1_response = client.post(
        "/action-items/", json={"description": "Action 1", "note_id": note_id}
    )
    item2_response = client.post(
        "/action-items/", json={"description": "Action 2", "note_id": note_id}
    )
    item1_id = item1_response.json()["id"]
    item2_id = item2_response.json()["id"]

    # Delete note
    delete_response = client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == 204

    # Verify action items are also deleted
    items_response = client.get("/action-items/?skip=0&limit=100")
    items = items_response.json()
    assert not any(item["id"] == item1_id for item in items)
    assert not any(item["id"] == item2_id for item in items)


def test_delete_tag_removes_associations(client: TestClient):
    """Test that deleting a tag removes all associations."""
    # Create note, action item, and tag
    note = client.post("/notes/", json={"title": "Test Note", "content": "Test content"}).json()
    action_item = client.post("/action-items/", json={"description": "Test action"}).json()
    tag = client.post("/tags/", json={"name": "to-delete"}).json()

    # Associate tag with both
    client.post(f"/tags/notes/{note['id']}/tags", json={"tag_ids": [tag["id"]]})
    client.post(f"/tags/action-items/{action_item['id']}/tags", json={"tag_ids": [tag["id"]]})

    # Delete tag
    client.delete(f"/tags/{tag['id']}")

    # Verify associations are removed
    note_after = client.get(f"/notes/{note['id']}").json()
    items_after = client.get("/action-items/?skip=0&limit=100").json()

    assert len(note_after["tags"]) == 0
    assert all(len(item["tags"]) == 0 for item in items_after)


def test_tags_stats(client: TestClient):
    """Test tags statistics endpoint."""
    # Create tags
    tag1 = client.post("/tags/", json={"name": "tag1"}).json()
    tag2 = client.post("/tags/", json={"name": "tag2"}).json()

    # Create notes and action items
    note1 = client.post("/notes/", json={"title": "Note 1", "content": "Content 1"}).json()
    note2 = client.post("/notes/", json={"title": "Note 2", "content": "Content 2"}).json()
    action_item1 = client.post("/action-items/", json={"description": "Action 1"}).json()

    # Associate tags
    client.post(f"/tags/notes/{note1['id']}/tags", json={"tag_ids": [tag1["id"]]})
    client.post(f"/tags/notes/{note2['id']}/tags", json={"tag_ids": [tag1["id"], tag2["id"]]})
    client.post(f"/tags/action-items/{action_item1['id']}/tags", json={"tag_ids": [tag1["id"]]})

    # Get stats
    response = client.get("/tags/stats/summary")
    assert response.status_code == 200
    stats = response.json()

    assert stats["total_count"] == 2
    assert stats["notes_tagged"] == 2
    assert stats["action_items_tagged"] == 1
    assert len(stats["most_used_tags"]) == 2

    # tag1 should be most used (3 times)
    assert stats["most_used_tags"][0]["name"] == "tag1"
    assert stats["most_used_tags"][0]["usage_count"] == 3


def test_tags_stats_empty_db(client: TestClient):
    """Test tags statistics with empty database."""
    response = client.get("/tags/stats/summary")
    assert response.status_code == 200
    stats = response.json()

    assert stats["total_count"] == 0
    assert stats["notes_tagged"] == 0
    assert stats["action_items_tagged"] == 0
    assert len(stats["most_used_tags"]) == 0
