# from kite_runner.tests.base import APIBaseTest
from rest_framework import status
from django.test import TestCase
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

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
