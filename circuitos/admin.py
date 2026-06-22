from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Ciudad, CircuitoCreativo, PuntoInteres,
    Protagonista, ProductoServicio, Evento, Resena
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'es_protagonista', 'es_turista', 'is_staff')
    list_filter = ('es_protagonista', 'es_turista', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Roles y Perfil', {'fields': ('es_protagonista', 'es_turista', 'telefono', 'foto_perfil')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Roles y Perfil', {'fields': ('es_protagonista', 'es_turista', 'telefono', 'foto_perfil')}),
    )


@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud_centro', 'longitud_centro', 'ver_circuitos')
    search_fields = ('nombre',)

    def ver_circuitos(self, obj):
        count = obj.circuitos.count()
        return f"{count} circuito(s)"
    ver_circuitos.short_description = "Circuitos"


class PuntoInteresInline(admin.TabularInline):
    model = PuntoInteres
    extra = 1
    fields = ('orden', 'nombre', 'categoria', 'latitud', 'longitud', 'imagen')
    ordering = ('orden',)


@admin.register(CircuitoCreativo)
class CircuitoCreativoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'distancia_km', 'duracion_estimada', 'dificultad', 'ver_puntos')
    list_filter = ('ciudad', 'dificultad')
    search_fields = ('nombre', 'descripcion')
    inlines = [PuntoInteresInline]

    def ver_puntos(self, obj):
        count = obj.puntos.count()
        return f"{count} parada(s)"
    ver_puntos.short_description = "Paradas"


@admin.register(PuntoInteres)
class PuntoInteresAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'circuito', 'categoria', 'orden', 'latitud', 'longitud', 'tiene_audio', 'tiene_visita_virtual')
    list_filter = ('circuito__ciudad', 'circuito', 'categoria')
    search_fields = ('nombre', 'descripcion', 'saberes_populares')
    ordering = ('circuito', 'orden')

    def tiene_audio(self, obj):
        return bool(obj.audio_guia)
    tiene_audio.boolean = True
    tiene_audio.short_description = "Audio"

    def tiene_visita_virtual(self, obj):
        return bool(obj.visita_virtual_url)
    tiene_visita_virtual.boolean = True
    tiene_visita_virtual.short_description = "Visita 360°"


class ProductoServicioInline(admin.TabularInline):
    model = ProductoServicio
    extra = 1
    fields = ('nombre', 'precio', 'imagen', 'es_emblematico')


@admin.register(Protagonista)
class ProtagonistaAdmin(admin.ModelAdmin):
    list_display = ('nombre_negocio', 'user', 'ciudad', 'categoria', 'telefono', 'verificado', 'ver_productos')
    list_filter = ('ciudad', 'categoria', 'verificado')
    search_fields = ('nombre_negocio', 'descripcion', 'user__username', 'user__first_name', 'user__last_name')
    actions = ['verificar_protagonistas', 'desverificar_protagonistas']
    inlines = [ProductoServicioInline]

    def ver_productos(self, obj):
        count = obj.productos.count()
        return f"{count} producto(s)"
    ver_productos.short_description = "Productos"

    @admin.action(description="Marcar protagonistas seleccionados como Verificados")
    def verificar_protagonistas(self, request, queryset):
        queryset.update(verificado=True)
        self.message_user(request, "Los protagonistas seleccionados han sido verificados oficialmente.")

    @admin.action(description="Quitar verificación a protagonistas seleccionados")
    def desverificar_protagonistas(self, request, queryset):
        queryset.update(verificado=False)
        self.message_user(request, "Se ha retirado la verificación a los protagonistas seleccionados.")


@admin.register(ProductoServicio)
class ProductoServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'protagonista', 'precio', 'es_emblematico')
    list_filter = ('es_emblematico', 'protagonista__ciudad')
    search_fields = ('nombre', 'descripcion', 'protagonista__nombre_negocio')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ciudad', 'categoria', 'fecha_inicio', 'fecha_fin', 'lugar', 'organizado_por')
    list_filter = ('ciudad', 'categoria', 'fecha_inicio')
    search_fields = ('titulo', 'descripcion', 'lugar')
    ordering = ('fecha_inicio',)

    def organizado_por(self, obj):
        if obj.protagonista_organizador:
            return obj.protagonista_organizador.nombre_negocio
        return "Oficial / Red Ciudades Creativas"
    organizado_por.short_description = "Organizador"


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('user', 'punto_interes', 'calificacion', 'fecha_creacion')
    list_filter = ('calificacion', 'fecha_creacion')
    search_fields = ('user__username', 'punto_interes__nombre', 'comentario')
    readonly_fields = ('fecha_creacion',)
