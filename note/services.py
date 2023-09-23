import dataclasses
import datetime
from users import services as user_services
from . import models

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from note.models import Note




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
