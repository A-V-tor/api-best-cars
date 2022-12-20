from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec


db = SQLAlchemy()
jwt = JWTManager()
docs = FlaskApiSpec()



def create_app():
    """Создание основного приложения."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config")

    db.init_app(app)
    jwt.init_app(app)
    docs.init_app(app)

    app.config.update(
        {
            'APISPEC_SPEC': APISpec(
                title='best cars',
                version='v1',
                openapi_version='2.0',
                plugins=[MarshmallowPlugin()]
            )
        }
    )

    with app.app_context():
        from . import routes

        # db.drop_all()
        db.create_all()

        return app
