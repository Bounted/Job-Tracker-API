from services.auth_service import authenticate_user, login
import pytest


def test_authenticate_user_valid(test_db):
    auth_user = authenticate_user(test_db, "TestUserName", "TestHashPassword")
    assert auth_user.name == "TestUserName"


@pytest.mark.parametrize(
    "username, password",
    [
        ("NotTestUserName", "TestHashPassword"),
        ("TestUserName", "NotTestHashPassword"),
    ],
)
def test_authenticate_user_invalid(test_db, username, password):
    assert authenticate_user(test_db, username, password) is None


def test_login_valid(test_db):
    log = login(test_db, "TestUserName", "TestHashPassword")
    assert log is not None


def test_login_invalid(test_db):
    log = login(test_db, "NotTestUserName", "NotTestHashPassword")
    assert log is None


def test_post_valid(test_client):
    response = test_client.post("/auth/token", data={
        "username": "TestUserName",
        "password": "TestHashPassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_post_invalid(test_client):
    response = test_client.post("/auth/token", data={
        "username": "TestUserName",
        "password": "WrongPassword"
    })
    assert response.status_code == 401