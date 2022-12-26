from marshmallow import Schema, fields, validate, post_load


class CarsSchema(Schema):
    id = fields.Integer(dump_only=True)
    brend = fields.String(required=True, validate=[validate.Length(max=255)])
    model = fields.String(validate=[validate.Length(max=255)])
    year = fields.Integer()
    engine = fields.String(validate=[validate.Length(max=255)])
    max_speed = fields.Integer()
    released_copies = fields.String(validate=[validate.Length(max=255)])
    description = fields.String(validate=[validate.Length(max=255)])
    message = fields.String(dump_only=True)


class UserSchema(Schema):
    name = fields.String(required=True, validate=[validate.Length(max=255)])
    email = fields.String(required=True, validate=[validate.Length(max=50)])
    psw = fields.String(required=True, validate=[validate.Length(max=255)])
    admin = fields.Boolean()
    owner = fields.Boolean()
    message = fields.String(dump_only=True)


class AuthSchema(Schema):
    access_token = fields.String(dump_only=True)
    message = fields.String(dump_only=True)
