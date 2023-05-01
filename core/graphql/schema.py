import graphene

from movies.graphql.queries import MoviesQuery
from movies.graphql.mutations import Mutation as MoviesMutation
from core.graphql.mutations import Mutation as CoreMutation
from meta.graphql.queries import MetaQuery
from core.graphql.queries import Query as CoreQuery


class Query(MetaQuery, MoviesQuery, CoreQuery, graphene.ObjectType):
    pass


class Mutation(MoviesMutation, CoreMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
