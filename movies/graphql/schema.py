import graphene
from .queries import MoviesQuery


class Query(MoviesQuery, graphene.ObjectType):
    pass
