from typing import Any, Dict, Optional

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase as DRFTestCase

from kite_runner.models import User
from kite_runner.utils.constants import DEFAULT_AVT_IMAGE


def _setup_test_data(klass: Any) -> None:
    klass.user = User.objects.create_user(
        email=klass.EMAIL, password=klass.PASSWORD, username=klass.USERNAME
    )
    klass.token = Token.objects.get_or_create(user=klass.user)
    klass.user_response = {
        "user": {
            "email": klass.EMAIL,
            "token": klass.token[0].key,
            "username": klass.USERNAME,
            "bio": klass.BIO,
            "image": klass.IMAGE,
        }
    }


class ErrorResponseMixin:
    def unauthenticated_response(
        self, message: str = "Authentication credentials were not provided."
    ) -> Dict[str, Dict[str, str]]:
        return {"errors": {"detail": message}}

    def not_found_response(
        self, message: str = "Not found."
    ) -> Dict[str, Dict[str, str]]:
        return {"errors": {"detail": message}}


class TestMixin:
    EMAIL: str = "test_user@kiterunner.com"
    PASSWORD: Optional[str] = "somepassword"
    USERNAME: str = "test_user"
    BIO: str = ""
    IMAGE: str = DEFAULT_AVT_IMAGE
    user_response: Dict

    user: User

    def _create_user(self, email: str, password: str, username: str) -> User:
        return User.objects.create_user(
            email=email, password=password, username=username
        )

    @classmethod
    def setup_test_data(cls):
        _setup_test_data(cls)


class APIBaseTest(TestMixin, ErrorResponseMixin, DRFTestCase):
    def setUp(self) -> None:
        return super().setUp()
