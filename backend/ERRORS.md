# Unified Error Response Structure

## Overview

The FastAPI Banking System now implements a consistent, unified error response structure across all API endpoints. All error responses follow this standardized JSON format:

```json
{
    "error": "ERROR_CODE",
    "message": "Human readable message describing the error"
}
```

## Error Response Format

Every error response includes:
- **error**: A unique, uppercase error code (e.g., `INVALID_CREDENTIALS`, `INSUFFICIENT_FUNDS`)
- **message**: A user-friendly message explaining what went wrong
- **HTTP Status Code**: Appropriate HTTP status code reflecting the error type

## HTTP Status Codes

The API uses standard HTTP status codes:
- **400 Bad Request**: Invalid input, business logic violations
- **401 Unauthorized**: Authentication failures
- **403 Forbidden**: Authorization failures
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Database and system errors

## Error Categories and Codes

### Authentication Errors (401)

| Error Code | Message | Cause |
|-----------|---------|-------|
| `INVALID_CREDENTIALS` | Invalid username or password | Login with wrong credentials |
| `INVALID_TOKEN` | Invalid or malformed token | Tampered or malformed JWT token |
| `TOKEN_EXPIRED` | Token has expired | JWT token expiration time exceeded |
| `USER_NOT_FOUND` | User not found | User doesn't exist in database |

**Example:**
```json
{
    "error": "INVALID_CREDENTIALS",
    "message": "Invalid username or password"
}
```

### Account Errors (400, 404)

| Error Code | HTTP Code | Message | Cause |
|-----------|-----------|---------|-------|
| `ACCOUNT_NOT_FOUND` | 404 | Account not found | Account ID doesn't exist or doesn't belong to user |
| `ACCOUNT_ALREADY_EXISTS` | 400 | Account number already exists | Duplicate account number |
| `ACCOUNT_INACTIVE` | 400 | Account is not active | Account status is not ACTIVE |
| `ACCOUNT_ALREADY_CLOSED` | 400 | Account is already closed | Attempting to close a closed account |

**Example:**
```json
{
    "error": "ACCOUNT_NOT_FOUND",
    "message": "Account not found"
}
```

### Transaction Errors (400)

| Error Code | Message | Cause |
|-----------|---------|-------|
| `INSUFFICIENT_FUNDS` | Insufficient balance for this transaction | Account balance too low |
| `DEPOSIT_LIMIT_EXCEEDED` | Deposit amount exceeds maximum limit | Deposit > $50,000 |
| `WITHDRAW_LIMIT_EXCEEDED` | Withdrawal amount exceeds maximum limit | Withdrawal > $20,000 |
| `TRANSFER_LIMIT_EXCEEDED` | Transfer amount exceeds maximum limit | Transfer > $100,000 |
| `NON_ZERO_BALANCE` | Account must have zero balance before closing | Attempting to close account with balance |

**Example:**
```json
{
    "error": "INSUFFICIENT_FUNDS",
    "message": "Insufficient balance for this transaction"
}
```

### Authorization Errors (403)

| Error Code | Message | Cause |
|-----------|---------|-------|
| `UNAUTHORIZED_ACCESS` | Not authorized to access this resource | User accessing another user's resource |
| `ADMIN_ACCESS_REQUIRED` | Admin access required | Non-admin accessing admin endpoints |

**Example:**
```json
{
    "error": "ADMIN_ACCESS_REQUIRED",
    "message": "Admin access required"
}
```

### User Registration Errors (400)

| Error Code | Message | Cause |
|-----------|---------|-------|
| `USERNAME_ALREADY_EXISTS` | Username already exists | Duplicate username registration |

**Example:**
```json
{
    "error": "USERNAME_ALREADY_EXISTS",
    "message": "Username already exists"
}
```

### Rate Limiting (429)

| Error Code | Message | Cause |
|-----------|---------|-------|
| `RATE_LIMIT_EXCEEDED` | Too many requests. Please slow down. | Too many requests in time window |

**Example:**
```json
{
    "error": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please slow down."
}
```

### System/Database Errors (500)

| Error Code | Message | Cause |
|-----------|---------|-------|
| `DATABASE_ERROR` | Database operation failed | Database connection or query error |
| `OPERATION_FAILED` | {Operation} failed. Please try again. | Generic operation failure |

**Example:**
```json
{
    "error": "DATABASE_ERROR",
    "message": "Database operation failed"
}
```

## Implementation Details

### Exception Classes

All exceptions inherit from `BankingAPIException` which extends FastAPI's `HTTPException`. The base class is located in `backend/core/exceptions.py` and provides:

- **Unified structure**: All exceptions generate the same JSON format
- **Type safety**: Custom exception classes for each error type
- **Proper HTTP codes**: Each exception sets the correct HTTP status code
- **Extensibility**: Easy to add new error types

### Files Modified

1. **backend/core/exceptions.py** (NEW)
   - Contains all custom exception classes
   - Base class `BankingAPIException`
   - Organized by category (Authentication, Account, Transaction, etc.)

2. **backend/core/__init__.py**
   - Exports all exception classes for easy import

3. **backend/main.py**
   - Added global exception handler for `BankingAPIException`
   - Updated rate limit exception handler
   - Both now return consistent error format

4. **backend/services/account_service.py**
   - Updated all `HTTPException` to custom exceptions
   - Proper error codes for all operations (deposit, withdraw, transfer, etc.)

5. **backend/services/user_service.py**
   - Updated to use `InvalidCredentialsError`
   - Updated to use `UsernameAlreadyExistsError`

6. **backend/dependencies/auth.py**
   - Updated JWT validation to use custom exceptions
   - Proper error codes for token validation

7. **backend/routes/admin.py**
   - Updated admin endpoints to use custom exceptions

## Usage Examples

### Handling Errors in Client Code

```python
# Python requests example
response = requests.post("http://localhost:8000/api/login", json={
    "username": "user",
    "password": "wrong_password"
})

if response.status_code == 401:
    error_data = response.json()
    print(f"Error: {error_data['error']}")
    print(f"Message: {error_data['message']}")
    # Output: 
    # Error: INVALID_CREDENTIALS
    # Message: Invalid username or password
```

### Using Errors in Frontend

```javascript
// JavaScript/React example
try {
    const response = await fetch('/api/accounts', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    
    if (!response.ok) {
        const error = await response.json();
        
        switch(error.error) {
            case 'INSUFFICIENT_FUNDS':
                showNotification('Not enough balance for this transaction');
                break;
            case 'TOKEN_EXPIRED':
                redirectToLogin();
                break;
            default:
                showNotification(error.message);
        }
    }
} catch (err) {
    console.error('API Error:', err);
}
```

## Testing

Comprehensive tests have been added in `backend/tests/test_errors.py` covering:

- All error code formats
- HTTP status codes
- Error message consistency
- Response structure validation
- Authentication errors
- Account errors
- Transaction errors
- Authorization errors
- Rate limiting

Run tests with:
```bash
pytest backend/tests/test_errors.py -v
```

## Migration Notes

### For Developers
- Replace all `HTTPException` with appropriate custom exception from `backend.core`
- Error codes are now standardized and documented
- Consistent error structure makes debugging easier

### For API Consumers
- All errors now follow the same JSON format
- Error codes are predictable and can be used for programmatic handling
- Messages are user-friendly and can be displayed directly to users

## Future Enhancements

Potential improvements:
1. Localization of error messages
2. Error documentation generation from exception classes
3. Error tracking and monitoring via `error_code`
4. Client-side error code documentation
5. Error recovery suggestions in messages
