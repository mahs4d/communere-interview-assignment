from functools import wraps
from typing import Callable

from dependency_injector.wiring import Provide, inject
from flask import request, g

from .entities import Role
from .errors import AuthRequiredError, PermissionDeniedError
from .services import AuthServices
from ..core.di import Container


def require_auth(
        fn: Callable,
):
    @wraps(fn)
    @inject
    def wrapper(*args, auth_services: AuthServices = Provide[Container.auth_services], **kwargs):
        if 'Authorization' not in request.headers:
            raise AuthRequiredError()

        token = request.headers['Authorization'].split(' ')[-1]

        if not token:
            raise AuthRequiredError()

        user = auth_services.get_user_by_token(token=token)
        g.user = user

        return fn(*args, **kwargs)

    return wrapper


def require_role(role: Role):
    def decorator(
            fn: Callable,
    ):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if g.user.role != role.value:
                raise PermissionDeniedError()

            return fn(*args, **kwargs)

        return wrapper

    return decorator
