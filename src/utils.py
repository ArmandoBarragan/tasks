import math
from src.models import SessionRecord
from src.settings.db import Session

def format_time(time) -> str:
    return "{hours}:{minutes}:{seconds}".format(
                hours=math.floor(time/3600),
                minutes=math.floor((time % 3600)/60),
                seconds=math.floor(time % 3600 % 60)
            )


def get_last_record(session, task_id):
    return session.query(SessionRecord).filter(SessionRecord.task_pk == task_id) \
        .order_by(SessionRecord.id.desc()).first()


def get_time_worked(session: Session, task_id: int) -> str:
    session_records = session.query(SessionRecord).filter(SessionRecord.task_pk == task_id).all()

    time_worked = 0
    for record in session_records:
        time_worked += (record.finishing_time - record.starting_time).total_seconds()

    return format_time(time_worked)

