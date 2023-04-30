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

    # @login_required
    # def resolve_list_movie_lang_by_city(
    #     root,
    #     info,
    #     city,
    # ):
    #     movie_langs = list(
    #         BookingSlot.objects.select_related("screen__theatre__city")
    #         .filter(
    #             screen__theatre__city_id=city,
    #             is_fully_booked=False,
    #             screening_datetime__gte=timezone.now(),
    #             screening_datetime__lte=timezone.now() + timedelta(days=7),
    #         )
    #         .order_by()
    #         .values_list("movie", "lang", "format")
    #         .distinct()
    #     )
    #     movie_details_dict = dict()
    #     for movie_lang in movie_langs:
    #         movie_id, lang_id, format_id = movie_lang
    #         if movie_id not in movie_details_dict.keys():
    #             movie_details_dict[movie_id] = {lang_id: set([format_id])}
    #         else:
    #             movie_details_dict[movie_id][lang_id].add(format_id)

    #     movies_details_list = []
    #     for movie_id in movie_details_dict.keys():
    #         movies_details_list.append({"movie": movie_id, "langs": list()})

    #     for movie in movies_details_list:
    #         [
    #             movie["langs"].append(
    #                 {
    #                     "lang": lang_id,
    #                     "formats": list(
    #                         movie_details_dict[movie["movie"]][lang_id]
    #                     ),
    #                 }
    #             )
    #             for lang_id in movie_details_dict[movie["movie"]].keys()
    #         ]

    #     for movie_detail in movies_details_list:
    #         movie_detail["movie"] = Movie.objects.get(pk=movie_detail["movie"])
    #         for lang_detail in movie_detail["langs"]:
    #             lang_detail["lang"] = Language.objects.get(
    #                 pk=lang_detail["lang"]
    #             )
    #             lang_detail["formats"] = MovieFormat.objects.filter(
    #                 id__in=lang_detail["formats"]
    #             )

    #     return movies_details_list

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
