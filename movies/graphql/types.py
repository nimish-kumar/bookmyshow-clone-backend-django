from django.db.models import Max, Min
from graphene_django import DjangoObjectType
from graphene import Int, List, ObjectType, Field
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

from meta.graphql.types import LanguageType


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

    max_cost = Int()
    min_cost = Int()

    @staticmethod
    def resolve_max_cost(root, info):
        slotgrp_bookings = SlotGroup.objects.filter(
            slot=root.id, slot__is_fully_booked=False
        )
        max_cost = slotgrp_bookings.aggregate(Max("cost"))

        return max_cost["cost__max"]

    @staticmethod
    def resolve_min_cost(root, info):
        slotgrp_bookings = SlotGroup.objects.filter(
            slot=root.id, slot__is_fully_booked=False
        )
        min_cost = slotgrp_bookings.aggregate(Min("cost"))
        return min_cost["cost__min"]


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


class LanguageFormatType(ObjectType):
    lang = Field(LanguageType)
    formats = List(MovieFormatType)


class MovieDetailsType(ObjectType):
    movie = Field(MovieType)
    langs = List(LanguageFormatType)
