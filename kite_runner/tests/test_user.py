from copy import deepcopy

from rest_framework import status

from kite_runner.utils.constants import TOKEN_HEADER

from .base import APIBaseTest


class TestUserAPI(APIBaseTest):

    user_api_url = "/api/v1/user/"

    @classmethod
    def setUpTestData(cls):
        super().setup_test_data()  # type: ignore

    def test_get_current_user(self):
        response = self.client.get(
            self.user_api_url, HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.user_response)

    def test_get_current_user_unauthorized(self):
        response = self.client.get(self.user_api_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), self.unauthenticated_response())

    def test_update_user(self):
        user_update_data = {
            "user": {
                "email": "update_email@gmail.com",
                "token": self.token[0].key,
                "username": "new username",
                "bio": "hello nehhh",
                "image": "https://www.gravatar.com/avatar/73af357c60e22857eda9a5dbf106e2f0",
            }
        }
        response = self.client.put(
            self.user_api_url,
            data=user_update_data,
            HTTP_AUTHORIZATION="Token {}".format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), user_update_data)

    def test_update_user_partial(self):
        user_update_data = {"user": {"email": "update_email@mail.com"}}
        update_user_reponse = deepcopy(self.user_response)
        update_user_reponse["user"]["email"] = "update_email@mail.com"

        response = self.client.patch(
            self.user_api_url,
            data=user_update_data,
            HTTP_AUTHORIZATION="Token {}".format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), update_user_reponse)
