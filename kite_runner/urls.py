from django.contrib import admin
from django.urls import path

from kite_runner.api import authentication, profile, signup, user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", signup.SignupAPIView.as_view()),
    path("api/v1/users/login/", authentication.LoginViewSet.as_view()),
    path("api/v1/user/", user.UserRetrieveUpdateAPIView.as_view()),
    path("api/v1/profiles/<str:username>", profile.ProfileRetrieveAPIView.as_view()),
    path("api/v1/profiles/<str:username>/follow/", profile.FollowUserAPIView.as_view()),
]
