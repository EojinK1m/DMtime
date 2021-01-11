from flask_restful import Resource
from flask import make_response, request

from app.api.v1.user.service import UserService

class User(Resource):
    def get(self, username):
        return make_response(UserService.provide_user_info(username))

    def patch(self, username):
        return make_response(UserService.modify_user_info(username, request.json))