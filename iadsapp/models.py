from django.contrib.auth.models import User
from django.db import models
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


class GameDetails(models.Model):
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


from django.db import models

# Create your models here.
