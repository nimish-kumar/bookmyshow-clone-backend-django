import graphene

from .types import BookingType
from ..models import Booking, Screen, BookingSlot, SlotGroup
from ..constants import BookingStatus
from ..utils import get_seat_details


class InitiateBookingTicket(graphene.Mutation):
    class Arguments:
        seats = graphene.List(graphene.String)
        screen = graphene.String(required=True)
        theatre_id = graphene.ID(required=True)
        movie_id = graphene.ID(required=True)
        screening_datetime = graphene.DateTime(required=True)

    ticket_details = graphene.List(BookingType)

    def mutate(root, info, seats, screen, theatre_id, movie_id, screening_datetime):
        active_user = info.context.user
        screen_obj = Screen.objects.get(
            screen_id=screen,
            theatre=theatre_id,
        )
        booking_slot = BookingSlot.objects.get(
            screen=screen_obj,
            movie=movie_id,
            screening_datetime=screening_datetime,
        )
        bookings = []
        for seat in seats:
            seat_info = get_seat_details(seat)
            seat_grp = seat_info["seat_grp"]
            row = seat_info["row"]
            seat_num = int(seat_info["seat_num"])
            slot_grp = SlotGroup.objects.get(grp_code=seat_grp, slot=booking_slot)
            bookings.append(
                Booking.objects.get(slot_grp=slot_grp, row=row, seat_number=seat_num)
            )
        for booking in bookings:
            booking.user = active_user
            booking.status = BookingStatus.IN_PROGRESS
        Booking.objects.bulk_update(bookings, ["user", "status"])
        return InitiateBookingTicket(
            ticket_details=Booking.objects.filter(
                pk__in=[booking.id for booking in bookings]
            ),
        )


class ProcessBooking(graphene.Mutation):
    class Arguments:
        bookings = graphene.List(graphene.ID)

    ok = graphene.Boolean()
    ticket_details = graphene.List(BookingType)

    def mutate(root, info, bookings):
        bookings_obj = Booking.objects.filter(pk__in=list(set(bookings)))
        if bookings_obj.count() != len(list(bookings_obj)):
            raise ValueError("Invalid Booking IDs entered")
        for booking in bookings_obj:
            booking.status = BookingStatus.BOOKED

        Booking.objects.bulk_update(bookings_obj, ["status"])
        return ProcessBooking(
            ticket_details=Booking.objects.filter(
                pk__in=[booking.id for booking in bookings]
            ),
        )


class Mutation(graphene.ObjectType):
    initiate_booking_ticket = InitiateBookingTicket.Field()
    process_booking = ProcessBooking.Field()
