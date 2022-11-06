from sqlalchemy import Column, Integer, String

from ..core.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(30), nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(10), nullable=False)
