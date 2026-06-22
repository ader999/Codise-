from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    es_protagonista = models.BooleanField(default=False)
    es_turista = models.BooleanField(default=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)

    def __str__(self):
        return self.username


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    imagen_portada = models.ImageField(upload_to='ciudades/portadas/')
    latitud_centro = models.FloatField()
    longitud_centro = models.FloatField()

    class Meta:
        verbose_name_plural = "Ciudades"

    def __str__(self):
        return self.nombre


class CircuitoCreativo(models.Model):
    DIFICULTAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]

    ciudad = models.ForeignKey(Ciudad, related_name='circuitos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    distancia_km = models.DecimalField(max_digits=5, decimal_places=2)
    duracion_estimada = models.CharField(max_length=50)
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES, default='Baja')
    imagen_mapa = models.ImageField(upload_to='circuitos/mapas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad.nombre})"


class PuntoInteres(models.Model):
    CATEGORIA_CHOICES = [
        ('Cultural', 'Cultural'),
        ('Historico', 'Histórico'),
        ('Natural', 'Natural'),
        ('Gastronomico', 'Gastronómico'),
        ('Taller Artesanal', 'Taller Artesanal'),
        ('Hospedaje', 'Hospedaje'),
        ('Otro', 'Otro'),
    ]

    circuito = models.ForeignKey(CircuitoCreativo, related_name='puntos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES, default='Cultural')
    latitud = models.FloatField()
    longitud = models.FloatField()
    imagen = models.ImageField(upload_to='puntos/imagenes/')
    audio_guia = models.FileField(upload_to='puntos/audios/', blank=True, null=True)
    visita_virtual_url = models.URLField(blank=True, null=True)
    saberes_populares = models.TextField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Puntos de Interés"

    def __str__(self):
        return f"{self.orden}. {self.nombre} ({self.circuito.nombre})"


class Protagonista(models.Model):
    CATEGORIA_PROT_CHOICES = [
        ('Artesania', 'Artesanía / Pintura'),
        ('Gastronomia', 'Gastronomía Tradicional'),
        ('Hospedaje', 'Hospedaje Familiar'),
        ('Servicios Turisticos', 'Servicios Turísticos y Guía'),
        ('Otro', 'Otro'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='protagonista')
    nombre_negocio = models.CharField(max_length=150)
    descripcion = models.TextField()
    ciudad = models.ForeignKey(Ciudad, related_name='protagonistas', on_delete=models.SET_NULL, null=True)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_PROT_CHOICES, default='Artesania')
    telefono = models.CharField(max_length=20)
    redes_sociales = models.JSONField(default=dict, blank=True)
    verificado = models.BooleanField(default=False)
    punto_interes_asociado = models.ForeignKey(PuntoInteres, related_name='protagonistas', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_negocio} - {self.user.get_full_name() or self.user.username}"


class ProductoServicio(models.Model):
    protagonista = models.ForeignKey(Protagonista, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    es_emblematico = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Producto o Servicio"
        verbose_name_plural = "Productos y Servicios"

    def __str__(self):
        return f"{self.nombre} - {self.protagonista.nombre_negocio}"


class Evento(models.Model):
    CATEGORIA_EVENTO_CHOICES = [
        ('Feria', 'Feria / Exposición'),
        ('Taller', 'Taller Educativo o Creativo'),
        ('ExpoVenta', 'Expo-Venta'),
        ('Cultural', 'Presentación Cultural / Tradicional'),
        ('Otro', 'Otro'),
    ]

    ciudad = models.ForeignKey(Ciudad, related_name='eventos', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    imagen = models.ImageField(upload_to='eventos/')
    categoria = models.CharField(max_length=30, choices=CATEGORIA_EVENTO_CHOICES, default='Feria')
    protagonista_organizador = models.ForeignKey(Protagonista, related_name='eventos_organizados', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.ciudad.nombre})"


class Resena(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resenas')
    punto_interes = models.ForeignKey(PuntoInteres, on_delete=models.CASCADE, related_name='resenas')
    calificacion = models.PositiveIntegerField()
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'punto_interes')
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Reseña de {self.user.username} para {self.punto_interes.nombre} ({self.calificacion}/5)"
