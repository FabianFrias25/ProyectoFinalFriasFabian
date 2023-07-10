from django.db import models
from AppFutbolArg.models import UserProfile


class Mensaje(models.Model):
    autor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    contenido = models.TextField()
    enviado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.user.username} - {self.enviado}"

    class Meta:
        verbose_name_plural = "Mensajes"
