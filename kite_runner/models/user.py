from datetime import datetime, timedelta
from typing import Optional

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: Optional[str], username: str) -> "User":
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, username: str) -> "User":
        user = self.create_user(email, password, username)
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    objects = UserManager()

    @property
    def is_superuser(self):
        return self.is_staff

    @property
    def token(self):
        return self._gererate_jwt_token()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _gererate_jwt_token(self) -> str:
        dt = datetime.now() + timedelta(days=60)
        return jwt.encode(
            {"id": self.pk, "exp": dt},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
