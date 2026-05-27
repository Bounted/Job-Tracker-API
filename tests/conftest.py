from db.base import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import pytest
from services.user_service import create_user
from services.application_service import create_application
from schemas.user import UserCreate
from schemas.application import ApplicationCreate
from repositories.user_repo import get_by_name
from repositories.application_repo import get_by_id_and_user
from main import app
from db.session import get_db
from httpx import ASGITransport, AsyncClient

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="session")
async def test_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as db:
        test_user = await create_user(
            db, UserCreate(name="TestUserName", password="TestHashPassword")
        )
        test_application = await create_application(
            db, ApplicationCreate(name="TestApplicationName"), user_id=test_user.id
        )
        await db.commit()
    yield test_user, test_application
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def test_client(test_table):
    async def override_get_db():
        async with SessionLocal() as db:
            yield db
            await db.commit()

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
async def test_db(test_table):
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()


@pytest.fixture
async def test_access_token(test_client):
    response = await test_client.post(
        "/auth/token", data={"username": "TestUserName", "password": "TestHashPassword"}
    )
    return response.json()["access_token"]


@pytest.fixture
async def test_create_user(test_db):
    return await get_by_name(test_db, "TestUserName")


@pytest.fixture
async def test_create_application(test_db, test_table):
    return await get_by_id_and_user(test_db, test_table[1].id, test_table[0].id)


@pytest.fixture
async def test_schemas_create_application():
    return ApplicationCreate(name="TestApplicationName")