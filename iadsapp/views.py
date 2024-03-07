from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from .models import GameDetail
from .forms import SignUpForm, SignInForm

from iadsapp.models import GameType, GameDetail, UpcomingRelease


def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            # Perform authentication and redirect to the home page if successful
            # For simplicity, assume authentication is successful and redirect to the home page
            return redirect('home')
    else:
        form = SignInForm()

    return render(request, 'signin.html', {'signin_form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Check if passwords match
            if form.cleaned_data['password'] == form.cleaned_data['reenter_password']:
                # Save the user profile if the passwords match
                form.save()
                return redirect('signup_success')  # Redirect to a success page or login page
            else:
                form.add_error('reenter_password', 'Passwords do not match.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def forgot_password_view(request, username):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                # Find the user based on the provided username
                user = User.objects.get(username=username)

                # Reset the user's password
                user.set_password(new_password)
                user.save()

                return HttpResponse('Password reset successfully. You can now log in with your new password.')
            except User.DoesNotExist:
                return HttpResponse('User not found. Please check the username and try again.')
        else:
            return HttpResponse('Passwords do not match. Please try again.')

    return HttpResponse('Forgot password form goes here')  # You can return an HTML form directly in this example


def homepage_view(request):
    return render(request, 'index.html')


def search_view(request):
    return HttpResponse('Welcome to the Search Results!')


def profile_view(request):
    return HttpResponse('Profile page!')


#@login_required
def edit_profile_view(request):
    return HttpResponse('Edit Profile Page!')


def game_type_view(request):
    game_types = GameType.objects.all()
    return render(request,'game_types.html',{'game_types':game_types})


def game_detail_view(request, game_type_id):
        game_type = GameType.objects.get(id=game_type_id)
        game_details = GameDetail.objects.filter(game_type=game_type)

        return render(request,'game_detail.html',{'game_details':game_details})


def upcoming_release_view(request):
    upcoming_releases = UpcomingRelease.objects.all()
    response = HttpResponse(content_type="text/plain")
    for release in upcoming_releases:
        response.write(f"Game Name: {release.game_name}\n")
        response.write(f"Game Image: {release.game_image}\n")
        response.write(f"Country: {release.country}\n")
        response.write(f"Release Date: {release.game_release_date}\n\n")
    return response


def most_popular_games_view(request):
    popular_games = GameDetail.objects.order_by('-game_rating')[:50]

    context = {
        'popular_games': popular_games,
    }

    return render(request, 'most_popular_games.html', context)



def top100_games(request):
    # Retrieve the top 100 games based on the rating in descending order
    top_games = GameDetail.objects.order_by('-game_rating')[:100]

    context = {
        'top_games': top_games,
    }

    return render(request, 'top100_games.html', context)
