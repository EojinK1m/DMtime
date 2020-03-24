from flask import jsonify
from flask_jwt_extended import jwt_required, jwt_refresh_token_required,\
    get_jwt_identity
from app.api.user.model import UserModel, user_schema
from app.api.user.account.model import AccountModel, account_schema
from app import db


class AccountService:


    @staticmethod
    @jwt_required
    def provide_account_info(account):
        identity = get_jwt_identity()

        if (account != identity):
            return jsonify({'msg':'access denied'}), 403

        account = AccountModel.query.filter_by(email=account).first()
        return jsonify(account_schema.dump(account)), 200



    @staticmethod
    def register_account(data):
        email = data.get('email', None)
        password = data.get('password', None)

        username = data.get('username', None)
        user_explain = data.get('user_explain', None)
        profile_image = data.get('profile_image', None)


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


        new_user = UserModel(username=username, account = new_account,
                             profile_image=profile_image, explain=user_explain)


        # try:
        db.session.add(new_user)
        db.session.commit()
        # except:
        #     print()
        #     return jsonify({'msg':'an error occurred while adding data to db'}), 500

        return jsonify({'msg':'register succeed'}), 200


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
                                'user':user_schema.dump(login_account.user)}), 200

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
