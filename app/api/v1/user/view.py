from flask import make_response, request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.util.request_validator import RequestValidator

from app.api.v1.user.service import UserService, AccountService, AuthService, DuplicateCheck
from app.api.v1.user.model import user_schema, UserPatchInputSchema, UserPutInputSchema


class User(Resource):

    def get(self, username):
        return user_schema.dump(UserService.get_user_by_username(username)), 200

    @jwt_required
    def put(self, username):
        RequestValidator.validate_request(UserPutInputSchema(), request.json)

        user2put = UserService.get_user_by_username(username)
        request_user = UserService.get_user_by_email(get_jwt_identity())

        if not user2put == request_user:
            abort(403)



    @jwt_required
    def patch(self, username):
        RequestValidator.validate_request(UserPatchInputSchema(), request.json)

        user = (UserModel.query.filter_by(email=get_jwt_identity()).first()).user
        if not user or not UserModel.query.filter_by(username=username).first():
            return jsonify({'msg': 'user not found'}), 404
        elif user.username != username:
            return jsonify({'msg': f'access denied, you are not {username}'}), 403

        new_username = data.get('username', None)
        new_explain = data.get('user_explain', None)
        new_profile_image_id = data.get('profile_image_id',
                                        user.profile_image.id if user.profile_image else None)


        if not (new_username == None):
            if(UserModel.query.filter_by(username=new_username).first()):
                return jsonify(msg='Bad request, same username exist'), 400
            user.username = new_username
        if not (new_explain == None):
            user.explain = new_explain
        if not UserService.set_profile_image(user, new_profile_image_id):
            return jsonify({'msg': f'image not found, image {new_profile_image_id}is not exist'}), 404

        db.session.commit()

        return jsonify({'msg':'modification succeed'}), 200

        return make_response(UserService.modify_user_info(username, request.json))


class Account(Resource):
    def get(self):
        return make_response(AccountService.provide_account_info())

    def post(self):
        return make_response(AccountService.register_account(request.json))

    def delete(self):
        return make_response(AccountService.delete_account(request.args.get('email')))


class AccountPassword(Resource):
    def put(self):
        return make_response(AccountService.change_account_password(request.json))


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


class AuthEmailVerificationCode(Resource):
    def post(self):
        return make_response(AccountService.verify_email_verification_code(verification_code=request.args.get('verification-code')))
