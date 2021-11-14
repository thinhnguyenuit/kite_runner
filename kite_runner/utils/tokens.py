from rest_framework_simplejwt.tokens import RefreshToken

from kite_runner.models import User


def get_user_token(user: User) -> str:
    """
    Returns the token for the current user.
    """

    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)
