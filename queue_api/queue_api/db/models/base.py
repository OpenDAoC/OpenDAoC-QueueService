import sqlalchemy as db
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class QueueBase(Base):
    __abstract__ = True

    date_create = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
