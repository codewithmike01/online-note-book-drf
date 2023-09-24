from django.shortcuts import render

from rest_framework import views, response, exceptions, status

from . import serializers as user_serializer
from . import services, authentication as auth_user, permission

# For email sending
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# password rerest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import  force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


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

    # Send verification email

    current_site = get_current_site(request).domain
    relative_link = reverse('verify-email')


    absolute_url = 'http://' + current_site + relative_link+"?token="+str(token)

    email_body = f'Hi {serializer.data.get("first_name")} {serializer.data.get("last_name")}, Please use the link below to verify your email. \n {absolute_url} '

    data = {"subject": "Verify your email", "body": email_body , "user_email": serializer.data.get("email") }

    services.send_email(data)

    resp = response.Response()

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

  authentication_classes = (auth_user.CustomUserAuthentication, )
  permission_classes = (permission.CustomPermision, )



  def get(self, request):
    user = request.user

    serializer = user_serializer.UserSerializer(user)

    return response.Response(data = serializer.data)



class LogoutApi(views.APIView):
  authentication_classes = (auth_user.CustomUserAuthentication, )
  permission_classes = (permission.CustomPermision, )

  def post(self, request):

    res = response.Response()

    res.delete_cookie('jwt')
    res.data = {"message": "Logged out Successfully"}
    return res



  # Verify User Email
  #
class VerifyEmailApi(views.APIView):
    def post(self, request):
      token = request.GET.get('token')

      user_data = services.verify_email_auth(token)

      resp = response.Response()

      resp.set_cookie(key='jwt', value=token, httponly=True)

      serializer = user_serializer.UserSerializer(user_data)

      resp.data = serializer.data

      return resp


class RequestPasswordReset(views.APIView):
  def post(self, request):
    serializer = user_serializer.EmailSerializer(data = request.data)

    serializer.is_valid(raise_exception= True)

    data = serializer.validated_data

    user_data = services.check_user_email(data.get("email"))

    if not  user_data:
      raise exceptions.NotFound('Email does not exist')

    # Encode user id
    uidb64 = urlsafe_base64_encode(force_bytes(user_data.id))

    token = PasswordResetTokenGenerator().make_token(user_data)

    current_site = get_current_site(request).domain

    relative_link = reverse('reset_password_confirm', args=( uidb64,  token))

    absolute_url = 'http://' + current_site + relative_link

    email_body = f'Hi,  \n Please use the link below to reset your password. \n {absolute_url} '

    data = {"subject": "Reset your password", "body": email_body , "user_email": user_data.email }

    services.send_email(data)

    return response.Response(data = {"message": "Password reset link sent!!"})



class PasswordResetConfirmApi(views.APIView):

  def patch(self, request, *args, **kwargs):
    serializer = user_serializer.PasswordResetSerializer(data = request.data)

    serializer.is_valid(raise_exception= True)

    data = serializer.validated_data

    print(data.get('token'), 'DATA')

    try:
      user_id = urlsafe_base64_decode(data.get("uidb64")).decode()

    except:
      raise exceptions.AuthenticationFailed('Unauthorized ggHrt')

    user_dc, user  = services.check_password_token(user_id, data.get("token"))

    user.set_password(data.get('password'))

    user.save()

    user_data = user_serializer.UserSerializer(user_dc)


    return response.Response(data = user_data.data , status=status.HTTP_200_OK)












