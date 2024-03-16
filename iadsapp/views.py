from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from .models import GameDetail, UpcomingRelease, GameType
from .forms import SignUpForm, SignInForm, UpdateUserForm,CustomPasswordResetForm
from django.shortcuts import render, get_object_or_404
from .models import GameDetail, GameType, GameNew
from .models import Award
from .models import CalendarEvent


def signin_view(request):
    error_message = None

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # User authenticated, log in the user
                login(request, user)
                return redirect('homepage')
            else:
                # Authentication failed, display error message
                error_message = 'Invalid email or password.'
    else:
        form = SignInForm()

    return render(request, 'signin.html', {'signin_form': form, 'error_message': error_message})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Check if passwords match
            if form.cleaned_data['password'] == form.cleaned_data['reenter_password']:
                # Save the user profile if the passwords match
                form.save()
                return redirect('signin')  # Redirect to the sign-in page
            else:
                form.add_error('reenter_password', 'Passwords do not match.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def signin1(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            # Add your authentication logic here
            # For example, checking credentials against the database
            return redirect('homepage')  # Replace 'home' with the URL of your home page
    else:
        form = SignInForm()

    return render(request, 'signin1.html', {'form': form})


def homepage_view(request):
    return render(request, 'index.html')

def profilepage_view(request):
    return render(request, 'profile.html')


def profile_view(request):
    return HttpResponse('Profile page!')


'''
def edit_profile_view(request):
    return render(request, 'edit_user.html', {})
'''
def edit_profile_view(request):
	#if request.user.is_authenticated:
		#current_user = User.objects.get(id=request.user.id)
		#user_form = UpdateUserForm(request.POST or None, instance=current_user)

		#if user_form.is_valid():
		#	user_form.save()

		#	login(request, current_user)
		#	messages.success(request, "User Has Been Updated!!")
		#	return redirect('homepage')
		#return render(request, "edit_user.html", {'user_form':user_form})

        return render(request, "edit_user.html", {})
	#else:
		#messages.success(request, "You Must Be Logged In To Access That Page!!")
		#return redirect('homepage')
#
def game_type_view(request):
    game_types = GameType.objects.all()
    return render(request,'game_types.html',{'game_types':game_types})


# View for game genre
#def games_by_genre_view(request):
 #   games_by_genre= GameType.objects.all()
  #  game_genre_selected= None
   # games=GameDetail.objects.all()

    # checking for game genre
    #games_by_genre_id=request.GET.get('game_by_genre_id')
    #if games_by_genre_id:
    #    game_genre_selected=get_object_or_404(GameType,pk=games_by_genre_id)
    #    games=games.filter(genre=game_genre_selected)

    #return render(request,'games_by_genre.html',{'games_by_genre':games_by_genre , 'game_genre_selected':game_genre_selected,'games':games})


def games_by_genre_view(request, game_type_id):
        game_genre = GameType.objects.get(id=game_type_id)
        sort_filter = request.GET.get('sort', '')
        games_by_genre = GameDetail.objects.filter(game_type=game_genre)

        if sort_filter == 'a_z':
            games_by_genre = games_by_genre.order_by('game_name')
        elif sort_filter == 'z_a':
            games_by_genre = games_by_genre.order_by('-game_name')
        elif sort_filter == 'rating':
            games_by_genre = games_by_genre.order_by('-game_rating')
        elif sort_filter == 'release_date':
            games_by_genre = games_by_genre.order_by('-game_release')


        return render(request,'games_by_genre.html',{'games_by_genre':games_by_genre})


def upcoming_release_view(request):
    upcoming_releases = UpcomingRelease.objects.all()
    response = HttpResponse(content_type="text/plain")
    for release in upcoming_releases:
        response.write(f"Game Name: {release.game_name}\n")
        response.write(f"Game Image: {release.game_image}\n")
        response.write(f"Country: {release.country}\n")
        response.write(f"Release Date: {release.game_release_date}\n\n")
    return response

# def awards(request):



def most_popular_games_view(request):
    popular_games = GameDetail.objects.order_by('-game_rating')[:50]

    context = {
        'popular_games': popular_games,
    }

    return render(request, 'most_popular_games.html', context)



def top100_games(request):
    sort_filter = request.GET.get('sort', '')

    if sort_filter == 'a_m':
        # Retrieve top 100 games with names starting from A to M
        top_games = GameDetail.objects.filter(game_name__istartswith='a') | GameDetail.objects.filter(game_name__istartswith='b') | GameDetail.objects.filter(game_name__istartswith='c') | GameDetail.objects.filter(game_name__istartswith='d') | GameDetail.objects.filter(game_name__istartswith='e') | GameDetail.objects.filter(game_name__istartswith='f') | GameDetail.objects.filter(game_name__istartswith='g') | GameDetail.objects.filter(game_name__istartswith='h') | GameDetail.objects.filter(game_name__istartswith='i') | GameDetail.objects.filter(game_name__istartswith='j') | GameDetail.objects.filter(game_name__istartswith='k') | GameDetail.objects.filter(game_name__istartswith='l') | GameDetail.objects.filter(game_name__istartswith='m')
    elif sort_filter == 'n_z':
        # Retrieve top 100 games with names starting from N to Z
        top_games = GameDetail.objects.filter(game_name__istartswith='n') | GameDetail.objects.filter(game_name__istartswith='o') | GameDetail.objects.filter(game_name__istartswith='p') | GameDetail.objects.filter(game_name__istartswith='q') | GameDetail.objects.filter(game_name__istartswith='r') | GameDetail.objects.filter(game_name__istartswith='s') | GameDetail.objects.filter(game_name__istartswith='t') | GameDetail.objects.filter(game_name__istartswith='u') | GameDetail.objects.filter(game_name__istartswith='v') | GameDetail.objects.filter(game_name__istartswith='w') | GameDetail.objects.filter(game_name__istartswith='x') | GameDetail.objects.filter(game_name__istartswith='y') | GameDetail.objects.filter(game_name__istartswith='z')
    else:
        # Retrieve the top 100 games based on the rating in descending order
        top_games = GameDetail.objects.order_by('-game_rating')[:100]

    context = {
        'top_games': top_games,
    }

    return render(request, 'top100_games.html', context)


def game_detail_view(request, game_id):
    # Fetch the GameDetail object based on game_id
    game = get_object_or_404(GameDetail, pk=game_id)

    # Prepare the context to pass to the template
    context = {
        'game': game,
    }

    # Render the template with the context
    return render(request, 'game_details.html', context)


def game_news(request):
    # Retrieve all game news objects from the database
    game_news = GameNew.objects.all()
    context = {
        'game_news': game_news
    }
    return render(request, 'game_news.html', context)



def awards_list(request):
    awards = Award.objects.all()

    return render(request, 'awards_list.html', {'awards': awards})


def award_detail(request, award_id):
    award = get_object_or_404(Award, pk=award_id)
    return render(request, 'award_detail.html', {'award': award})



def search_view(request):
    query = request.GET.get('q', '')
    game_type_name = request.GET.get('game_type', '')  # Retrieve game type name from the query parameters
    results = []

    # Fetch game types for populating the dropdown
    game_types = GameType.objects.all()
    # Pass game types to the template context
    context = {'game_types': game_types, 'query': query}

    # Filter games based on the provided game type name or search query
    if game_type_name:
        games = GameDetail.objects.filter(game_type__name__iexact=game_type_name)  # Filter games by game type name
        results = games
    else:
        results = GameDetail.objects.filter(game_name__icontains=query)

    context['results'] = results  # Add results to the template context

    return render(request, 'search_results.html', context)


def calendar_view(request):
    events = CalendarEvent.objects.all()
    return render(request, 'iadsapp/calendar.html', {'events': events})

#FORGOT PASSWORD
# views.py
from django.contrib.auth.forms import PasswordResetForm

def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})
