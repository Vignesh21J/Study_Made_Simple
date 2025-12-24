from django.db import models

from django.contrib.auth.models import AbstractUser

from .managers import UserManager


import uuid

def default_name():
    return f"user_{uuid.uuid4().hex[:8]}"

# Create your models here.

class User(AbstractUser):
    username = None
    name = models.CharField(max_length=20, default=default_name, blank=True)
    email = models.EmailField(max_length=60, unique=True)
    bio = models.TextField(null=True)

    # avatar = models.ImageField(upload_to='avatars', default='static/images/avatar.svg', null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()