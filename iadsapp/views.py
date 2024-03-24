from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from .models import GameDetail, UpcomingRelease, GameType
from .forms import CustomPasswordResetForm, RatingCommentForm
from django.shortcuts import render, get_object_or_404
from .models import GameDetail, GameType, GameNew
from .models import Award

from .models import CalendarEvent
from .models import UserProfile
from django.contrib.auth.hashers import check_password
from datetime import datetime
from django.contrib.auth import logout
from .models import UpcomingRelease
from datetime import date
from .models import CustomUser


from .models import CalendarEvent

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the User instance
            CustomUser.objects.create(user=user)
            return redirect('signin')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomAuthenticationForm  # Import your custom authentication form
from django.contrib.auth.models import User

def signin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not hasattr(user, 'customuser'):
                    CustomUser.objects.create(user=user)
                return redirect('homepage')  # Redirect to the homepage after successful login
            else:
                # Add an error message for invalid credentials
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('homepage')  # Redirect to the sign-in page after logout


#Umer: Home page view
# def homepage_view(request):
#     return render(request, 'index.html')



# def homepage_view(request):
#     visit_key=None
#     if request.user.is_authenticated: # if authenticated user
#         today_date = date.today()
#
#         # visit_key = f"visits_{request.user.id}_{request.user.username}-{today_date}"
#         visit_key = f"{request.user.username} visited the homepage at {today_date}"
#
#         print(visit_key)
#
#         print(request.session.keys())  # Print all keys in the session
#         print(request.session.get(visit_key))  # Print the value of 'visit_key' in the session
#
#
#         if visit_key in request.session:
#             request.session[visit_key] += 1
#         else:
#             request.session[visit_key] = 1
#
#     # Get the session visit count for the current day
#     today_visit_count = request.session.get(visit_key, 0)
#
#     # Set a cookie with an expiration time of 10 seconds
#     response = render(request, 'index.html')
#     response.set_cookie('homepage_visits', today_visit_count, max_age=100)
#
#     return response
#


def homepage_view(request):
    if request.user.is_authenticated:
        visit_key = 'homepage_visits'

        if visit_key not in request.session:
            request.session[visit_key] = []

        current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session[visit_key].append(current_time_str)

        # Limit the list to the last 5 visits
        request.session[visit_key] = request.session[visit_key][-15:]

        # Set cookies for username, visit count, and last visits
        response = HttpResponse(render(request, 'index.html'))
        response.set_cookie('username', request.user.username)
        response.set_cookie('homepage_visits', len(request.session[visit_key]))
        response.set_cookie('last_visits', ','.join(request.session[visit_key]))

        return response

    return render(request, 'index.html')



#Umer: Profile page view
# def profilepage_view(request):
#     return render(request, 'profile.html')
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
'''
@login_required
def profilepage_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})
'''
@login_required
def profilepage_view(request):
    user = request.user
    custom_user = CustomUser.objects.get(user=user)
    games_rated_count = GameRating.objects.filter(user=request.user).count()
    user_comments = GameComment.objects.filter(user=request.user)
    user_ratings = GameRating.objects.filter(user=request.user)

    last_visits_str = request.COOKIES.get('last_visits')

    last_visits = []
    if last_visits_str:
        last_visits = [datetime.strptime(visit, '%Y-%m-%d %H:%M:%S') for visit in last_visits_str.split(',')]

    print(last_visits)

    return render(request, 'profile.html', {'user': user, 'custom_user': custom_user, 'games_rated_count': games_rated_count, 'user_comments': user_comments, 'user_ratings': user_ratings,"last_visits": last_visits})

#Haari: Edit profile view
'''
def edit_profile_view(request):
    return render(request, 'edit_user.html', {})
'''
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
'''
from .forms import EditProfileForm
@login_required
def edit_profile_view(request):
    custom_user = request.user.customuser
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.customuser)
        if form.is_valid():
            form.save()
            return redirect('profilepage_view')
    else:
        form = EditProfileForm(instance=request.user.customuser)
    return render(request, 'edit_user.html', {'form': form, 'custom_user': custom_user})



from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import CustomPasswordChangeForm

def update_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            logout(request)  # Logout the user
            return redirect('signin')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'update_password.html', {'form': form})

#JasPreet: Game type view
def game_type_view(request):
    game_types = GameType.objects.all()
    return render(request,'game_types.html',{'game_types':game_types})


#Jaspreet: Games by Genre
def games_by_genre_view(request, game_type_id):
    game_genre = GameType.objects.get(id=game_type_id)
    sort_filter = request.GET.get('sort', '')
    search_query = request.GET.get('query', '')  # Get the search query
    games_by_genre = GameDetail.objects.filter(game_type=game_genre)

    # Apply sorting based on the sort_filter parameter
    if sort_filter == 'a_z':
        games_by_genre = games_by_genre.order_by('game_name')
    elif sort_filter == 'z_a':
        games_by_genre = games_by_genre.order_by('-game_name')
    elif sort_filter == 'rating':
        games_by_genre = games_by_genre.order_by('-game_rating')
    elif sort_filter == 'release_date':
        games_by_genre = games_by_genre.order_by('-game_release', 'id')

    # Apply search filtering if a search query is provided
    if search_query:
        games_by_genre = games_by_genre.filter(game_name__icontains=search_query)

    # Check if any games were found
    if not games_by_genre:  # If no games found
        message = "No games found "
    else:
        message = ""

    return render(request, 'games_by_genre.html', {'games_by_genre': games_by_genre, 'query': search_query, 'message': message})

#JasPreet: Upcoming releases
# def upcoming_release_view(request):
#     upcoming_releases = UpcomingRelease.objects.all()
#     response = HttpResponse(content_type="text/plain")
#     for release in upcoming_releases:
#         response.write(f"Game Name: {release.game_name}\n")
#         response.write(f"Game Image: {release.game_image}\n")
#         response.write(f"Country: {release.country}\n")
#         response.write(f"Release Date: {release.game_release_date}\n\n")
#     return response




@login_required
def upcoming_release_view(request):
    upcoming_releases = UpcomingRelease.objects.all()
    return render(request, 'upcoming_releases.html', {'upcoming_releases': upcoming_releases})


# def awards(request):


#Haari: Most popular games
'''
def most_popular_games_view(request):
    popular_games = GameDetail.objects.order_by('-game_rating')[:50]

    context = {
        'popular_games': popular_games,
    }

    return render(request, 'most_popular_games.html', context)
'''

def most_popular_games_view(request):
    sort_filter = request.GET.get('sort', '')
    search_query = request.GET.get('query', '')  # Get the search query
    popular_games = GameDetail.objects.all()

    # Apply sorting based on the sort_filter parameter
    if sort_filter == 'a_z':
        popular_games = popular_games.order_by('game_name')
    elif sort_filter == 'z_a':
        popular_games = popular_games.order_by('-game_name')
    elif sort_filter == 'rating':
        popular_games = popular_games.order_by('-game_rating')
    elif sort_filter == 'release_date':
        popular_games = popular_games.order_by('-game_release', 'id')

    popular_games = popular_games[:50]  # Slice the queryset after ordering

    context = {
        'popular_games': popular_games,
        'query': search_query,
        #'message': "No games found." if not popular_games else None
    }

    return render(request, 'most_popular_games.html', context)

#Chandana: Top 100 games
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


#Ruchi: Game details view
def game_detail_view(request, game_id):
    # Fetch the GameDetail object based on game_id
    game = get_object_or_404(GameDetail, pk=game_id)

    # Prepare the context to pass to the template
    context = {
        'game': game,
    }

    # Render the template with the context
    return render(request, 'game_details.html', context)


#Ruchi: Game news
def game_news(request):
    # Retrieve all game news objects from the database
    game_news = GameNew.objects.all()
    context = {
        'game_news': game_news
    }
    return render(request, 'game_news.html', context)



#Navjot: Awards list

# def awards_list(request):
#     awards = Award.objects.all()
#     return render(request, 'awards_list.html', {'awards': awards})

def awards_list(request):
    query = request.GET.get('search', '')

    # Filter awards based on the search query
    awards = Award.objects.filter(award_name__icontains=query)

# def awards_list(request):
#     awards = Award.objects.all()
#
#     return render(request, 'awards_list.html', {'awards': awards})

def awards_list(request):
    query = request.GET.get('search', '')

    # Filter awards based on the search query
    awards = Award.objects.filter(award_name__icontains=query)

    return render(request, 'awards_list.html', {'awards': awards})

#Navjot: Awards detail
def award_detail(request, award_id):
    award = get_object_or_404(Award, pk=award_id)
    return render(request, 'award_detail.html', {'award': award})


#Umer: Search view

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


#Navjot: Upcoming releases
def calendar_view(request):
    events = CalendarEvent.objects.all()
    return render(request, 'iadsapp/calendar.html', {'events': events})



# Chandana: FORGOT PASSWORD

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


#Chandana: FOOTER ITEMS
def privacy_notice(request):
    return render(request, 'privacy_notice.html')

def terms(request):
    return render(request, 'terms.html')

def user_policy(request):
    return render(request, 'user_policy.html')

def team_details(request):
    return render(request, 'team_details.html')

#
from django.contrib.auth.decorators import login_required
from .models import GameComment, GameRating
from .forms import RatingCommentForm

def game_detail_view(request, game_id):
    game = get_object_or_404(GameDetail, pk=game_id)
    comments = GameComment.objects.filter(game=game)
    ratings = GameRating.objects.filter(game=game)
    form = None

    if request.method == 'POST' and request.user.is_authenticated:
        form = RatingCommentForm(request.POST)
        if form.is_valid():
            GameRating.objects.create(
                game=game,
                user=request.user,
                rating=form.cleaned_data['ratings']  # Corrected rating field
            )
            GameComment.objects.create(
                game=game,
                user=request.user,
                comment=form.cleaned_data['comments']
            )
            return redirect('game_detail', game_id=game_id)
    elif request.user.is_authenticated:
        form = RatingCommentForm()

    context = {
        'game': game,
        'form': form,
        'comments': comments,
        'ratings': ratings,
    }

    return render(request, 'game_details.html', context)

