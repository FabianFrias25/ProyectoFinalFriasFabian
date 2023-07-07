from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Equipos, Posiciones, Fixture, Blogs, Avatar
from .forms import RegistrationForm, UserEditForm, BlogForm, AvatarForm


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


def registro(request):
    if request.user.is_authenticated:
        return redirect('Inicio')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
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
def ver_perfil(request):
    return render(request, 'AppFutbolArg/Perfil/perfil.html')


@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return render(request, 'AppFutbolArg/Perfil/perfil.html')
    else:
        form = UserEditForm(instance=usuario)
    return render(request, 'AppFutbolArg/Perfil/editarPerfil.html', {"form": form})


def editAvatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            avatar = Avatar(user=user, image=form.cleaned_data['avatar'], id=request.user.id)
            avatar.save()
            avatar = Avatar.objects.filter(user=request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render(request, "AppFutbolArg/Inicio.html", {'avatar': avatar})
    else:
        try:
            avatar = Avatar.objects.filter(user=request.user.id)
            form = AvatarForm()
        except:
            form = AvatarForm()
    return render(request, "AppFutbolArg/Perfil/avatar.html", {'form': form})


def getavatar(request):
    avatar = Avatar.objects.filter(user=request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return avatar


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
