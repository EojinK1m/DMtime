from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token

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


class AccountModel(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)


    user = db.relationship('UserModel', uselist=False, backref='account')


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

    @staticmethod
    def get_user_by_email(email):
        account = AccountModel.get_account_by_email(email)
        if not account:
            return None
        else:
            return account.user

    @staticmethod
    def get_account_by_email(email):
        return AccountModel.query.filter_by(email=email).first()

from app.api.user.model import UserSchema

class AccountSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AccountModel
    user = ma.Nested(UserSchema)
    email = ma.auto_field()

account_schema = AccountSchema()
accounts_schema =  AccountSchema(many=True)


from marshmallow import validate
class AccountInputSchema(ma.Schema):
    email = ma.Str(required = True, validate = validate.Email())
    username = ma.Str(required = True, validate = validate.Length(min = 2, max = 20))
    password = ma.Str(required = True, validate = validate.Length(min = 8))
    

class AccountLoginInputSchema(ma.Schema):
    password = ma.Str(required = True, validate = validate.Length(min = 8))
    email = ma.Str(required = True, validate = validate.Email())

class AccountChangePasswrodInputSchema(ma.Schema):
    password = ma.Str(required = True, validate = validate.Length(min = 8))
    new_password = ma.Str(required = True, validate = validate.Length(min = 8))