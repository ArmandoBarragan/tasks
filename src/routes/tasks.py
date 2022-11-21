from fastapi import APIRouter, status, HTTPException

from src.settings.db import Session
from src.models import Task, SessionRecord
from src.schemas.tasks import CreateTaskSchema, ReturnTaskSchema
from src.utils import format_time

router = APIRouter()


@router.post('/tasks/',
          response_model=ReturnTaskSchema,
          status_code=status.HTTP_201_CREATED,
          tags=["tasks"])
def create_task(task: CreateTaskSchema):
    """
    Create task: I would normally create a base CRUD class and the Task class would inherit from it,
    but it's only one model. This method creates an instance of a task and stores it in the database.
    :param task:
    :return:
    """
    with Session() as session:
        db_task = Task(name=task.name)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@router.get('/tasks/{task_id}',
         response_model=ReturnTaskSchema,
         status_code=status.HTTP_200_OK,
         tags=["tasks"])
def task_detail(task_id: int):
    """ Returns information of a requested task"""
    with Session() as session:
        task = session.query(Task).filter(Task.id == task_id).first()

        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='This task does not exist.')

        session_records = session.query(SessionRecord).filter(SessionRecord.task_pk == task_id).all()

        time_worked = 0
        for record in session_records:
            time_worked += (record.finishing_time - record.starting_time).total_seconds()

        returnable_task = task
        returnable_task.time_worked = format_time(time_worked)
        return returnable_task


@router.get('/tasks/',
         status_code=status.HTTP_200_OK,
         tags=["tasks"])
def list_tasks():
    """ List tasks: Returns a list of all the tasks in the database."""
    with Session() as session:
        db_tasks = session.query(Task).all()
        tasks = []

        for task in db_tasks:
            tasks.append(ReturnTaskSchema(id=task.id, name=task.name))

        return tasks