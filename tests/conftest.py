import pytest

from users import services as user_services, serializers as user_serializer
from note import models

from rest_framework.test import APIClient

import datetime
import pytz

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
        title="Testing Fixer",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=False,
        priority=3,
        user_id=user.id,
    )

    return instance
