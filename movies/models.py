from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_fsm import FSMIntegerField

from .constants import BookingStatus

User = get_user_model()


class MovieFormat(models.Model):
    format = models.CharField(max_length=8, unique=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.format}"


class TrailerUrl(models.Model):
    movie = models.ForeignKey(
        "Movie",
        on_delete=models.CASCADE,
        related_name="movie_trailers",
    )
    trailer_url = models.URLField(max_length=250)

    class Meta:
        ordering = ["-id"]


class Movie(models.Model):
    cast = models.ManyToManyField(
        "meta.Artist", related_name="cast_movies", blank=True
    )
    crew = models.ManyToManyField(
        "meta.Artist", related_name="crew_movies", blank=True
    )
    name = models.CharField(max_length=255)
    is_released = models.BooleanField(default=False)
    genre = models.ManyToManyField("meta.Genre", related_name="genre_movies")
    release_date = models.DateField()
    format = models.ManyToManyField("MovieFormat", related_name="format_movies")
    description = models.TextField(null=True, blank=True)
    movie_length = models.DurationField(help_text="Movie length in hours")
    lang = models.ManyToManyField(
        "meta.Language",
        related_name="lang_movies",
    )
    subtitles_lang = models.ManyToManyField(
        "meta.Language",
        related_name="subtitle_lang_movies",
        blank=True,
    )
    poster_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.name}"


class Theatre(models.Model):
    name = models.CharField(max_length=255)
    postal_code = models.IntegerField(
        validators=[
            MaxValueValidator(855117),
            MinValueValidator(110001),
        ]
    )
    address = models.TextField()
    area_name = models.CharField(max_length=30)
    city = models.ForeignKey(
        "meta.City", on_delete=models.CASCADE, related_name="city_theatres"
    )
    facilities = models.ManyToManyField(
        "meta.Facility", related_name="facility_theatres"
    )
    coordinates = models.CharField(max_length=30, null=True, blank=True)
    location_link = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.name}"


class Screen(models.Model):
    screen_id = models.CharField(max_length=5)
    theatre = models.ForeignKey(
        "Theatre",
        on_delete=models.CASCADE,
        related_name="theatre_screen",
    )
    layout = models.TextField()

    class Meta:
        ordering = ["-id"]
        unique_together = ("screen_id", "theatre")
        indexes = [
            models.Index(
                name="screen_idx",
                fields=[
                    "screen_id",
                    "theatre",
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.theatre.name} --> {self.screen_id}"


class BookingSlot(models.Model):
    movie = models.ForeignKey(
        "Movie", on_delete=models.CASCADE, related_name="movie_slots"
    )
    is_fully_booked = models.BooleanField(default=False)
    screen = models.ForeignKey(
        "Screen", on_delete=models.CASCADE, related_name="screen_slots"
    )
    screening_datetime = models.DateTimeField()
    lang = models.ForeignKey(
        "meta.Language",
        on_delete=models.CASCADE,
        related_name="movie_lang_slots",
    )
    subtitles_lang = models.ForeignKey(
        "meta.Language",
        on_delete=models.CASCADE,
        related_name="subtitle_lang_slots",
        null=True,
        blank=True,
    )
    format = models.ForeignKey(
        "MovieFormat",
        on_delete=models.CASCADE,
        related_name="format_slot",
        null=True,
        blank=True,
    )
    current_layout = models.TextField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-id"]
        unique_together = [
            "movie",
            "screen",
            "screening_datetime",
        ]


class SlotGroup(models.Model):
    name = models.CharField(max_length=20)
    grp_code = models.CharField(max_length=2)
    cost = models.PositiveSmallIntegerField()
    slot = models.ForeignKey(
        "BookingSlot",
        on_delete=models.CASCADE,
        related_name="slotgrp_booking",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(name="slot_grp_idx", fields=["grp_code", "slot"])
        ]
        unique_together = ["grp_code", "slot"]


class Booking(models.Model):
    slot_grp = models.ForeignKey(
        "SlotGroup",
        on_delete=models.CASCADE,
        related_name="slot_grp",
        verbose_name="Theatre group",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_bookings",
        null=True,
        blank=True,
    )
    seat_number = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
        ]
    )
    status = FSMIntegerField(
        choices=BookingStatus.choices,
        default=BookingStatus.AVAILABLE,
        validators=[
            MinValueValidator(0),
        ],
    )
    row = models.CharField(max_length=3)
    column = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    booked_at = models.DateTimeField(null=True, blank=True)
    paid_amt = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        # Orders by bookings which have been recently added.
        ordering = ["-id"]
        unique_together = ["slot_grp", "row", "seat_number"]
        indexes = [
            models.Index(
                name="uniq_booking_idx",
                fields=["slot_grp", "row", "seat_number"],
            ),
            models.Index(name="booking_status_idx", fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"{self.slot_grp} -> {self.row}{self.seat_number}"
