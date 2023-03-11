from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import Genders, Priorities, States


class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(
                name="genre_idx",
                fields=[
                    "name",
                ],
            )
        ]


# Create your models here.
class Facility(models.Model):
    name = models.CharField(max_length=255)
    priority = models.IntegerField(choices=Priorities.choices, default=Priorities.LO)

    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(
                name="facilities_name_idx",
                fields=[
                    "name",
                ],
            )
        ]
        verbose_name_plural = "Facilities"


ordering = ["-id"]


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["-id"]


class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.IntegerField(choices=States.choices)
    icon_url = models.URLField(
        verbose_name="Icon location",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = _("Cities")
        indexes = [models.Index(name="cities_idx", fields=["name"])]

    def __str__(self) -> str:
        return f"{self.name}"


class Artist(models.Model):
    name = models.CharField(max_length=255)
    gender = models.IntegerField(choices=Genders.choices)
    profile_pic_url = models.URLField(
        verbose_name=_("Profile pic location"),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.name}"


class Language(models.Model):
    from core.fields import get_upperfield

    UpperField = get_upperfield()
    lang_code = UpperField(
        max_length=2,
        unique=True,
        validators=[
            RegexValidator("^[A-Z]+$"),
        ],
    )
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"
