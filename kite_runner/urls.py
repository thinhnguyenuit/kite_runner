from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from kite_runner.api import (article, authentication, comment, profile, signup,
                            tag, user)
from kite_runner.router import OptionalSlashRouter

router = OptionalSlashRouter() # type: ignore
router.register(r"articles", article.ArticleViewset, basename="articles")

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/articles/feed/", article.ArticlesFeedAPIView.as_view()),
    path(r"api/v1/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/v1/users/", signup.SignupAPIView.as_view()),
    path("api/v1/users/login/", authentication.LoginViewSet.as_view()),
    path("api/v1/user/", user.UserRetrieveUpdateAPIView.as_view()),
    path("api/v1/profiles/<str:username>", profile.ProfileRetrieveAPIView.as_view()),
    path("api/v1/profiles/<str:username>/follow/", profile.FollowUserAPIView.as_view()),
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
