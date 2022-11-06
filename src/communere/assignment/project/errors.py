from ..core.errors import ApiError


class ProjectNotFoundError(ApiError):
    def __init__(self):
        super().__init__('project not found', 404)


class TaskNotFoundError(ApiError):
    def __init__(self):
        super().__init__('task not found', 404)
