# #!/usr/bin/env python3
# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
#
#
# db = SQLAlchemy()
#
# # def init_app():
# #     app = Flask(__name__, instance_relative_config=False)
# #     app.config.from_object('config')
# #
# #     db.init_app(app)
# #
# #     with app.app_context():
# #         #from api_best_cars.models import Cars, CombustionEngine, ElectricEngine
# #         import models
# #
# #         #db.drop_all()
# #         db.create_all()
# #         return app
# #
# #
# # app = init_app()
# # client = app.test_client()
#
# def create_app():
#     app = Flask(__name__, instance_relative_config=False)
#     app.config.from_object('config')
#
#     db.init_app(app)
#
#     with app.app_context():
#         from api_best_cars.models import Cars, CombustionEngine, ElectricEngine
#         db.create_all()
#         return app
#
# app = create_app()
# client = app.test_client()
#
# data_for_entries = [
#     {   'id': 1,
#         "model": "Ford Model T",
#         "year": 1908,
#         "engine": ["internal combustion engine", (20, "horsepower"), (15, "kW")],
#         "speed": [64, 72, "km/h"],
#         "released": "over 15 million",
#     },
#     {   'id': 2,
#         "model": "Dodge Brothers Model 30",
#         "year": 1919,
#         "engine": ["internal combustion engine", (35, "horsepower"), (25.7, "kW")],
#         "speed": [64, 80, "km/h"],
#         "released": "116 400 copies",
#     },
#     {   'id': 3,
#         "model": "Detroit Electric",
#         "year": 1920,
#         "power reserve": (129, "m"),
#         "speed": [32, "km/h"],
#         "released": "13 000 copies",
#     }
# ]
#
#
# @app.route('/', methods=['GET'])
# def get_data():
#     return jsonify([i for i in data_for_entries])
#
#
# @app.route('/', methods=['POST'])
# def send_data():
#     data_for_add = request.json
#     data_for_entries.append(data_for_add)
#     return data_for_entries
#
#
# @app.route('/<int:id>', methods=['PUT'])
# def make_update(id):
#     data_for_update = request.json
#     check_sl = [i for i in data_for_entries if i['id'] == id]
#     if check_sl:
#         sl = check_sl[0]
#     else:
#         return {"message": "No car with this id"}, 400
#     sl.update(data_for_update)
#     return data_for_entries
#
#
# @app.route('/<int:id>', methods=['DELETE'])
# def data_delete(id):
#     id = [i[0] for i in enumerate(data_for_entries) if i[1]['id'] == id][0]
#     data_for_entries.pop(id)
#     return data_for_entries
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
