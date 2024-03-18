# accounts/urls.py
from django.urls import path
from . import views
from .views import signup, signin_view, signin1, logout_view
from django.conf import settings
from django.conf.urls.static import static
from .views import awards_list, award_detail

from .views import calendar_view

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('signin1/', signin1, name='signin1'),
    path('signin/', signin_view, name='signin'),
    path('signup/', signup, name='signup'),
    path('', views.homepage_view, name='homepage'),
    path('profile/', views.profilepage_view, name='profilepage_view'),
    path('search/', views.search_view, name='search_view'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('game_type/', views.game_type_view, name='game_type'),
    path('most_popular_games/', views.most_popular_games_view, name='most_popular_games'),
    path('upcoming_releases/', views.upcoming_release_view, name='upcoming_releases'),
    path('top100/', views.top100_games, name='top100_games'),
    path('game_detail/<int:game_id>/', views.game_detail_view, name='game_detail'),
    path('game_news/', views.game_news, name='game_news'),


    path('games_by_genre/<int:game_type_id>/', views.games_by_genre_view, name='games_by_genre'),
    path('awards_list/', views.awards_list, name='awards_list'),  # Update 'views.awards' to 'views.awards_list'
    path('award_detail/<int:award_id>/', award_detail, name='award_detail'),
    path('calendar/', calendar_view, name='calendar'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    #path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/uidb64/token/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('privacy_notice/', views.privacy_notice, name='privacy_notice'),
    path('terms/', views.terms, name='terms'),
    path('user_policy/', views.user_policy, name='user_policy'),
    path('team_details/', views.team_details, name='team_details'),


    path('awards_list/', views.awards_list, name='awards_list'),  # Update 'views.awards' to 'views.awards_list'
    path('award_detail/<int:award_id>/', award_detail, name='award_detail'),
path('upcoming-releases/', views.upcoming_release_view, name='upcoming_releases'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
