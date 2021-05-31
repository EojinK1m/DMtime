import re
from marshmallow import validate

from app.extensions import ma

from .model import UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    username = ma.auto_field()
    explain = ma.auto_field()
    profile_image = ma.Method(
        serialize="get_profile_image"
    )
    email = ma.auto_field()

    def get_profile_image(self, obj):
        image = obj.profile_image

        return None if image is None else image.id


user_schema = UserSchema(exclude=["email"])
users_schema = UserSchema(many=True, only=["username", "profile_image"])
account_schema = UserSchema(only=["email"])

# 비밀번호
# 8자리 이상 36자리 이하
# 숫자, 알파벳 최소 1개씩 포함
password_validates = \
    validate.Regexp(
        re.compile(
            r"^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z*.!@$%^&(){}\[\]:;<>,.?/~_+-=|\\]{8,36}$"
        )
    )
username_validates = \
    [
        validate.Length(min=2, max=20),
        validate.Regexp(re.compile(r"^[가-힣\w]+$")),
    ]
email_validates = \
    [
        validate.Email(error="Email parameter is not email"),
        validate.Regexp(".*@dsm.hs.kr$", error="Email is not email of dsm"),
    ]


class UserPutInputSchema(ma.Schema):
    username = ma.Str(required=True, validate=username_validates)
    user_explain = ma.Str(required=True, validate=validate.Length(max=400))
    profile_image = ma.String(required=True, allow_none=True, validate=validate.Length(max=100))


class AccountRegisterSchema(ma.Schema):
    email = ma.Str(
        required=True,
        validate=email_validates
    )
    username = ma.Str(
        required=True,
        validate=username_validates
    )
    password = ma.Str(
        required=True,
        validate=password_validates
    )


class AccountLoginInputSchema(ma.Schema):
    password = ma.Str(required=True, validate=password_validates)
    email = ma.Str(required=True, validate=validate.Email())


class AccountChangePasswordInputSchema(ma.Schema):
    password = ma.Str(
        required=True,
        validate=password_validates
    )

    new_password = ma.Str(
        required=True,
        validate=password_validates
    )


class EmailVerificationCodePostSchema(ma.Schema):
    verification_code = ma.Str(data_key="verification-code", required=True)


class GetEmailDuplicationSchema(ma.Schema):
    email = ma.Str(required=True, validate=validate.Email())


class GetUsernameDuplicationSchema(ma.Schema):
    username = ma.Str(required=True, validate=validate.Length(min=2, max=20))


class DeleteUserSchema(ma.Schema):
    password = ma.Str(required=True, validate=validate.Length(min=8))
