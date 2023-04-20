from django.contrib import admin
from .models import (
    Booking,
    BookingSlot,
    Movie,
    MovieFormat,
    Screen,
    SlotGroup,
    Theatre,
    TrailerUrl,
)

admin.site.register(Booking)
admin.site.register(BookingSlot)
admin.site.register(Movie)
admin.site.register(MovieFormat)
admin.site.register(Screen)
admin.site.register(SlotGroup)
admin.site.register(Theatre)
admin.site.register(TrailerUrl)
