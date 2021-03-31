from flask_restful import Api

from app.api.v1.user.view import (
    User,
    Account,
    AccountPassword,
    DuplicateCheckEmail,
    DuplicateCheckUsername,
    Users,
)

user_api = Api()

user_api.add_resource(Users, "/users")
user_api.add_resource(User, "/users/<username>")
user_api.add_resource(Account, "/users/<username>/account")
user_api.add_resource(AccountPassword, "/users/<username>/account/password")
user_api.add_resource(DuplicateCheckEmail, "/users/email-duplication")
user_api.add_resource(DuplicateCheckUsername, "/users/username-duplication")
