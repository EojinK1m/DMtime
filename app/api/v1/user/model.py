import re
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import validate

from app import bcrypt
from app import db, ma
from app import jwt

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    if identity in current_app.config['ADMIN_LIST']:
        print('admin')
        return {'roles': 'admin'}
    else:
        print('peasant')
        return {'roles': 'peasant'}


class UserModel(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(320), primary_key=True)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)

    username = db.Column(db.String(16), unique=True, nullable=False)
    explain = db.Column(db.Text, nullable=True)

    posts = db.relationship('PostModel', backref='uploader')
    profile_image = db.relationship('ImageModel', uselist=False)
    managing_gallery = db.relationship('GalleryModel', backref='manager')

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
        return self.email in current_app.config['ADMIN_LIST']

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
    profile_image = ma.Nested('ImageSchema', only=["url", "id"])
    email = ma.auto_field()


user_schema = UserSchema(exclude=['email'])
users_schema = UserSchema(many=True, only=['username', 'profile_image'])

account_schema = UserSchema(only = ['email'])


class UserPatchInputSchema(ma.Schema):
    username = ma.Str(required = False, validate = validate.Length(min = 2, max = 20))
    user_explain = ma.Str(required = False, validate = validate.Length(max = 400))
    profile_image_id = ma.Int(required = False, allow_null = True)


class UserPutInputSchema(ma.Schema):
    username = ma.Str(required = True, validate = validate.Length(min = 2, max = 20))
    user_explain = ma.Str(required = True, validate = validate.Length(max = 400))
    profile_image_id = ma.Int(required = False, allow_null = True)


class AccountRegisterSchema(ma.Schema):
    email = ma.Str(
        required = True,
        validate = [
            validate.Email(error='Email parameter is not email'),
            validate.Regexp('.*@dsm.hs.kr', error='Email is not of dsm')
        ]
    )
    username = ma.Str(
        required = True,
        validate = [
            validate.Length(min = 2, max = 20),
            validate.Regexp(re.compile('^[가-힣\w]+$'))
        ]
    )
    password = ma.Str(required = True, validate = validate.Length(min = 8))


class AccountLoginInputSchema(ma.Schema):
    password = ma.Str(required = True, validate = validate.Length(min = 8))
    email = ma.Str(required = True, validate = validate.Email())


class AccountChangePasswordInputSchema(ma.Schema):
    password = ma.Str(required = True, validate = validate.Length(min = 8))
    new_password = ma.Str(required = True, validate = validate.Length(min = 8))


class EmailVerificationCodePostSchema(ma.Schema):
    verification_code = ma.Str(data_key = 'verification-code', required = True)


class GetEmailDuplicationSchema(ma.Schema):
    email = ma.Str(required = True, validate = validate.Email())


class GetUsernameDuplicationSchema(ma.Schema):
    username = ma.Str(required = True, validate = validate.Length(min = 2, max = 20))


class DeleteUserSchema(ma.Schema):
    password = ma.Str(required = True, validate = validate.Length(min = 8))
