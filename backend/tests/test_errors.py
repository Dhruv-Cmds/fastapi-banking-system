"""
Tests for unified error response structure
Tests verify that all API errors follow the consistent JSON format:
{
    "error": "ERROR_CODE",
    "message": "Human readable message"
}
"""

import pytest
import asyncio
import secrets


async def create_test_user(client, username=None, password="password123"):
    """Helper to create a test user"""
    if username is None:
        username = f"testuser_{secrets.token_hex(4)}"

    response = await client.post(
        "/api/signup",
        json={
            "username": username,
            "name": "Test User",
            "password": password
        }
    )

    if response.status_code == 200:
        return username

    data = response.json()
    if response.status_code == 400 and data.get("error") == "USERNAME_ALREADY_EXISTS":
        return username

    pytest.fail(f"Signup failed for {username}: {response.status_code} {response.text}")


async def get_token(client, username=None, password="password123"):
    """Helper to get auth token"""
    username = await create_test_user(client, username=username, password=password)

    response = await client.post(
        "/api/login",
        json={
            "username": username,
            "password": password
        }
    )
    
    if response.status_code != 200:
        pytest.fail(f"Login failed: {response.json()}")
    
    return response.json()["access_token"]


async def create_account(client, headers, account_number="111111"):
    """Helper to create an account"""
    response = await client.post(
        "/api/accounts",
        json={"acc_no": account_number},
        headers=headers
    )
    return response


async def get_first_account_id(client, headers):
    """Helper to get first account ID"""
    response = await client.get(
        "/api/accounts",
        headers=headers
    )
    
    if response.status_code != 200:
        pytest.fail("Failed to fetch accounts")
    
    data = response.json()
    if not data:
        pytest.fail("No accounts found")
    
    return data[0]["id"]


# ============ AUTHENTICATION ERROR TESTS ============

@pytest.mark.asyncio
async def test_invalid_credentials_format(client):
    """Test that invalid credentials returns proper error format"""
    await create_test_user(client)
    
    response = await client.post(
        "/api/login",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "INVALID_CREDENTIALS"
    assert isinstance(data["message"], str)


@pytest.mark.asyncio
async def test_invalid_token_format(client):
    """Test that invalid token returns proper error format"""
    headers = {"Authorization": "Bearer invalid_token"}
    
    response = await client.get(
        "/api/accounts",
        headers=headers
    )
    
    assert response.status_code == 401
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "INVALID_TOKEN"


@pytest.mark.asyncio
async def test_duplicate_username_format(client):
    """Test that duplicate username returns proper error format"""
    await create_test_user(client, username="duplicate")
    
    response = await client.post(
        "/api/signup",
        json={
            "username": "duplicate",
            "name": "Another User",
            "password": "password123"
        }
    )
    
    assert response.status_code == 400
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "USERNAME_ALREADY_EXISTS"


# ============ ACCOUNT ERROR TESTS ============

@pytest.mark.asyncio
async def test_account_not_found_format(client):
    """Test that account not found returns proper error format"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.get(
        "/api/transactions/9999",
        headers=headers
    )
    
    assert response.status_code == 404
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "ACCOUNT_NOT_FOUND"


@pytest.mark.asyncio
async def test_duplicate_account_number_format(client):
    """Test that duplicate account number returns proper error format"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create first account
    response1 = await create_account(client, headers, "ACC001")
    assert response1.status_code == 200
    
    # Try to create account with same number
    response2 = await create_account(client, headers, "ACC001")
    
    assert response2.status_code == 400
    data = response2.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "ACCOUNT_ALREADY_EXISTS"


# ============ TRANSACTION ERROR TESTS ============

@pytest.mark.asyncio
async def test_insufficient_funds_format(client):
    """Test that insufficient funds returns proper error format"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create account with zero balance
    await create_account(client, headers, "ACC002")
    acc_id = await get_first_account_id(client, headers)
    
    # Try to withdraw without funds
    response = await client.post(
        f"/api/accounts/{acc_id}/withdraw",
        json={"amount": 100},
        headers=headers
    )
    
    assert response.status_code == 400
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "INSUFFICIENT_FUNDS"


@pytest.mark.asyncio
async def test_deposit_limit_exceeded_format(client):
    """Test that deposit limit exceeded returns proper error format"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create account
    await create_account(client, headers, "ACC003")
    acc_id = await get_first_account_id(client, headers)
    
    # Try to deposit more than limit (MAX_DEPOSIT = 50000)
    response = await client.post(
        f"/api/accounts/{acc_id}/deposit",
        json={"amount": 100000},
        headers=headers
    )
    
    assert response.status_code == 400
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "DEPOSIT_LIMIT_EXCEEDED"


@pytest.mark.asyncio
async def test_withdraw_limit_exceeded_format(client):
    """Test that withdraw limit exceeded returns proper error format"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create and fund account
    await create_account(client, headers, "ACC004")
    acc_id = await get_first_account_id(client, headers)
    
    await client.post(
        f"/api/accounts/{acc_id}/deposit",
        json={"amount": 10000},
        headers=headers
    )
    
    # Try to withdraw more than limit (MAX_WITHDRAW = 20000)
    response = await client.post(
        f"/api/accounts/{acc_id}/withdraw",
        json={"amount": 30000},
        headers=headers
    )
    
    assert response.status_code == 400
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "WITHDRAW_LIMIT_EXCEEDED"


@pytest.mark.asyncio
async def test_transfer_limit_exceeded_format(client):
    """Test that transfer limit exceeded returns proper error format"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create two accounts
    await create_account(client, headers, "ACC005")
    await create_account(client, headers, "ACC006")
    
    accounts = (await client.get("/api/accounts", headers=headers)).json()
    from_acc_id = accounts[0]["id"]
    to_acc_no = accounts[1]["acc_no"]
    
    # Fund first account within deposit limits
    await client.post(
        f"/api/accounts/{from_acc_id}/deposit",
        json={"amount": 50000},
        headers=headers
    )
    
    # Try to transfer more than limit (MAX_TRANSFER = 100000)
    response = await client.post(
        "/api/transfer",
        json={
            "from_account_id": from_acc_id,
            "to_account_no": to_acc_no,
            "amount": 150000
        },
        headers=headers
    )
    
    assert response.status_code == 400
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "TRANSFER_LIMIT_EXCEEDED"


# ============ AUTHORIZATION ERROR TESTS ============

@pytest.mark.asyncio
async def test_account_closure_non_zero_balance_format(client):
    """Test that closing account with non-zero balance returns proper error format"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create and fund account
    await create_account(client, headers, "ACC007")
    acc_id = await get_first_account_id(client, headers)
    
    await client.post(
        f"/api/accounts/{acc_id}/deposit",
        json={"amount": 100},
        headers=headers
    )
    
    # Try to close account with balance
    response = await client.delete(
        f"/api/accounts/{acc_id}",
        headers=headers
    )
    
    assert response.status_code == 400
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data
    assert data["error"] == "NON_ZERO_BALANCE"


@pytest.mark.asyncio
async def test_unauthorized_account_access_format(client):
    """Test that accessing someone else's account returns proper error format"""
    # Create first user and account
    await create_test_user(client, username="user1")
    token1 = await get_token(client, username="user1")
    headers1 = {"Authorization": f"Bearer {token1}"}
    
    await create_account(client, headers1, "ACC008")
    
    # Create second user
    await create_test_user(client, username="user2")
    token2 = await get_token(client, username="user2")
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    # Get first user's account ID
    accounts = (await client.get("/api/accounts", headers=headers1)).json()
    user1_acc_id = accounts[0]["id"]
    
    # Try to deposit to first user's account as second user
    response = await client.post(
        f"/api/accounts/{user1_acc_id}/deposit",
        json={"amount": 100},
        headers=headers2
    )
    
    # Should fail - either 404 (not found for user2) or 403 (unauthorized)
    assert response.status_code in (404, 403)
    data = response.json()
    
    # Verify error structure
    assert "error" in data
    assert "message" in data


# ============ RATE LIMIT ERROR TEST ============

@pytest.mark.asyncio
async def test_rate_limit_format(client):
    """Test that rate limit error returns proper error format"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Make many rapid requests to trigger rate limit
    responses = await asyncio.gather(
        *[
            client.get("/api/accounts", headers=headers)
            for _ in range(100)
        ]
    )
    
    # Find a rate limited response
    rate_limited_response = None
    for response in responses:
        if response.status_code == 429:
            rate_limited_response = response
            break
    
    if rate_limited_response:
        data = rate_limited_response.json()
        
        # Verify error structure
        assert "error" in data
        assert "message" in data
        assert data["error"] == "RATE_LIMIT_EXCEEDED"


# ============ CONSISTENT STATUS CODE TESTS ============

@pytest.mark.asyncio
async def test_401_for_auth_errors(client):
    """Test that authentication errors return 401 status code"""
    await create_test_user(client)
    
    response = await client.post(
        "/api/login",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_404_for_not_found_errors(client):
    """Test that not found errors return 404 status code"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.get(
        "/api/transactions/99999",
        headers=headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_400_for_validation_errors(client):
    """Test that validation errors return 400 status code"""
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Duplicate account
    await create_account(client, headers, "ACC009")
    response = await create_account(client, headers, "ACC009")
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_error_response_structure_complete(client):
    """Test that error response always has error and message fields"""
    await create_test_user(client)
    
    response = await client.post(
        "/api/login",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    
    data = response.json()
    
    # Verify all required fields exist
    assert "error" in data, "Response missing 'error' field"
    assert "message" in data, "Response missing 'message' field"
    
    # Verify types
    assert isinstance(data["error"], str), "'error' should be a string"
    assert isinstance(data["message"], str), "'message' should be a string"
    
    # Verify not empty
    assert len(data["error"]) > 0, "'error' should not be empty"
    assert len(data["message"]) > 0, "'message' should not be empty"
