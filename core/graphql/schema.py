import graphene

from movies.graphql.queries import MoviesQuery
from movies.graphql.mutations import Mutation as MoviesMutation
from meta.graphql.queries import MetaQuery


class Query(MetaQuery, MoviesQuery, graphene.ObjectType):
    pass


class Mutation(MoviesMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
