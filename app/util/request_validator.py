from flask import abort

class RequestValidator:

    @staticmethod
    def validate_request(schema, data):
        error = schema.validate(data)
        if error:
            abort(400, str(error))