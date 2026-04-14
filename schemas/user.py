from pydantic import BaseModel, StringConstraints

''' BaseModel = helps you to define structure how data will store.
    Its like a set of rule that must be followed.

    StringConstraints = Set rules for string such as minimum or 
    maximum length of string. '''

# ---------------------------------------------------------------------------------------

from typing import Annotated

''' Annotated = Gives you extra conditions like someof your data will 
    store as string Annotated also check the length of data (as per amount you pass).'''

# ---------------------------------------------------------------------------------------

passwordStr = Annotated[str, StringConstraints(min_length=4, max_length=72)]

class UserCreate(BaseModel):

    username: str
    name: str
    password: passwordStr

class UserLogin(BaseModel):
    username: str
    password: passwordStr

    