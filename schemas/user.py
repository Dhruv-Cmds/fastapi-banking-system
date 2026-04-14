from pydantic import BaseModel, StringConstraints
from typing import Annotated

passwordStr = Annotated[str, StringConstraints(min_length=4, max_length=72)]

class UserCreate(BaseModel):

    username: str
    name: str
    password: passwordStr

class UserLogin(BaseModel):
    username: str
    password: passwordStr