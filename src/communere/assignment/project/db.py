from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..core.db import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)

    name = Column(String(30), nullable=False)


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    name = Column(String(30), nullable=False)

    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    project = relationship('ProjectModel', backref='tasks')
    assignee = relationship('UserModel', backref='tasks')
