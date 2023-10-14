import pytest
from rest_framework.test import APIClient
from users import services

# password rerest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


# Allows to use http methods
client = APIClient()


@pytest.mark.django_db
def test_register_user():
    # Registration details
    reg_payload = {
        "first_name": "Johnny",
        "last_name": "Gray",
        "email": "Royalcodemate@gmail.com",
        "password": "password",
    }

    # Register user
    reg_response = client.post("/api/users/register/", reg_payload).data

    assert reg_response["first_name"] == reg_payload["first_name"]
    assert reg_response["last_name"] == reg_payload["last_name"]
    assert reg_response["email"] == reg_payload["email"]
    assert reg_response["is_email_verified"] == False
    assert "password" not in reg_response
    assert "id" in reg_response


@pytest.mark.django_db
def test_user_login():
    # Registration details
    reg_payload = {
        "first_name": "Johnny",
        "last_name": "Gray",
        "email": "Royalcodemate@gmail.com",
        "password": "password",
    }

    # Register user
    client.post("/api/users/register/", reg_payload)

    # ====  Correct credentails can login ====

    # Login details
    correct_login_payload = {"email": "royalcodemate@gmail.com", "password": "password"}

    # Login user
    correct_login_response = client.post(
        "/api/users/login/", correct_login_payload
    ).data

    assert correct_login_response["message"] == "Successfully logged in"


@pytest.mark.django_db
def test_fail_user_login():
    # Registration details
    reg_payload = {
        "first_name": "Johnny",
        "last_name": "Gray",
        "email": "Royalcodemate@gmail.com",
        "password": "password",
    }

    # Register user
    client.post("/api/users/register/", reg_payload)

    # ====  Wrong credentails can not login ====

    # Login details
    wrong_login_payload = {"email": "royalcodemate@gmail.com", "password": "wrong"}

    # Login user
    wrong_login_response = client.post("/api/users/login/", wrong_login_payload).data

    assert wrong_login_response["message"] == "Wrong credentials provided"


@pytest.mark.django_db
def test_user_logout():
    # Login details
    login_payload = {"email": "royalcodemate@gmail.com", "password": "password"}

    # Login user
    client.post("/api/users/login/", login_payload)

    # Logout user
    logout_response = client.post("/api/users/logout/").data

    assert logout_response["message"] == "Logged out Successfully"


@pytest.mark.django_db
def test_user_get_current_user():
    # Registration details
    reg_payload = {
        "first_name": "Johnny",
        "last_name": "Gray",
        "email": "Royalcodemate@gmail.com",
        "password": "password",
    }

    # Register user
    reg_response = client.post("/api/users/register/", reg_payload).data

    # Generate email verification token
    token = services.create_token(reg_response["id"])

    # Verify user email
    client.post(f"/api/users/verify-email/{token}")

    # Get current user
    cur_user_response = client.get("/api/users/me/").data

    assert cur_user_response["first_name"] == reg_payload["first_name"]
    assert cur_user_response["last_name"] == reg_payload["last_name"]
    assert cur_user_response["email"] == reg_payload["email"]
    assert cur_user_response["is_email_verified"] == True
    assert "password" not in cur_user_response
    assert "id" in cur_user_response


@pytest.mark.django_db
def test_user_verify_email():
    # Registration details
    reg_payload = {
        "first_name": "Johnny",
        "last_name": "Gray",
        "email": "newuser1@gmail.com",
        "password": "password",
    }

    # Register user
    reg_response = client.post("/api/users/register/", reg_payload).data

    # Generate email verification token
    token = services.create_token(reg_response["id"])

    # Verify user email
    verify_response = client.post(f"/api/users/verify-email/{token}").status_code

    assert verify_response == 200


@pytest.mark.django_db
def test_user_req_password_email_reset():
    # Registration details
    reg_payload = {
        "first_name": "Johnny",
        "last_name": "Gray",
        "email": "royalcodemate@gmail.com",
        "password": "password",
    }

    # Register user
    reg_response = client.post("/api/users/register/", reg_payload).data

    # Generate email verification token
    token = services.create_token(reg_response["id"])

    # Verify user email
    client.post(f"/api/users/verify-email/{token}")

    password_reset_response = client.post(
        f"/api/users/request-password-reset/", {"email": "Royalcodemate@gmail.com"}
    ).data

    assert password_reset_response["message"] == "Password reset link sent!!"


@pytest.mark.django_db
def test_user_confirm_password_email_reset():
    # Registration details
    reg_payload = {
        "first_name": "Frank",
        "last_name": "Gray",
        "email": "newuser2@gmail.com",
        "password": "password",
    }

    # Register user
    reg_response = client.post("/api/users/register/", reg_payload).data

    # Generate email verification token
    token = services.create_token(reg_response["id"])

    # Verify user email
    client.post(f"/api/users/verify-email/{token}")

    # Get user details from table
    user_data = services.check_user_email(reg_response["email"])

    # Encode user id
    uidb64 = urlsafe_base64_encode(force_bytes(user_data.id))

    # Generate password reset token
    password_token = PasswordResetTokenGenerator().make_token(user_data)

    # Confirm password reset with new password
    password_confirm_response = client.patch(
        f"/api/users/reset_password_confirm/{uidb64}/{password_token}/",
        {"password": "smartpass"},
    ).data

    assert password_confirm_response["first_name"] == reg_payload["first_name"]
    assert password_confirm_response["first_name"] == reg_payload["first_name"]
    assert password_confirm_response["last_name"] == reg_payload["last_name"]
    assert password_confirm_response["email"] == reg_payload["email"]
    assert password_confirm_response["is_email_verified"] == True
    assert "password" not in password_confirm_response
    assert "id" in password_confirm_response


@pytest.mark.django_db
def test_user_fail_confirm_password_email_reset():
    # fail  password reset with wrong credentails
    password_confirm_response = client.patch(
        f"/api/users/reset_password_confirm/wrong66/wrongpa4444/",
        {"password": "smartpass"},
    ).status_code

    password_confirm_response == 401
