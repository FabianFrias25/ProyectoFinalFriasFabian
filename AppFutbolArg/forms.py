from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
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
    nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={"placeholder": "Fecha de nacimiento (YYYY-MM-DD)"}),
    )
    nacionalidad = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nacionalidad"}))
    hincha = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Hincha de"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'nacimiento', 'nacionalidad', 'hincha']
        help_texts = {k: "" for k in fields}


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña actual"}),
        error_messages={
            'password_incorrect': "",
        },
    )

    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Nueva Contraseña"}),
    )

    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmar nueva Contraseña"}),
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['titulo', 'subtitulo', 'cuerpo', 'imagen']


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']
