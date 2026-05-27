from schemas.application import ApplicationCreate, ApplicationPut
from pydantic import ValidationError
import pytest
from services.application_service import (
    create_application,
    update_application_status,
    delete_application,
    update_application,
)
from core.exceptions import NotFoundError, AlreadyExistsError
from models.application import ApplicationStatus
from repositories.application_repo import get_by_id_and_user


async def test_application_create_valid():
    application = ApplicationCreate(name="Work")
    assert application.name == "Work"


@pytest.mark.parametrize("name", ["A", "a" * 101])
async def test_application_create_invalid(name):
    with pytest.raises(ValidationError):
        ApplicationCreate(name=name)


async def test_post_application_duplicate(test_client, test_access_token):
    response = await test_client.post(
        "/applications/",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "TestApplicationName"},
    )
    assert response.status_code == 409


async def test_create_application_valid(test_db, test_create_user):
    test = await create_application(
        test_db, ApplicationCreate(name="Application_name"), test_create_user.id
    )
    assert test.name == "Application_name"  # type: ignore


async def test_create_application_duplicate(
    test_db, test_schemas_create_application, test_create_user
):
    with pytest.raises(AlreadyExistsError):
        await create_application(
            test_db, test_schemas_create_application, test_create_user.id
        )


async def test_put_application_service_valid(
    test_db, test_create_application, test_create_user
):
    application = await update_application(
        test_db,
        test_create_application.id,
        ApplicationPut(
            name="TestTaskName", content="testcontent", state=ApplicationStatus("offer")
        ),
        test_create_user.id,
    )
    assert application.content == "testcontent"  # type: ignore


async def test_put_application_invalid(test_db, test_create_application):
    with pytest.raises(NotFoundError):
        await update_application(
            test_db,
            test_create_application.id,
            ApplicationPut(
                name="TestApplicationName",
                content="testcontent",
                state=ApplicationStatus("offer"),
            ),
            999,
        )


async def test_update_application_status_valid(
    test_db, test_create_application, test_create_user
):
    application = await update_application_status(
        test_db,
        test_create_application.id,
        ApplicationStatus("offer"),
        test_create_user.id,
    )
    assert application.state == "offer"  # type: ignore


async def test_update_application_status_invalid(test_db, test_create_user):
    with pytest.raises(NotFoundError):
        await update_application_status(
            test_db, 999, ApplicationStatus("offer"), test_create_user.id
        )


async def test_delete_application_not_found(test_db, test_create_user):
    with pytest.raises(NotFoundError):
        await delete_application(test_db, 999, test_create_user.id)


async def test_post_application_valid(test_client, test_access_token):
    response = await test_client.post(
        "/applications/",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "NewTestApplication"},
    )
    assert response.status_code == 201


async def test_get_applications_valid(test_client, test_access_token):
    response = await test_client.get(
        "/applications/me", headers={"Authorization": f"Bearer {test_access_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_patch_applications_valid(
    test_client, test_access_token, test_create_application
):
    response = await test_client.patch(
        f"/applications/{test_create_application.id}/offer",
        headers={"Authorization": f"Bearer {test_access_token}"},
    )
    assert response.status_code == 200


async def test_patch_application_not_found(test_client, test_access_token):
    response = await test_client.patch(
        f"/applications/999/offer",
        headers={"Authorization": f"Bearer {test_access_token}"},
    )
    assert response.status_code == 404


async def test_put_application_valid(
    test_client, test_access_token, test_create_application
):
    response = await test_client.put(
        f"/applications/{test_create_application.id}",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "TestPutApplicationName", "content": "string", "state": "offer"},
    )

    assert response.status_code == 200


async def test_put_application_not_found(test_client, test_access_token):
    response = await test_client.put(
        f"/applications/{999}",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "TestApplicationName", "content": "string", "state": "offer"},
    )

    assert response.status_code == 404


async def test_get_application_stats(test_client, test_access_token):
    response = await test_client.get(
        "/applications/stats",
        headers={"Authorization": f"Bearer {test_access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "by_status" in data
    assert isinstance(data["by_status"], dict)


async def test_delete_application_service_valid(test_db, test_create_user):
    application = await create_application(
        test_db, ApplicationCreate(name="TestApplicationDelete"), test_create_user.id
    )
    await delete_application(test_db, application.id, test_create_user.id)  # type: ignore
    deleted = await get_by_id_and_user(test_db, application.id, test_create_user.id)  # type: ignore
    assert deleted is None


async def test_delete_application_valid(test_client, test_access_token):
    create_resp = await test_client.post(
        "/applications/",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "ApplicationToDelete"},
    )
    application_id = create_resp.json()["id"]
    response = await test_client.delete(
        f"/applications/{application_id}",
        headers={"Authorization": f"Bearer {test_access_token}"},
    )
    assert response.status_code == 204
