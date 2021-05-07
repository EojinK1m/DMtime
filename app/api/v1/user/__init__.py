from flask_restful import Api

from app.api.v1.board.comment import model
from app.api.v1.board.post import model
from app.api.v1.board.gallery import model
from app.api.v1.image import model

from app.api.v1.user.view import (
    User,
    Account,
    AccountPassword,
    DuplicateCheckEmail,
    DuplicateCheckUsername,
    Users,
    Me
)

user_api = Api()

user_api.add_resource(Users, "/users")
user_api.add_resource(User, "/users/<username>")
user_api.add_resource(Account, "/users/<username>/account")
user_api.add_resource(AccountPassword, "/users/<username>/account/password")
user_api.add_resource(DuplicateCheckEmail, "/users/email-duplication")
user_api.add_resource(DuplicateCheckUsername, "/users/username-duplication")
user_api.add_resource(Me, "/me")
