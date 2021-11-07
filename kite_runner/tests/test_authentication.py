from rest_framework import status

from .base import APIBaseTest


class TestAuthentication(APIBaseTest):
    def test_user_login(self) -> None:
        response = self.client.post(
            "/api/v1/users/login/",
            {"user": {"email": self.EMAIL, "password": self.PASSWORD}},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["user"]["email"], self.user.email)

    def test_user_login_wrong_password(self) -> None:
        response = self.client.post(
            "/api/v1/users/login/",
            {"user": {"email": self.EMAIL, "password": "wrong_password"}},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"]["error"][0], "wrong username or password"
        )
