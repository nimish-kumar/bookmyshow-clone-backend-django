import graphene
import graphql_jwt
from .types import UserType
from graphql_jwt.decorators import login_required


class UpdateUserDetails(graphene.Mutation):
    user_details = graphene.Field(UserType)

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        profile_image_url = graphene.String()

    @login_required
    def resolve(
        self,
        info,
        first_name=None,
        last_name=None,
        profile_image_url=None,
    ):
        current_user = info.context.user
        if first_name:
            current_user.first_name = first_name
        if last_name:
            current_user.last_name = last_name
        if profile_image_url:
            current_user.profile_image_url = profile_image_url
        current_user.save()
        return UpdateUserDetails(user_details=current_user)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    update_user = UpdateUserDetails.Field()
