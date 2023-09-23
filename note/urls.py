from django.urls import path

from . import views as apis

urlpatterns = [
    path('create/', apis.NoteApi.as_view() , name = 'create note'),
]
