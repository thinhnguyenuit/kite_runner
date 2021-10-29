from django.db import models


class Article(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    body = models.TextField()
    tags = models.ManyToManyField("kite_runner.Tag", related_name="articles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        "kite_runner.Profile", on_delete=models.CASCADE, related_name="articles"
    )

    def __str__(self) -> str:
        return self.title
