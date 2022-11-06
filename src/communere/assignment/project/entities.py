from pydantic import BaseModel

from ..auth.entities import User


class Task(BaseModel):
    id: str
    name: str
    assignee: User | None

    class Config:
        orm_mode = True
