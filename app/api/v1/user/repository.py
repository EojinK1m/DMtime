from .model import UserModel

class UserRepository:

    @classmethod
    def get_user_by_username(cls, username):
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return UserModel.query.filter_by(email=email).first()

    def save(self, user):
        pass

    def delete_user(self, user):
        pass
