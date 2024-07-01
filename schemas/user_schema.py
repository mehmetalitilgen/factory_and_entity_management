from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=2))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    factory = fields.Str(validate=validate.Length(min=1))


class UserRegisterSchema(UserSchema):
    confirm_password = fields.Str(required=True)

