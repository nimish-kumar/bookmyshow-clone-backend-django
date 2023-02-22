from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_fsm import FSMIntegerField, transition

from .constants import BookingStatus

User = get_user_model()


class MovieFormat(models.Model):
    format = models.CharField(max_length=5)

    class Meta:
        ordering = ["-id"]


class TrailerUrl(models.Model):
    movie = models.ForeignKey(
        "Movies",
        on_delete=models.CASCADE,
        related_name="movie_trailers",
    )
    trailer_url = models.URLField(max_length=250)

    class Meta:
        ordering = ["-id"]


# Create your models here.
class Movie(models.Model):
    cast = models.ManyToManyField("meta.Artist", related_name="cast_movies")
    crew = models.ManyToManyField("meta.Artist", related_name="crew_movies")
    name = models.CharField(max_length=255)
    is_released = models.BooleanField(default=False)
    genre = models.ManyToManyField("meta.Genre", related_name="genre_movies")
    release_date = models.DateField()
    format = models.ManyToManyField("MovieFormat", related_name="format_movies")
    descriptiom = models.TextField(null=True, blank=True)
    movie_length = models.DecimalField(help_text="Movie length in hours")
    lang = models.ManyToManyField(
        "meta.Language",
        related_name="lang_movies",
    )
    subtitles_lang = models.ManyToManyField(
        "meta.Language",
        related_name="subtitle_lang_movies",
    )


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
    details = models.TextField()
    facilities = models.ManyToManyField(
        "meta.Facility", related_name="faicility_theatres"
    )
    coordinates = models.CharField(max_length=30, null=True, blank=True)
    location_link = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]


class Screen(models.Model):
    screen_id = models.CharField(max_length=5)
    theatre = models.ForeignKey(
        "Theatre",
        on_delete=models.CASCADE,
        related_name="theatre_screen",
    )

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


class BookingSlot(models.Model):
    movie = models.ForeignKey(
        "Movie", on_delete=models.CASCADE, related_name="movie_slots"
    )
    is_fully_booked = models.BooleanField(default=False)
    screen = models.ForeignKey(
        "Screen", on_delete=models.CASCADE, related_name="screen_slots"
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    lang = models.ForeignKey(
        "meta.Language",
        on_delete=models.CASCADE,
        related_name="movie_lang_slots",
    )
    subtitles_lang = models.ForeignKey(
        "meta.Language",
        on_delete=models.CASCADE,
        related_name="subtitle_lang_slots",
    )
    layout = models.TextField()


class Booking(models.Model):
    slot = models.ForeignKey(
        "BookingSlot",
        on_delete=models.CASCADE,
        related_name="slot_bookings",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_bookings",
    )
    seat_number = models.SmallIntegerField(validators=MinValueValidator(0))
    grp_row_head = models.CharField(max_length=2)
    status = FSMIntegerField(
        state_choices=BookingStatus.choices,
        default=BookingStatus.AVAILABLE,
        validators=[
            MinValueValidator(0),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["slot", "seat_number", "grp_row_head"]
        indexes = [
            models.Index(
                "uniq_booking_idx",
                fields=["slot", "seat_number", "grp_row_head"],
            ),
            models.Index("booking_status_idx", fields=["status"]),
        ]

    def get_seat_number(self):
        return f"{self.grp_row_head}{self.seat_number}"

    @transition(
        source=BookingStatus.ERROR,
        target=BookingStatus.AVAILABLE,
    )
    def fallback(self):
        pass

    @transition(
        source=BookingStatus.AVAILABLE,
        target=BookingStatus.IN_PROGRESS,
        on_error=BookingStatus.ERROR,
    )
    def initiate_booking(self):
        # if last seat payment in progress, change property slot's value to True
        pass

    @transition(
        source=BookingStatus.IN_PROGRESS,
        target=[BookingStatus.PAYMENT_DONE, BookingStatus.PAYMENT_FAILED],
        on_error=BookingStatus.ERROR,
    )
    def payment_process(self):
        # if last payment fails, change property slot's value to False
        pass

    @transition(
        source=BookingStatus.PAYMENT_DONE,
        target=BookingStatus.BOOKED,
        on_error=BookingStatus.ERROR,
    )
    def on_payment_completion(self):
        pass
