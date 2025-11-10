def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_delete_action_item(client):
    # Create an action item
    r = client.post("/action-items/", json={"description": "To delete"})
    assert r.status_code == 201
    item_id = r.json()["id"]

    # Delete it
    r = client.delete(f"/action-items/{item_id}")
    assert r.status_code == 204

    # Verify it's gone
    r = client.get("/action-items/")
    items = r.json()
    assert not any(item["id"] == item_id for item in items)


def test_delete_nonexistent_action_item(client):
    r = client.delete("/action-items/99999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_validation_empty_description(client):
    r = client.post("/action-items/", json={"description": ""})
    assert r.status_code == 422


def test_validation_whitespace_only_description(client):
    r = client.post("/action-items/", json={"description": "   "})
    assert r.status_code == 422


def test_validation_description_too_long(client):
    r = client.post("/action-items/", json={"description": "x" * 501})
    assert r.status_code == 422


def test_validation_description_trimming(client):
    r = client.post("/action-items/", json={"description": "  Trimmed  "})
    assert r.status_code == 201
    data = r.json()
    assert data["description"] == "Trimmed"


def test_bulk_create_action_items(client):
    payload = {
        "items": [
            {"description": "Task 1"},
            {"description": "Task 2"},
            {"description": "Task 3"},
        ]
    }
    r = client.post("/action-items/bulk", json=payload)
    assert r.status_code == 201
    items = r.json()
    assert len(items) == 3
    assert items[0]["description"] == "Task 1"
    assert items[1]["description"] == "Task 2"
    assert items[2]["description"] == "Task 3"
    assert all(not item["completed"] for item in items)


def test_bulk_create_action_items_empty_list(client):
    r = client.post("/action-items/bulk", json={"items": []})
    assert r.status_code == 422


def test_bulk_create_action_items_too_many(client):
    payload = {"items": [{"description": f"Task {i}"} for i in range(101)]}
    r = client.post("/action-items/bulk", json=payload)
    assert r.status_code == 422


def test_bulk_delete_action_items(client):
    # Create three items
    ids = []
    for i in range(3):
        r = client.post("/action-items/", json={"description": f"Task {i}"})
        assert r.status_code == 201
        ids.append(r.json()["id"])

    # Bulk delete
    r = client.post("/action-items/bulk/delete", json={"ids": ids})
    assert r.status_code == 200
    assert r.json()["deleted_count"] == 3

    # Verify all are deleted
    r = client.get("/action-items/")
    items = r.json()
    for deleted_id in ids:
        assert not any(item["id"] == deleted_id for item in items)


def test_bulk_delete_action_items_partial_missing(client):
    # Create one item
    r = client.post("/action-items/", json={"description": "Task"})
    item_id = r.json()["id"]

    # Try to delete it plus a nonexistent one
    r = client.post("/action-items/bulk/delete", json={"ids": [item_id, 99999]})
    assert r.status_code == 404
    assert "Missing IDs" in r.json()["detail"]


def test_bulk_delete_action_items_empty_list(client):
    r = client.post("/action-items/bulk/delete", json={"ids": []})
    assert r.status_code == 422


def test_bulk_complete_action_items(client):
    # Create three items
    ids = []
    for i in range(3):
        r = client.post("/action-items/", json={"description": f"Task {i}"})
        assert r.status_code == 201
        ids.append(r.json()["id"])

    # Bulk complete
    r = client.put("/action-items/bulk/complete", json={"ids": ids})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 3
    assert all(item["completed"] for item in items)

    # Verify via list endpoint
    r = client.get("/action-items/", params={"completed": True})
    completed_items = r.json()
    for item_id in ids:
        assert any(item["id"] == item_id for item in completed_items)


def test_bulk_complete_partial_missing(client):
    # Create one item
    r = client.post("/action-items/", json={"description": "Task"})
    item_id = r.json()["id"]

    # Try to complete it plus a nonexistent one
    r = client.put("/action-items/bulk/complete", json={"ids": [item_id, 99999]})
    assert r.status_code == 404
    assert "Missing IDs" in r.json()["detail"]


def test_bulk_complete_empty_list(client):
    r = client.put("/action-items/bulk/complete", json={"ids": []})
    assert r.status_code == 422


def test_action_items_stats(client):
    # Create some items
    client.post("/action-items/", json={"description": "Task 1"})
    client.post("/action-items/", json={"description": "Task 2"})
    r = client.post("/action-items/", json={"description": "Task 3"})
    item_id = r.json()["id"]

    # Complete one
    client.put(f"/action-items/{item_id}/complete")

    r = client.get("/action-items/stats/summary")
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_count"] >= 3
    assert stats["completed_count"] >= 1
    assert stats["pending_count"] >= 2
    assert 0 <= stats["completion_rate"] <= 100


def test_action_items_stats_empty_db(client):
    r = client.get("/action-items/stats/summary")
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_count"] == 0
    assert stats["completed_count"] == 0
    assert stats["pending_count"] == 0
    assert stats["completion_rate"] == 0.0


def test_action_items_stats_all_completed(client):
    # Create and complete all items
    for i in range(3):
        r = client.post("/action-items/", json={"description": f"Task {i}"})
        item_id = r.json()["id"]
        client.put(f"/action-items/{item_id}/complete")

    r = client.get("/action-items/stats/summary")
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_count"] >= 3
    assert stats["completed_count"] == stats["total_count"]
    assert stats["pending_count"] == 0
    assert stats["completion_rate"] == 100.0
