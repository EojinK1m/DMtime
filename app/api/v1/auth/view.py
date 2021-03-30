import pickle

from flask import request, abort
from flask_restful import Resource

from app import redis_client

from app.util.request_validator import RequestValidator
from app.util.db_helper import DBHelper

from app.api.v1.auth.schema import (
    PostTokenValidateSchema,
    PostEmailVerificationCodeSchema,
)
from app.api.v1.user.service import UserService


class Token(Resource):
    def post(self):
        RequestValidator.validate_request(PostTokenValidateSchema(), request.json)
        email = request.json.get("email")
        password = request.json.get("password")

        login_user = UserService.get_user_by_email_or_none(email)

        if login_user and login_user.verify_password(password):
            return {
                "access_token": login_user.generate_access_token(),
                "refresh_token": login_user.generate_refresh_token(),
            }, 201

        abort(401, "incorrect username or password")


class EmailVerificationCode(Resource):
    def post(self):
        RequestValidator.validate_request(
            PostEmailVerificationCodeSchema(), request.args
        )
        verification_code = request.args["verification-code"]

        user_to_register = self.find_user_by_verificatino_code(verification_code)
        self.delete_from_temporary_storage(verification_code)

        DBHelper.add_model(user_to_register)
        return {}, 200

    def find_user_by_verificatino_code(self, verification_code):
        dumped_user_data = redis_client.get(verification_code)

        if dumped_user_data is None:
            abort(404, "Verification code not found.")

        return pickle.loads(dumped_user_data)

    def delete_from_temporary_storage(self, verification_code):
        redis_client.delete(verification_code)
