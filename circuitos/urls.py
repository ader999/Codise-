from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, PerfilView, CiudadViewSet,
    CircuitoCreativoViewSet, PuntoInteresViewSet,
    ProtagonistaViewSet, ProductoServicioViewSet, EventoViewSet
)

router = DefaultRouter()
router.register(r'ciudades', CiudadViewSet, basename='ciudad')
router.register(r'circuitos', CircuitoCreativoViewSet, basename='circuito')
router.register(r'puntos-interes', PuntoInteresViewSet, basename='puntointeres')
router.register(r'protagonistas', ProtagonistaViewSet, basename='protagonista')
router.register(r'productos', ProductoServicioViewSet, basename='producto')
router.register(r'eventos', EventoViewSet, basename='evento')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
]
