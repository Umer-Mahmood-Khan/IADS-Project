from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from .models import GameDetail


from iadsapp.models import GameType, GameDetail, UpcomingRelease


def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')  # Or wherever you want to redirect users after login
        else:
            # Return an 'invalid login' error message.
            return HttpResponse('Invalid login details')
    else:
        # Return your login template here or just a simple placeholder for this example
        return HttpResponse('Login form goes here')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:
            # Check if the username or email already exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return HttpResponse('Username or email already exists. Please choose a different one.')

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Redirect to the login page after successful registration
            return redirect('login')  # Update 'login' to your actual login URL
        else:
            return HttpResponse('Passwords do not match. Please try again.')

    return HttpResponse('Sign-up form goes here')  # You can return an HTML form directly in this example


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
    return HttpResponse('Welcome to the Homepage!')


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
