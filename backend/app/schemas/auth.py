from pydantic import BaseModel, Field

from app.schemas.common import UsernameStr, NameStr, passwordStr

from pydantic import BaseModel, Field

from typing import  Optional

class UserLogin(BaseModel):

    username: UsernameStr = Field(..., example="jdoe")
    password: passwordStr = Field(..., example="strongPass123")

class UserUpdate(BaseModel):

    name: Optional[NameStr] = Field(None, example="Jane Doe")
    password: Optional[passwordStr] = Field(None, example="newSecurePass456")

class TokenResponse(BaseModel):
    
    access_token: str = Field(
        ..., 
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    
    token_type: str = Field(
        "bearer", 
        example="bearer"
    )