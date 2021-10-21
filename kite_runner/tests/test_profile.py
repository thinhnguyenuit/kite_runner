from rest_framework import status

from kite_runner.models import User

from .base import APIBaseTest


class TestProfileAPI(APIBaseTest):
    @classmethod
    def setUpTestData(cls):
        super().setup_test_data()  # type: ignore

    def test_get_profile(self):
        response = self.client.get("/api/v1/profile/test_user")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "profile": {
                    "username": self.USERNAME,
                    "bio": self.BIO,
                    "image": self.IMAGE,
                    "following": False,
                }
            },
        )

    def test_get_profile_not_found(self):
        response = self.client.get("/api/v1/profile/test_user_not_found")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            self.not_found_response(
                "Profile with username: test_user_not_found not found."
            ),
        )

    def test_follow_profile(self):
        User.objects.create(
            username="hunrie", email="hun@email.com", password="123test"
        )

        response = self.client.post(
            "/api/v1/profile/hunrie/follow/",
            HTTP_AUTHORIZATION="Token {}".format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "profile": {
                    "username": "hunrie",
                    "bio": "",
                    "image": self.IMAGE,
                    "following": True,
                }
            },
        )

    def test_follow_profile_not_found(self):
        response = self.client.post(
            "/api/v1/profile/user_not_found/follow/",
            HTTP_AUTHORIZATION="Token {}".format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            self.not_found_response("Profile with username: user_not_found not found."),
        )

    def test_follow_profile_not_authenticated(self):
        response = self.client.post("/api/v1/profile/test_user/follow/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), self.unauthenticated_response())

    # def test_unfollow_profile(self):
