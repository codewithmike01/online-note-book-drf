import dataclasses
import datetime
from rest_framework import exceptions
from users import services as user_services
from . import models

# To validate uuid passed in api
from uuid import UUID

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from note.models import Note
  from users.models import User



@dataclasses.dataclass
class NoteDataClass:
  title: str
  due_date: datetime.datetime
  content: str
  priority: int
  id: str = None
  created_at: datetime.datetime = None
  user: user_services.UserDataClass = None
  is_complete: bool = False

  @classmethod
  def from_instance(cls, note: 'Note') -> 'NoteDataClass':
    return cls(
      id = note.id,
      title = note.title,
      content = note.content,
      due_date = note.due_date,
      is_complete = note.is_complete,
      priority = note.priority,
      created_at = note.created_at,
      user = note.user
    )



####### Helper Function #######
def check_valid_uuid(id):
  try:
    UUID(id, version=4)

  except:
    raise exceptions.ValidationError('Id is not valid')



###### Api Essentials functions ########

def create_note(user, note_dc: 'NoteDataClass') -> 'NoteDataClass':
  instance = models.Note(
    title = note_dc.title,
    due_date = note_dc.due_date,
    content = note_dc.content,
    priority = note_dc.priority,
    user = user
  )

  instance.save()

  return NoteDataClass.from_instance(instance)


def get_user_notes(user: "User") -> list['NoteDataClass']:
  user_note = models.Note.objects.filter(user=user)

  return [NoteDataClass.from_instance(single_note) for single_note in user_note]


def get_notes() -> list['NoteDataClass']:
  notes = models.Note.objects.all()

  return [NoteDataClass.from_instance(single_note) for single_note in notes ]


def get_user_note(note_id: str) -> 'NoteDataClass':

  check_valid_uuid(note_id)

  note = models.Note.objects.filter(id = note_id).first()

  if  not note:
    raise exceptions.NotFound('Note Does not exist')

  return NoteDataClass.from_instance(note)




def delete_user_note(user: 'User', note_id: str) -> None:
  check_valid_uuid(note_id)

  note = models.Note.objects.filter(id = note_id).first()

  if  not note:
    raise exceptions.NotFound('Note Does not exist')

  if note.user.id != user.id:
    raise exceptions.PermissionDenied('Unauthorized')

  note.delete()



def update_user_note(user: "User", note_id: str, note_data: "NoteDataClass") -> 'NoteDataClass':
  check_valid_uuid(note_id)

  note = models.Note.objects.filter(id = note_id).first()

  if not note:
    raise exceptions.NotFound('Note Does not exist')

  if note.user.id != user.id:
    raise exceptions.PermissionDenied('Unauthorized')

  note.title = note_data.title
  note.content = note_data.content
  note.due_date = note_data.due_date
  note.priority = note_data.priority
  note.is_complete = note_data.is_complete

  note.save()

  return NoteDataClass.from_instance(note)
