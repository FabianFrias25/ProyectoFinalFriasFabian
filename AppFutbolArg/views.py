from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Equipos, Posiciones, Fixture, Blogs
from .forms import RegistrationForm


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
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'AppFutbolArg/login.html')
    else:
        form = RegistrationForm()
    return render(request, 'AppFutbolArg/registro.html', {'form': form})


def ver_login(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'AppFutbolArg/Inicio.html')
        else:
            return render(request, 'AppFutbolArg/login.html', {'error': 'Nombre de usuario o contraseña incorrectos.'})
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
@login_required
def bloguear(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.autor = request.user
            blog.save()
            return render(request, 'AppFutbolArg/Blogs/blogs.html')
    else:
        form = BlogForm()
    return render(request, 'AppFutbolArg/Blogs/bloguear.html', {'form': form})
