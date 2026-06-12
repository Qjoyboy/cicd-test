import pytest



async def get_access_token(client):
    await client.post(
        "/api/v1/user/",
        json={
            "email":"task@test.com",
            "username":"task",
            "password":"123456"
        }
    )

    response = await client.post(
        "/api/v1/user/login",
        json={
            "email":"task@test.com",
            "password":"123456"
        }
    )

    return response.json()["access_token"]

async def get_access_token_for_user(
    client,
    email: str,
    username: str
):
    await client.post(
        "/api/v1/user/",
        json={
            "email": email,
            "username": username,
            "password": "123456"
        }
    )

    response = await client.post(
        "/api/v1/user/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_create_task(client):

    token = await get_access_token(client)

    response = await client.post(
        "/api/v1/tasks/",
        headers={
            "Authorization":f"Bearer {token}"
        },
        json={
            "title":"Test Task",
            "description":"Test Description",
            "completed":False
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"

@pytest.mark.asyncio
async def test_get_all_tasks(client):

    token = await get_access_token(client)

    headers = {
        "Authorization":f"Bearer {token}"
    }

    await client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={
            "title":"Task1",
            "description":"Description1",
            "completed": False
        }
    )

    await client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={
            "title":"Task2",
            "description":"Description2",
            "completed": False
            
        }
    )

    response = await client.get(
        "/api/v1/tasks/",
        headers=headers
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

@pytest.mark.asyncio
async def test_get_all_tasks_empty(client):
    token = await get_access_token(client)
    response = await client.get(
        "/api/v1/tasks/",
        headers={
            "Authorization":f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_task_by_id(client):
    token = await get_access_token(client)

    headers={
            "Authorization":f"Bearer {token}"
    }

    response = await client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={
            "title":"Task",
            "description":"Description",
            "completed":False
        }
    )

    task_id = response.json()["id"]

    res = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers
    )

    assert res.status_code == 200

    data = res.json()
    assert data["id"] == task_id
    assert data["title"] == "Task"

@pytest.mark.asyncio
async def test_update_task(client):
    token = await get_access_token(client)
    headers ={
        "Authorization":f"Bearer {token}"
    }
    url = "/api/v1/tasks/"

    create_response = await client.post(
        url,
        headers=headers,
        json={
            "title":"Old",
            "description":"old",
            "completed":False
        }
    )

    task_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={
            "title":"New",
            "description":"new",
            "completed":True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New"
    assert data["description"] == "new"
    assert data["completed"] is True

@pytest.mark.asyncio
async def test_delete_task(client):
    token = await get_access_token(client)
    headers = {
        "Authorization":f"Bearer {token}"
    }
    url = "/api/v1/tasks/"
    create_response = await client.post(
        url,
        headers=headers,
        json={
            "title":"New",
            "description":"new",
            "completed":False
        }
    )

    task_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=headers
    )

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_nonexistent_task(client):
    token = await get_access_token(client)

    response = await client.get(
        "/api/v1/tasks/39218410",
        headers={
            "Authorization":f"Bearer {token}"
        }
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_nonexistent_task(client):

    token = await get_access_token(client)

    response = await client.patch(
        "/api/v1/tasks/999",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Updated",
            "description": "Updated",
            "completed": True
        }
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_nonexistent_task(client):

    token = await get_access_token(client)

    response = await client.delete(
        "/api/v1/tasks/999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_user_cannot_access_foreign_tasks(client):
    token_a = await get_access_token_for_user(client, "user_a@test.com", "usera")
    token_b = await get_access_token_for_user(client, "user_b@test.com", "userb")

    headers_a = {
        "Authorization":f"Bearer {token_a}"
    }
    headers_b = {
        "Authorization":f"Bearer {token_b}"
    }
    
    create_response = await client.post(
        "/api/v1/tasks/",
        headers=headers_a,
        json={
            "title":"Ultra Super-Puper Mega Secret Task",
            "description":"Ultra Super-Puper Mega Secret Description",
            "completed": False
        }
    )

    task_id = create_response.json()["id"]

    response = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers_b
    )

    assert response.status_code == 404