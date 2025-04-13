from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_staff_user = models.BooleanField(default=False, help_text="Designates whether the user is staff (non-admin).")
