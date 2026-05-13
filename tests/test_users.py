from schemas.user import UserCreate
import pytest
from pydantic import ValidationError
from services.user_service import ensure_user_exists, get_user_by_id, create_user
from core.exceptions import NotFoundError, AlreadyExistsError
from schemas.user import UserCreate


def test_user_create_valid():
    user = UserCreate(name="TestUserName", password="password")
    assert user.name == "TestUserName"


@pytest.mark.parametrize(
    "name, password",
    [("A", "123456"), ("Anna", "q"), ("Anna", "q" * 51), ("A" * 51, "123456")],
)
def test_user_create_invalid(name, password):
    with pytest.raises(ValidationError):
        UserCreate(name=name, password=password)


def test_ensure_user_exists_valid(test_db, test_create_user):
    user = ensure_user_exists(test_db, test_create_user.name)
    assert user.name == "TestUserName"


def test_ensure_user_exists_invalid(test_db):
    with pytest.raises(NotFoundError):
        ensure_user_exists(test_db, "Ghost")


def test_get_user_by_id_valid(test_db, test_create_user):
    user = get_user_by_id(test_db, test_create_user.id)
    assert user.name == "TestUserName"


def test_get_user_by_id_invalid(test_db):
    with pytest.raises(NotFoundError):
        get_user_by_id(test_db, 999)


def test_create_user_valid(test_create_user):
    assert test_create_user.name == "TestUserName"
    assert test_create_user.hashed_password != "TestHashPassword"


def test_create_user_duplicate(test_db, test_create_user):
    with pytest.raises(AlreadyExistsError):
        create_user(test_db, UserCreate(name=test_create_user.name, password="123456"))


def test_post_user_valid(test_client):
    response = test_client.post("/users", json={"name": "string", "password": "string"})
    assert response.status_code == 201


def test_post_user_duplicate(test_client):
    response = test_client.post(
        "/users", json={"name": "TestUserName", "password": "string"}
    )
    assert response.status_code == 409


def test_get_user_valid(test_client, test_access_token):
    response = test_client.get(
        "/users/me", headers={"Authorization": f"Bearer {test_access_token}"}
    )
    assert response.status_code == 200


def test_get_user_unauthorized(test_client):
    response = test_client.get("/users/me")
    assert response.status_code == 401


def test_delete_user_valid(test_client, test_access_token):
    response = test_client.delete(
        "/users/me", headers={"Authorization": f"Bearer {test_access_token}"}
    )
    assert response.status_code == 204


def test_delete_user_unauthorized(test_client):
    response = test_client.delete("/users/me")
    assert response.status_code == 401
