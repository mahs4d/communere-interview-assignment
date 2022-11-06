from ..core.errors import ApiError


class WrongUsernamePasswordError(ApiError):
    def __init__(self):
        super().__init__('wrong username/password combination', 400)


class UsernameExistsError(ApiError):
    def __init__(self):
        super().__init__('username already exists', 400)


class AuthRequiredError(ApiError):
    def __init__(self):
        super().__init__('auth required', 401)


class PermissionDeniedError(ApiError):
    def __init__(self):
        super().__init__('permission denied', 403)


class InvalidTokenError(ApiError):
    def __init__(self):
        super().__init__('invalid token', 400)


class UserNotFoundError(ApiError):
    def __init__(self):
        super().__init__('user not found', 404)
