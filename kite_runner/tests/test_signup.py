# from kite_runner.tests.base import APIBaseTest
from typing import cast

from rest_framework import status

from kite_runner.models import User
from kite_runner.utils import tokens

from .base import APIBaseTest


class TestSignupAPI(APIBaseTest):
    def test_api_sign_up(self):
        response = self.client.post(
            "/api/v1/users/",
            {
                "user": {
                    "username": "test_user",
                    "email": "test@mail.com",
                    "password": "test_password",
                }
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = cast(User, User.objects.get(username="test_user"))
        token = tokens.get_user_token(user)

        self.assertEqual(
            response.json(),
            {
                "user": {
                    "username": "test_user",
                    "email": "test@mail.com",
                    "token": token,
                    "bio": "",
                    "image": "https://www.gravatar.com/avatar/73af357c60e22857eda9a5dbf106e2f0",
                }
            },
        )

    def test_api_sign_up_already_exist(self):
        response = self.client.post(
            "/api/v1/users/",
            {
                "user": {
                    "username": "test_user",
                    "email": "test@mail.com",
                    "password": "test_password",
                }
            },
        )

        response = self.client.post(
            "/api/v1/users/",
            {
                "user": {
                    "username": "test_user",
                    "email": "test@mail.com",
                    "password": "test_password",
                }
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
