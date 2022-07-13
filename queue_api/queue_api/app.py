from flask import Flask

from .api import v1
from .credentials import (
    ATLAS_DB_USER,
    ATLAS_DB_HOST,
    ATLAS_DB_NAME,
    ATLAS_DB_PASS,
    ATLAS_DB_PORT
)
from queue_api.queue_api.db.database import DATABASE_URL, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_BINDS"] = {
    "atlas_game_server": f'mysql://{ATLAS_DB_USER}:{ATLAS_DB_PASS}@{ATLAS_DB_HOST}:{ATLAS_DB_PORT}/{ATLAS_DB_NAME}'
}
app.config["SQLALCHEMY_ECHO"] = False
db.init_app(app)

app.register_blueprint(v1, url_prefix="/api/v1")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
