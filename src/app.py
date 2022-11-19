""" This file contains all the endpoints of the app. For a bigger project I would use, for example, one file
for the tasks endpoints, one for the timer, one for auth, etc."""

from fastapi import FastAPI, Depends, status

from src.settings.db import Session

# Models
from src.tasks import Task, SessionRecord

# Schemas
from src.tasks import CreateTaskSchema, CreateSessionRecordSchema
from src.tasks import UpdateSessionRecordSchema, ReturnTaskSchema, ReturnSessionRecordSchema


app = FastAPI()

@app.post('/tasks/',
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


@app.get('/tasks/{task_id}',
         response_model=ReturnTaskSchema,
         status_code=status.HTTP_200_OK,
         tags=["tasks"])
def task_detail(task_id: int):
    """ Returns information of a requested task"""
    with Session() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        return task


@app.get('/tasks/',
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

@app.post('/tasks/start/{task_id}/',
          response_model=ReturnSessionRecordSchema,
          status_code=status.HTTP_201_CREATED,
          tags=["timer"])
def start_timer(session_record: CreateSessionRecordSchema):
    """ Creates a Session Record for the database with the upload time from the client as the starting time."""
    with Session() as session:
        db_session_record = SessionRecord(
            starting_time=session_record.starting_time,
            task_pk=session_record.task_pk
        )

        session.add(db_session_record)
        session.commit()
        session.refresh(db_session_record)

        return db_session_record


@app.post('tasks/stop/{task_id}',
          status_code=status.HTTP_200_OK,
          tags=["timer"])
def stop_timer():
    return "Time stopped"


