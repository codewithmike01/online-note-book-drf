import pytest
from rest_framework.test import APIClient
from users import services

# Allows to use http methods
client = APIClient()


@pytest.mark.django_db
def test_register_user():
    # Regitration details
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
    # Regitration details
    reg_payload = {
        "first_name": "Johnny",
        "last_name": "Gray",
        "email": "Royalcodemate@gmail.com",
        "password": "password",
    }

    # Register user
    client.post("/api/users/register/", reg_payload)

    # Login details
    login_payload = {"email": "royalcodemate@gmail.com", "password": "password"}

    # Login user
    login_response = client.post("/api/users/login/", login_payload).data

    assert login_response["message"] == "Successfully logged in"


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
    # Regitration details
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
