from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_apispec.extension import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
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

    app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title="best cars",
                version="v1",
                openapi_version="2.0",
                plugins=[FlaskPlugin(), MarshmallowPlugin()],
            )
        }
    )

    with app.app_context():
        from . import routes
        from authentic import authentic

        # db.drop_all()
        db.create_all()

        app.register_blueprint(authentic.user)
        docs.init_app(app)

        return app
