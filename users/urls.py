from django.urls import path

from . import views as apis

urlpatterns = [
    path('register/', apis.RegisterApi.as_view() , name = 'register'),
    path('login/', apis.LoginApi.as_view(), name= 'login'),
    path('logout/', apis.LogoutApi.as_view(), name = 'logout'),
    path('me/', apis.UserApi.as_view(), name = 'me'),
    path('verify-email/', apis.VerifyEmailApi.as_view(), name = 'verify-email'),
]
