import graphene
from django.db.models import Q
from .types import BookingSlotType
from ..models import BookingSlot

from datetime import datetime


class MoviesQuery(graphene.ObjectType):
    list_movie_slots_by_city_date_lang = graphene.List(
        BookingSlotType,
        city=graphene.Argument(
            graphene.ID,
            description="City ID",
            required=True,
        ),
        language=graphene.Argument(
            graphene.ID,
            description="Movie language",
            required=True,
        ),
        datetime=graphene.Argument(
            graphene.DateTime,
            description="Bookings date",
        ),
    )

    def resolve_list_movies_by_city(
        root,
        info,
        city,
        language,
        datetime=datetime.now(),
    ):
        filters = Q()
        filter_by_city = Q(screen__theatre__city_id=city)
        filter_by_datetime = Q(screening_datetime__gte=datetime)
        filter_by_language = Q(lang_id=language)
        filters = filters & filter_by_city & filter_by_datetime & filter_by_language

        return (
            BookingSlot.objects.select_related("movie", "screen__theatre__city")
            .prefetch_related("slot_booking", "movie__format", "movie__genre")
            .filter(filters)
            .all()
        )
