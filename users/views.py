from django.shortcuts import render



from rest_framework import views, response, exceptions, permissions

from . import serializers as user_serializer
from . import services, authencation, permission


class RegisterApi(views.APIView):

  def post(self,request):
    serializer = user_serializer.UserSerializer(data = request.data)

    #  check validity

    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    user_data = services.check_user_email(data.email)

    if user_data:
      raise exceptions.NotAcceptable('Email already exist')

    serializer.instance = services.create_user(data)

    # Token (To auth user on registraion successful)
    token = services.create_token(serializer.data.get("id"))

    resp = response.Response()

    resp.set_cookie(key='jwt', value=token, httponly=True)

    resp.data = serializer.data

    return resp


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



class UserApi(views.APIView):
  """
  description: Endpoint to get current login user

  return: user: json
  """

  authentication_classes = (authencation.CustomUserAuthentication, )
  permission_classes = (permission.CustomPermision, )



  def get(self, request):
    user = request.user

    serializer = user_serializer.UserSerializer(user)

    return response.Response(data = serializer.data)



class LogoutApi(views.APIView):
  authentication_classes = (authencation.CustomUserAuthentication, )
  permission_classes = (permission.CustomPermision, )

  def post(self, request):

    res = response.Response()

    res.delete_cookie('jwt')
    res.data = {"message": "Logged out Successfully"}
    return res




