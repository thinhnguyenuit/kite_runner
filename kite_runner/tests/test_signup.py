# from kite_runner.tests.base import APIBaseTest
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestSignupAPI(TestCase):
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
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
            content_type="application/json",
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
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
