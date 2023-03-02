import graphene
from graphene_django import DjangoObjectType

from movies.graphql.schema import MoviesQuery
from meta.graphql.schema import MetaQuery


class Query(MoviesQuery, graphene.ObjectType):
    pass


# class Mutation(MoviesMutation, graphene.ObjectType):
#     pass


schema = graphene.Schema(query=Query)
