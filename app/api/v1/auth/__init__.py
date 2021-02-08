from flask_restful import Api

from app.api.v1.auth.view import Token, EmailVerificationCode

auth_api = Api()

auth_api.add_resource(Token, '/token')
auth_api.add_resource(EmailVerificationCode, '/email-verification-code')