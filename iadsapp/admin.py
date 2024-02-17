from django.contrib import admin
from django.db import models
from .models import Game, GameType, Rating, GameDetails

# Register your models here.
admin.site.register(Game)
admin.site.register(GameType)
admin.site.register(Rating)
admin.site.register(GameDetails)

