import dataclasses
from . import models
from rest_framework import exceptions

# Email
from django.core.mail import EmailMessage

# For jwt
import datetime
import jwt

# setting
from django.conf import settings

# Generated password token
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# For type checking of model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User


@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    is_email_verified: bool = None
    password: str = None
    id: str = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_email_verified=user.is_email_verified,
            id=user.id,
        )


@dataclasses.dataclass
class PasswordDataClass:
    email: str
    password: str

    @classmethod
    def from_instance(cls, user: "User") -> "PasswordDataClass":
        return cls(
            email=user.email,
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    instance = models.User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email,
    )

    if user_dc.password is not None:
        instance.set_password(user_dc.password)

    instance.save()

    return UserDataClass.from_instance(instance)


def check_user_email(email: str) -> "User":
    user_email = models.User.objects.filter(email=email).first()

    return user_email


def create_token(user_id: str) -> str:
    payload = {
        "id": str(user_id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.JWT_KEY, algorithm="HS256")

    return token


def send_email(data: dict) -> None:
    email = EmailMessage(
        subject=data.get("subject"),
        body=data.get("body"),
        from_email=settings.EMAIL_HOST_USER,
        to=[data.get("user_email")],
    )

    try:
        email.send()
    except:
        raise exceptions.ErrorDetail("Email not sent")


def verify_email_auth(token) -> "UserDataClass":
    if not token:
        raise exceptions.AuthenticationFailed("Unauthorized")

    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"])

        user = models.User.objects.filter(id=payload.get("id")).first()

        user.is_email_verified = True

        user.save()

        return UserDataClass.from_instance(user)

    except:
        raise exceptions.AuthenticationFailed("Unauthorized")


def check_password_token(user_id: bytes, token: bytes) -> "User":
    user = models.User.objects.get(id=user_id)

    #  Check if token is correct
    if not PasswordResetTokenGenerator().check_token(user, token):
        raise exceptions.AuthenticationFailed("Token not valid")

    return (UserDataClass.from_instance(user), user)


def delete_user(user_id: str) -> None:
    user = models.User.objects.filter(id=user_id).first()
    user.delete()
