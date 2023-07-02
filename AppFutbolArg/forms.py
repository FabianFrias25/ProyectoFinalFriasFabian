from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    nacionalidad = forms.CharField(max_length=100)
    nacimiento = forms.DateField()
    hincha = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nacionalidad', 'nacimiento', 'hincha']

