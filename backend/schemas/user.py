# BaseModel = helps you to define structure how data will store.
# StringConstraints = Set rules for string such as minimum or maximum length of string.
from pydantic import BaseModel, Field, StringConstraints

# Annotated = Gives you extra conditions check the length of data
from typing import Annotated, Optional

UsernameStr = Annotated[
    str,
    StringConstraints(
        min_length=3, 
        max_length=30
    )
]

NameStr = Annotated[
    str,
    StringConstraints(
        min_length=1, 
        max_length=50
    )
]

PasswordStr = Annotated[
    str,
    StringConstraints(
        min_length=4, 
        max_length=72
    )
]

passwordStr = Annotated[str,
                         StringConstraints(
                             min_length=4, 
                             max_length=72
                             )
                        ]

class UserCreate(BaseModel):

    username: UsernameStr = Field(..., example="jdoe")

    name: NameStr = Field(..., example="John Doe")

    password: passwordStr = Field(..., example="strongPass123")

class UserLogin(BaseModel):
    username: UsernameStr = Field(..., example="jdoe")

    password: passwordStr = Field(..., example="strongPass123")


class UserUpdate(BaseModel):
    name: Optional[NameStr] = Field(None, example="Jane Doe")

    password: Optional[passwordStr] = Field(None, example="newSecurePass456")


class MessageResponse(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {"message": "User created"}
        }


class TokenResponse(BaseModel):
    access_token: str = Field(
        ..., 
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    
    token_type: str = Field(
        "bearer", 
        example="bearer"
    )
