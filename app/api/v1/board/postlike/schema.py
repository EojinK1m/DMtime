from app.extentions import ma

from marshmallow.validate import Range


class RequestPostlikeApiQueryParameterVaidateSchema(ma.Schema):
    post_id = ma.Integer(
        required=True, validate=Range(min=0)
    )