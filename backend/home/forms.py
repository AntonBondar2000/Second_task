from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = {'username', 'password'}
