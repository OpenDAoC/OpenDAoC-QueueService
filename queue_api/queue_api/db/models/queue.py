import sqlalchemy as db
from sqlalchemy import func, BOOLEAN
from sqlalchemy.dialects.mysql import VARCHAR

from queue_api.queue_api.db.models.base import QueueBase


class QueueEntries(QueueBase):
    __tablename__ = "queue_entries"

    name = db.Column(VARCHAR(), unique=True, nullable=False, primary_key=True)
    date_revoke = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    whitelisted = db.Column(BOOLEAN(), default=False, nullable=False)