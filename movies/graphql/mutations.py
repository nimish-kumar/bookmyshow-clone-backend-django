import graphene
from django.db import transaction
from graphql_jwt.decorators import login_required
from .types import BookingType
from ..models import Booking, Screen, BookingSlot, SlotGroup
from ..constants import BookingStatus, SeatStatus
from ..utils import get_seat_details, create_seat
from django.utils import timezone


class InitiateBookingTicket(graphene.Mutation):
    class Arguments:
        seats = graphene.List(graphene.String)
        screen = graphene.String(required=True)
        theatre_id = graphene.ID(required=True)
        movie_id = graphene.ID(required=True)
        screening_datetime = graphene.DateTime(required=True)

    ticket_details = graphene.List(BookingType)

    @transaction.atomic
    def mutate(
        root, info, seats, screen, theatre_id, movie_id, screening_datetime
    ):
        active_user = info.context.user
        seats_set = list(set(seats))
        if seats.count() != seats_set.count():
            raise ValueError("Repeated number of seats entered")
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
        # Update Booking slot layout
        updated_layout = booking_slot.screen.layout

        for seat in seats:
            if seat not in updated_layout:
                raise ValueError("Seat not present in the layout")
            seat_info = get_seat_details(seat, re_status=False)
            seat_status = seat_info["seat_status"]
            if int(seat_status) != SeatStatus.AVAILABLE:
                raise ValueError("Seat status is not set as available")
            seat_grp = seat_info["seat_grp"]
            row = seat_info["row"]
            col = seat_info["col"]
            seat_num = int(seat_info["seat_num"])
            slot_grp = SlotGroup.objects.get(
                grp_code=seat_grp, slot=booking_slot
            )
            bookings.append(
                Booking.objects.get(
                    slot_grp=slot_grp, row=row, seat_number=seat_num
                )
            )
            updated_seat = create_seat(
                status_code=SeatStatus.SOLD,
                col=col,
                row=row,
                grp_code=seat_grp,
                seat_num=seat_num,
            )

            updated_layout = updated_layout.replace(seat, updated_seat, 1)

        for booking in bookings:
            booking.user = active_user
            booking.status = BookingStatus.IN_PROGRESS
        Booking.objects.bulk_update(bookings, ["user", "status"])

        # Update count of remaining seats
        slot_grps = list(SlotGroup.objects.filter(slot=booking_slot))
        if (
            Booking.objects.filter(
                slot_grp__in=slot_grps, status=BookingStatus.AVAILABLE
            ).count()
            == 0
        ):
            booking_slot.is_fully_booked = True
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

    @transaction.atomic
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


class DirectBookingTicket(graphene.Mutation):
    class Arguments:
        seats = graphene.List(graphene.String)
        slot_id = graphene.ID(required=True)

    ticket_details = graphene.List(BookingType)

    @login_required
    @transaction.atomic
    def mutate(root, info, seats, slot_id):
        active_user = info.context.user
        seats_set = list(set(seats))
        if len(seats) != len(seats_set):
            raise ValueError("Repeated number of seats entered")
        try:
            booking_slot = BookingSlot.objects.get(pk=slot_id)
        except BookingSlot.DoesNotExist:
            raise ValueError("Wrong slot ID")
        bookings = []
        # Update Booking slot layout
        updated_layout = booking_slot.current_layout

        for seat in seats:
            if seat not in updated_layout:
                raise ValueError("Seat not present in the layout")
            seat_info = get_seat_details(seat)
            seat_grp = seat_info["seat_grp"]
            row = seat_info["row"]
            col = seat_info["col"]
            seat_num = int(seat_info["seat_num"])
            slot_grp = SlotGroup.objects.get(
                grp_code=seat_grp, slot=booking_slot
            )
            try:
                bookings.append(
                    Booking.objects.get(
                        slot_grp=slot_grp,
                        row=row,
                        seat_number=seat_num,
                        status=BookingStatus.AVAILABLE,
                    )
                )
            except Booking.DoesNotExist:
                raise ValueError("Request seat is not available for booking")
            updated_seat = create_seat(
                status_code=SeatStatus.SOLD,
                col=col,
                row=row,
                grp_code=seat_grp,
                seat_num=seat_num,
            )

            updated_layout = updated_layout.replace(seat, updated_seat, 1)
            booking_slot.current_layout = updated_layout
            booking_slot.save()

        for booking in bookings:
            booking.user = active_user
            booking.status = BookingStatus.BOOKED
            booking.booked_at = timezone.now()
        Booking.objects.bulk_update(bookings, ["user", "status", "booked_at"])

        # Update count of remaining seats
        slot_grps = list(SlotGroup.objects.filter(slot=booking_slot))
        if (
            Booking.objects.filter(
                slot_grp__in=slot_grps, status=BookingStatus.AVAILABLE
            ).count()
            == 0
        ):
            booking_slot.is_fully_booked = True
        return InitiateBookingTicket(
            ticket_details=Booking.objects.filter(
                pk__in=[booking.id for booking in bookings]
            ),
        )


class Mutation(graphene.ObjectType):
    # initiate_booking_ticket = InitiateBookingTicket.Field()
    # process_booking = ProcessBooking.Field()
    book_tickets = DirectBookingTicket.Field()
