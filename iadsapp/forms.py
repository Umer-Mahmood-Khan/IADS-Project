from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile, Review, RATE_CHOICES


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['FirstName', 'LastName', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    reenter_password = forms.CharField(label='Re-enter Password', widget=forms.PasswordInput, min_length=8)


class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Perform custom validation for email and password if needed
        if not email:
            raise forms.ValidationError("Email field is required.")
        if not password:
            raise forms.ValidationError("Password field is required.")

        return cleaned_data


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


#forgot password
# forms.py

from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model: Review
        fields = ('text', 'rate')