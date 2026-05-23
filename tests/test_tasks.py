from schemas.task import TaskCreate, TaskPut
from pydantic import ValidationError
import pytest
from services.task_service import (
    create_task,
    update_task_status,
    delete_task,
    update_task,
)
from core.exceptions import NotFoundError, AlreadyExistsError
from models.task import TaskStatus
from repositories.task_repo import get_by_id_and_user


async def test_task_create_valid():
    task = TaskCreate(name="Work")
    assert task.name == "Work"


@pytest.mark.parametrize("name", ["A", "a" * 101])
async def test_task_create_invalid(name):
    with pytest.raises(ValidationError):
        TaskCreate(name=name)


async def test_create_task_valid(test_db, test_create_user):
    test = await create_task(test_db, TaskCreate(name="Task_name"), test_create_user.id)
    assert test.name == "Task_name"


async def test_create_task_duplicate(
    test_db, test_schemas_create_task, test_create_user
):
    with pytest.raises(AlreadyExistsError):
        await create_task(test_db, test_schemas_create_task, test_create_user.id)


async def test_put_task_valid(test_db, test_create_task, test_create_user):
    task = await update_task(
        test_db,
        test_create_task.id,
        TaskPut(
            name="TestTaskName", content="testcontent", state=TaskStatus("at_work")
        ),
        test_create_user.id,
    )
    assert task.content == "testcontent"


async def test_put_task_invalid(test_db, test_create_task):
    with pytest.raises(NotFoundError):
        await update_task(
            test_db,
            test_create_task.id,
            TaskPut(
                name="TestTaskName", content="testcontent", state=TaskStatus("at_work")
            ),
            999,
        )


async def test_update_task_status_valid(test_db, test_create_task, test_create_user):
    task = await update_task_status(
        test_db, test_create_task.id, TaskStatus("at_work"), test_create_user.id
    )
    assert task.state == "at_work"


async def test_update_task_status_invalid(test_db, test_create_user):
    with pytest.raises(NotFoundError):
        await update_task_status(
            test_db, 999, TaskStatus("at_work"), test_create_user.id
        )


async def test_delete_task_valid(test_db, test_create_user):
    task = await create_task(
        test_db, TaskCreate(name="TestTaskDelete"), test_create_user.id
    )
    await delete_task(test_db, task.id, test_create_user.id)
    deleted = await get_by_id_and_user(test_db, task.id, test_create_user.id)
    assert deleted is None


async def test_delete_task_not_found(test_db, test_create_user):
    with pytest.raises(NotFoundError):
        await delete_task(test_db, 999, test_create_user.id)


async def test_post_task_valid(test_client, test_access_token):
    response = await test_client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "NewTestTask"},
    )
    assert response.status_code == 201


async def test_post_task_duplicate(test_client, test_access_token):
    response = await test_client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "TestTaskName"},
    )
    assert response.status_code == 409


async def test_get_tasks_valid(test_client, test_access_token):
    response = await test_client.get(
        "/tasks/me", headers={"Authorization": f"Bearer {test_access_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_patch_tasks_valid(test_client, test_access_token, test_create_task):
    response = await test_client.patch(
        f"/tasks/{test_create_task.id}/ready",
        headers={"Authorization": f"Bearer {test_access_token}"},
    )
    assert response.status_code == 200


async def test_patch_task_not_found(test_client, test_access_token):
    response = await test_client.patch(
        f"/tasks/999/ready",
        headers={"Authorization": f"Bearer {test_access_token}"},
    )
    assert response.status_code == 404


async def test_delete_task_valid(test_client, test_access_token):
    create_resp = await test_client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "TaskToDelete"},
    )
    task_id = create_resp.json()["id"]
    response = await test_client.delete(
        f"/tasks/{task_id}", headers={"Authorization": f"Bearer {test_access_token}"}
    )
    assert response.status_code == 204


async def test_put_task_valid(test_client, test_access_token, test_create_task):
    response = await test_client.put(
        f"/tasks/{test_create_task.id}",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "TestTaskName", "content": "string", "state": "ready"},
    )

    assert response.status_code == 200


async def test_put_task_not_found(test_client, test_access_token):
    response = await test_client.put(
        f"/tasks/{999}",
        headers={"Authorization": f"Bearer {test_access_token}"},
        json={"name": "TestTaskName", "content": "string", "state": "ready"},
    )

    assert response.status_code == 404
