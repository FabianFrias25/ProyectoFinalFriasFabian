from django.urls import path
from AppFutbolArg.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('inicio/', Inicio, name="Inicio"),
    path('equipos/', ver_equipos, name="Equipos"),
    path('posiciones/', ver_posiciones, name="Posiciones"),
    path('fixture/', ver_fixture, name="Fixture"),
    path('getequipo/', ver_equipo, name="ver_equipo"),
    path('prode/', prode, name="Prode"),
    path('registro/', registro, name="registro"),
    path('login/', ver_login, name="login"),
    path('logout/', LogoutView.as_view(template_name='AppFutbolArg/login.html'), name="logout"),
]