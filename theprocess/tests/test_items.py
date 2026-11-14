BASE = "/api/v1/items"


def test_health(client):
    assert client.get("/").json() == {"status": "ok"}


def test_create_and_get(client):
    r = client.post(BASE, json={"text": "first"})
    assert r.status_code == 201
    item = r.json()
    assert item["text"] == "first" and item["is_done"] is False and item["id"]

    r = client.get(f"{BASE}/{item['id']}")
    assert r.status_code == 200 and r.json()["text"] == "first"


def test_list_newest_first_and_limit(client):
    for t in ["a", "b", "c"]:
        client.post(BASE, json={"text": t})
    assert [i["text"] for i in client.get(BASE).json()] == ["c", "b", "a"]
    assert len(client.get(f"{BASE}?limit=2").json()) == 2


def test_update_only_sent_fields(client):
    item_id = client.post(BASE, json={"text": "x"}).json()["id"]
    r = client.patch(f"{BASE}/{item_id}", json={"is_done": True})
    assert r.status_code == 200
    assert r.json()["is_done"] is True and r.json()["text"] == "x"


def test_delete(client):
    item_id = client.post(BASE, json={"text": "x"}).json()["id"]
    assert client.delete(f"{BASE}/{item_id}").status_code == 204
    assert client.get(f"{BASE}/{item_id}").status_code == 404


def test_not_found_and_validation(client):
    assert client.get(f"{BASE}/nope").status_code == 404
    assert client.patch(f"{BASE}/nope", json={"is_done": True}).status_code == 404
    assert client.delete(f"{BASE}/nope").status_code == 404
    assert client.post(BASE, json={}).status_code == 422
    assert client.post(BASE, json={"text": ""}).status_code == 422
    assert client.get(f"{BASE}?limit=0").status_code == 422
