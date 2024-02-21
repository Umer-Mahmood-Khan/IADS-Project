# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/<str:username>/', views.forgot_password_view, name='forgot-password'),
    path('', views.homepage_view, name='homepage'),
]