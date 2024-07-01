from marshmallow import Schema, fields, validate


class EntitySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    factory = fields.Str(required=True)
