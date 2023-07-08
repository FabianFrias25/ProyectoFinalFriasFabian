# from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Equipos, Posiciones, Fixture, Blogs, Avatar, UserProfile
from .forms import RegistrationForm, UserEditForm, BlogForm, AvatarForm, ChangePasswordForm


# FUTBOL:

def Inicio(request):
    return render(request, 'AppFutbolArg/Inicio.html')


def ver_equipos(request):
    return render(request, 'AppFutbolArg/Equipos.html')


def ver_fixture(request):
    partidos = Fixture.objects.order_by('dia', 'hora')
    return render(request, 'AppFutbolArg/Fixture.html', {'partidos': partidos})


def ver_posiciones(request):
    posiciones = Posiciones.objects.order_by('-puntos', '-difgol')
    return render(request, 'AppFutbolArg/Posiciones.html', {'posiciones': posiciones})


def ver_equipo(request):
    if "Nombre" in request.GET:
        nombre = request.GET["Nombre"]
        equipo = Equipos.objects.filter(nombre=nombre)
        return render(request, "AppFutbolArg/getEquipos.html", {"equipos": equipo})


# PERFIL

def registro(request):
    if request.user.is_authenticated:
        return redirect('Inicio')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()  # Guardar el usuario registrado
                nacionalidad = form.cleaned_data['nacionalidad']
                nacimiento = form.cleaned_data['nacimiento']
                hincha = form.cleaned_data['hincha']

                perfil = UserProfile(user=user, nacionalidad=nacionalidad, nacimiento=nacimiento, hincha=hincha)
                perfil.save()

                return redirect('../login')
        else:
            form = RegistrationForm()
        return render(request, 'AppFutbolArg/registro.html', {'form': form})


def ver_login(request):
    if request.user.is_authenticated:
        return redirect('Inicio')
    else:
        if request.method == 'POST':
            username = request.POST['user']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'AppFutbolArg/Inicio.html')
            else:
                return render(request, 'AppFutbolArg/login.html', {'error': 'Nombre de usuario o contraseña '
                                                                            'incorrectos.'})
        return render(request, 'AppFutbolArg/login.html')


@login_required
def ver_perfil(request):
    usuario = request.user
    try:
        perfil = UserProfile.objects.get(user=usuario)
    except UserProfile.DoesNotExist:
        perfil = None

    avatar = getavatar(request)
    return render(request, 'AppFutbolArg/Perfil/perfil.html', {'avatar': avatar, 'perfil': perfil})


@login_required
def editarPerfil(request):
    usuario = request.user
    try:
        perfil = UserProfile.objects.get(user=usuario)
    except UserProfile.DoesNotExist:
        perfil = None

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()

            # Actualizar los campos en el perfil
            perfil.nacionalidad = form.cleaned_data['nacionalidad']
            perfil.nacimiento = form.cleaned_data['nacimiento']
            perfil.hincha = form.cleaned_data['hincha']
            perfil.save()

            return redirect('perfil')
    else:
        form = UserEditForm(instance=usuario)

    return render(request, 'AppFutbolArg/Perfil/editarPerfil.html', {"form": form, "perfil": perfil})


@login_required
def changePassword(request):
    usuario = request.user

    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=usuario)
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            if new_password1 == new_password2:
                form.save()
                update_session_auth_hash(request, usuario)
                return redirect('perfil')
            else:
                error_message = "Las contraseñas no coinciden"
                return render(request, 'AppFutbolArg/Perfil/cambiarPassword.html',
                              {"form": form, "error_message": error_message})
    else:
        form = ChangePasswordForm(user=usuario)

    return render(request, 'AppFutbolArg/Perfil/cambiarPassword.html', {"form": form})


@login_required
def getavatar(request):
    try:
        avatar = Avatar.objects.filter(user=request.user).first()
        if avatar:
            return avatar.image.url
    except Avatar.DoesNotExist:
        pass
    return None


@login_required
def editAvatar(request):
    try:
        avatar = Avatar.objects.filter(user=request.user).first()
    except Avatar.DoesNotExist:
        avatar = Avatar(user=request.user)  # Crea un nuevo objeto Avatar para el usuario

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=avatar)  # Usa el objeto Avatar existente
        if form.is_valid():
            avatar = form.save(commit=False)
            avatar.user = request.user  # Asigna el usuario al objeto Avatar
            avatar.save()  # Guarda el objeto Avatar actualizado
            return redirect('perfil')
    else:
        form = AvatarForm(instance=avatar)  # Usa el objeto Avatar existente

    return render(request, "AppFutbolArg/Perfil/avatar.html", {'form': form})


# BLOGS:

@login_required
def ver_blogs(request):
    blogs = Blogs.objects.all()
    return render(request, 'AppFutbolArg/Blogs/blogs.html', {'blogs': blogs})


@login_required
def detalle_blog(request, blog_id):
    blog = get_object_or_404(Blogs, pk=blog_id)
    return render(request, 'AppFutbolArg/Blogs/leermas.html', {'blog': blog})


@login_required
def bloguear(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.autor = request.user
            blog.save()
            return redirect('Blogs')
    else:
        form = BlogForm()
    return render(request, 'AppFutbolArg/Blogs/bloguear.html', {'form': form})


@login_required
def editar_blog(request, blog_id):
    blog = get_object_or_404(Blogs, pk=blog_id)

    if request.user != blog.autor and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para editar este blog.")

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('detalle_blog', blog_id=blog_id)
    else:
        form = BlogForm(instance=blog)

    return render(request, 'AppFutbolArg/Blogs/editar_blog.html', {'form': form, 'blog': blog})


@login_required
def eliminar_blog(request, blog_id):
    blog = get_object_or_404(Blogs, pk=blog_id)

    if request.user != blog.autor and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para eliminar este blog.")

    if request.method == 'POST':
        blog.delete()
        return redirect('Blogs')

    return render(request, 'AppFutbolArg/Blogs/eliminar_blog.html', {'blog': blog})
