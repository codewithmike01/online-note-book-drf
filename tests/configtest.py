import pytest

from users import services as user_services

from rest_framework.test import APIClient


@pytest.fixture
def user():
    user_dc = user_services(
        first_name="Johnny",
        last_name="Gray",
        email="Royalcodemate@gmail.com",
        password="password",
    )

    user = user_services.create_user(user_dc)

    return user


@pytest.fixture
def client():
    return APIClient()
