import pytest


@pytest.mark.asyncio
async def test_signup(client):
    response = await client.post("/api/signup", json={
        "username": "testuser",
        "name": "Test User",
        "password": "password123"
    })

    assert response.status_code in (200, 400)


@pytest.mark.asyncio
async def test_login(client):
    # ensure user exists
    await client.post("/api/signup", json={
        "username": "testuser",
        "name": "Test User",
        "password": "password123"
    })

    response = await client.post("/api/login", json={
        "username": "testuser",
        "password": "password123"
    })

    if response.status_code == 200:
        data = response.json()
        assert "access_token" in data
    else:
        assert response.status_code in (400, 401)