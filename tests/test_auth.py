VALID_PASSWORD = "Testpass123"


def test_signup(client):
    response = client.post(
        "/signup", json={"name": "testuser", "password": VALID_PASSWORD}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_signup_duplicate_user(client):
    client.post("/signup", json={"name": "testuser", "password": VALID_PASSWORD})
    response = client.post(
        "/signup", json={"name": "testuser", "password": VALID_PASSWORD}
    )
    assert response.status_code == 409


def test_login_success(client):
    client.post("/signup", json={"name": "testuser", "password": VALID_PASSWORD})
    response = client.post(
        "/login", json={"name": "testuser", "password": VALID_PASSWORD}
    )
    assert response.status_code == 200
    assert "accessToken" in response.json()


def test_login_wrong_password(client):
    client.post("/signup", json={"name": "testuser", "password": VALID_PASSWORD})
    response = client.post(
        "/login", json={"name": "testuser", "password": "Wrongpass1"}
    )
    assert response.status_code == 401


def test_password_short(client):
    response = client.post("/signup", json={"name": "testuser", "password": "Ab1"})
    assert response.status_code == 422
    assert "must be >= 8" in response.text


def test_password_lowercase(client):
    response = client.post(
        "/signup", json={"name": "testuser", "password": "test12345"}
    )
    assert response.status_code == 422
    assert "must have 1 upper letter" in response.text


def test_password_alpha(client):
    response = client.post(
        "/signup", json={"name": "testuser", "password": "Testtesttest"}
    )
    assert response.status_code == 422
    assert "must include at least one number" in response.text


def test_password_digit(client):
    response = client.post(
        "/signup", json={"name": "testuser", "password": "123456789"}
    )
    assert response.status_code == 422
    assert "must include at least one letter" in response.text


def get_tokens(client, name="tokenuser", password=VALID_PASSWORD):
    client.post("/signup", json={"name": name, "password": password})
    return client.post("/login", json={"name": name, "password": password}).json()


def test_refresh_returns_usable_access_token(client):
    tokens = get_tokens(client)

    response = client.post(
        "/refresh", headers={"Authorization": f"Bearer {tokens['refreshToken']}"}
    )
    assert response.status_code == 200
    assert "accessToken" in response.json()
    assert "refreshToken" not in response.json()

    new_access = response.json()["accessToken"]
    notes = client.get("/notes", headers={"Authorization": f"Bearer {new_access}"})
    assert notes.status_code == 200


def test_access_token_rejected_by_refresh(client):
    tokens = get_tokens(client)
    response = client.post(
        "/refresh", headers={"Authorization": f"Bearer {tokens['accessToken']}"}
    )
    assert response.status_code == 401


def test_refresh_token_rejected_by_notes(client):
    tokens = get_tokens(client)
    response = client.get(
        "/notes", headers={"Authorization": f"Bearer {tokens['refreshToken']}"}
    )
    assert response.status_code == 401


def test_refresh_without_token(client):
    assert client.post("/refresh").status_code == 401
