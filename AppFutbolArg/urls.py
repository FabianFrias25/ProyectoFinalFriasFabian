from django.urls import path
from AppFutbolArg.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('inicio/', Inicio, name="Inicio"),
    path('equipos/', ver_equipos, name="Equipos"),
    path('posiciones/', ver_posiciones, name="Posiciones"),
    path('fixture/', ver_fixture, name="Fixture"),
    path('getequipo/', ver_equipo, name="ver_equipo"),
    path('blogs/', ver_blogs, name="Blogs"),
    path('blogs/bloguear/', bloguear, name='bloguear'),
    path('blogs/<int:blog_id>/', detalle_blog, name='detalle_blog'),
    path('registro/', registro, name="registro"),
    path('login/', ver_login, name="login"),
    path('perfil/', ver_perfil, name='perfil'),
    path('perfil/editarPerfil/', editarPerfil, name="editarPerfil"),
    path('perfil/cambiarAvatar/', editAvatar, name="editAvatar"),
    path('logout/', LogoutView.as_view(template_name='AppFutbolArg/login.html'), name="logout"),
]
