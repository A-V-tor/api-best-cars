from marshmallow import Schema, fields, validate


class CarsSchema(Schema):
    id = fields.Integer(dump_only=True)
    model = fields.String(required=True, validate=[
        validate.Length(max=50)
    ])
    year = fields.Integer()
    engine = fields.String(required=True, validate=[
        validate.Length(max=50)
    ])
    max_speed_lower_limit = fields.Integer()
    max_speed_upper_limit = fields.Integer()
    eletric_engine_type = fields.Nested('ElectricEngineSchema', many=True)
    combustion_engine_type = fields.Nested('CombustionEngine', many=True)


class ElectricEngineSchema(Schema):
    id = fields.Integer(dump_only=True)
    power_reserve = fields.String(required=True, validate=[
        validate.Length(max=50)
    ])


class CombustionEngine(Schema):
    id = fields.Integer(dump_only=True)
    horsepower = fields.Integer()
    kW = fields.Integer()