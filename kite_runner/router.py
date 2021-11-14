"""
Custom router that make trailing slash is optional.
Code from: https://stackoverflow.com/questions/46163838/how-can-i-make-a-trailing-slash-optional-on-a-django-rest-framework-simplerouter
""" # noqa

from rest_framework.routers import SimpleRouter


class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"
