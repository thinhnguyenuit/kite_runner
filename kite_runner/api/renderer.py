from kite_runner.renderer import KRJSONRenderer


class UserJSONRenderer(KRJSONRenderer):
    charset = "utf-8"
    object_label = "user"
    pagination_object_label = "users"
    pagination_count_label = "usersCount"

    def render(self, data, media_type=None, renderer_context=None):
        token = data.get("token", None)
        if token and isinstance(token, bytes):
            data["token"] = token.decode("utf-8")

        return super(UserJSONRenderer, self).render(data)  # type: ignore
