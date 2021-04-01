from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    bio = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    confirmation_code = models.CharField(max_length=8,
                                         null=True, blank=True)
    is_code_expired = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)

    def __str__(self):
        return User.username


class Genre(models.Model):
    name = models.CharField('Название жанра', unique=True, max_length=20)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название категории', unique=True, max_length=20)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=20)
    year = models.IntegerField('Год выпуска', blank=True, null=True)
    description = models.TextField('Описание', max_length=400, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='genres')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 verbose_name='categories')

    def validate_year(self, value):
        if value < 1900 or value > datetime.now().year:
            raise ValidationError(
                f'{value} is is not a correct year!',
                params={'value': value},
            )

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'
        ordering = ('-name',)


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
        Title, on_delete=models.CASCADE, related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(choices=Score.choices)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    def __str__(self):
        return self.text
