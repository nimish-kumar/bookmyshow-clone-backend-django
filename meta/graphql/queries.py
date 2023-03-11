import graphene
from .types import CityType
from ..models import City


class MetaQuery(graphene.ObjectType):
    list_cities = graphene.List(CityType)
    # list_bookings_by_movies_and_date = graphene.List()

    def resolve_list_movies_by_city(root, info, **kwargs):
        # Querying a list
        return City.objects.all()
