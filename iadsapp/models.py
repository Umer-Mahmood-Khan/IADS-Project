from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.contrib.auth.hashers import make_password


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


class Award(models.Model):
    award_name = models.CharField(max_length=100, unique=True)
    award_date = models.DateField(default=date.today)  # Set default value to today's date
    award_description = models.TextField(default='')

    game_name = models.CharField(max_length=100, default='')  # Remove unique constraint


    game_name = models.CharField(max_length=100, unique=True, default='')


    def __str__(self):
        return self.award_name



# iadsapp/models.py
from django.db import models


class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()


class UserProfile(models.Model):
    FirstName = models.CharField(max_length=50, default='')
    LastName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed password
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.FirstName



RATE_CHOICES = [
    (1, '1 - Unplayable'),
    (2, '2 - Awful'),
    (3, '3 - Poor'),
    (4, '4 - Mediocre'),
    (5, '5 - Average'),
    (6, '6 - Decent'),
    (7, '7 - Good'),
    (8, '8 - Very Good'),
    (9, '9 - Excellent'),
    (10, '10 - Outstanding'),
]

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=3000,blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, blank=True)
    likes = models.PositiveIntegerField(default=0)
    unlikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username