import graphene

from movies.graphql.queries import MoviesQuery
from movies.graphql.mutations import Mutation as MoviesMutation
from core.graphql.mutations import Mutation as CoreMutation
from meta.graphql.queries import MetaQuery


class Query(MetaQuery, MoviesQuery, graphene.ObjectType):
    pass


class Mutation(MoviesMutation, CoreMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
