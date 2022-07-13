import sqlalchemy as db
from sqlalchemy.dialects.mysql import VARCHAR

from base import QueueBase


class QueueEntries(QueueBase):
    __tablename__ = "queue_entries"

    name = db.Column(VARCHAR(), unique=True, nullable=False, primary_key=True)