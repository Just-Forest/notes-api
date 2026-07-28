def get_auth_header(client, name="noteuser", password="testpass123"):
    client.post("/signup", json={"name": name, "password": password})
    response = client.post("/login", json={"name": name, "password": password})
    token = response.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


def test_create_note(client):
    headers = get_auth_header(client)
    response = client.post("/notes", json={"title": "Test", "content": "Hello"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test"


def test_get_notes_only_own(client):
    headers_a = get_auth_header(client, name="usera")
    headers_b = get_auth_header(client, name="userb")

    client.post("/notes", json={"title": "A's note", "content": "secret"}, headers=headers_a)

    response = client.get("/notes", headers=headers_b)
    assert response.status_code == 200
    assert response.json()["allNotes"] == []


def test_cannot_delete_others_note(client):
    headers_a = get_auth_header(client, name="usera")
    headers_b = get_auth_header(client, name="userb")

    create = client.post("/notes", json={"title": "A's note", "content": "secret"}, headers=headers_a)
    note_id = create.json()["id"]

    response = client.delete(f"/notes/{note_id}", headers=headers_b)
    assert response.status_code == 404