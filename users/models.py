from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# For creating user in Cli
class UserManager(BaseUserManager):
  def create_user(self, first_name: str, last_name:str, email: str, password: str, is_staff: bool = False, is_superuser: bool = False) -> "User":
    if not email:
      raise ValueError('User must have an email')
    if not first_name:
      raise ValueError('User must have First name')
    if not last_name:
      raise ValueError('User must have Last name')

    user = self.model(email= self.normalize_email(email))
    user.first_name = first_name
    user.last_name = last_name
    user.set_password(password)
    user.is_active = True
    user.is_staff = is_staff
    user.is_superuser = is_superuser

# save to db
    user.save()

    return user

  def create_superuser(self, first_name: str, last_name:str, email: str, password: str) -> "User":
    user = self.create_user(
      first_name= first_name,
      last_name= last_name,
      email = email,
      password= password,
      is_staff= True,
      is_superuser= True
    )

    user.save()

    return user


class User(AbstractUser):
  first_name = models.CharField(blank=False, null=False, max_length=250)
  last_name = models.CharField(blank=False, null=False, max_length=250)
  email = models.EmailField(blank=False, max_length=250, unique=True)
  password = models.CharField(max_length=255)
  username = None

  objects = UserManager()

  USERNAME_FIELD = 'email'


  REQUIRED_FIELDS = ["first_name", "last_name"]



  def __str__(self):
    return f"{self.email}"


