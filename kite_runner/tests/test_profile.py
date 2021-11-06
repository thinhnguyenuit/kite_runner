from rest_framework import status

from kite_runner.models import User
from kite_runner.utils.constants import TOKEN_HEADER

from .base import APIBaseTest


class TestProfileAPI(APIBaseTest):

    profile_url = "/api/v1/profiles"
    test_username = "test_user1"
    test_password = "12345678"
    test_email = "test1@mail.com"

    def test_get_profile(self):
        response = self.client.get(f"{self.profile_url}/{self.USERNAME}")

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
        response = self.client.get(f"{self.profile_url}/test_user_not_found")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            self.not_found_response(
                "Profile with username: test_user_not_found not found."
            ),
        )

    def test_follow_profile(self):
        User.objects.create(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password,
        )

        response = self.client.post(
            f"{self.profile_url}/{self.test_username}/follow/",
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "profile": {
                    "username": self.test_username,
                    "bio": "",
                    "image": self.IMAGE,
                    "following": True,
                }
            },
        )

    def test_follow_profile_not_found(self):
        response = self.client.post(
            f"{self.profile_url}/user_not_found/follow/",
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            self.not_found_response("Profile with username: user_not_found not found."),
        )

    def test_follow_profile_not_authenticated(self):
        response = self.client.post(f"{self.profile_url}/test_user/follow/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), self.unauthenticated_response())

    def test_follow_profile_already_following(self):
        test_user: User = User.objects.create(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password,
        )
        self.user.profile.follow(test_user.profile)

        response = self.client.post(
            f"{self.profile_url}/{self.test_username}/follow/",
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_profile(self):
        test_user: User = User.objects.create(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password,
        )
        self.user.profile.follow(test_user.profile)

        response = self.client.delete(
            f"{self.profile_url}/{self.test_username}/follow/",
            HTTP_AUTHORIZATION=TOKEN_HEADER.format(self.token[0].key),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
