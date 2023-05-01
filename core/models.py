from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import UserManager


# Create your models here.
class User(AbstractUser):
    class ReviewerType(models.IntegerChoices):
        user = 0, _("user")
        critic = 1, _("critic")

    username = None
    email = models.EmailField(_("email address"), unique=True)
    reviewer_type = models.PositiveSmallIntegerField(
        choices=ReviewerType.choices,
        default=ReviewerType.user,
    )
    profile_image_url = models.URLField(blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(name="usr_email_idx", fields=["email"]),
            models.Index(
                name="usr_names_idx", fields=["first_name", "last_name"]
            ),
        ]

    def __str__(self):
        return self.email


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_movie_reviews"
    )
    created_at = models.DateTimeField(auto_created=True)
    review = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
