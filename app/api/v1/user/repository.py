from ..base_classes import BaseRepository
from .model import UserModel


class UserRepository(BaseRepository):

    @classmethod
    def get_user_by_username(cls, username):
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return UserModel.query.filter_by(email=email).first()
