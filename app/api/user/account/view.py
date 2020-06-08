from flask import make_response, request
from flask_restful import Resource

from app.api.user.account.service import AccountService, AuthService, DuplicateCheck


class Account(Resource):
    def get(self):
        return make_response(AccountService.provide_account_info())

    def post(self):
        return make_response(AccountService.register_account(request.json))

    def delete(self):
        return make_response(AccountService.delete_account(request.args.get('email')))

class Auth(Resource):
    def post(self):
        return make_response(AuthService.login(request.json))

class Refresh(Resource):
    def get(self):
        return make_response(AuthService.refresh())

class DuplicateCheckEmail(Resource):
    def get(self):
        return make_response(DuplicateCheck.email_check(request.args.get('email')))

class DuplicateCheckUsername(Resource):
    def get(self):
        return make_response(DuplicateCheck.username_check(request.args.get('username')))
