from flask import request, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import Cars, CombustionEngine, ElectricEngine, User, db
from . import jwt
from .shcema import CarsSchema

@app.route("/", methods=["GET"])
#@jwt_required()
def get_data():
    data = Cars.query.filter_by().all()
    schema = CarsSchema(many=True)
    return jsonify(schema.dump(data))



@app.route("/", methods=["POST"])
@jwt_required()
def send_data():
    data_for_add = request.json
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    check = hasattr(user, "admin")
    if not check:
        return {"message": "No access"}
    try:
        model = data_for_add["model"]
        year = data_for_add["year"]
        engine = data_for_add["engine"]
        max_speed_lower_limit = data_for_add.get("max_speed_lower_limit", None)
        max_speed_upper_limit = data_for_add.get("max_speed_upper_limit", None)
        released_copies = data_for_add.get("released", None)
        data_car = Cars(
            model=model,
            year=year,
            engine=engine,
            max_speed_lower_limit=max_speed_lower_limit,
            max_speed_upper_limit=max_speed_upper_limit,
            released_copies=released_copies,
        )
    except ValueError("Invalid data entry!"):
        pass
    if engine == "combustion":
        try:
            horsepower = data_for_add.get("horsepower", None)
            kW = data_for_add.get("kW", None)
            data_for_engine = CombustionEngine(
                horsepower=horsepower, kW=kW, car=data_car
            )
            db.session.add(data_car, data_for_engine)
        except ValueError("Invalid data entry!"):
            pass
    elif engine == "electric":
        try:
            power_reserve = data_for_add.get("power_reserve", None)
            data_for_engine = ElectricEngine(power_reserve=power_reserve, car=data_car)
            db.session.add(data_car, data_for_engine)
        except ValueError("Invalid data entry!"):
            pass
    else:
        pass
    db.session.commit()
    return data_for_add


@app.route("/<model>", methods=["PUT"])
@jwt_required()
def make_update(model):
    data_for_update = request.json
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    check = hasattr(user, "admin")
    if not check:
        return {"message": "No access"}
    item = Cars.query.filter_by(model=model).first()
    if not item:
        return {"message": "No such model"}, 400
    try:
        for (
            key,
            value,
        ) in data_for_update.items():
            setattr(item, key, value)
        db.session.commit()
        check = hasattr(item, f"{item.eletric_engine_type}")
        if check:
            serializad = {
                "model": item.model,
                "year": item.year,
                "engine": item.engine,
                "max_speed_lower_limit": item.max_speed_lower_limit,
                "max_speed_upper_limit": item.max_speed_upper_limit,
                "released_copies": item.released_copies,
                "eletric_engine_type": item.eletric_engine_type[0].power_reserve,
            }
        else:
            serializad = {
                "model": item.model,
                "year": item.year,
                "engine": item.engine,
                "max_speed_lower_limit": item.max_speed_lower_limit,
                "max_speed_upper_limit": item.max_speed_upper_limit,
                "released_copies": item.released_copies,
                "combustion_engine_type": [
                    item.combustion_engine_type[0].horsepower,
                    item.combustion_engine_type[0].kW,
                ],
            }
        return jsonify(serializad)
    except ValueError("Invalid data entry!"):
        pass


@app.route("/<model>", methods=["DELETE"])
@jwt_required()
def data_delete(model):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    check = hasattr(user, "admin")
    if not check:
        return {"message": "No access"}
    item = Cars.query.filter_by(model=model).first()
    if not item:
        return {"message": "No such model"}, 400
    db.session.delete(item)
    db.session.commit()
    return {"message": "Entry deleted"}, 200


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    db.session.add(user)
    db.session.commit()
    token = user.get_token()
    return {"access token": token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    return {"access token": token}
