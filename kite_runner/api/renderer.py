from kite_runner.renderer import KRJSONRenderer


class UserJSONRenderer(KRJSONRenderer):
    object_label = "user"
    pagination_object_label = "users"
    pagination_count_label = "usersCount"

    def render(self, data, media_type=None, renderer_context=None):
        token = data.get("token", None)
        if token and isinstance(token, bytes):
            data["token"] = token.decode("utf-8")

        return super(UserJSONRenderer, self).render(data)  # type: ignore


class ProfileJSONRenderer(KRJSONRenderer):
    object_label = "profile"
    pagination_object_label = "profiles"
    pagination_count_label = "profilesCount"


class ArticleJSONRenderer(KRJSONRenderer):
    object_label = "article"
    pagination_object_label = "articles"
    pagination_count_label = "articlesCount"


class CommentJSONRenderer(KRJSONRenderer):
    object_label = "comment"
    pagination_object_label = "comments"
    pagination_count_label = "commentsCount"
