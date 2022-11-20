""" This file contains all the endpoints of the app. For a bigger project I would use, for example, one file
for the tasks endpoints, one for the timer, one for auth, etc."""
from datetime import datetime, timedelta

# Fastapi
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse

# Project
from src.settings.db import Session
from src.utils import format_time, get_last_record
from src.tasks import Task, SessionRecord
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
        session_records = session.query(SessionRecord).filter(SessionRecord.task_pk == task_id).all()

        time_worked = 0
        for record in session_records:
            time_worked += (record.finishing_time - record.starting_time).total_seconds()

        returnable_task = task
        returnable_task.time_worked = format_time(time_worked)
        return returnable_task


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

@app.post('/timer/start/{task_id}/',
          response_model=ReturnSessionRecordSchema,
          status_code=status.HTTP_201_CREATED,
          tags=["timer"])
def start_timer(task_id:int, session_record: CreateSessionRecordSchema):
    """ Creates a Session Record for the database with the upload time from the client as the starting time."""
    with Session() as session:
        last_session = get_last_record(session, task_id)

        if last_session.finishing_time is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Timer already started")

        db_session_record = SessionRecord(
            starting_time=session_record.starting_time,
            task_pk=task_id
        )

        session.add(db_session_record)
        session.commit()
        session.refresh(db_session_record)

        return db_session_record


@app.post('/timer/stop/{task_id}',
          status_code=status.HTTP_200_OK,
          tags=["timer"],
          response_model=ReturnSessionRecordSchema)
def stop_timer(task_id: int, update: UpdateSessionRecordSchema):
    """ Sets the session record's finishing_time to the moment the user is done."""
    with Session() as session:
        session_record = get_last_record(session, task_id)

        if session_record.finishing_time is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="There's no session to stop")

        session_record.finishing_time = update.finishing_time
        returnable_session_record = ReturnSessionRecordSchema(
            id=session_record.id,
            task_pk=session_record.task_pk,
            starting_time=session_record.starting_time,
            finishing_time=session_record.finishing_time
        )

        session.commit()
        return returnable_session_record


@app.get('/timer/{task_id}',
         status_code=status.HTTP_200_OK,
         tags=['timer'])
def get_current_time(task_id: int):
    """ Returns the time the user has had the current session active."""
    import math
    with Session() as session:
        session_record = get_last_record(session, task_id)

        if session_record.finishing_time is not None:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                                content="No task is being worked on.")

        time = (datetime.now() - session_record.starting_time).total_seconds()
        return format_time(time)