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
from .utils import get_layout_details, test_seat_details, get_seat_details

admin.site.register(Booking)

@admin.register(BookingSlot)
class BookingSlotAdmin(admin.ModelAdmin):
    list_display = (
        "movie",
        "is_fully_booked",
        "screening_datetime",
    )

    def save_model(self, request, obj, form, change):
        layout = get_layout_details(layout=self.screen.layout)
        layout_grps = layout["grp_details"]
        rows = layout["seating_layout"].split("|")
        if self.id:
            # delete existing slot grps
            SlotGroup.objects.filter(slot=self.id).delete()
        else:
            self.current_layout = self.screen.layout
        super().save_model(request, obj, form, change)
        object_grps = []
        for grp in layout_grps:
            object_grps.append(
                SlotGroup(
                    name=grp["grp_name"],
                    grp_code=grp["grp_code"],
                    cost=grp["cost"],
                    slot=self,
                )
            )
        SlotGroup.objects.bulk_create(object_grps)
        bookings = []
        for row in rows:
            seats_arr = row.split(":")
            for seat in seats_arr:
                if test_seat_details(seat):
                    seat_details = get_seat_details(seat)
                    grp_code = seat_details["seat_grp"]
                    slot_grp = SlotGroup.objects.get(
                        slot=self, grp_code=grp_code
                    )
                    bookings.append(
                        Booking(
                            slot_grp=slot_grp,
                            seat_number=seat_details["seat_num"],
                            row=seat_details["row"],
                            column=seat_details["col"],
                        )
                    )
        Booking.objects.bulk_create(bookings)
        return super().save()

admin.site.register(Movie)
admin.site.register(MovieFormat)
admin.site.register(Screen)
admin.site.register(SlotGroup)
admin.site.register(Theatre)
admin.site.register(TrailerUrl)
