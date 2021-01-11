from flask import Request
from flask_restful import Resource

from app.util.request_validator import RequestValidator

from app.api.v1.auth.schema import PostTokenValidateSchema
from app.api.v1.user.account.service import AccountService

class Token(Resource):

    def post(self):
        RequestValidator.validate_request(PostTokenValidateSchema(), Request.json)

        # account_2_generate_token = AccountService.get_account_by_email

        pass
