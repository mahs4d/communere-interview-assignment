from pydantic import BaseSettings


class Config(BaseSettings):
    db_connection: str = 'sqlite:///sqlite.db'
    db_echo: bool = False

    auth_secret: str = 'secret'

    class Config:
        env_prefix = 'my_prefix_'
