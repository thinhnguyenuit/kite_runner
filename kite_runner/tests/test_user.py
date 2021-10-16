from .base import APIBaseTest
from rest_framework import status


class TestUserAPI(APIBaseTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_get_current_user(self):
        response = self.client.get('/api/v1/user/', HTTP_AUTHORIZATION='Token {}'.format(self.token[0].key))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.user_response)

    def test_get_current_user_unauthorized(self):
        response = self.client.get('/api/v1/user/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), self.unauthenticated_response())
