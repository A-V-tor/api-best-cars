from marshmallow import Schema, fields, validate, post_load


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
