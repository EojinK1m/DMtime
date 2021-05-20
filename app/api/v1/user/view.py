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
    user_schema,
    UserPutInputSchema,
    AccountRegisterSchema,
    UserModel,
    GetUsernameDuplicationSchema,
    GetEmailDuplicationSchema,
    DeleteUserSchema,
    account_schema,
    AccountChangePasswordInputSchema,
)
from ..image.service import ImageService


class Users(Resource):
    def post(self):
        RequestValidator.validate_request(
            AccountRegisterSchema(), request.json
        )

        email = request.json.get("email")
        username = request.json.get("username")

        AccountService.check_exist_same_email(email)
        AccountService.check_exist_same_username(username)

        new_user = self.create_new_user(
            username=username,
            email=email,
            password=request.json.get("password"),
        )
        verification_code = AccountService.generate_verification_code()

        self.store_account_data_with_verification_code(
            verification_code, new_user
        )
        self.send_verification_code_by_email(verification_code, email)

        return {}, 201

    def create_new_user(self, username, email, password):
        return UserModel(
            username=username,
            email=email,
            password_hash=bcrypt.generate_password_hash(password),
        )

    def send_verification_code_by_email(self, verification_code, email):
        mail_title = "[대마타임] 회원가입 인증 코드입니다."
        mail = email_sender.make_mail(
            subject=mail_title, message=verification_code
        )

        try:
            email_sender.send_mail(to_email=email, message=mail)
        except SMTPException:
            abort(
                500, "An error occurred while send e-mail, plz try again later"
            )

    def store_account_data_with_verification_code(
        self, verification_code, account
    ):
        with redis_client.pipeline() as pipe:
            pipe.mset({verification_code: pickle.dumps(account)})
            pipe.expire(
                verification_code, current_app.config["EMAIL_VERIFY_DEADLINE"]
            )
            pipe.execute()


class User(Resource):
    def get(self, username):
        return (
            user_schema.dump(UserService.get_user_by_username(username)),
            200,
        )

    @UserService.user_access_authorize_required
    def put(self, username):
        user = UserService.get_user_by_username(username)
        json = request.json

        RequestValidator.validate_request(UserPutInputSchema(), json)

        username = json["username"]
        explain = json["user_explain"]
        profile_image = json["profile_image"]

        if profile_image is not None:
            profile_image = ImageService.get_image_by_id(profile_image)
        if user.username != username:
            AccountService.check_exist_same_username(json["username"])

        UserService.update_user(
            user=user,
            username=username,
            explain=explain,
            email=user.email,
            profile_image=profile_image,
            password_hash=user.password_hash,
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