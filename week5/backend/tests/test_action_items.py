def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    response = r.json()
    assert response["ok"] is True
    assert "data" in response
    item = response["data"]
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    response = r.json()
    assert response["ok"] is True
    done = response["data"]
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    response = r.json()
    assert response["ok"] is True
    items = response["data"]
    assert len(items) == 1


def test_create_action_item_validation_error(client):
    # Empty description
    payload = {"description": ""}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False
    assert "error" in response
    assert response["error"]["code"] == "VALIDATION_ERROR"

    # Whitespace only description
    payload = {"description": "   "}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False
    assert response["error"]["code"] == "VALIDATION_ERROR"


def test_complete_action_item_not_found(client):
    r = client.put("/action-items/99999/complete")
    assert r.status_code == 404
    response = r.json()
    assert response["ok"] is False
    assert "error" in response
    assert response["error"]["code"] == "NOT_FOUND"
    assert response["error"]["message"] == "Action item not found"


def test_list_action_items_empty(client):
    # Empty database should return empty list
    r = client.get("/action-items/")
    assert r.status_code == 200
    response = r.json()
    assert response["ok"] is True
    assert isinstance(response["data"], list)
    assert len(response["data"]) == 0


def test_create_action_item_missing_field(client):
    # Empty payload
    r = client.post("/action-items/", json={})
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False
    assert response["error"]["code"] == "VALIDATION_ERROR"


def test_complete_action_item_idempotent(client):
    # Create and complete an action item
    payload = {"description": "Task to complete"}
    r = client.post("/action-items/", json=payload)
    item_id = r.json()["data"]["id"]

    # Complete it once
    r = client.put(f"/action-items/{item_id}/complete")
    assert r.status_code == 200
    assert r.json()["data"]["completed"] is True

    # Complete it again - should still work (idempotent)
    r = client.put(f"/action-items/{item_id}/complete")
    assert r.status_code == 200
    assert r.json()["data"]["completed"] is True


def test_create_multiple_action_items(client):
    # Create multiple items
    items = [
        {"description": "First task"},
        {"description": "Second task"},
        {"description": "Third task"},
    ]

    created_ids = []
    for item in items:
        r = client.post("/action-items/", json=item)
        assert r.status_code == 201
        created_ids.append(r.json()["data"]["id"])

    # List should have all three
    r = client.get("/action-items/")
    assert r.status_code == 200
    response = r.json()
    assert len(response["data"]) == 3

    # All should be incomplete initially
    for item in response["data"]:
        assert item["completed"] is False


def test_action_item_with_long_description(client):
    # Very long description should work
    long_desc = "x" * 1000
    payload = {"description": long_desc}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201
    response = r.json()
    assert response["data"]["description"] == long_desc
