from dependency_injector.wiring import inject, Provide
from flask import request, Blueprint, g

from .services import ProjectServices
from ..auth.decorators import require_auth, require_role
from ..auth.entities import Role
from ..core.di import Container
from ..core.errors import ApiError

blueprint = Blueprint('project', __name__)


@blueprint.get('/projects/<project_id>/tasks')
@require_auth
@inject
def get_project_tasks(
        project_id: str,
        project_services: ProjectServices = Provide[Container.project_services],
):
    tasks = project_services.get_project_tasks(project_id=project_id)

    return {'tasks': [task.dict() for task in tasks]}


@blueprint.get('/projects/<project_id>/my-tasks')
@require_auth
@inject
def get_project_my_tasks(
        project_id: str,
        project_services: ProjectServices = Provide[Container.project_services],
):
    user_id = g.user.id

    tasks = project_services.get_project_tasks_by_assignee(project_id=project_id, assignee_id=user_id)

    return {'tasks': [task.dict() for task in tasks]}


@blueprint.put('/projects/<project_id>/tasks/<task_id>/assignee')
@require_auth
@require_role(Role.MANAGER)
@inject
def assign_project_task(
        project_id: str, task_id: str,
        project_services: ProjectServices = Provide[Container.project_services],
):
    assignee_username = request.get_json().get('assignee_username')
    if not assignee_username:
        raise ApiError('assignee_username required', 400)

    project_services.assign_task(project_id=project_id, task_id=task_id, assignee_username=assignee_username)

    return {'message': 'done'}
