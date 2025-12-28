from django.contrib.auth.models import AbstractUser
from django.db import models

# Özel kullanıcı modeli: Django'nun varsayılan User modelini genişletir
class User(AbstractUser):
    is_approved = models.BooleanField(default=False)  # Admin onayı (firma kullanıcıları için)
    is_company = models.BooleanField(default=False)   # Firma kullanıcısı mı? (True ise firma paneli erişimi var)