import json
from smtplib import SMTPException
from functools import wraps

from flask import abort, current_app
from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request,
)

import pickle

from app.extensions import db, redis_client, email_sender
from app.util import random_string_generator

from app.api.v1.user.model import UserModel
from app.api.v1.image.service import ImageService

from .repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    @staticmethod
    def get_user_by_username(username):
        find_user = UserModel.query.filter_by(username=username).first()
        if find_user is None:
            abort(404, "User not found")

        return find_user

    @staticmethod
    def get_user_by_username_or_none(username):
        return UserModel.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email_or_404(email):
        find_user = UserModel.query.filter_by(email=email).first()
        if find_user is None:
            abort(404, "User not found")

        return find_user

    @staticmethod
    def get_user_by_email_or_none(email):
        return UserModel.query.filter_by(email=email).first()

    def update_user(
        self, username, new_username, explain, profile_image
    ):
        user = self.user_repository.get_user_by_username(username)
        image = ImageService.get_image_by_id(profile_image) if profile_image else None

        self.update_username(user, new_username)
        self.update_profile_image(user, image)
        user.explain = explain

        self.user_repository.add(user)
        return user

    @classmethod
    def update_username(cls, user, new_username):
        if new_username != user.username:
            AccountService().abort_409_if_username_is_using(new_username)
            user.username = new_username

    @classmethod
    def update_profile_image(cls, user, image):
        if user.profile_image != image:
            user.profile_image = image

    @staticmethod
    def delete_user(user):
        profile_image = user.profile_image

        if profile_image:
            ImageService.delete_image(profile_image.id)
        user.delete_user()

    @staticmethod
    def user_access_authorize_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_to_work = UserService.get_user_by_username(kwargs["username"])
            request_user = UserService.get_user_by_email_or_none(
                email=get_jwt_identity()
            )

            if not user_to_work == request_user:
                abort(
                    403, f"access denied, you are not {user_to_work.username}"
                )

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def raise_401_if_not_password_verified(user, password):
        if not user.verify_password(password):
            abort(401, "password not match")


class AccountService:

    def __init__(self):
        self.user_repository: UserRepository = UserRepository()
        self.random_string_generator = random_string_generator

    def register_user_temporarily(self, email: str, password: str, username: str):
        new_user = self.create_user(email, password, username)
        verification_code = self.generate_verification_code()

        self.store_user_temporarily_with_verification_code(new_user, verification_code)
        self.send_verification_code_by_email(verification_code, email)

    def create_user(self, email, password, username):
        self.abort_409_if_email_is_using(email)
        self.abort_409_if_username_is_using(username)

        return UserModel(
            email=email,
            password=password,
            username=username
        )

    def abort_409_if_username_is_using(self, username):
        if self.user_repository.get_user_by_username(username) is not None:
            abort(409)

    def abort_409_if_email_is_using(self, email):
        if self.user_repository.get_user_by_email(email) is not None:
            abort(409)

    def generate_verification_code(self):
        while True:
            temp_code = (
                random_string_generator.generate_verification_code()
            )

            if not (redis_client.exists(temp_code)):
                return temp_code

    def store_user_temporarily_with_verification_code(self, user, verification_code):
        with redis_client.pipeline() as pipe:
            pipe.mset({verification_code: pickle.dumps(user)})
            pipe.expire(
                verification_code, current_app.config["EMAIL_VERIFY_DEADLINE"]
            )
            pipe.execute()

    def send_verification_code_by_email(self, verification_code, email):
        mail_title = "[대마타임] 회원가입 인증 코드입니다."
        mail = email_sender.make_mail(
            subject=mail_title, message=verification_code
        )

        try:
            email_sender.send_mail(to_email=email, message=mail)
        except SMTPException:
            abort(
                500, "An error occurred while send e-mail, plz try again later"
            )

    @staticmethod
    def validate_verification_code(code):
        if not (random_string_generator.validate_verification_code(code)):
            raise abort(400)

    @staticmethod
    def find_register_data_by_verification_code(verification_code):
        AccountService.validate_verification_code(verification_code)
        register_data = redis_client.get(verification_code)

        if register_data is None:
            abort(404, "Verification code not found.")

        return json.loads(register_data.decode("utf-8"))

    @staticmethod
    def change_account_password(user, password):
        user.password_hash = user.hash_password(password)

    @staticmethod
    def find_user_by_email(email):
        found_account = UserModel.get_user_by_email(email)

        if found_account is None:
            abort(
                404,
                "Account not found, there is no account include the email.",
            )

        return found_account

