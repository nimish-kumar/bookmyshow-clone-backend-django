from graphene_django import DjangoObjectType
from ..models import Artist, City, Facility, Genre, Language, Tag


class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist
        fields = "__all__"


class CityType(DjangoObjectType):
    class Meta:
        model = City
        fields = "__all__"


class FacilityType(DjangoObjectType):
    class Meta:
        model = Facility
        fields = "__all__"


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre
        fields = "__all__"


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language
        fields = "__all__"


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = "__all__"
