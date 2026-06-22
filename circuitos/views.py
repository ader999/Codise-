from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date
from .models import (
    Ciudad, CircuitoCreativo, PuntoInteres,
    Protagonista, ProductoServicio, Evento, Resena
)
from .serializers import (
    UserSerializer, RegisterSerializer, CiudadSerializer,
    CircuitoCreativoListSerializer, CircuitoCreativoDetailSerializer,
    PuntoInteresSerializer, ProtagonistaSerializer,
    ProductoServicioSerializer, EventoSerializer, ResenaSerializer
)

User = get_user_model()

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, obj, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsProtagonistaOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.es_protagonista

    def has_object_permission(self, request, obj, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.protagonista.user == request.user


class IsAdminOrVerifiedProtagonista(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user.protagonista.verificado
        except Protagonista.DoesNotExist:
            return False


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class PerfilView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        data = serializer.data
        if request.user.es_protagonista:
            try:
                protagonista = request.user.protagonista
                data['negocio'] = ProtagonistaSerializer(protagonista).data
            except Protagonista.DoesNotExist:
                data['negocio'] = None
        return Response(data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre']


class CircuitoCreativoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CircuitoCreativoDetailSerializer
        return CircuitoCreativoListSerializer

    def get_queryset(self):
        queryset = CircuitoCreativo.objects.all()
        ciudad_id = self.request.query_params.get('ciudad')
        if ciudad_id:
            queryset = queryset.filter(ciudad_id=ciudad_id)
        return queryset


class PuntoInteresViewSet(viewsets.ModelViewSet):
    queryset = PuntoInteres.objects.all()
    serializer_class = PuntoInteresSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = PuntoInteres.objects.all()
        circuito_id = self.request.query_params.get('circuito')
        categoria = self.request.query_params.get('categoria')
        
        if circuito_id:
            queryset = queryset.filter(circuito_id=circuito_id)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
            
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resena(self, request, pk=None):
        punto = self.get_object()
        user = request.user
        
        if Resena.objects.filter(user=user, punto_interes=punto).exists():
            return Response(
                {"detail": "Ya has calificado este punto de interés anteriormente."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        data = request.data.copy()
        data['punto_interes'] = punto.id
        
        serializer = ResenaSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user, punto_interes=punto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtagonistaViewSet(viewsets.ModelViewSet):
    serializer_class = ProtagonistaSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Protagonista.objects.all()
        ciudad_id = self.request.query_params.get('ciudad')
        categoria = self.request.query_params.get('categoria')
        verificado = self.request.query_params.get('verificado')

        if ciudad_id:
            queryset = queryset.filter(ciudad_id=ciudad_id)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if verificado is not None:
            is_verified = verificado.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(verificado=is_verified)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        user.es_protagonista = True
        user.es_turista = False
        user.save()
        serializer.save(user=user)


class ProductoServicioViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoServicioSerializer
    permission_classes = [IsProtagonistaOwnerOrReadOnly]

    def get_queryset(self):
        queryset = ProductoServicio.objects.all()
        protagonista_id = self.request.query_params.get('protagonista')
        es_emblematico = self.request.query_params.get('es_emblematico')
        ciudad_id = self.request.query_params.get('ciudad')

        if protagonista_id:
            queryset = queryset.filter(protagonista_id=protagonista_id)
        if es_emblematico is not None:
            is_emblematic = es_emblematico.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(es_emblematico=is_emblematic)
        if ciudad_id:
            queryset = queryset.filter(protagonista__ciudad_id=ciudad_id)

        return queryset

    def perform_create(self, serializer):
        try:
            protagonista = self.request.user.protagonista
            serializer.save(protagonista=protagonista)
        except Protagonista.DoesNotExist:
            raise status.ValidationError({"detail": "El usuario no tiene un perfil de protagonista creado."})


class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    permission_classes = [IsAdminOrVerifiedProtagonista]

    def get_queryset(self):
        queryset = Evento.objects.all()
        ciudad_id = self.request.query_params.get('ciudad')
        categoria = self.request.query_params.get('categoria')
        fecha_desde = self.request.query_params.get('fecha_desde')

        if ciudad_id:
            queryset = queryset.filter(ciudad_id=ciudad_id)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if fecha_desde:
            date_parsed = parse_date(fecha_desde)
            if date_parsed:
                queryset = queryset.filter(fecha_inicio__date__gte=date_parsed)

        return queryset.order_by('fecha_inicio')

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            try:
                protagonista = self.request.user.protagonista
                serializer.save(protagonista_organizador=protagonista, ciudad=protagonista.ciudad)
            except Protagonista.DoesNotExist:
                raise status.ValidationError({"detail": "No tienes un perfil de protagonista para organizar eventos."})
