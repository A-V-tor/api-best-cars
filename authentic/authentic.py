from flask import Blueprint, jsonify, current_app as app
from flask_apispec import use_kwargs, marshal_with
from api_best_cars.models import User, db
from .shcema import UserSchema, AuthSchema
from api_best_cars import docs


user = Blueprint(
    "user", "__name__", template_folder="templates", static_folder="static"
)


@user.route("/register", methods=["POST"])
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
def register(**kwargs):
    try:
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        token = user.get_token()
        return {"message": token}, 200
    except Exception:
        app.logger.error("request failed")
        return jsonify({"message": "error"})


@user.route("/login", methods=["POST"])
@use_kwargs(UserSchema(only=("email", "psw")))
@marshal_with(AuthSchema)
def login(**kwargs):
    try:
        user = User.authenticate(**kwargs)
        token = user.get_token()
        return {"message": token}, 200
    except Exception:
        app.logger.error(f"not found user")
        return jsonify({"message": "error"})


@user.errorhandler(422)
def error_handler(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request"])
    if headers:
        return jsonify({"messages": messages}), headers
    else:
        return jsonify(messages)


docs.register(register, blueprint="user")
docs.register(login, blueprint="user")
