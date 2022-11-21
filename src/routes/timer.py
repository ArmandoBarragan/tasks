from datetime import datetime
from fastapi import APIRouter, status, HTTPException

from src.settings.db import Session
from src.utils import get_last_record, format_time
from src.models import SessionRecord
from src.schemas import ReturnSessionRecordSchema, CreateSessionRecordSchema, UpdateSessionRecordSchema


router = APIRouter()


@router.post('/timer/start/{task_id}/',
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


@router.post('/timer/stop/{task_id}',
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


@router.get('/timer/{task_id}',
         status_code=status.HTTP_200_OK,
         tags=['timer'])
def get_current_time(task_id: int):
    """ Returns the time the user has had the current session active."""
    with Session() as session:
        session_record = get_last_record(session, task_id)

        if session_record.finishing_time is not None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                detail="No task is being worked on.")

        time = (datetime.now() - session_record.starting_time).total_seconds()
        return format_time(time)