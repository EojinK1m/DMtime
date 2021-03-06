import json
from smtplib import SMTPException
from flask import jsonify, abort, current_app
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity

from app import db, redis_client, email_sender
from app.util import verification_code_generater

from app.api.v1.user.model import UserModel
from app.api.v1.user.account.model import AccountModel, account_schema, AccountInputSchema, AccountChangePasswrodInputSchema
from app.api.v1.user.service import UserService


class AccountService:

    @staticmethod
    @jwt_required
    def provide_account_info():
        email = get_jwt_identity()
        account = AccountModel.get_account_by_email(email)

        return jsonify(account_info=account_schema.dump(account),
                       msg='query succeed'), 200


    @staticmethod
    def register_account(data):
        AccountService.validate_account_register_data(data)

        email = data.get('email')
        AccountService.check_exist_same_email(email)
        AccountService.check_exist_same_username(data.get('username'))
        
        verification_code = AccountService.generate_verification_code()

        AccountService.store_register_data_temporally(verification_code, data)
        AccountService.send_verification_by_email(verification_code=verification_code, to_send_email=email)

        return jsonify(message='register account temporally succeed, plz verify requested email'), 201


    @staticmethod
    def validate_account_register_data(data):
        errors = AccountInputSchema().validate(data)
        if errors:
            abort(400, str(errors))


    @staticmethod
    def check_exist_same_username(username):
        if UserModel.query.filter_by(username=username).first():
            abort(409, 'same username exist')


    @staticmethod
    def check_exist_same_email(email):
        if AccountModel.get_account_by_email(email):
            abort(409, 'same email exist')


    @staticmethod
    def store_register_data_temporally(verification_code, data):
        with redis_client.pipeline() as pipe:
            pipe.mset({verification_code: json.dumps(data)})
            pipe.expire(verification_code, current_app.config['EMAIL_VERIFY_DEADLINE'])
            pipe.execute()


    @staticmethod
    def send_verification_by_email(verification_code, to_send_email):
        mail_title = '[대마타임] 회원가입 인증 코드입니다.'
        mail = email_sender.make_mail(subject=mail_title, message=verification_code)

        try:
            email_sender.send_mail(to_email=to_send_email, message=mail)
        except SMTPException as e:
            abort(500, 'An error occurred while send e-mail, plz try again later')


    @staticmethod
    def generate_verification_code():
        while(True):
            temp_code = verification_code_generater.generate_verification_code()

            if not (redis_client.exists(temp_code)):
                return temp_code


    @staticmethod
    def verify_email_verification_code(verification_code):
        AccountService.validate_verification_code(verification_code)
        register_data = AccountService.find_register_data_by_verification_code(verification_code)

        AccountService.check_exist_same_username(register_data.get('username'))
        AccountService.check_exist_same_email(register_data.get('email'))
        AccountService.store_account_user_information(register_data)

        redis_client.delete(verification_code)
        return jsonify(msg='Verify succeed'), 200


    @staticmethod
    def validate_verification_code(code):
        if not (verification_code_generater.validate_verification_code(code)):
            raise abort(400)


    @staticmethod
    def find_register_data_by_verification_code(verification_code):
        AccountService.validate_verification_code(verification_code)
        register_data = redis_client.get(verification_code)

        if(register_data == None):
            abort(404, 'Verification code not found.')

        return json.loads(register_data.decode('utf-8'))


    @staticmethod
    def store_account_user_information(register_data):
        try:
            new_account = AccountModel(
                email=register_data.get('email'),
                password_hash=AccountModel.hash_password(register_data.get('password'))
            )
            db.session.add(new_account)
            db.session.flush()

            new_user = UserModel(
                username=register_data.get('username'),
                account=new_account
            )
            db.session.add(new_user)

            db.session.commit()
        except:
            db.session.rollback()
            abort(500, 'an error occurred while adding infos in db')


    @staticmethod
    @jwt_required
    def delete_account(email):
        account = AccountModel.get_account_by_email(email)
        if not account:
            abort(404, 'Account not found')

        if not get_jwt_identity() == email:
            abort(403, 'Access denied')


        UserService.delete_user(account.user)
        account.delete_account()

        db.session.commit()
        return jsonify(msg='account deleted!'), 200


    @staticmethod
    @jwt_required
    def change_account_password(data):
        errors = AccountChangePasswrodInputSchema().validate(data)
        if errors:
            abort(400, 'missing parameter exist')
        
        email = get_jwt_identity()
        account = AccountModel.get_account_by_email(email)
        password = data.get('password')
        new_password = data.get('new_password')

        if not (account.verify_password(password)):
            abort(403, 'Access denied')
        
        account.password_hash = AccountModel.hash_password(new_password)
        
        db.session.commit()
        return jsonify(msg='change password succeed!')

    @staticmethod
    def find_account_by_email(email):
        found_account = AccountModel.get_account_by_email(email)

        if found_account is None:
            abort(404, 'Account not found, there is no account include the email.')

        return found_account


class AuthService:

    @staticmethod
    def login(data):
        from app.api.v1.user.account.model import AccountLoginInputSchema
        error = AccountLoginInputSchema().validate(data)
        if error:
            return jsonify(msg='Bad request, wrong json body'), 400

        email = data.get('email', None)
        password = data.get('password', None)

        login_account = AccountModel.get_account_by_email(email)

        if login_account:
            if login_account.verify_password(password):
                access_token = login_account.generate_access_token()
                refresh_token = login_account.generate_refresh_token()

                return jsonify({'access_token':access_token,
                                'refresh_token':refresh_token,
                                'msg':'login succeed'}), 200

        return jsonify({'msg':'incorrect username or password'}), 401


    @staticmethod
    @jwt_refresh_token_required
    def refresh():
        email = get_jwt_identity()
        account = AccountModel.get_account_by_email(email)
        access_token = account.generate_access_token()

        return jsonify({'access_token': access_token}), 200


class DuplicateCheck:

    @staticmethod
    def email_check(email):
        if(email == None):
            abort(400, 'email parameter missed')
        if (AccountModel.get_account_by_email(email) == None):
            return jsonify({'msg':'same email does not exist', 'usable':True}), 200
        else:
            return jsonify({'msg': 'same email exist', 'usable':False}), 200


    @staticmethod
    def username_check(username):
        if(username == None):
            abort(400, 'username parameter missed')
        if (UserModel.query.filter_by(username=username).first() == None):
            return jsonify({'msg':'same username does not exist', 'usable':True}), 200
        else:
            return jsonify({'msg': 'same username exist', 'usable':False}), 200