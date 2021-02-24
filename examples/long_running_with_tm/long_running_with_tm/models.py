from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

class TaskItem(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task = Column(Text, unique=True)
