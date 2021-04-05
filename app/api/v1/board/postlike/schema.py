from app import ma

class RequestPostlikeApiQueryParameterVaidateSchema(ma.Schema):
    post_id = ma.Integer(
        data_key="post-id", required=True, validate=Range(min=0)
    )
    