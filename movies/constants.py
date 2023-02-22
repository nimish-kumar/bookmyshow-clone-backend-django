from django.db import models
class BookingStatus(models.IntegerChoices):
    AVAILABLE = 0
    IN_PROGRESS = 1
    PAYMENT_FAILED = 2
    PAYMENT_DONE = 3
    BOOKED = 4
    ERROR = 5