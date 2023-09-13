from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from utils.models import TrackObjectStateMixin


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, password=None, username: str = None, **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.username = username
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(TrackObjectStateMixin, AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True)
    # username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email
