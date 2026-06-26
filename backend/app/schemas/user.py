from app.schemas.common import UsernameStr, NameStr, passwordStr

from pydantic import BaseModel, Field

from app.core import UserRole, UserStatus

class UserBase(BaseModel):

    username: UsernameStr = Field(..., examples=["jdoe"])
    name: NameStr = Field(..., examples=["John Doe"])

class UserCreate(UserBase):

    password: passwordStr = Field(..., examples=["strongPass123"])

class UserResponse(UserBase):
    
    id: int = Field(..., examples=[1])
    role: UserRole = Field(..., examples=[UserRole.USER])
    status: UserStatus = Field(..., examples=[UserStatus.ACTIVE])
     
    model_config = {
        "from_attributes": True
    }