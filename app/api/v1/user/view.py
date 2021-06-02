import pickle
from smtplib import SMTPException

from flask import request, current_app, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app.extensions import redis_client
from app.extensions import bcrypt
from app.extensions import email_sender

from app.util.request_validator import RequestValidator

from app.api.v1.user.service import UserService, AccountService
from app.api.v1.user.model import (
    UserModel,
)
from .schema import user_schema, account_schema, UserPutInputSchema, AccountRegisterSchema, \
    AccountChangePasswordInputSchema, GetEmailDuplicationSchema, GetUsernameDuplicationSchema, DeleteUserSchema
from ..image.service import ImageService


class Users(Resource):
    def __init__(self) -> None:
        self.user_service = AccountService()

    def post(self):
        RequestValidator.validate_request(
            AccountRegisterSchema(), request.json
        )
        email = request.json.get("email")
        password = request.json.get("password")
        username = request.json.get("username")

        self.user_service.register_user_temporarily(
            email, password, username
        )

        return {}, 201

class User(Resource):
    def get(self, username):
        return (
            user_schema.dump(UserService.get_user_by_username(username)),
            200,
        )

    @UserService.user_access_authorize_required
    def put(self, username):
        json = request.json
        RequestValidator.validate_request(UserPutInputSchema(), json)

        UserService().update_user(
            username=username,
            new_username=json['username'],
            explain=json['user_explain'],
            profile_image=json['profile_image']
        )

        return {}, 200

    #
    # @jwt_required
    # def patch(self, username):
    #     RequestValidator.validate_request(UserPatchInputSchema(), request.json)
    #
    #     user = (UserModel.query.filter_by(email=get_jwt_identity()).first()).user
    #     if not user or not UserModel.query.filter_by(username=username).first():
    #         return jsonify({'msg': 'user not found'}), 404
    #     elif user.username != username:
    #         return jsonify({'msg': f'access denied, you are not {username}'}), 403
    #
    #     new_username = data.get('username', None)
    #     new_explain = data.get('user_explain', None)
    #     new_profile_image_id = data.get('profile_image_id',
    #                                     user.profile_image.id if user.profile_image else None)
    #
    #
    #     if not (new_username == None):
    #         if(UserModel.query.filter_by(username=new_username).first()):
    #             return jsonify(msg='Bad request, same username exist'), 400
    #         user.username = new_username
    #     if not (new_explain == None):
    #         user.explain = new_explain
    #     if not UserService.set_profile_image(user, new_profile_image_id):
    #         return jsonify({'msg': f'image not found, image {new_profile_image_id}is not exist'}), 404
    #
    #     db.session.commit()
    #
    #     return jsonify({'msg':'modification succeed'}), 200
    #
    #     return make_response(UserService.modify_user_info(username, request.json))


class Account(Resource):
    @UserService.user_access_authorize_required
    def get(self, username):
        user = UserService.get_user_by_username(username)
        return account_schema.dump(user), 200

    @UserService.user_access_authorize_required
    def delete(self, username):
        RequestValidator.validate_request(DeleteUserSchema(), request.json)

        user = UserService.get_user_by_username(username)
        password = request.json.get("password")

        UserService.raise_401_if_not_password_verified(user, password=password)
        user.delete_user()

        return {}, 200


class AccountPassword(Resource):
    @UserService.user_access_authorize_required
    def put(self, username):
        RequestValidator.validate_request(
            AccountChangePasswordInputSchema(), request.json
        )

        json = request.json
        user = UserService.get_user_by_username(username)
        password = json["password"]
        new_password = json["new_password"]

        UserService.raise_401_if_not_password_verified(user, password)
        AccountService.change_account_password(user, new_password)

        return {}, 200


class DuplicateCheckEmail(Resource):
    def get(self):
        RequestValidator.validate_request(
            GetEmailDuplicationSchema(), request.args
        )
        email = request.args["email"]

        usable = UserService.get_user_by_email_or_none(email) is None

        return {"usable": usable}, 200


class DuplicateCheckUsername(Resource):
    def get(self):
        RequestValidator.validate_request(
            GetUsernameDuplicationSchema(), request.args
        )
        username = request.args["username"]

        usable = UserService.get_user_by_username_or_none(username) is None

        return {"usable": usable}, 200


class Me(Resource):
    @jwt_required
    def get(self):
        user = UserService.get_user_by_email_or_none(get_jwt_identity())

        return user_schema.dump(user)