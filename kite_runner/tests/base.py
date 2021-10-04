import inspect
from rest_framework.test import APITestCase as DRFTestCase
from kite_runner.models import User

def _setup_test_data(klass):
    pass


class ErrorResponseMixin:
    ERROR_INVALID_ID_CREDENTIALS = {
        "type": "validation_error",
        "code": "invalid_credentials",
        "detail": "Invalid credentials"
    }


class TestMixin:
    CONFIG_PASSWORD = "testpassword"
    # CLASS_DATA_SETUP = False

    user: User = None

    def _create_user(self, email, password):
        return User.objects.create_user(email=email, password=password)


class APIBaseTest(TestMixin, ErrorResponseMixin, DRFTestCase):
    def setUp(self):
        super().setUp()
