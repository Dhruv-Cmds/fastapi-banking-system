"""
Unified exception handling for the banking system.
All API errors follow a consistent JSON structure:
{
    "error": "ERROR_CODE",
    "message": "Human readable message"
}
"""

from fastapi import HTTPException, status
from typing import Optional


class BankingAPIException(HTTPException):
    """
    Base exception class for all banking API errors.
    Ensures consistent error response structure across the application.
    """
    
    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: Optional[dict] = None
    ):
        self.error_code = error_code
        self.message = message
        detail = {
            "error": error_code,
            "message": message
        }
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers
        )


# ============ AUTHENTICATION ERRORS ============

class InvalidCredentialsError(BankingAPIException):
    """Raised when login credentials are invalid"""
    def __init__(self, message: str = "Invalid username or password"):
        super().__init__(
            error_code="INVALID_CREDENTIALS",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class TokenExpiredError(BankingAPIException):
    """Raised when JWT token has expired"""
    def __init__(self, message: str = "Token has expired"):
        super().__init__(
            error_code="TOKEN_EXPIRED",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class InvalidTokenError(BankingAPIException):
    """Raised when JWT token is invalid or tampered"""
    def __init__(self, message: str = "Invalid or malformed token"):
        super().__init__(
            error_code="INVALID_TOKEN",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class UserNotFoundError(BankingAPIException):
    """Raised when user is not found"""
    def __init__(self, message: str = "User not found"):
        super().__init__(
            error_code="USER_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )


class UsernameAlreadyExistsError(BankingAPIException):
    """Raised when attempting to create user with duplicate username"""
    def __init__(self, message: str = "Username already exists"):
        super().__init__(
            error_code="USERNAME_ALREADY_EXISTS",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


# ============ AUTHORIZATION ERRORS ============

class AdminAccessRequiredError(BankingAPIException):
    """Raised when non-admin user tries to access admin endpoint"""
    def __init__(self, message: str = "Admin access required"):
        super().__init__(
            error_code="ADMIN_ACCESS_REQUIRED",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )


class UnauthorizedAccessError(BankingAPIException):
    """Raised when user tries to access resource they don't own"""
    def __init__(self, message: str = "Not authorized to access this resource"):
        super().__init__(
            error_code="UNAUTHORIZED_ACCESS",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )


# ============ ACCOUNT ERRORS ============

class AccountNotFoundError(BankingAPIException):
    """Raised when account is not found"""
    def __init__(self, message: str = "Account not found"):
        super().__init__(
            error_code="ACCOUNT_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )


class AccountAlreadyExistsError(BankingAPIException):
    """Raised when account number already exists"""
    def __init__(self, message: str = "Account number already exists"):
        super().__init__(
            error_code="ACCOUNT_ALREADY_EXISTS",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class AccountInactiveError(BankingAPIException):
    """Raised when attempting operation on inactive account"""
    def __init__(self, message: str = "Account is not active"):
        super().__init__(
            error_code="ACCOUNT_INACTIVE",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class AccountAlreadyClosedError(BankingAPIException):
    """Raised when attempting to close an already closed account"""
    def __init__(self, message: str = "Account is already closed"):
        super().__init__(
            error_code="ACCOUNT_ALREADY_CLOSED",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


# ============ BALANCE & TRANSACTION ERRORS ============

class InsufficientFundsError(BankingAPIException):
    """Raised when account balance is insufficient"""
    def __init__(self, message: str = "Insufficient balance for this transaction"):
        super().__init__(
            error_code="INSUFFICIENT_FUNDS",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class DepositLimitExceededError(BankingAPIException):
    """Raised when deposit amount exceeds limit"""
    def __init__(self, message: str = "Deposit amount exceeds maximum limit"):
        super().__init__(
            error_code="DEPOSIT_LIMIT_EXCEEDED",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class WithdrawLimitExceededError(BankingAPIException):
    """Raised when withdrawal amount exceeds limit"""
    def __init__(self, message: str = "Withdrawal amount exceeds maximum limit"):
        super().__init__(
            error_code="WITHDRAW_LIMIT_EXCEEDED",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class TransferLimitExceededError(BankingAPIException):
    """Raised when transfer amount exceeds limit"""
    def __init__(self, message: str = "Transfer amount exceeds maximum limit"):
        super().__init__(
            error_code="TRANSFER_LIMIT_EXCEEDED",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class NonZeroBalanceError(BankingAPIException):
    """Raised when attempting to close account with remaining balance"""
    def __init__(self, message: str = "Account must have zero balance before closing"):
        super().__init__(
            error_code="NON_ZERO_BALANCE",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


# ============ DATABASE & SYSTEM ERRORS ============

class DatabaseError(BankingAPIException):
    """Raised when a database operation fails"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            error_code="DATABASE_ERROR",
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class OperationFailedError(BankingAPIException):
    """Raised when an operation fails"""
    def __init__(self, operation: str = "Operation"):
        message = f"{operation} failed. Please try again."
        super().__init__(
            error_code="OPERATION_FAILED",
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
