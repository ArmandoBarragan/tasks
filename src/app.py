from fastapi import FastAPI, status

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
def task_detail():
    return "Task"


@app.get('/tasks/',
         status_code=status.HTTP_200_OK,
         tags=["tasks"])
def list_tasks():
    return "Tasks"


@app.post('/tasks/start/{task_id}/',
          status_code=status.HTTP_201_CREATED,
          tags=["timer"])
def start_timer():
    return "Time started"


@app.post('tasks/stop/{task_id}',
          status_code=status.HTTP_200_OK,
          tags=["timer"])
def stop_timer():
    return "Time stopped"
