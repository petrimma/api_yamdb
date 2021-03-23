from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    user = 'user', 'Пользователь'
    moderator = 'moderator', 'Модератор'
    admin = 'admin', 'Администратор'


class User(AbstractUser):
    bio = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.user
    )
    confirmation_code = models.CharField(max_length=40,
                                         null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)
