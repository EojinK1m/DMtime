from flask import jsonify
from flask_jwt_extended import jwt_required, jwt_refresh_token_required,\
    get_jwt_identity
from app.api.user.model import UserModel, UserSchema
from app.api.user.account.model import AccountModel, account_schema
from app.api.user.service import UserService
from app import db


class AccountService:


    @staticmethod
    @jwt_required
    def provide_account_info(email):
        identity = get_jwt_identity()
        account = AccountModel.query.filter_by(email=email).first()

        if not account:
            return jsonify(msg='account not found'), 404

        if (email != identity):
            return jsonify(msg='access denied'), 403


        return jsonify(account_info=account_schema.dump(account),
                       msg='query succeed'), 200



    @staticmethod
    def register_account(data):
        email = data.get('email', None)
        password = data.get('password', None)

        username = data.get('username', None)
        user_explain = data.get('user_explain', None)
        profile_image_id = data.get('profile_image', None)


        if email is None or password is None or username is None:
            return jsonify({'msg':'missing parameter exist'}), 400

        if AccountModel.query.filter_by(email=email).first():
            return jsonify({'msg':'same email exist'}), 400
        if UserModel.query.filter_by(username=username).first():
            return jsonify({'msg':'same username exist'}), 400

        new_account = AccountModel(email=email,
                                   password_hash=AccountModel.hash_password(password))

        db.session.add(new_account)
        db.session.commit()

        try:
            new_user = UserModel(username=username, account = new_account,\
                                 explain=user_explain)

            db.session.add(new_user)
            db.session.commit()
        except:
            new_account.delete_account()
            return jsonify(msg='an error occurred while creating new_user'), 500

        if(UserService.set_profile_image(new_user, profile_image_id)):
            return jsonify(msg='register succeed but while setting profile image, an error occurred'), 206

        return jsonify(msg='register succeed'), 200


    @staticmethod
    @jwt_required
    def delete_account(email):
        account = AccountModel.query.filter_by(email=email).first()
        if not account:
            return jsonify(msg='account not found'), 404

        if not get_jwt_identity() == email:
            return jsonify(msg='access denied'), 403


        UserService.delete_user(account.user)
        account.delete_account()

        db.session.commit()

        return jsonify(msg='account deleted!'), 200






class AuthService:

    @staticmethod
    def login(data):
        email = data.get('email', None)
        password = data.get('password', None)

        if not email or not password:
            return jsonify({'msg':'missing parameter exist'}), 400

        login_account = AccountModel.query.filter_by(email=email).first()

        if login_account:
            if login_account.verify_password(password):
                access_token = login_account.generate_access_token()
                refresh_token = login_account.generate_refresh_token()

                return jsonify({'access_token':access_token,
                                'refresh_token':refresh_token,
                                'msg':'login succeed',
                                'user':UserSchema(only=['username', 'profile_image']).dump(login_account.user)}), 200

        return jsonify({'msg':'incorrect username or password'}), 401

    @staticmethod
    @jwt_refresh_token_required
    def refresh():
        email = get_jwt_identity()
        account = AccountModel.query.filter_by(email=email).first()
        access_token = account.generate_access_token()

        return jsonify({'access_token': access_token}), 200


class DuplicateCheck:

    @staticmethod
    def email_check(email):
        if(email == None):
            return jsonify({'msg':'email parameter missed'}), 400
        if (AccountModel.query.filter_by(email=email).first() == None):
            return jsonify({'msg':'same email does not exist', 'usable':True}), 200
        else:
            return jsonify({'msg': 'same email exist', 'usable':False}), 200

    @staticmethod
    def username_check(username):
        if(username == None):
            return jsonify({'msg':'username parameter missed'}), 400
        if (UserModel.query.filter_by(username=username).first() == None):
            return jsonify({'msg':'same username does not exist', 'usable':True}), 200
        else:
            return jsonify({'msg': 'same username exist', 'usable':False}), 200
