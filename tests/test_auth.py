from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "auth_test@example.com",
            "password": "123456",
            "full_name": "Auth Test User",
        },
    )

    assert response.status_code in [200, 201, 400]

    if response.status_code in [200, 201]:
        data = response.json()
        assert data["email"] == "auth_test@example.com"


def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user():
    login_response = client.post(
        "/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "123456",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "email" in data
    assert "full_name" in data