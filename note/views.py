from django.shortcuts import render
from rest_framework import response, exceptions, views, permissions
from users import permission,  authentication as user_auth
from . import  serializers as note_serializer

from . import services

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
    return response.Response(data ='Get note')

