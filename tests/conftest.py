import pytest

from users import services as user_services, serializers as user_serializer
from note import services as note_services, models

from rest_framework.test import APIClient

client = APIClient()


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


@pytest.fixture
def auth_client(user):
    # Generate email verification token
    token = user_services.create_token(user.id)

    client.post(f"/api/users/verify-email/{token}")

    return client


@pytest.fixture
def note(user):
    instance = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date="2023-09-23 20:45:37.013440",
        is_complete=False,
        priority=3,
        user_id=user.id,
    )

    return instance
