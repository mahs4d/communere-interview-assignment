from sqlalchemy.orm import joinedload

from .db import TaskModel, ProjectModel
from .entities import Task
from .errors import ProjectNotFoundError, TaskNotFoundError
from ..auth.db import UserModel
from ..auth.errors import UserNotFoundError
from ..core.db import SqlAlchemyDatabase


class ProjectServices:
    def __init__(self, db: SqlAlchemyDatabase):
        self.db = db

    def get_project_tasks(self, project_id: str) -> list[Task]:
        with self.db.Session() as session:
            project = session.query(ProjectModel).filter(ProjectModel.id == project_id).first()

            if not project:
                raise ProjectNotFoundError()

            tasks = session.query(TaskModel).options(joinedload(TaskModel.assignee)).filter(
                TaskModel.project_id == project_id,
            ).all()

            return [Task.from_orm(tsk) for tsk in tasks]

    def get_project_tasks_by_assignee(self, project_id: str, assignee_id: str) -> list[Task]:
        with self.db.Session() as session:
            project = session.query(ProjectModel).filter(ProjectModel.id == project_id).first()

            if not project:
                raise ProjectNotFoundError()

            tasks = session.query(TaskModel).options(joinedload(TaskModel.assignee)).filter(
                TaskModel.project_id == project_id,
                TaskModel.assignee_id == assignee_id,
            ).all()

            return [Task.from_orm(tsk) for tsk in tasks]

    def assign_task(self, project_id: str, task_id: str, assignee_username: str | None):
        with self.db.Session() as session:
            project = session.query(ProjectModel).filter(ProjectModel.id == project_id).first()

            if not project:
                raise ProjectNotFoundError()

            task = session.query(TaskModel).filter(TaskModel.id == task_id).first()

            if not task:
                raise TaskNotFoundError()

            if assignee_username:
                user = session.query(UserModel).filter(UserModel.username == assignee_username).first()
                if not user:
                    raise UserNotFoundError()

            if assignee_username:
                task.assignee_id = user.id
            else:
                task.assignee_id = None

            session.commit()
