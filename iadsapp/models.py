from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Game(User):
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class GameType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Rating(models.Model):
    rating = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        return f"Rating: {self.rating}"


class GameDetail(models.Model):
    # Define fields
    game_name = models.CharField(max_length=200)
    game_image = models.ImageField(upload_to='game_images/')
    game_production = models.CharField(max_length=200)
    game_release = models.DateField()
    game_platform = models.CharField(max_length=100)
    game_rating = models.DecimalField(max_digits=3, decimal_places=1)
    game_bio = models.TextField()

    # Define foreign key to GameType
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)

    def __str__(self):
        return self.game_name


class GameNew(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='news_images/')
    bio = models.TextField()
    description = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title


class UpcomingRelease(models.Model):
    country = models.CharField(max_length=100)
    game_name = models.CharField(max_length=200)
    game_release_date = models.DateField()
    game_image = models.ImageField(upload_to='upcoming_images/')

    def __str__(self):
        return self.game_name


class Award(models.Model):
    award_name = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.award_name

