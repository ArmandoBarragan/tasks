from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from src.settings.settings import DATABASE, Base


def create_sessionmaker():
    """Sets the database parameters that will be used to start sessions."""
    uri = 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
        user=DATABASE['USER'],
        password=DATABASE['PASSWORD'],
        host=DATABASE['HOST'],
        name=DATABASE['NAME'],
        port=DATABASE['PORT']
    )

    try:
        db_engine = create_engine(uri)
        Base.metadata.create_all(db_engine)

    except OperationalError:
        print('Something failed')
        raise OperationalError

    return sessionmaker(db_engine), db_engine


Session, engine = create_sessionmaker()


