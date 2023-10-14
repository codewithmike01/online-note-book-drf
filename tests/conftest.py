import pytest

from users import services as user_services


@pytest.fixture
def user():
    user_dc = user_services.UserDataClass(
        first_name="Johnny",
        last_name="Gray",
        email="royalcodemate@gmail.com",
        password="password",
    )

    user = user_services.create_user(user_dc)

    return user
