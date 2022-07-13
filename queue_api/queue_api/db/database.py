from flask_sqlalchemy import SQLAlchemy

from .models.base import Base
from ..credentials import (
    QUEUE_DB_USER,
    QUEUE_DB_PASS,
    QUEUE_DB_HOST,
    QUEUE_DB_PORT,
    QUEUE_DB_NAME
)

DATABASE_URL = (
    f'mysql://{QUEUE_DB_USER}:{QUEUE_DB_PASS}@{QUEUE_DB_HOST}:{QUEUE_DB_PORT}/{QUEUE_DB_NAME}'
)

db = SQLAlchemy(model_class=Base)
