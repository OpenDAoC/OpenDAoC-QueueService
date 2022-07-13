import sqlalchemy as db
from sqlalchemy.dialects.mysql import VARCHAR

from base import QueueBase


class WhitelistEntries(QueueBase):
    __tablename__ = "whitelist_entries"

    name = db.Column(VARCHAR(), unique=True, nullable=False, primary_key=True)
    revoke_date = db.Column(
        db.DateTime(timezone=True), nullable=True
    )