from flask import abort, make_response, jsonify

class RequestValidator:

    @staticmethod
    def validate_request(schema, data):
        error = schema.validate(data)
        if error:
            response = make_response(jsonify({
                'message':'Request validate failed.',
                'errors':error
            }), 400)

            abort(response)