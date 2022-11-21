from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.settings.settings import Base


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    project = Column(ForeignKey("projects.id"))


class SessionRecord(Base):
    __tablename__ = "session_records"

    id = Column(Integer(), primary_key=True)
    starting_time = Column(DateTime())
    finishing_time = Column(DateTime())
    task_pk = Column(ForeignKey('tasks.id'))

