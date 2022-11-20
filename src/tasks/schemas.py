from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.schema import Optional


class TaskMixin(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class CreateTaskSchema(TaskMixin):
    pass


class  ReturnTaskSchema(TaskMixin):
    id: int
    time_worked: str

    class Config:
        orm_mode = True


class SessionRecordMixin(BaseModel):
    starting_time: datetime = Field(...)


class CreateSessionRecordSchema(SessionRecordMixin):
    """Attr: starting_time and task_pk"""
    pass


class UpdateSessionRecordSchema(BaseModel):
    """This model is ment to be used when a session ends, so that the finishing_time value of the record is set.
    Attr: finishing_time"""
    finishing_time: datetime = Field(...)


class ReturnSessionRecordSchema(SessionRecordMixin):
    """ Attr: starting_time, finishing_time, id and task_pk."""
    id: int
    finishing_time: Optional[datetime]

    class Config:
        orm_mode = True