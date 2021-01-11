from app import ma
from marshmallow import validate


class PostTokenValidateSchema(ma.Schema):
    password = ma.Str(required = True, validate = validate.Length(min = 8))
    email = ma.Str(required = True, validate = validate.Email())

