import logging
from flask import request, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with

from .models import User, db, Cars
from . import jwt, docs
from .shcema import CarsSchema


logging.basicConfig(
    filename="record.log",
    level=logging.ERROR,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


@app.route("/", methods=["GET"])
@jwt_required()
@marshal_with(CarsSchema(many=True))
def get_all_data_cars():
    try:
        data = Cars.query.filter_by().all()
        return data
    except Exception:
        app.logger.error("request error for page")
        return jsonify({"message": "error"})


@app.route("/<model>", methods=["GET"])
@jwt_required()
@marshal_with(CarsSchema)
def get_data_car(model):
    try:
        data = Cars.query.filter_by(model=model).order_by(Cars.data).first()
        return data
    except Exception:
        app.logger.error(f"not found {model}")
        return jsonify({"message": "error"})


@app.route("/", methods=["POST"])
@jwt_required()
@use_kwargs(CarsSchema)
@marshal_with(CarsSchema)
def send_data(**kwargs):
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        admin = hasattr(user, "admin")
        if not admin:
            return {"message": "No access"}
        new_car = Cars(**kwargs)
        db.session.add(new_car)
        db.session.commit()
        return new_car
    except Exception:
        app.logger.error("request failed")
        return jsonify({"message": "error"})


@app.route("/<model>", methods=["PUT"])
@jwt_required()
@use_kwargs(CarsSchema)
@marshal_with(CarsSchema)
def make_update(model, **kwargs):
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        admin = hasattr(user, "admin")
        if not admin:
            return {"message": "No access"}
        item = Cars.query.filter_by(model=model).first()
        if not item:
            return {"message": "No such model"}, 400
        for key, value in kwargs.items():
            setattr(item, key, value)
        db.session.commit()
        return item, 200
    except Exception:
        app.logger.error("request failed")
        return jsonify({"message": "error"})


@app.route("/<model>", methods=["DELETE"])
@jwt_required()
@marshal_with(CarsSchema)
def data_delete(model):
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        admin = hasattr(user, "admin")
        if not admin:
            return {"message": "No access"}
        item = Cars.query.filter_by(model=model).first()
        if not item:
            return {"message": "No such model"}, 400
        db.session.delete(item)
        db.session.commit()
        return {"message": "Entry deleted"}, 200
    except Exception:
        app.logger.error("request failed")
        return jsonify({"message": "error"})


docs.register(get_all_data_cars)
docs.register(get_data_car)
docs.register(send_data)
docs.register(make_update)
docs.register(data_delete)
