from http.client import HTTPException


class ApiError(HTTPException):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status
