from django.contrib import admin
from django.urls import path

from kite_runner.api import authentication, signup

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", signup.SignupViewSet.as_view()),
    path("api/v1/users/login/", authentication.LoginViewSet.as_view()),
]
