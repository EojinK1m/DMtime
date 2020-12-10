from flask_restful import Api

from app.api.v1.user.view import user
from app.api.v1.user.account.view import Account, AccountPassword, Auth, Refresh,\
                                    DuplicateCheckEmail, DuplicateCheckUsername,\
                                    AuthEmailVerificationCode


user_api = Api()

user_api.add_resource(user, '/users/<username>')


account_api = Api()

account_api.add_resource(Account, '/users/accounts')
account_api.add_resource(AccountPassword, '/users/accounts/password')
account_api.add_resource(Auth, '/users/accounts/auth')
account_api.add_resource(AuthEmailVerificationCode, '/users/accounts/auth/verification-code')
account_api.add_resource(Refresh, '/users/accounts/auth/refresh')
account_api.add_resource(DuplicateCheckEmail, '/users/accounts/duplicate-check/email')
account_api.add_resource(DuplicateCheckUsername, '/users/accounts/duplicate-check/username')