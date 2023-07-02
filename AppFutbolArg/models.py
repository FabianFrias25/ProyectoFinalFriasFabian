from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Equipos(models.Model):
    nombre = models.CharField(max_length=50)
    completo = models.CharField(max_length=100)
    fundacion = models.DateField()
    ligas = models.IntegerField(default=0)
    nacionales = models.IntegerField(default=0)
    internacionales = models.IntegerField(default=0)
    ciudad = models.CharField(max_length=100)
    apodo = models.CharField(max_length=50)
    estadio = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Equipos"


class Posiciones(models.Model):
    equipo = models.OneToOneField(Equipos, on_delete=models.CASCADE, null=True, blank=True)
    puntos = models.IntegerField()
    partidosJugados = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.equipo.nombre} - PJ: {self.partidosJugados}'

    class Meta:
        verbose_name_plural = "Posiciones"


class Fixture(models.Model):
    dia = models.DateField()
    hora = models.CharField(max_length=5)
    local = models.ForeignKey(Equipos, on_delete=models.CASCADE, related_name='fixtureLocal')
    visitante = models.ForeignKey(Equipos, on_delete=models.CASCADE, related_name='fixtureVisitante')
    resultadoLocal = models.IntegerField(blank=True, null=True)
    resultadoVisitante = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.dia} - {self.local.nombre} vs {self.visitante.nombre}'

    class Meta:
        verbose_name_plural = "Fixture"


class Prode(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    resultadoLocal = models.IntegerField()
    resultadoVisitante = models.IntegerField()

    def __str__(self):
        return self.usuario


def validate_positive_or_null(value):
    if value is not None and value < 0:
        raise ValidationError("El resultado debe ser un número positivo o nulo.")
