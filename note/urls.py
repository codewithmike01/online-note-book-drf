from django.urls import path

from . import views as apis

urlpatterns = [
    path("create/", apis.NoteApi.as_view(), name="create note"),
    path("", apis.NotesApi.as_view(), name="all notes"),
    path("unfinished/", apis.UnfinishedNote.as_view(), name="unfinished"),
    path("finished/", apis.FinishedNote.as_view(), name="finished"),
    path(
        "<str:note_id>/",
        apis.NoteRetreiveUpdateDelete.as_view(),
        name="Retreive update delete",
    ),
]
