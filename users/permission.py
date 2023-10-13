from rest_framework.permissions import BasePermission, exceptions
from rest_framework import response, status
from . import serializers as user_serializer
from django.conf import settings
import jwt
from . import models


class CustomPermision(BasePermission):
    def has_permission(self, request, view):
        token = request.COOKIES.get("jwt")
        token_is_verified = False

        if not token:
            raise exceptions.AuthenticationFailed("Unauthorized")

        try:
            payload = jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"])
            token_is_verified = True

        except:
            return bool(False)

        # To get user details from db
        user_data = user_serializer.UserSerializer(request.user)

        # Return false when email is not verified
        if not user_data.data["is_email_verified"]:
            return bool(False)

        return bool(
            request.user and user_data.data["is_email_verified"] and token_is_verified
        )
