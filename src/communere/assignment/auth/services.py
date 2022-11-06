import jwt

from .db import UserModel
from .entities import Role, User
from .errors import (
    UsernameExistsError,
    WrongUsernamePasswordError,
    InvalidTokenError,
    UserNotFoundError,
)
from .utils import hash_password
from ..core.config import Config
from ..core.db import SqlAlchemyDatabase


class AuthServices:
    def __init__(self, config: Config, db: SqlAlchemyDatabase):
        self.config = config
        self.db = db

    def create_token_by_username_password(self, username: str, password: str, ) -> str:
        with self.db.Session() as session:
            user = session.query(UserModel).filter(UserModel.username == username).first()
            if not user:
                raise WrongUsernamePasswordError()

            if user.hashed_password != hash_password(password=password):
                raise WrongUsernamePasswordError()

            token = jwt.encode({'sub': username}, key=self.config.auth_secret, algorithm='HS256')

        return token

    def get_user_by_token(self, token: str) -> User:
        try:
            data = jwt.decode(jwt=token, key=self.config.auth_secret, algorithms=['HS256'])
        except jwt.DecodeError:
            raise InvalidTokenError()

        username = data.get('sub')
        if not username:
            raise InvalidTokenError()

        with self.db.Session() as session:
            user = session.query(UserModel).filter(UserModel.username == username).first()
            if not user:
                raise UserNotFoundError()

        return user

    def create_user(
            self,
            username: str,
            password: str,
            role: Role,
    ) -> User:
        with self.db.Session() as session:
            same_username_user = session.query(UserModel).filter(UserModel.username == username).first()
            if same_username_user:
                raise UsernameExistsError()

            user = UserModel(
                username=username,
                hashed_password=hash_password(password=password),
                role=role.value,
            )
            session.add(user)
            session.commit()

            return User.from_orm(user)
