import graphene
from graphql_jwt.decorators import login_required
from django.db.models import Q
from .types import (
    BookingSlotType,
    PaginatedBookingType,
    PaginatedMoviesListFormats,
)
from ..models import BookingSlot
from .resolvers import PaginatorBookingResolver, PaginatedMoviesDetailsResolver
from django.utils import timezone
from datetime import timedelta


class MoviesQuery(graphene.ObjectType):
    list_movie_lang_by_city = graphene.Field(
        PaginatedMoviesListFormats,
        city=graphene.Argument(
            graphene.ID,
            description="City ID",
            required=True,
        ),
        page=graphene.Argument(
            graphene.Int,
            description="Page number",
            required=True,
        ),
        limit=graphene.Argument(
            graphene.Int,
            description="Number of items in a page",
            default_value=10,
        ),
        resolver=PaginatedMoviesDetailsResolver(),
    )
    list_movie_slots_by_city_date_lang = graphene.List(
        BookingSlotType,
        city=graphene.Argument(
            graphene.ID,
            description="City ID",
            required=True,
        ),
        language=graphene.Argument(
            graphene.String,
            description="Movie language",
            required=True,
        ),
        movie=graphene.Argument(
            graphene.ID,
            description="Movie ID",
            required=True,
        ),
        format=graphene.Argument(
            graphene.String,
            description="Movie Format ID",
            required=True,
        ),
    )
    get_slot_details = graphene.Field(
        BookingSlotType,
        id=graphene.Argument(
            graphene.ID,
            description="Slot ID",
            required=True,
        ),
    )
    list_booking_details = graphene.Field(
        PaginatedBookingType,
        resolver=PaginatorBookingResolver(),
        page=graphene.Argument(
            graphene.Int,
            description="Page number",
            required=True,
        ),
        limit=graphene.Argument(
            graphene.Int,
            description="Number of items in a page",
            default_value=10,
        ),
    )

    @login_required
    def resolve_list_movie_slots_by_city_date_lang(
        root, info, city, language, movie, format
    ):
        filters = Q()
        filter_by_city = Q(screen__theatre__city_id=city)
        filter_by_movie = Q(movie_id=movie)
        filter_by_datetime = Q(screening_datetime__gte=timezone.now()) & Q(
            screening_datetime__lte=timezone.now() + timedelta(days=7)
        )
        filter_by_language = Q(lang__lang_code=language)
        filter_by_availability = Q(is_fully_booked=False)
        filter_by_format = Q(format__format=format)

        filters = (
            filters
            & filter_by_city
            & filter_by_movie
            & filter_by_datetime
            & filter_by_language
            & filter_by_availability
            & filter_by_format
        )
        return (
            BookingSlot.objects.select_related("movie", "screen__theatre__city")
            .prefetch_related(
                "slotgrp_booking",
                "movie__format",
                "movie__genre",
            )
            .filter(filters)
            .all()
        )

    @login_required
    def resolve_get_slot_details(root, info, id):
        return BookingSlot.objects.get(pk=id)
