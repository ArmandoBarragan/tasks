from typing import Optional
from pydantic import BaseModel, Field


class TaskMixin(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    project_pk: Optional[int] = Field()


class CreateTaskSchema(TaskMixin):
    pass


class  ReturnTaskSchema(TaskMixin):
    id: int
    time_worked: str

    class Config:
        orm_mode = True