from django.db import models
from django.contrib.auth.models import User


class Mensajes(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    enviado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.username} - {self.enviado}"

    class Meta:
        verbose_name_plural = "Mensajes"
        ordering = ('enviado',)
