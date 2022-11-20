import math
from sqlalchemy.orm import Session
from src.tasks.models import SessionRecord

def format_time(time):
    return "{hours}:{minutes}:{seconds}".format(
                hours=math.floor(time/3600),
                minutes=math.floor((time % 3600)/60),
                seconds=math.floor(time % 3600 % 60)
            )


def get_last_record(session, task_id):
    return session.query(SessionRecord).filter(SessionRecord.task_pk == task_id) \
        .order_by(SessionRecord.id.desc()).first()