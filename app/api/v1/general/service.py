from flask import abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims, jwt_required, get_jwt_identity
from functools import wraps

from ..user.repository import UserRepository

user_repository = UserRepository()

def verify_admin_jwt_in_request():
    verify_jwt_in_request()

    claims = get_jwt_claims()
    if not claims["roles"] == "admin":
        abort(403, "Access denied, admin only!")


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_admin_jwt_in_request()
        return fn(*args, **kwargs)

    return wrapper


@jwt_required
def get_user_from_token():
    return user_repository.get_user_by_email(get_jwt_identity())

