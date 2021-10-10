from rest_framework.authtoken.models import Token

from kite_runner.models import User


def get_user_token(User: "User") -> str:
    """
    Returns the token for the current user.
    """
    return Token.objects.get(user=User).key
