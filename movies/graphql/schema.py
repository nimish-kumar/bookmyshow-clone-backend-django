import graphene
from django.db.models import Q
from .types import BookingSlotType
from ..models import BookingSlot

from datetime import datetime


class MoviesQuery(graphene.ObjectType):
    list_movies_by_city = graphene.List(
        BookingSlotType,
        city=graphene.Argument(
            graphene.ID,
            description="City ID",
        ),
        language=graphene.Argument(
            graphene.ID,
            description="Movie language",
        ),
        datetime=graphene.Argument(
            graphene.DateTime,
            description="Bookings date",
            required=False,
        ),
    )
    # list_bookings_by_movies_and_date = graphene.List()

    def resolve_list_movies_by_city(
        root,
        info,
        city,
        language,
        datetime=datetime.now(),
    ):
        # Querying a list

        filters = Q()
        filter_by_city = Q(screen__theatre__city_id=city)
        filter_by_datetime = Q(screening_datetime__gte=datetime)
        filter_by_language = Q(movie__lang_id=language)
        filters = filters & filter_by_city & filter_by_datetime & filter_by_language

        return (
            BookingSlot.objects.select_related("movie", "screen__theatre__city")
            .prefetch_related(
                "slot_booking", "movie__format", "movie__genre", "movie__lang"
            )
            .filter(filters)
            .all()
        )


# class MoviesMutation(graphene.ObjectType):
#     pass
