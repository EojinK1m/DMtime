from app import ma
from marshmallow import validate, ValidationError


class PostTokenValidateSchema(ma.Schema):
    @staticmethod
    def check_is_school_email(email):
        email_domain = email.rsplit("@")[-1]

        if not email_domain == "dsm.hs.kr":
            raise ValidationError("Email is not email of DSM.")

    password = ma.Str(required=True, validate=validate.Length(min=8))
    email = ma.Str(
        required=True, validate=[validate.Email(), check_is_school_email.__func__]
    )


class PostEmailVerificationCodeSchema(ma.Schema):
    verification_code = ma.Str(data_key="verification-code", required=True)
