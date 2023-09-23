from django.shortcuts import render
from rest_framework import response, exceptions, views, status as rest_status
from users import permission,  authentication as user_auth
from . import  serializers as note_serializer

from . import services

# Create and Get user notes
class NoteApi(views.APIView):

  authentication_classes = (user_auth.CustomUserAuthentication, )
  permission_classes = (permission.CustomPermision, )

  def post(self, request):
    serializer = note_serializer.NoteSeralizer(data = request.data)

    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    # create note
    serializer.instance = services.create_note(request.user, data)

    return response.Response(data= serializer.data)

  def get(self, request):

    user_note_collection = services.get_user_notes(request.user)

    serializer  = note_serializer.NoteSeralizer(user_note_collection, many=True)


    return response.Response(data = serializer.data)


# Get all notes
class NotesApi(views.APIView):
  authentication_classes = (user_auth.CustomUserAuthentication, )
  permission_classes = (permission.CustomPermision, )

  def get(self, request):

    note_collection = services.get_notes()


    serializer =  note_serializer.NoteSeralizer(note_collection, many=True)

    return response.Response(data = serializer.data)



class NoteRetreiveUpdateDelete(views.APIView):
  authentication_classes = (user_auth.CustomUserAuthentication, )
  permission_classes = (permission.CustomPermision, )

  def get(self, request, note_id):

    note = services.get_user_note(note_id)

    serializer = note_serializer.NoteSeralizer(note)

    return response.Response(data = serializer.data)

  def delete(self, request, note_id):
    services.delete_user_note(request.user, note_id)

    return response.Response(status= rest_status.HTTP_204_NO_CONTENT)


  def put(self, request, note_id):

    serializer = note_serializer.NoteSeralizer(data = request.data)
    serializer.is_valid(raise_exception=True)

    note_data = serializer.validated_data

    serializer.instance = services.update_user_note(request.user, note_id, note_data)

    return response.Response(data = serializer.data)




