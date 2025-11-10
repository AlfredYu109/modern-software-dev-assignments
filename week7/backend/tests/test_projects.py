def test_project_crud_and_relationships(client):
    payload = {"name": "Backend Revamp", "description": "API polish"}
    r = client.post("/projects/", json=payload)
    assert r.status_code == 201, r.text
    project = r.json()
    assert project["name"] == payload["name"]

    r = client.get("/projects/")
    assert r.status_code == 200
    assert any(p["id"] == project["id"] for p in r.json())

    item_payload = {"description": "Sync with design", "project_id": project["id"]}
    r = client.post("/action-items/", json=item_payload)
    assert r.status_code == 201
    action_item = r.json()
    assert action_item["project"]["id"] == project["id"]

    r = client.get(f"/projects/{project['id']}/action-items")
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = client.get("/action-items/", params={"project_id": project["id"]})
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = client.patch(f"/action-items/{action_item['id']}", json={"project_id": None})
    assert r.status_code == 200
    assert r.json()["project_id"] is None

    r = client.patch(f"/projects/{project['id']}", json={"name": "Backend 2"})
    assert r.status_code == 200
    assert r.json()["name"] == "Backend 2"

    r = client.delete(f"/projects/{project['id']}")
    assert r.status_code == 204

    r = client.get(f"/projects/{project['id']}")
    assert r.status_code == 404
