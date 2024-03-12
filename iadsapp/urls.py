# accounts/urls.py
from django.urls import path
from . import views
from .views import signup, signin_view, signin1
from django.conf import settings
from django.conf.urls.static import static
from .views import awards_list, award_detail

urlpatterns = [
    path('signin1/', signin1, name='signin1'),
    path('signin/', signin_view, name='signin'),
    path('signup/', signup, name='signup'),
    path('', views.homepage_view, name='homepage'),
    path('search/', views.search_view, name='search_results'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('game_type/', views.game_type_view, name='game_type'),
    # path('game_detail/<int:game_type_id>/', views.game_detail_view, name='game_detail'),
    path('most_popular_games/', views.most_popular_games_view, name='most_popular_games'),
    path('upcoming_releases/', views.upcoming_release_view, name='upcoming_releases'),
    path('top100/', views.top100_games, name='top100_games'),
    path('game_detail/<int:game_id>/', views.game_detail_view, name='game_detail'),
    path('game_news/', views.game_news, name='game_news'),
#<<<<<<< Updated upstream
    path('games_by_genre/<int:game_type_id>/', views.games_by_genre_view, name='games_by_genre'),
#=======

    path('awards_list/', views.awards_list, name='awards_list'),  # Update 'views.awards' to 'views.awards_list'
    path('award_detail/<int:award_id>/', award_detail, name='award_detail'),
#>>>>>>> Stashed changes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)