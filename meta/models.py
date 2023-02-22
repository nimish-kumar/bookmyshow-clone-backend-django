from django.db import models

from .constants import Priority, States


# Create your models here.
class Facilities(models.Model):
    name = models.CharField(max_length=255)
    priority = models.IntegerField(choices=Priority, default=Priority.LO)

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


class Tags(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["-id"]


class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.IntegerField(choices=States.choices)
