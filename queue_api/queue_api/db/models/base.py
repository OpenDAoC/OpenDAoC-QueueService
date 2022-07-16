import sqlalchemy as db
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class QueueBase(Base):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    __abstract__ = True

    date_create = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
