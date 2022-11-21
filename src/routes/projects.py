from fastapi import APIRouter

from src.schemas.projects import CreateProjectSchema, ReturnProjectSchema


router = APIRouter()


@router.post('/projects/',
             tags=['projects'])
def create_project():
    pass


@router.get('/projects/',
            tags=['projects'])
def list_projects():
    pass


@router.get('/projects/{project_id}',
            tags=['projects'])
def project_detail(project_id: int):
    pass


