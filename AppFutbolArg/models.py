from django.db import models
from django.contrib.auth.models import User


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
    ganados = models.IntegerField(default=0)
    empatados = models.IntegerField(default=0)
    perdidos = models.IntegerField(default=0)
    difgol = models.IntegerField(default=0)

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


def blog_image_path(instance, filename):
    return f'blogs/{instance.id}/{filename}'


class Blogs(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to=blog_image_path)

    def __str__(self):
        return f'{self.titulo} - {self.autor}'

    class Meta:
        verbose_name_plural = "Blogs"


def avatar_image_path(instance, filename):
    return f'avatares/{instance.id}/{filename}'


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=avatar_image_path, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Avatar"
