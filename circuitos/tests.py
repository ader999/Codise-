from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from circuitos.models import Ciudad, CircuitoCreativo, PuntoInteres, Resena

User = get_user_model()

class CircuitosAPITests(APITestCase):

    def setUp(self):
        self.ciudad = Ciudad.objects.create(
            nombre="Masaya Test",
            descripcion="Ciudad de prueba",
            imagen_portada="test.jpg",
            latitud_centro=11.97,
            longitud_centro=-86.09
        )
        
        self.circuito = CircuitoCreativo.objects.create(
            ciudad=self.ciudad,
            nombre="Circuito de Prueba",
            descripcion="Descripción del circuito de prueba",
            distancia_km=5.50,
            duracion_estimada="1 hora",
            dificultad="Baja"
        )
        
        self.punto = PuntoInteres.objects.create(
            circuito=self.circuito,
            nombre="Punto de Prueba",
            descripcion="Descripción del punto",
            categoria="Cultural",
            latitud=11.98,
            longitud=-86.10,
            imagen="punto.jpg",
            orden=1
        )
        
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')
        self.perfil_url = reverse('perfil')
        
        self.user_data = {
            "username": "turista_test",
            "email": "turista@test.com",
            "password": "PasswordTest123!",
            "confirm_password": "PasswordTest123!",
            "first_name": "Turista",
            "last_name": "Nica",
            "es_turista": True,
            "es_protagonista": False
        }

    def test_registro_usuario_exitoso(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username="turista_test").count(), 1)

    def test_registro_contrasenas_no_coinciden(self):
        bad_data = self.user_data.copy()
        bad_data['confirm_password'] = 'Diferente123'
        response = self.client.post(self.register_url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_exitoso_y_obtencion_jwt(self):
        self.client.post(self.register_url, self.user_data, format='json')
        
        login_data = {
            "username": "turista_test",
            "password": "PasswordTest123!"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_listar_ciudades(self):
        url = reverse('ciudad-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], "Masaya Test")

    def test_listar_circuitos_filtrados(self):
        url = reverse('circuito-list')
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response_filtrado = self.client.get(f"{url}?ciudad={self.ciudad.id}", format='json')
        self.assertEqual(len(response_filtrado.data), 1)

        response_vacio = self.client.get(f"{url}?ciudad=9999", format='json')
        self.assertEqual(len(response_vacio.data), 0)

    def test_detalle_circuito_con_puntos_anidados(self):
        url = reverse('circuito-detail', kwargs={'pk': self.circuito.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('puntos', response.data)
        self.assertEqual(len(response.data['puntos']), 1)
        self.assertEqual(response.data['puntos'][0]['nombre'], "Punto de Prueba")

    def test_crear_resena_sin_autenticar_falla(self):
        url = reverse('puntointeres-resena', kwargs={'pk': self.punto.id})
        resena_data = {
            "calificacion": 5,
            "comentario": "¡Excelente lugar!"
        }
        response = self.client.post(url, resena_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crear_resena_autenticado_exitoso(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {"username": "turista_test", "password": "PasswordTest123!"}
        login_response = self.client.post(self.login_url, login_data, format='json')
        token = login_response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('puntointeres-resena', kwargs={'pk': self.punto.id})
        resena_data = {
            "calificacion": 5,
            "comentario": "¡Increíble parada cultural!"
        }
        response = self.client.post(url, resena_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resena.objects.count(), 1)
        self.assertEqual(Resena.objects.first().calificacion, 5)

    def test_doble_resena_mismo_usuario_falla(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {"username": "turista_test", "password": "PasswordTest123!"}
        login_response = self.client.post(self.login_url, login_data, format='json')
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('puntointeres-resena', kwargs={'pk': self.punto.id})
        resena_data = {
            "calificacion": 4,
            "comentario": "Me gustó bastante."
        }
        response1 = self.client.post(url, resena_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(url, resena_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Resena.objects.count(), 1)
