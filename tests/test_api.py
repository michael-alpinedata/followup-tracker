"""Integration tests: HTTP -> FastAPI -> SQLAlchemy -> database."""


def make(client, **overrides):
    payload = {"name": "Data engineer @ Acme", "organization": "Acme", **overrides}
    return client.post("/api/entries", json=payload)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}


def test_create_and_list_persists(client):
    r = make(client)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] and body["status"] == "to_contact" and body["due"] is True
    listed = client.get("/api/entries").json()
    assert [e["name"] for e in listed] == ["Data engineer @ Acme"]


def test_validation_rejects_bad_status_and_empty_name(client):
    assert make(client, status="nope").status_code == 422
    assert make(client, name="").status_code == 422
    assert make(client, followup_days=0).status_code == 422


def test_mark_contacted_sets_date_and_removes_from_due(client):
    entry_id = make(client).json()["id"]
    r = client.post(f"/api/entries/{entry_id}/contacted")
    assert r.status_code == 200
    body = r.json()
    assert body["last_contact"] == "2026-11-15"
    assert body["status"] == "waiting"
    assert body["next_followup"] == "2026-11-22"
    assert body["due"] is False
    assert client.get("/api/entries?due_only=true").json() == []


def test_due_only_filters_closed_and_recent(client):
    make(client, name="never contacted")
    make(client, name="recent", status="waiting", last_contact="2026-11-14")
    make(client, name="overdue", status="waiting", last_contact="2026-11-01")
    make(client, name="rejected", status="rejected")
    due = {e["name"] for e in client.get("/api/entries?due_only=true").json()}
    assert due == {"never contacted", "overdue"}


def test_update_and_delete(client):
    entry_id = make(client).json()["id"]
    r = client.put(f"/api/entries/{entry_id}", json={"name": "Renamed", "status": "interview"})
    assert r.status_code == 200 and r.json()["name"] == "Renamed"
    assert client.delete(f"/api/entries/{entry_id}").status_code == 204
    assert client.get("/api/entries").json() == []


def test_404_on_unknown_id(client):
    assert client.post("/api/entries/999/contacted").status_code == 404
    assert client.delete("/api/entries/999").status_code == 404


def test_request_id_header_is_echoed(client):
    r = client.get("/health", headers={"x-request-id": "abc123"})
    assert r.headers["x-request-id"] == "abc123"
