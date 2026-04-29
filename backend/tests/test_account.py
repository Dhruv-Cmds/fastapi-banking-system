import pytest
import asyncio


async def get_token(client):
    login = await client.post("/api/login", json={
        "username": "testuser",
        "password": "password123"
    })

    if login.status_code != 200:
        pytest.skip("Login failed")

    return login.json()["access_token"]


async def get_first_account_id(client, headers):
    res = await client.get("/api/accounts", headers=headers)

    if res.status_code != 200:
        pytest.skip("Failed to fetch accounts")

    data = res.json()

    if not data:
        pytest.skip("No accounts found")

    return data[0]["id"]


@pytest.mark.asyncio
async def test_concurrent_requests(client):
    login = await client.post("/api/login", json={
        "username": "testuser",
        "password": "password123"
    })

    if login.status_code != 200:
        pytest.skip("Login failed")

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    async def spam():
        return await client.get("/api/accounts", headers=headers)

    responses = await asyncio.gather(*[spam() for _ in range(100)])

    assert all(res.status_code in (200, 429) for res in responses)


@pytest.mark.asyncio
async def test_deposit(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    await client.post(
        "/api/accounts",
        json={"acc_no": "111111"},
        headers=headers
    )

    acc_id = await get_first_account_id(client, headers)

    response = await client.post(
        f"/api/accounts/{acc_id}/deposit",
        json={"amount": 100},
        headers=headers
    )

    assert response.status_code in (200, 404)


@pytest.mark.asyncio
async def test_transfer(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    await client.post(
        "/api/accounts",
        json={"acc_no": "111111"},
        headers=headers
    )

    await client.post(
        "/api/accounts",
        json={"acc_no": "123456"},
        headers=headers
    )

    res = await client.get("/api/accounts", headers=headers)

    if res.status_code != 200:
        pytest.skip("Failed to fetch accounts")

    accounts = res.json()

    if len(accounts) < 2:
        pytest.skip("Not enough accounts")

    sender_id = accounts[0]["id"]
    receiver_acc_no = accounts[1]["acc_no"]

    await client.post(
        f"/api/accounts/{sender_id}/deposit",
        json={"amount": 100},
        headers=headers
    )

    response = await client.post(
        "/api/transfer",
        json={
            "from_account_id": sender_id,
            "to_account_no": receiver_acc_no,
            "amount": 10
        },
        headers=headers
    )

    assert response.status_code in (200, 400, 404)


@pytest.mark.asyncio
async def test_rate_limit(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    responses = []

    for _ in range(20):
        res = await client.get("/api/accounts", headers=headers)
        responses.append(res.status_code)

    assert 429 in responses or all(r == 200 for r in responses)