from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from queue_api.queue_api.credentials import (
    ATLAS_DB_USER,
    ATLAS_DB_HOST,
    ATLAS_DB_NAME,
    ATLAS_DB_PASS,
    ATLAS_DB_PORT
)


ATLAS_DATABASE_URL = (
    f'mysql://{ATLAS_DB_USER}:{ATLAS_DB_PASS}@{ATLAS_DB_HOST}:{ATLAS_DB_PORT}/{ATLAS_DB_NAME}'
)
atlas_db_engine = create_engine(ATLAS_DATABASE_URL)


def atlas_session():
    session_maker = sessionmaker(atlas_db_engine)
    return session_maker()
