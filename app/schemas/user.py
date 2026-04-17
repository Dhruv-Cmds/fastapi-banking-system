# BaseModel = helps you to define structure how data will store.
# StringConstraints = Set rules for string such as minimum or maximum length of string.
from pydantic import BaseModel, StringConstraints

# Annotated = Gives you extra conditions check the length of data
from typing import Annotated, Optional

passwordStr = Annotated[str,
                         StringConstraints(
                             min_length=4, 
                             max_length=72
                             )
                        ]

class UserCreate(BaseModel):

    username: Annotated[
        str,
        StringConstraints(min_length=3, max_length=30)
    ]

    name: Annotated[
        str,
        StringConstraints(min_length=1, max_length=50)
    ]

    password: passwordStr

class UserLogin(BaseModel):
    username: Annotated[
        str,
        StringConstraints(min_length=3, max_length=30)
    ]
    password: passwordStr


class UserUpdate(BaseModel):
    name: Optional[
        Annotated[
            str,
            StringConstraints(min_length=1, max_length=50)
        ]
    ] = None

    password: Optional[passwordStr] = None
