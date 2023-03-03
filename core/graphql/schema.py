import graphene

from movies.graphql.schema import Query as MoviesQuery
from meta.graphql.schema import MetaQuery


class Query(MoviesQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
