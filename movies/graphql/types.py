from graphene_django import DjangoObjectType

from ..models import (
    Booking,
    BookingSlot,
    Movie,
    MovieFormat,
    Screen,
    SlotGroup,
    Theatre,
    TrailerUrl,
)

class TrailerUrlType(DjangoObjectType):
    class Meta:
        model = TrailerUrl
        fields = "__all__"


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
        fields = "__all__"


class BookingType(DjangoObjectType):
    class Meta:
        model = Booking
        fields = "__all__"


class BookingSlotType(DjangoObjectType):
    class Meta:
        model = BookingSlot
        fields = "__all__"


class MovieFormatType(DjangoObjectType):
    class Meta:
        model = MovieFormat
        fields = "__all__"


class ScreenType(DjangoObjectType):
    class Meta:
        model = Screen
        fields = "__all__"


class SlotGroupType(DjangoObjectType):
    class Meta:
        model = SlotGroup
        fields = "__all__"


class TheatreType(DjangoObjectType):
    class Meta:
        model = Theatre
        fields = "__all__"

