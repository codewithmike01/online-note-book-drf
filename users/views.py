from django.shortcuts import render

from rest_framework import views, response, exceptions, status

from . import serializers as user_serializer
from . import services, authentication as auth_user, permission

# For email sending
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# password rerest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Swagger Spectacular
from drf_spectacular.utils import (
    extend_schema,
)


#  covert html to pdf
from django.template.loader import get_template


class RegisterApi(views.APIView):
    @extend_schema(request=user_serializer.UserSerializer())
    def post(self, request):
        serializer = user_serializer.UserSerializer(data=request.data)

        #  check validity

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user_data = services.check_user_email(data.email)

        if user_data:
            raise exceptions.NotAcceptable("Email already exist")

        try:
            serializer.instance = services.create_user(data)

            # Token (To auth user on registraion successful)
            token = services.create_token(serializer.data.get("id"))

            # Send verification email

            current_site = get_current_site(request).domain
            # relative_link = reverse(f"api/users/verify-email/{str(token)}")

            absolute_url = (
                "http://" + current_site + f"/api/users/verify-email/{str(token)}"
            )

            email_context = {
                "text_greeting": f'Hi {serializer.data.get("first_name")} {serializer.data.get("last_name")}',
                "text_content": " Please click on the button below to verify your email.",
                "link": absolute_url,
                "btn_text": "Proceed to verify email",
            }

            html_template = get_template("user_notice.html").render(email_context)

            data = {
                "subject": "Verify your email",
                "body": html_template,
                "user_email": serializer.data.get("email"),
            }

            services.send_email(data)
        except:
            services.delete_user(serializer.data.get("id"))
            raise exceptions.ErrorDetail("Error creating user")

        resp = response.Response()

        resp.data = serializer.data

        return resp


class LoginApi(views.APIView):
    # Swagger docs params

    @extend_schema(request=user_serializer.LoginSerializer())
    def post(self, request):
        serializer = user_serializer.LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user_data = services.check_user_email(data.email)

        if user_data is None:
            raise exceptions.AuthenticationFailed("Wrong credentials provided")

        if not user_data.check_password(raw_password=data.password):
            raise exceptions.AuthenticationFailed("Wrong credentials provided")

        # Token
        token = services.create_token(user_data.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserApi(views.APIView):
    """
    description: Endpoint to get current login user

    return: user: json
    """

    authentication_classes = (auth_user.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    @extend_schema(responses=user_serializer.UserSerializer)
    def get(self, request):
        user = request.user

        serializer = user_serializer.UserSerializer(user)

        return response.Response(data=serializer.data)


class LogoutApi(views.APIView):
    authentication_classes = (auth_user.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def post(self, request):
        res = response.Response()

        res.delete_cookie("jwt")
        res.data = {"message": "Logged out Successfully"}
        return res


class VerifyEmailApi(views.APIView):
    def post(self, request, token):
        # token = request.GET.get("token")

        print(token, "Token ")

        user_data = services.verify_email_auth(token)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        serializer = user_serializer.UserSerializer(user_data)

        resp.data = serializer.data

        return resp


class RequestPasswordReset(views.APIView):
    @extend_schema(request=user_serializer.EmailSerializer())
    def post(self, request):
        serializer = user_serializer.EmailSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user_data = services.check_user_email(data.get("email"))

        if not user_data:
            raise exceptions.NotFound("Email does not exist")

        # Encode user id
        uidb64 = urlsafe_base64_encode(force_bytes(user_data.id))

        token = PasswordResetTokenGenerator().make_token(user_data)

        current_site = get_current_site(request).domain

        relative_link = reverse("reset_password_confirm", args=(uidb64, token))

        absolute_url = "http://" + current_site + relative_link

        email_context = {
            "text_greeting": "Hi,",
            "text_content": "Please click on the button below to reset your password.",
            "link": absolute_url,
            "btn_text": "Proceed to reset password.",
        }

        html_template = get_template("user_notice.html").render(email_context)

        data = {
            "subject": "Reset your password",
            "body": html_template,
            "user_email": user_data.email,
        }

        services.send_email(data)

        return response.Response(data={"message": "Password reset link sent!!"})


class PasswordResetConfirmApi(views.APIView):
    @extend_schema(request=user_serializer.PasswordResetSerializer())
    def patch(self, request, token, uidb64, *args, **kwargs):
        serializer = user_serializer.PasswordResetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            user_id = urlsafe_base64_decode(uidb64).decode()

        except:
            raise exceptions.AuthenticationFailed("Unauthorized")

        user_dc, user = services.check_password_token(user_id, token)

        user.set_password(data.get("password"))

        user.save()

        user_data = user_serializer.UserSerializer(user_dc)

        return response.Response(data=user_data.data, status=status.HTTP_200_OK)
