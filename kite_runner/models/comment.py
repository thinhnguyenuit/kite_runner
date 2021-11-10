from django.db import models


class Comment(models.Model):

    body = models.TextField()

    article = models.ForeignKey(
        "kite_runner.Article", related_name="comments", on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        "kite_runner.Profile", related_name="comments", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
