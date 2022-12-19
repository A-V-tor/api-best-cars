from flask import request, jsonify, current_app as app

from .models import Cars, CombustionEngine, ElectricEngine, db


@app.route("/", methods=["GET"])
def get_data():
    data = Cars.query.filter_by().all()
    lst = []
    for item in data:
        serializad = {
            "model": item.model,
            "year": item.year,
            "engine": item.engine,
            "max_speed_lower_limit": item.max_speed_lower_limit,
            "max_speed_upper_limit": item.max_speed_upper_limit,
            "released_copies": item.released_copies,
        }
        if serializad["engine"] == "combustion":
            horsepower = item.combustion_engine_type[0].horsepower
            kW = item.combustion_engine_type[0].kW
            serializad.update({"horsepower": horsepower, "kW": kW})
        else:
            power_reserve = item.eletric_engine_type[0].power_reserve
            serializad.update({"power_reserve": power_reserve})
        lst.append(jsonify(serializad))
    return [i.get_json() for i in lst]


@app.route("/", methods=["POST"])
def send_data():
    data_for_add = request.json
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
    except ValueError("Не корректный ввод данных!"):
        pass
    if engine == "combustion":
        try:
            horsepower = data_for_add.get("horsepower", None)
            kW = data_for_add.get("kW", None)
            data_for_engine = CombustionEngine(
                horsepower=horsepower, kW=kW, car=data_car
            )
        except ValueError("Не корректный ввод данных!"):
            pass
    else:
        try:
            power_reserve = data_for_add.get("power_reserve", None)
            data_for_engine = ElectricEngine(power_reserve=power_reserve, car=data_car)
        except ValueError("Не корректный ввод данных!"):
            pass
    db.session.add(data_car, data_for_engine)
    db.session.commit()
    return data_for_add


@app.route("/<model>", methods=["PUT"])
def make_update(model):
    data_for_update = request.json
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
    except ValueError("Не корректный ввод данных!"):
        pass


@app.route("/<model>", methods=["DELETE"])
def data_delete(model):
    item = Cars.query.filter_by(model=model).first()
    if not item:
        return {"message": "No such model"}, 400
    db.session.delete(item)
    db.session.commit()
    return {"message": "Entry deleted"}, 200
