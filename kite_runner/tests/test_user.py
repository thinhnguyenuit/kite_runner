from rest_framework import status

from kite_runner.utils.constants import TOKEN_HEADER
from kite_runner.utils.tokens import get_user_token

from .base import APIBaseTest


class TestUserAPI(APIBaseTest):

    user_api_url = "/api/v1/user/"

    def setUp(self) -> None:
        super().setUp()
        self.token = get_user_token(self.user)

    def test_get_current_user(self):
        response = self.client.get(
            self.user_api_url, HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user_unauthorized(self):
        response = self.client.get(self.user_api_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), self.unauthenticated_response())

    def test_update_user(self):
        user_update_data = {
            "user": {
                "email": "update_email@gmail.com",
                "username": "new username",
                "bio": "hello nehhh",
                "image": "https://www.gravatar.com/avatar/73af357c60e22857eda9a5dbf106e2f0",
            }
        }
        response = self.client.put(
            self.user_api_url,
            data=user_update_data,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertIsNotNone(response_data)
        self.assertEqual(
            response_data["user"]["email"], user_update_data["user"]["email"]
        )
        self.assertEqual(
            response_data["user"]["username"], user_update_data["user"]["username"]
        )
        self.assertEqual(response_data["user"]["bio"], user_update_data["user"]["bio"])
        self.assertEqual(
            response_data["user"]["image"], user_update_data["user"]["image"]
        )

    def test_update_user_partial(self):
        user_update_data = {"user": {"email": "update_email@mail.com"}}

        response = self.client.patch(
            self.user_api_url,
            data=user_update_data,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["user"]["email"], "update_email@mail.com")
