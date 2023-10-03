from django.urls import path

from . import views as apis

urlpatterns = [
    path("create/", apis.NoteApi.as_view(), name="create note"),
    path("", apis.NotesApi.as_view(), name="all notes"),
    path("unfinished/", apis.UnfinishedNoteApi.as_view(), name="unfinished"),
    path("finished/", apis.FinishedNoteApi.as_view(), name="finished"),
    path("overdue/", apis.OverDueNoteApi.as_view(), name="overdue"),
    path("generate-csv/", apis.GenerateCSVApi.as_view(), name="Generate csv"),
    path("generate-pdf/", apis.GeneratePDFApi.as_view(), name="Generate pdf"),
    path(
        "order-duedate/<str:order_arg>/",
        apis.OrderNoteDueDateApi.as_view(),
        name="order-duedate",
    ),
    path(
        "order-priority/<str:order_arg>/",
        apis.OrderNotePriorityApi.as_view(),
        name="order-priority",
    ),
    path(
        "order-created-at/<str:order_arg>/",
        apis.OrderNoteCreatedAtApi.as_view(),
        name="order-created-at",
    ),
    path(
        "note/<str:note_id>/",
        apis.NoteRetreiveUpdateDelete.as_view(),
        name="Retreive update delete",
    ),
]
