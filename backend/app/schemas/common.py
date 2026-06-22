# BaseModel = helps you to define structure how data will store.
# StringConstraints = Set rules for string such as minimum or maximum length of string.
from pydantic import StringConstraints

# Annotated = Gives you extra conditions check the length of data
from typing import Annotated

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

passwordStr = Annotated[
    str,
    StringConstraints(
        min_length=4, 
        max_length=72
        )
]