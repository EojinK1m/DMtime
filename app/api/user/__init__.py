from flask import Blueprint
from flask_restful import Api

from app.api.user.view import user
from app.api.user.account.view import Account, AccountPassword, Auth, Refresh,\
                                    DuplicateCheckEmail, DuplicateCheckUsername
                                    


user_blueprint = Blueprint('user_api', 'User api')

user_api = Api(user_blueprint)

user_api.add_resource(user, '/<username>')


account_api = Api(user_blueprint)

account_api.add_resource(Account, '/accounts')
account_api.add_resource(AccountPassword, '/accounts/password')
account_api.add_resource(Auth, '/accounts/auth')
account_api.add_resource(Refresh, '/accounts/auth/refresh')
account_api.add_resource(DuplicateCheckEmail, '/accounts/duplicate-check/email')
account_api.add_resource(DuplicateCheckUsername, '/accounts/duplicate-check/username')