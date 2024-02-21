from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse


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
