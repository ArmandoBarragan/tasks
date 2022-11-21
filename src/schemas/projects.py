from typing import Optional, List
from pydantic import BaseModel, Field
from src.schemas.tasks import ReturnTaskSchema


class ProjectMixin(BaseModel):
    name: str = Field(...)


class CreateProjectSchema(ProjectMixin):
    pass


class ReturnProjectSchema(ProjectMixin):
    """ This can be instantiated from the database showing only the name,
    but you can also show with it the tasks that belong to that project."""
    id: int
    tasks: Optional[List[ReturnTaskSchema]]

    class Config:
        orm_mode = True

