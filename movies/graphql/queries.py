import graphene
from django.db.models import Q
from meta.models import Language
from .types import BookingSlotType, MovieDetailsType
from ..models import BookingSlot, Movie, MovieFormat

from django.utils import timezone
from datetime import timedelta


class MoviesQuery(graphene.ObjectType):
    list_movie_lang_by_city = graphene.List(
        MovieDetailsType,
        city=graphene.Argument(
            graphene.ID,
            description="City ID",
            required=True,
        ),
    )
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
        movie=graphene.Argument(
            graphene.ID,
            description="Movie ID",
            required=True,
        ),
        format=graphene.Argument(
            graphene.ID,
            description="Movie Format ID",
            required=True,
        ),
    )

    def resolve_list_movie_lang_by_city(
        root,
        info,
        city,
    ):
        slots = list(
            BookingSlot.objects.select_related("screen__theatre__city")
            .filter(
                screen__theatre__city_id=city,
                is_fully_booked=False,
                screening_datetime__gte=timezone.now(),
                screening_datetime__lte=timezone.now() + timedelta(days=7),
            )
            .values("movie", "lang", "format")
            .distinct()
        )
        movie_ids = []
        movie_details_list = []
        for i in range(len(slots)):
            slot = slots[i]
            if slot["movie"] not in movie_ids:
                movies_list = list(
                    filter(lambda s: s["movie"] == slot["movie"], slots)
                )

                movie_details_list.append(
                    {
                        "movie": slot["movie"],
                        "langs": [
                            {
                                "lang": movie_detail["lang"],
                                "formats": [
                                    format["format"]
                                    for format in list(
                                        filter(
                                            lambda x: x["lang"]
                                            == movie_detail["lang"],
                                            movies_list,
                                        )
                                    )
                                ],
                            }
                            for movie_detail in movies_list
                        ],
                    }
                )
                movie_ids.append(slot["movie"])
        for movie_detail in movie_details_list:
            movie_detail["movie"] = Movie.objects.get(pk=movie_detail["movie"])
            for lang_detail in movie_detail["langs"]:
                lang_detail["lang"] = Language.objects.get(
                    pk=lang_detail["lang"]
                )
                lang_detail["formats"] = MovieFormat.objects.filter(
                    id__in=lang_detail["formats"]
                )

        return movie_details_list

    def resolve_list_movie_slots_by_city_date_lang(
        root, info, city, language, movie, format
    ):
        filters = Q()
        filter_by_city = Q(screen__theatre__city_id=city)
        filter_by_movie = Q(movie_id=movie)
        filter_by_datetime = Q(screening_datetime__gte=timezone.now()) & Q(
            screening_datetime__lte=timezone.now() + timedelta(days=7)
        )
        filter_by_language = Q(lang_id=language)
        filter_by_availability = Q(is_fully_booked=False)
        filter_by_format = Q(format_id=format)

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
