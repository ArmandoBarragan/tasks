from typing import Optional
from pydantic import BaseModel, Field


class TaskMixin(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    project_pk: Optional[int] = Field()


class CreateTaskSchema(TaskMixin):
    pass


class UpdateTaskSchema(TaskMixin):
    pass


class  ReturnTaskSchema(TaskMixin):
    """Attributes are id, name, project_pk and time_worked"""
    id: int
    time_worked: str

    class Config:
        orm_mode = True


