from rest_framework import status

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

        self.assertEqual(
            response.data["username"], self.user_test_data["user"]["username"]
        )
        self.assertEqual(response.data["email"], self.user_test_data["user"]["email"])

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
