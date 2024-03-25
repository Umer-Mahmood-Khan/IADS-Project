from django.contrib import admin
from django.db import models
from .models import Game, GameType, Rating, GameDetail, GameNew, UpcomingRelease, Award, UserProfile, CustomUser, UserReview

# Register your models here.
admin.site.register(Game)
admin.site.register(GameType)
admin.site.register(Rating)
admin.site.register(GameDetail)
admin.site.register(GameNew)
admin.site.register(UpcomingRelease)
admin.site.register(Award)
admin.site.register(UserProfile)
admin.site.register(UserReview)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'profile_pic']  # Customize the fields displayed in the admin list view

admin.site.register(CustomUser, CustomUserAdmin)