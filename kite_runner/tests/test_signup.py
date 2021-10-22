from typing import cast

from rest_framework import status

from kite_runner.models import User
from kite_runner.utils import tokens

from .base import APIBaseTest


class TestSignupAPI(APIBaseTest):
    user_url = "/api/v1/users/"
    user_test_data = {
        "user": {
            "username": "someuser",
            "email": "test@mail.com",
            "password": "test_password",
        }
    }

    def test_api_sign_up(self):
        response = self.client.post(
            self.user_url,
            self.user_test_data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = cast(User, User.objects.get(username="someuser"))
        token = tokens.get_user_token(user)

        self.assertEqual(
            response.json(),
            {
                "user": {
                    "username": "someuser",
                    "email": "test@mail.com",
                    "token": token,
                    "bio": "",
                    "image": "https://www.gravatar.com/avatar/73af357c60e22857eda9a5dbf106e2f0",
                }
            },
        )

    def test_api_sign_up_already_exist(self):
        self.client.post(
            self.user_url,
            self.user_test_data,
        )

        response = self.client.post(
            self.user_url,
            self.user_test_data,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
