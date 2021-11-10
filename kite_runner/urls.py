from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from kite_runner.api import (article, authentication, comment, profile, signup,
                             tag, user)

router = DefaultRouter(trailing_slash=False)
router.register(r"articles", article.ArticleViewset, basename="articles")

urlpatterns = [
    path(r"api/v1/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/v1/users/", signup.SignupAPIView.as_view()),
    path("api/v1/users/login/", authentication.LoginViewSet.as_view()),
    path("api/v1/user/", user.UserRetrieveUpdateAPIView.as_view()),
    path("api/v1/profiles/<str:username>", profile.ProfileRetrieveAPIView.as_view()),
    path("api/v1/profiles/<str:username>/follow/", profile.FollowUserAPIView.as_view()),
    path("api/v1/articles/feed/", article.ArticlesFeedAPIView.as_view()),
    path(
        "api/v1/articles/<str:slug>/favorite/",
        article.ArticlesFavoriteAPIView.as_view(),
    ),
    path(
        "api/v1/articles/<str:article_slug>/comments/",
        comment.CommentListCreateAPIView.as_view(),
    ),
    path(
        "api/v1/articles/<str:article_slug>/comments/<int:pk>",
        comment.CommentDestroyAPIView.as_view(),
    ),
    path("api/v1/tags/", tag.TagListAPIView.as_view()),
]
