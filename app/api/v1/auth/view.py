from flask import request, abort
from flask_restful import Resource

from app.util.request_validator import RequestValidator

from app.api.v1.auth.schema import PostTokenValidateSchema
from app.api.v1.user.service import UserService


class Token(Resource):

    def post(self):
        RequestValidator.validate_request(PostTokenValidateSchema(), request.json)
        email = request.json.get('email')
        password = request.json.get('password')

        login_user = UserService.get_user_by_email_or_None(email)

        if login_user and login_user.verify_password(password):
            return {
                'access_token':login_user.generate_access_token(),
                'refresh_token':login_user.generate_refresh_token()
            }, 200

        abort(401, 'incorrect username or password')