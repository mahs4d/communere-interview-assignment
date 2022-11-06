from dependency_injector import containers, providers

from .config import Config
from .db import SqlAlchemyDatabase
from ..auth.services import AuthServices
from ..project.services import ProjectServices


class Container(containers.DeclarativeContainer):
    config = providers.Factory(Config)

    db = providers.Singleton(SqlAlchemyDatabase, config=config)

    auth_services = providers.Factory(AuthServices, config=config, db=db)
    project_services = providers.Factory(ProjectServices, db=db)
