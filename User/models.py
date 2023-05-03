from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=120, null=False)
    password = models.CharField(max_length=120, null=False)
    is_employee = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
