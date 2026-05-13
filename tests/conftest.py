from db.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
import pytest
from services.user_service import create_user
from services.task_service import create_task
from schemas.user import UserCreate
from schemas.task import TaskCreate
from repositories.user_repo import get_by_name
from repositories.task_repo import get_by_id_and_user
from fastapi.testclient import TestClient
from main import app
from db.session import get_db

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session")
def global_setup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    create_user(db, UserCreate(name="TestUserName", password="TestHashPassword"))
    create_task(db, TaskCreate(name="TestTaskName"), user_id=1)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db(global_setup):
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()


@pytest.fixture
def test_create_user(test_db):
    return get_by_name(test_db, "TestUserName")


@pytest.fixture
def test_create_task(test_db):
    return get_by_id_and_user(test_db, 1, 1)


@pytest.fixture
def test_schemas_create_task():
    task = TaskCreate(name="TestTaskName")
    return task


@pytest.fixture
def test_client(test_db):
    def override_get_db():
        yield test_db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_access_token(test_client):
    response = test_client.post("/auth/token", data={
    "username": "TestUserName",
    "password": "TestHashPassword"
})
    return response.json()["access_token"]
