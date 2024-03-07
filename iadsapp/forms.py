from django import forms
from .models import UserProfile


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    reenter_password = forms.CharField(label='Re-enter Password', widget=forms.PasswordInput, min_length=8)