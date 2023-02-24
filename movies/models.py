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
        "Movie",
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
    movie_length = models.DurationField(help_text="Movie length in hours")
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

    def create_slot_groups(self):
        pass


class SlotGroup(models.Model):
    name = models.CharField(max_length=10)
    grp_code = models.CharField(max_length=2)
    start_rowhead = models.CharField(max_length=3)
    end_rowhead = models.CharField(max_length=3)
    cost = models.PositiveSmallIntegerField()
    slot = models.ForeignKey(
        "BookingSlot",
        on_delete=models.CASCADE,
        related_name="slot_booking",
    )

    class Meta:
        ordering = ["-id"]
        indexes = [models.Index(name="slot_grp_idx", fields=["grp_code", "slot"])]
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
    )
    seat_number = models.SmallIntegerField(validators=[MinValueValidator(0)])
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
    updated_at = models.DateTimeField(auto_now=True)
    paid_amt = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        # Orders by bookings which have been recently added/updated.
        ordering = ["-updated_at", "-id"]
        unique_together = ["slot_grp", "seat_number"]
        indexes = [
            models.Index(
                name="uniq_booking_idx",
                fields=["slot_grp", "seat_number"],
            ),
            models.Index(name="booking_status_idx", fields=["status"]),
            models.Index(name="booking_row_col_idx", fields=["row", "column"]),
        ]

    def get_seat_number(self):
        return f"{self.row}{self.seat_number}"

    @transition(
        field=status,
        source=BookingStatus.ERROR,
        target=BookingStatus.AVAILABLE,
    )
    def fallback(self):
        pass

    @transition(
        field=status,
        source=BookingStatus.AVAILABLE,
        target=BookingStatus.IN_PROGRESS,
        on_error=BookingStatus.ERROR,
    )
    def initiate_booking(self, user):
        # if last seat payment in progress, change property slot's value to True
        pass

    @transition(
        field=status,
        source=BookingStatus.IN_PROGRESS,
        target=BookingStatus.PAYMENT_DONE,
        on_error=BookingStatus.ERROR,
    )
    def payment_done(self):
        pass

    @transition(
        field=status,
        source=BookingStatus.IN_PROGRESS,
        target=BookingStatus.PAYMENT_FAILED,
        on_error=BookingStatus.ERROR,
    )
    def payment_failed(self):
        # if last payment fails, change property slot's value to False
        pass

    @transition(
        field=status,
        source=BookingStatus.PAYMENT_DONE,
        target=BookingStatus.BOOKED,
        on_error=BookingStatus.ERROR,
    )
    def on_payment_completion(self):
        pass
