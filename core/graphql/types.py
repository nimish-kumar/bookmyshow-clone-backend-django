from graphene_django import DjangoObjectType
from ..models import User

class UserType(DjangoObjectType):
    class Meta:
        model= User
        fields = ["first_name", "last_name", "profile_image_url"]