from django.contrib import admin
from django.db import models
from .models import Game, GameType, Rating, GameDetail, GameNew, UpcomingRelease, Award, UserProfile

# Register your models here.
admin.site.register(Game)
admin.site.register(GameType)
admin.site.register(Rating)
admin.site.register(GameDetail)
admin.site.register(GameNew)
admin.site.register(UpcomingRelease)
admin.site.register(Award)
admin.site.register(UserProfile)

