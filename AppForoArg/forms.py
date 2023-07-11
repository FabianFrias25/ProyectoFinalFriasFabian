from django import forms
from AppForoArg.models import Mensajes

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensajes
        fields = ('contenido',)
