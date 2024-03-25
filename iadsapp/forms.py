from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile, Review, RATE_CHOICES


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User



'''
class UpdateUserForm(UserChangeForm):
    # Hide Password stuff
    password = None
    # Get other fields
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
    #first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
    #last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

    class Meta:
        model = UserProfile
        fields = ('FirstName', 'LastName','email')
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

'''
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Old Password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})


from .models import CustomUser

class EditProfileForm(forms.ModelForm):
    #bio = forms.CharField(max_length=500, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), max_length=500, required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_pic']

#forgot password
# forms.py

from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RatingCommentForm(forms.Form):
    comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)
    ratings = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(11)],
        widget=forms.Select(attrs={'class': 'browser-default'}))