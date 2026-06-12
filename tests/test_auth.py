import pytest

@pytest.mark.asyncio
async def test_register_user(client):

    response = await client.post(
        "/api/v1/user/",
        json={
            "email":"test@test.com",
            "username":"test",
            "password":"123456"
        }
    )
    print(response.json())
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_login_user(client):

    await client.post(
        "/api/v1/user/",
        json={
            "email":"login@test.com",
            "username":"login",
            "password":"123456"
        }
    )

    response = await client.post(
        "/api/v1/user/login",
        json={
            "email":"login@test.com",
            "password":"123456"
        }
    )
    print(response.json())
    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_refresh_token(client):
    await client.post(
        "/api/v1/user/",
        json={
            "email":"refresh@test.com",
            "username":"test",
            "password":"123456"
        }
    )

    login_response = await client.post(
        "/api/v1/user/login",
        json={
            "email":"refresh@test.com",
            "password":"123456"
        }
    )

    refresh_token = login_response.json()["refresh_token"]

    response = await client.post("/api/v1/user/refresh",
        json={
            "refresh_token": refresh_token
        })
    
    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    await client.post(
        "/api/v1/user/",
        json={
            "email":"wrong@test.com",
            "username":"test",
            "password":"123456"
        }
    )

    response = await client.post(
         "/api/v1/user/login",
        json={
            "email":"wrong@test.com",
            "password":"WRONG_PASSWORD"
        }
    )

    assert response.status_code == 401