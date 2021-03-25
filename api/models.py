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

    def __str__(self):
        return User.username


class Title(models.Model):
    pass


class Review(models.Model):

    class Score(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.IntegerField(choices=Score.choices)
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True
    )

    def __str__(self):
        return self.text
