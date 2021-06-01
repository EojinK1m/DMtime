from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token\

from app.extensions import bcrypt, db, jwt


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

    def __init__(
            self,
            email,
            password,
            username,
            explain=""
    ):
        kwargs = {
            "email": email,
            "password_hash": bcrypt.generate_password_hash(password),
            "username": username,
            "explain": explain
        }
        
        self.read_posts = set()

        super().__init__(**kwargs)

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
