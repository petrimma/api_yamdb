from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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


class Comment:
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
