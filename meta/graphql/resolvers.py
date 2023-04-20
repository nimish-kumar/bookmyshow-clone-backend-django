# Used for resolver classes/functions in Queries
from ..models import City
from graphql_jwt.decorators import login_required


class CityResolver:
    @login_required
    def __call__(self, root, info, *args, **kwargs):
        return City.objects.all()
