from graphql_jwt.backends import JSONWebTokenBackend


class FirebaseGoogleWebTokenBackend(JSONWebTokenBackend):
    def authenticate(self, request=None, **kwargs):
        from graphql_jwt.utils import get_credentials

        if request is None or getattr(request, "_jwt_token_auth", False):
            return None

        token = get_credentials(request, **kwargs)

        if token is not None:
            return self.get_user_by_token(token)

        return None

    def get_user_by_token(self, token: str):
        from firebase_admin import auth
        from django.contrib.auth import get_user_model

        User = get_user_model()

        decoded_token = auth.verify_id_token(token)
        email = decoded_token["email"]
        firstname, lastname = decoded_token["name"].split(" ")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email, first_name=firstname, last_name=lastname
            )

        return user
