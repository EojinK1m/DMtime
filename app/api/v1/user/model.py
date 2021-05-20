import re
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import validate

from app.extentions import bcrypt
from app.extentions import db, ma
from app.extentions import jwt


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    if identity in current_app.config["ADMIN_LIST"]:
        return {"roles": "admin"}
    else:
        return {"roles": "peasant"}


class UserModel(db.Model):
    __tablename__ = "user"

    email = db.Column(db.String(320), primary_key=True)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)

    username = db.Column(db.String(16), unique=True, nullable=False)
    explain = db.Column(db.Text, nullable=True)

    posts = db.relationship("PostModel", backref="uploader")
    profile_image = db.relationship("ImageModel", uselist=False)
    managing_gallery = db.relationship("GalleryModel", backref="manager")
    comments = db.relationship("CommentModel", backref="writer")

    @property
    def id(self):
        return self.email

    @id.setter
    def id(self, email):
        self.email = email

    def delete_user(self):
        db.session.delete(self)

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password)

    def generate_access_token(self, expire=None):
        return create_access_token(identity=self.email, expires_delta=expire)

    def generate_refresh_token(self, expire=None):
        return create_refresh_token(identity=self.email, expires_delta=expire)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def delete_account(self):
        db.session.delete(self)

    def is_admin(self):
        return self.email in current_app.config["ADMIN_LIST"]

    @staticmethod
    def get_user_by_email(email):
        user = UserModel.get_user_by_email(email)
        if not user:
            return None
        else:
            return user

    @staticmethod
    def get_user_by_email(email):
        return UserModel.query.filter_by(email=email).first()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel()

    username = ma.auto_field()
    explain = ma.auto_field()
    # profile_image = ma.Nested("ImageSchema", only=["url", "filename"])
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
