from dependency_injector.wiring import Provide, inject
from flask import request, Blueprint

from .entities import Role
from .services import AuthServices
from ..core.di import Container
from ..core.errors import ApiError

blueprint = Blueprint('auth', __name__)


@blueprint.post('/users')
@inject
def create_user(
        auth_services: AuthServices = Provide[Container.auth_services],
):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', Role.DEVELOPER.name)

    if not username:
        raise ApiError('missing username', 400)

    if not password:
        raise ApiError('missing password', 400)

    try:
        role = Role(role)
    except:
        raise ApiError('invalid role', 400)

    user = auth_services.create_user(
        username=username,
        password=password,
        role=role,
    )

    return {'user': user.dict()}


@blueprint.post('/tokens')
@inject
def create_token(
        auth_services: AuthServices = Provide[Container.auth_services],
):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username:
        raise ApiError('missing username', 400)

    if not password:
        raise ApiError('missing password', 400)

    token = auth_services.create_token_by_username_password(
        username=username,
        password=password,
    )

    return {'token': token}
