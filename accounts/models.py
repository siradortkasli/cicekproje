from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_approved = models.BooleanField(default=False)  # Admin onaylayınca aktif olacak
    is_company = models.BooleanField(default=False)   #firma onay