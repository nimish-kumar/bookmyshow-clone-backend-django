from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import UserManager


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(name="usr_email_idx", fields=["email"]),
            models.Index(name="usr_names_idx", fields=["first_name", "last_name"]),
        ]

    def __str__(self):
        return self.email
