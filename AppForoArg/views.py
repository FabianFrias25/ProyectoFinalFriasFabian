from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Mensajes
from .forms import MensajeForm
from django.utils import timezone
import pytz


@login_required
def foro(request):
    mensajes = Mensajes.objects.all()
    form = MensajeForm()

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.autor = request.user
            mensaje.enviado = timezone.now()
            tz = pytz.timezone('America/Argentina/Buenos_Aires')  # Zona horaria de Argentina
            mensaje.enviado = mensaje.enviado.astimezone(tz)
            mensaje.save()
            return redirect('AppForoArg:foro')

    return render(request, 'AppForoArg/foro.html', {'mensajes': mensajes, 'form': form})


@login_required
def eliminar_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(Mensajes, id=mensaje_id)

    if not request.user.is_superuser:
        return redirect('nombre_de_la_vista_de_error')

    mensaje.delete()
    return redirect('AppForoArg:foro')
