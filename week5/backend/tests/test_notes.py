def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    response = r.json()
    assert response["ok"] is True
    assert "data" in response
    data = response["data"]
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    response = r.json()
    assert response["ok"] is True
    assert "data" in response
    items = response["data"]
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200
    response = r.json()
    assert response["ok"] is True

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    response = r.json()
    assert response["ok"] is True
    items = response["data"]
    assert len(items) >= 1


def test_create_note_validation_error(client):
    # Empty title
    payload = {"title": "", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False
    assert "error" in response
    assert response["error"]["code"] == "VALIDATION_ERROR"
    assert "message" in response["error"]

    # Whitespace only title
    payload = {"title": "   ", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False
    assert response["error"]["code"] == "VALIDATION_ERROR"

    # Empty content
    payload = {"title": "Test", "content": ""}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False
    assert response["error"]["code"] == "VALIDATION_ERROR"


def test_get_note_not_found(client):
    r = client.get("/notes/99999")
    assert r.status_code == 404
    response = r.json()
    assert response["ok"] is False
    assert "error" in response
    assert response["error"]["code"] == "NOT_FOUND"
    assert response["error"]["message"] == "Note not found"


def test_create_note_with_max_length_title(client):
    # Title at max length (200 chars) should succeed
    long_title = "a" * 200
    payload = {"title": long_title, "content": "Test content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    response = r.json()
    assert response["ok"] is True
    assert response["data"]["title"] == long_title


def test_create_note_with_too_long_title(client):
    # Title over max length (201 chars) should fail
    too_long_title = "a" * 201
    payload = {"title": too_long_title, "content": "Test content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False
    assert response["error"]["code"] == "VALIDATION_ERROR"


def test_create_note_missing_fields(client):
    # Missing title
    payload = {"content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False

    # Missing content
    payload = {"title": "Test"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False

    # Empty payload
    r = client.post("/notes/", json={})
    assert r.status_code == 422
    response = r.json()
    assert response["ok"] is False


def test_search_notes_with_no_results(client):
    # Search for something that doesn't exist
    r = client.get("/notes/search/", params={"q": "nonexistent12345"})
    assert r.status_code == 200
    response = r.json()
    assert response["ok"] is True
    assert len(response["data"]) == 0


def test_list_notes_empty(client):
    # With empty database
    r = client.get("/notes/")
    assert r.status_code == 200
    response = r.json()
    assert response["ok"] is True
    assert isinstance(response["data"], list)


def test_search_notes_case_insensitive(client):
    # Create note with mixed case
    payload = {"title": "Important Meeting", "content": "Discuss PROJECT details"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201

    # Search with lowercase should match
    r = client.get("/notes/search/", params={"q": "project"})
    assert r.status_code == 200
    response = r.json()
    assert response["ok"] is True
    assert len(response["data"]) >= 1
    found = any("PROJECT" in note["content"] for note in response["data"])
    assert found
