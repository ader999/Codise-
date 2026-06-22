from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Ciudad, CircuitoCreativo, PuntoInteres,
    Protagonista, ProductoServicio, Evento, Resena
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'es_protagonista', 'es_turista', 'telefono', 'foto_perfil')
        read_only_fields = ('id', 'es_protagonista', 'es_turista')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'es_protagonista', 'es_turista', 'telefono')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CiudadSerializer(serializers.ModelSerializer):
    circuitos_count = serializers.SerializerMethodField()

    class Meta:
        model = Ciudad
        fields = ('id', 'nombre', 'descripcion', 'imagen_portada', 'latitud_centro', 'longitud_centro', 'circuitos_count')

    def get_circuitos_count(self, obj):
        return obj.circuitos.count()


class CircuitoCreativoListSerializer(serializers.ModelSerializer):
    ciudad_nombre = serializers.CharField(source='ciudad.nombre', read_only=True)

    class Meta:
        model = CircuitoCreativo
        fields = ('id', 'ciudad', 'ciudad_nombre', 'nombre', 'descripcion', 'distancia_km', 'duracion_estimada', 'dificultad')


class ResenaSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Resena
        fields = ('id', 'user', 'username', 'punto_interes', 'calificacion', 'comentario', 'fecha_creacion')
        read_only_fields = ('id', 'user', 'fecha_creacion')

    def validate_calificacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5.")
        return value


class PuntoInteresSerializer(serializers.ModelSerializer):
    resenas = ResenaSerializer(many=True, read_only=True)
    calificacion_promedio = serializers.SerializerMethodField()

    class Meta:
        model = PuntoInteres
        fields = (
            'id', 'circuito', 'nombre', 'descripcion', 'categoria', 
            'latitud', 'longitud', 'imagen', 'audio_guia', 
            'visita_virtual_url', 'saberes_populares', 'orden', 
            'resenas', 'calificacion_promedio'
        )

    def get_calificacion_promedio(self, obj):
        resenas = obj.resenas.all()
        if not resenas:
            return 0
        total = sum(r.calificacion for r in resenas)
        return round(total / len(resenas), 1)


class CircuitoCreativoDetailSerializer(serializers.ModelSerializer):
    ciudad_nombre = serializers.CharField(source='ciudad.nombre', read_only=True)
    puntos = serializers.SerializerMethodField()

    class Meta:
        model = CircuitoCreativo
        fields = ('id', 'ciudad', 'ciudad_nombre', 'nombre', 'descripcion', 'distancia_km', 'duracion_estimada', 'dificultad', 'imagen_mapa', 'puntos')

    def get_puntos(self, obj):
        puntos_ordenados = obj.puntos.all().order_by('orden')
        return PuntoInteresSerializer(puntos_ordenados, many=True, context=self.context).data


class ProductoServicioSerializer(serializers.ModelSerializer):
    protagonista_nombre = serializers.CharField(source='protagonista.nombre_negocio', read_only=True)

    class Meta:
        model = ProductoServicio
        fields = ('id', 'protagonista', 'protagonista_nombre', 'nombre', 'descripcion', 'precio', 'imagen', 'es_emblematico')


class ProtagonistaSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    nombre_completo = serializers.SerializerMethodField()
    productos = ProductoServicioSerializer(many=True, read_only=True)
    ciudad_nombre = serializers.CharField(source='ciudad.nombre', read_only=True)

    class Meta:
        model = Protagonista
        fields = (
            'id', 'user', 'username', 'nombre_completo', 'nombre_negocio', 
            'descripcion', 'ciudad', 'ciudad_nombre', 'categoria', 
            'telefono', 'redes_sociales', 'verificado', 
            'punto_interes_asociado', 'productos'
        )
        read_only_fields = ('id', 'user', 'verificado')

    def get_nombre_completo(self, obj):
        return obj.user.get_full_name() or obj.user.username


class EventoSerializer(serializers.ModelSerializer):
    ciudad_nombre = serializers.CharField(source='ciudad.nombre', read_only=True)
    organizador_nombre = serializers.CharField(source='protagonista_organizador.nombre_negocio', read_only=True, default="Oficial / Red Ciudades Creativas")

    class Meta:
        model = Evento
        fields = (
            'id', 'ciudad', 'ciudad_nombre', 'titulo', 'descripcion', 
            'fecha_inicio', 'fecha_fin', 'lugar', 'latitud', 'longitud', 
            'imagen', 'categoria', 'protagonista_organizador', 'organizador_nombre'
        )
