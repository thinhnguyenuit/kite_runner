from __future__ import annotations

from django.db import models


class Profile(models.Model):
    user = models.OneToOneField("kite_runner.User", on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = models.URLField(
        default="https://www.gravatar.com/avatar/73af357c60e22857eda9a5dbf106e2f0"
    )
    following = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False
    )

    def __str__(self):
        return self.user.username

    def follow(self, profile: Profile) -> None:
        self.following.add(profile)

    def unfollow(self, profile: Profile) -> None:
        self.following.remove(profile)

    def is_following(self, profile: Profile) -> bool:
        return self.following.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile: Profile) -> bool:
        return self.followed_by.filter(pk=profile.pk).exists()
