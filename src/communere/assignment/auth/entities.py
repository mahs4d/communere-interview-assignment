from enum import Enum

from pydantic import BaseModel


class Role(Enum):
    DEVELOPER = 'DEVELOPER'
    MANAGER = 'MANAGER'


class User(BaseModel):
    id: str
    username: str
    role: Role

    class Config:
        orm_mode = True
        use_enum_values = True
