from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=120, null=False)
    password = models.CharField(max_length=120, null=False)
    is_employee = models.BooleanField(default=False)
    is_banned = models.DateField(null=True)
