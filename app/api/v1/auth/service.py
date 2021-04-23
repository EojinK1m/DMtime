from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from ..user.service import UserService


class TokenService:

    @classmethod
    def get_user_from_token(cls):
        verify_jwt_in_request()
        return UserService.get_user_by_email_or_404(get_jwt_identity())