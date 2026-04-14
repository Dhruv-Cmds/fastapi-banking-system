# BaseModel = helps you to define structure how data will store.
# StringConstraints = Set rules for string such as minimum or maximum length of string.
from pydantic import BaseModel, StringConstraints

# Annotated = Gives you extra conditions check the length of data
from typing import Annotated

passwordStr = Annotated[str, StringConstraints(min_length=4, max_length=72)]

class UserCreate(BaseModel):

    username: str
    name: str
    password: passwordStr

class UserLogin(BaseModel):
    username: str
    password: passwordStr

    