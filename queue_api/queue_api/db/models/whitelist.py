import sqlalchemy as db
from sqlalchemy.dialects.mysql import VARCHAR

from queue_api.queue_api.db.models.base import QueueBase


class WhitelistEntries(QueueBase):
    __tablename__ = "whitelist_entries"

    name = db.Column(VARCHAR(), unique=True, nullable=False, primary_key=True)
    date_revoke = db.Column(
        db.DateTime(timezone=True), nullable=True
    )