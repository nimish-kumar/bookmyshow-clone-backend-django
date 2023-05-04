from typing import Any
from django.core.paginator import Paginator, EmptyPage
from graphql_jwt.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from ..models import Booking, BookingSlot, Movie, MovieFormat
from meta.models import Language
from ..constants import BookingStatus
from .types import PaginatedBookingType, PaginatedMoviesListFormats


class PaginatorBookingResolver:
    @login_required
    def __call__(self, root, info, page: int, limit: int):
        results = Paginator(
            Booking.objects.filter(
                user=info.context.user, status=BookingStatus.BOOKED.value
            )
            .select_related(
                "slot_grp__slot__movie",
                "slot_grp__slot__format",
                "slot_grp__slot__screen__theatre",
            )
            .order_by("-booked_at")
            .all(),
            limit,
        )
        total_pages = results.num_pages
        prev_page = None
        next_page = None
        count = 0
        if page != 1:
            prev_page = page - 1
        if page != total_pages:
            next_page = page + 1
        try:
            results = results.page(page).object_list
            count = len(results)
        except EmptyPage:
            results = []
        return PaginatedBookingType(
            prev_page=prev_page,
            next_page=next_page,
            results=results,
            count=count,
        )


class PaginatedMoviesDetailsResolver:
    @login_required
    def __call__(self, root, info, page: int, limit: int, city):
        movie_langs = list(
            BookingSlot.objects.select_related("screen__theatre__city")
            .filter(
                screen__theatre__city_id=city,
                is_fully_booked=False,
                screening_datetime__gte=timezone.now(),
                screening_datetime__lte=timezone.now() + timedelta(days=7),
            )
            .order_by()
            .values_list("movie", "lang", "format")
            .distinct()
        )
        movie_details_dict = dict()
        for movie_lang in movie_langs:
            movie_id, lang_id, format_id = movie_lang
            if movie_id not in movie_details_dict.keys():
                movie_details_dict[movie_id] = {lang_id: set([format_id])}
            else:
                if lang_id not in movie_details_dict[movie_id].keys():
                    movie_details_dict[movie_id][lang_id] = set([format_id])
                else:
                    movie_details_dict[movie_id][lang_id].add(format_id)

        movies_details_list = []
        for movie_id in movie_details_dict.keys():
            movies_details_list.append({"movie": movie_id, "langs": list()})

        for movie in movies_details_list:
            [
                movie["langs"].append(
                    {
                        "lang": lang_id,
                        "formats": list(
                            movie_details_dict[movie["movie"]][lang_id]
                        ),
                    }
                )
                for lang_id in movie_details_dict[movie["movie"]].keys()
            ]

        for movie_detail in movies_details_list:
            movie_detail["movie"] = Movie.objects.get(pk=movie_detail["movie"])
            for lang_detail in movie_detail["langs"]:
                lang_detail["lang"] = Language.objects.get(
                    pk=lang_detail["lang"]
                )
                lang_detail["formats"] = MovieFormat.objects.filter(
                    id__in=lang_detail["formats"]
                )

        results = Paginator(
            movies_details_list,
            limit,
        )
        total_pages = results.num_pages
        prev_page = None
        next_page = None
        count = 0
        if page != 1:
            prev_page = page - 1
        if page != total_pages:
            next_page = page + 1
        try:
            results = results.page(page).object_list
            count = len(results)
        except EmptyPage:
            results = []

        return PaginatedMoviesListFormats(
            prev_page=prev_page,
            next_page=next_page,
            results=results,
            count=count,
        )
