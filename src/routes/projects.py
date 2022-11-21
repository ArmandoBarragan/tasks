from fastapi import APIRouter, HTTPException, status

from src.schemas.projects import CreateProjectSchema, ReturnProjectSchema
from src.schemas.tasks import ReturnTaskSchema
from src.settings.db import Session
from src.models import Project, Task
from src.utils import get_project_tasks

router = APIRouter()


@router.post('/projects/',
             tags=['projects'],
             response_model=ReturnProjectSchema,
            status_code=201)
def create_project(project: CreateProjectSchema):
    with Session() as session:
        db_project = Project(name=project.name)

        session.add(db_project)
        session.commit()
        session.refresh(db_project)

        return db_project


@router.get('/projects/',
            tags=['projects'],
            status_code=200)
def list_projects():
    with Session() as session:
        returnable_projects = []

        for project in session.query(Project).all():
            returnable_projects.append(ReturnProjectSchema(
                name=project.name,
                id=project.id,
                tasks=get_project_tasks(session, project.id)
            ))

        return returnable_projects


@router.get('/projects/{project_id}',
            tags=['projects'],
            response_model=ReturnProjectSchema,
            status_code=200)
def project_detail(project_id: int):
    with Session() as session:
        project = session.query(Project).filter(Project.id == project_id).first()

        if project is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="This project does not exist.")

        returnable_project = ReturnProjectSchema(
            id=project.id,
            name=project.name,
            tasks=get_project_tasks(session, project.id)
        )

        return returnable_project

