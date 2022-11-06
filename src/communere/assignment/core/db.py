from __future__ import annotations

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker

from ..core.config import Config

Base = orm.declarative_base()


class SqlAlchemyDatabase:
    def __init__(self, config: Config):
        self.engine = sqlalchemy.create_engine(config.db_connection, echo=config.db_echo, future=True)
        self.Session = sessionmaker(bind=self.engine)

    def setup(self):
        Base.metadata.create_all(self.engine)
