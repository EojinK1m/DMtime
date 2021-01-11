import re
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token

from app import bcrypt
from app import db, ma
from app import jwt


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


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel()


    username = ma.auto_field()
    explain = ma.auto_field()
    profile_image = ma.Nested('ImageSchema', only=["url", "id"])


user_schema = UserSchema()
users_schema = UserSchema(many=True, only=['username', 'profile_image'])

from marshmallow import validate

class UserPatchInputSchema(ma.Schema):
    username = ma.Str(required = False, validate = validate.Length(min = 2, max = 20))
    user_explain = ma.Str(required = False, validate = validate.Length(max = 400))
    profile_image_id = ma.Int(required = False, allow_null = True)

class UserPutInputSchema(ma.Schema):
    username = ma.Str(required = True, validate = validate.Length(min = 2, max = 20))
    user_explain = ma.Str(required = True, validate = validate.Length(max = 400))
    profile_image_id = ma.Int(required = False, allow_null = True)