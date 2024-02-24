from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

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


def game_type_view(request):
    game_types = GameType.objects.all()
    response=HttpResponse()
    for game in game_types:
        response.write(game.name + '\n')
    return response

def game_detail_view(request, game_type_id):
    try:
        game_type = GameType.objects.get(id=game_type_id)
        game_details = GameDetail.objects.filter(game_type=game_type)
        response = HttpResponse(content_type="text/plain")
        for game_detail in game_details:
            response.write(f"Game Name: {game_detail.game_name}\n")
            response.write(f"Game Image: {game_detail.game_image}\n")
            response.write(f"Production: {game_detail.game_production}\n")
            response.write(f"Release Date: {game_detail.game_release}\n")
            response.write(f"Platform: {game_detail.game_platform}\n")
            response.write(f"Rating: {game_detail.game_rating}\n")
            response.write(f"Bio: {game_detail.game_bio}\n")
            response.write("\n")  # Add an empty line after each game detail
    except GameType.DoesNotExist:
        response = HttpResponse("Game type does not exist", content_type="text/plain", status=404)
    return response

def upcoming_release_view(request):
    upcoming_releases = UpcomingRelease.objects.all()
    response = HttpResponse(content_type="text/plain")
    for release in upcoming_releases:
        response.write(f"Game Name: {release.game_name}\n")
        response.write(f"Game Image: {release.game_image}\n")
        response.write(f"Country: {release.country}\n")
        response.write(f"Release Date: {release.game_release_date}\n\n")
    return response
