from marshmallow import Schema, fields, validate


class FactorySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    location = fields.Str(required=True)
    capacity = fields.Int(required=True, validate=validate.Range(min=1))
