from flask import Flask

from .api import v1

from queue_api.queue_api.db.database import DATABASE_URL, db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_ECHO"] = False
    db.init_app(app)
    app.register_blueprint(v1, url_prefix="/api/v1")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    app = create_app()
