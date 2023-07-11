from django.urls import path
from AppForoArg.views import foro, eliminar_mensaje

app_name = 'AppForoArg'

urlpatterns = [
    path('foro/', foro, name="foro"),
    path('eliminar/<int:mensaje_id>/', eliminar_mensaje, name='eliminar_mensaje'),
]
