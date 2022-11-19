from datetime import datetime
from pydantic import BaseModel, Field


class TaskMixin(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class CreateTask(TaskMixin):
    pass


class  ReturnTask(TaskMixin):
    id: int

    class Config:
        orm_mode = True


class SessionRecordMixin(BaseModel):
    starting_time: datetime = Field(...)
    task_pk: int = Field(...)


class CreateSessionRecord(SessionRecordMixin):
    pass


class ReturnSessionRecord(SessionRecordMixin):
    id: int

    class Config:
        orm_mode = True


class UpdateSessionRecord(BaseModel):
    """This model is ment to be used when a session ends, so that the finishing_time value of the record is set."""
    finishing_time: datetime = Field()
