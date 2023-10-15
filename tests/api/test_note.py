import pytest

from note import services

from users import services as user_services

from rest_framework.test import APIClient

from note import models

import datetime

import time

import pytz

from django.utils import timezone

# initialize client
client = APIClient()


@pytest.mark.django_db
def test_note_create(user, auth_client):
    note_payload = {
        "title": "Fix bug",
        "content": "This is bug Fixed over here",
        "due_date": datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        "is_complete": False,
        "priority": 3,
    }

    note_response = auth_client.post("/api/notes/create/", note_payload).status_code

    assert note_response == 201


@pytest.mark.django_db
def test_note_get_user_note(user, auth_client):
    instance = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=False,
        priority=3,
        user_id=user.id,
    )

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=False,
        priority=3,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/create/")

    assert len(note_response.data) == 2
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_all(user, auth_client, note):
    note_response = auth_client.get("/api/notes/")

    assert len(note_response.data) == 1
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_get_by_id(user, note, auth_client):
    note_response = auth_client.get(f"/api/notes/note/{note.id}/")

    assert note_response.data["title"] == "Testing Fixer"
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_get_by_id_400(user, note, auth_client):
    note_response = auth_client.get(f"/api/notes/note/33/")

    assert note_response.status_code == 400


@pytest.mark.django_db
def test_note_get_by_id_delete(user, note, auth_client):
    note_response = auth_client.delete(f"/api/notes/note/{note.id}/")

    note_response.data["message"] == "Note deleted successfully"

    assert note_response.status_code == 204


@pytest.mark.django_db
def test_note_get_by_id_update(user, note, auth_client):
    note_response = auth_client.put(
        f"/api/notes/note/{note.id}/",
        {
            "title": "Host DRF",
            "content": "Host DRF onn AWS",
            "due_date": datetime.datetime(
                2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC
            ),
            "is_complete": True,
            "priority": 3,
        },
    ).data

    assert note_response["title"] == "Host DRF"
    assert note_response["is_complete"] == True
    assert note_response["due_date"] == "2023-09-23T20:45:37.127325Z"
    assert note_response["priority"] == 3


@pytest.mark.django_db
def test_note_unfinished(user, auth_client):
    instance = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=False,
        priority=3,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/unfinished/")

    assert len(note_response.data) == 1
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_finished(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/finished/")

    assert len(note_response.data) == 2
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_overdue(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=timezone.now() + datetime.timedelta(hours=24),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/overdue/")

    assert len(note_response.data) == 1
    assert note_response.status_code == 200
    assert note_response.data[len(note_response.data) - 1]["title"] == "Hot Fix"


@pytest.mark.django_db
def test_note_order_duedate_ascending(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=timezone.now() + datetime.timedelta(hours=24),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/order-duedate/asc/")

    assert note_response.data[0]["title"] == "Hot Fix"
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_order_duedate_descending(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=timezone.now() + datetime.timedelta(hours=24),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/order-duedate/desc/")

    assert note_response.data[0]["title"] == "Fix bug"
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_order_priority_ascending(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=9,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/order-priority/asc/")

    assert note_response.data[0]["title"] == "Hot Fix"
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_order_priority_descending(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=9,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/order-priority/desc/")

    assert note_response.data[0]["title"] == "Fix bug"
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_order_created_date_ascending(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    # To allow a significate difference in created at date for instance
    time.sleep(3)

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=9,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/order-created-at/asc/")

    assert note_response.data[0]["title"] == "Hot Fix"
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_order_created_date_descending(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    # To allow a significate difference in created at date for instance
    time.sleep(3)

    instance2 = models.Note.objects.create(
        title="Fix bug",
        content="This is bug Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=9,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/order-created-at/desc/")

    assert note_response.data[0]["title"] == "Fix bug"
    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_generate_csv(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/generate-csv/")

    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_generate_pdf(user, auth_client):
    instance = models.Note.objects.create(
        title="Hot Fix",
        content="Fixed over here",
        due_date=datetime.datetime(2023, 9, 23, 20, 45, 37, 127325, tzinfo=pytz.UTC),
        is_complete=True,
        priority=3,
        user_id=user.id,
    )

    note_response = auth_client.get("/api/notes/generate-pdf/")

    assert note_response.status_code == 200


@pytest.mark.django_db
def test_note_send_note_via_email(user, note, auth_client):
    note_response = auth_client.post("/api/notes/mail-notes/")

    assert note_response.data["message"] == "Note sent to mail Successfully!!"
    assert note_response.status_code == 200
