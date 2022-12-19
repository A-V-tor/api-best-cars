from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    """Создание основного приложения."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config")

    db.init_app(app)

    with app.app_context():
        from . import routes

        # db.drop_all()
        db.create_all()

        return app
