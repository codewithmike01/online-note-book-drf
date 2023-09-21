from django.shortcuts import render

from rest_framework import views, response, exceptions, permissions

from . import serializers as user_serializer
from . import services

class RegisterApi(views.APIView):

  def post(self,request):
    serializer = user_serializer.UserSerializer(data = request.data)

    #  check validity

    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    serializer.instance = services.create_user(data)




    return response.Response(data = serializer.data)


class LoginApi(views.APIView):
  def post(self , request):
    email = request.data['email']
    password = request.data['password']

    user_data = services.check_user_email(email)

    if  user_data  is None:
      raise exceptions.AuthenticationFailed('Wrong credentials provided')

    if not user_data.check_password(raw_password= password):
      raise exceptions.AuthenticationFailed('Wrong credentials provided')



    # Token
    token = services.create_token(user_data.id)


    resp = response.Response()

    resp.set_cookie(key='jwt', value=token, httponly=True)

    return resp



