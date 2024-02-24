# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/<str:username>/', views.forgot_password_view, name='forgot-password'),
    path('', views.homepage_view, name='homepage'),
    path('search/', views.search_view, name='search_results'),
    path('profile/', views.profile_view, name='profile'),
    path('game_type/', views.game_type_view, name='game_type'),
    path('game_detail/<int:game_type_id>/', views.game_detail_view, name='game_detail'),
    path('upcoming_releases/', views.upcoming_release_view, name='upcoming_releases'),

]