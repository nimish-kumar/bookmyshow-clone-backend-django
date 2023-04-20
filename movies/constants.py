from django.db import models


class BookingStatus(models.IntegerChoices):
    AVAILABLE = 0
    IN_PROGRESS = 1
    PAYMENT_FAILED = 2
    PAYMENT_DONE = 3
    BOOKED = 4
    ERROR = 5


class SeatStatus(models.IntegerChoices):
    SOLD = 0
    AVAILABLE = 1
    SELECTED = 2
