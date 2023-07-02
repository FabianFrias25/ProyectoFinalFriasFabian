from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Equipos, Posiciones, Fixture
from .forms import RegistrationForm


def Inicio(request):
    return render(request, 'AppFutbolArg/Inicio.html')


def ver_equipos(request):
    return render(request, 'AppFutbolArg/Equipos.html')


def ver_fixture(request):
    partidos = Fixture.objects.order_by('dia', 'hora')
    return render(request, 'AppFutbolArg/Fixture.html', {'partidos': partidos})


def ver_posiciones(request):
    posiciones = Posiciones.objects.order_by('-puntos', 'partidosJugados')
    return render(request, 'AppFutbolArg/Posiciones.html', {'posiciones': posiciones})


def ver_equipo(request):
    if "Nombre" in request.GET:
        nombre = request.GET["Nombre"]
        equipo = Equipos.objects.filter(nombre=nombre)
        return render(request, "AppFutbolArg/getEquipos.html", {"equipo": equipo})


def registro(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = RegistrationForm()
    return render(request, 'AppFutbolArg/registro.html', {'form': form})


def ver_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'AppFutbolArg/login.html', {'error': 'Nombre de usuario o contraseña incorrectos.'})
    return render(request, 'AppFutbolArg/login.html')


@login_required
def prode(request):
    if request.method == 'POST':
        fixture_id = request.POST.get('fixture_id')
        resultado_local = request.POST.get('resultado_local')
        resultado_visitante = request.POST.get('resultado_visitante')

        fixture = Fixture.objects.get(id=fixture_id)
        usuario = request.user

        prode, created = Prode.objects.get_or_create(fixture=fixture, usuario=usuario)
        prode.resultadoLocal = resultado_local
        prode.resultadoVisitante = resultado_visitante
        prode.save()

        return render(request, 'AppFutbolArg/Prode.html')

    return render(request, 'AppFutbolArg/Prode.html')