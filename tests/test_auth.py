def test_signup(client):
    response = client.post("/signup", json={
        "name": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_signup_duplicate_user(client):
    client.post("/signup", json={"name": "testuser", "password": "testpass123"})
    response = client.post("/signup", json={"name": "testuser", "password": "testpass123"})
    assert response.status_code == 409


def test_login_success(client):
    client.post("/signup", json={"name": "testuser", "password": "testpass123"})
    response = client.post("/login", json={"name": "testuser", "password": "testpass123"})
    assert response.status_code == 200
    assert "accessToken" in response.json()


def test_login_wrong_password(client):
    client.post("/signup", json={"name": "testuser", "password": "testpass123"})
    response = client.post("/login", json={"name": "testuser", "password": "wrongpass1"})
    assert response.status_code == 401