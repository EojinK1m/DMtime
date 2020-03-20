from flask import Blueprint
from flask_restful import Api

from app.api.user.view import user
from app.api.user.account.view import Account, Auth, Refresh,\
                                    DuplicateCheckEmail, DuplicateCheckUsername


user_blueprint = Blueprint('user_api', 'User api')

user_api = Api(user_blueprint)

user_api.add_resource(user, '/<username>')


account_api = Api(user_blueprint)

account_api.add_resource(Account, '/account')
account_api.add_resource(Auth, '/account/auth')
account_api.add_resource(Refresh, '/account/auth/refresh')
account_api.add_resource(DuplicateCheckEmail, '/account/duplicate-check/email')
account_api.add_resource(DuplicateCheckUsername, '/account/duplicate-check/username')