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

    class Meta:
        ordering=['game_type']


class GameNew(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='news_images/')
    bio = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title


class UpcomingRelease(models.Model):
    country = models.CharField(max_length=100)
    game_name = models.CharField(max_length=200)
    game_release_date = models.DateField()
    game_image = models.ImageField(upload_to='upcoming_images/')

    def __str__(self):
        return self.game_name


from django.db import models

from django.db import models
from datetime import date

class Award(models.Model):
    award_name = models.CharField(max_length=100, unique=True)
    award_date = models.DateField(default=date.today)  # Set default value to today's date
    award_description = models.TextField(default='')
    game_name = models.CharField(max_length=100, unique=True, default='')

    def __str__(self):
        return self.award_name





class UserProfile(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)