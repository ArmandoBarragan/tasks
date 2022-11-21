from fastapi import APIRouter

from src.schemas.projects import CreateProjectSchema, ReturnProjectSchema
from src.schemas.tasks import ReturnTaskSchema
from src.settings.db import Session
from src.models import Project, Task
from src.utils import get_time_worked

router = APIRouter()


@router.post('/projects/',
             tags=['projects'],
             response_model=ReturnProjectSchema)
def create_project(project: CreateProjectSchema):
    with Session() as session:
        db_project = Project(name=project.name)

        session.add(db_project)
        session.commit()
        session.refresh(db_project)

        return db_project


@router.get('/projects/',
            tags=['projects'])
def list_projects():
    with Session() as session:
        returnable_projects = []

        for project in session.query(Project).all():
            tasks = []

            for task in session.query(Task).filter(Task.project_pk == project.id):
                tasks.append(ReturnTaskSchema(
                    id=task.id,
                    name=task.name,
                    project_pk=task.project_pk,
                    time_worked=get_time_worked(session, task.id)
                ))

            returnable_projects.append(ReturnProjectSchema(
                name=project.name,
                id=project.id,
                tasks=tasks
            ))

@router.get('/projects/{project_id}',
            tags=['projects'])
def project_detail(project_id: int):
    pass


