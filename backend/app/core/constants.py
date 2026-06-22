from enum import Enum

class UserRole(str, Enum):

    USER = "USER"
    ADMIN = "ADMIN"

class UserStatus(str, Enum):

    ACTIVE = "ACTIVE"
    CLOSE = "CLOSE"