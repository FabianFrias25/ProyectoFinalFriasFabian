from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Blogs, Avatar


class RegistrationForm(UserCreationForm):
    nacionalidad = forms.CharField(max_length=100)
    nacimiento = forms.DateField()
    hincha = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nacionalidad', 'nacimiento', 'hincha']


class UserEditForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Email"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    nacionalidad = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nacionalidad"}))
    hincha = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Hincha de"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'nacionalidad', 'hincha']
        help_texts = {k: "" for k in fields}


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['titulo', 'subtitulo', 'cuerpo', 'imagen']


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']
