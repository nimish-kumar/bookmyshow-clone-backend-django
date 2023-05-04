import graphene
from graphql_jwt.decorators import login_required

from .types import UserType

class Query(graphene.ObjectType):
    get_user_details = graphene.Field(UserType)

    @login_required
    def resolve_get_user_details(self, info):
        return info.context.user
