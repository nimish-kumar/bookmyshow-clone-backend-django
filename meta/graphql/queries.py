import graphene
from .types import CityType
from .resolvers import CityResolver


class MetaQuery(graphene.ObjectType):
    list_cities = graphene.List(CityType, resolver=CityResolver())
