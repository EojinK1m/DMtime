from app.extensions import ma

from marshmallow.validate import Range


class RequestPostlikeApiQueryParameterValidateSchema(ma.Schema):
    post_id = ma.Integer(
        required=True, validate=Range(min=0)
    )