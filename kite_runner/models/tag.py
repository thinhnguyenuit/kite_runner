from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self) -> str:
        return self.tag
