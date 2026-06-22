import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# ⚙️ Configurar el entorno de Django para ejecutar script independiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from circuitos.models import (
    Ciudad, CircuitoCreativo, PuntoInteres,
    Protagonista, ProductoServicio, Evento
)

User = get_user_model()

def populate():
    print("🧹 Limpiando base de datos existente...")
    Evento.objects.all().delete()
    ProductoServicio.objects.all().delete()
    Protagonista.objects.all().delete()
    PuntoInteres.objects.all().delete()
    CircuitoCreativo.objects.all().delete()
    Ciudad.objects.all().delete()
    
    # Conservar el superusuario si ya existe, si no, crearlo
    if not User.objects.filter(username='admin').exists():
        print("👤 Creando superusuario administrador (admin / adminpass)...")
        User.objects.create_superuser('admin', 'admin@circuitos.com', 'adminpass', first_name="Admin", last_name="Nicaragua")
    else:
        print("👤 Superusuario 'admin' ya existe.")

    # 1. Crear usuarios para protagonistas
    print("👥 Creando usuarios de prueba para protagonistas...")
    u_marcos, _ = User.objects.get_or_create(username='marcos_ceramica', email='marcos@sanjuandeoriente.com')
    u_marcos.set_password('protagonista123')
    u_marcos.es_protagonista = True
    u_marcos.es_turista = False
    u_marcos.first_name = "Marcos"
    u_marcos.last_name = "Gutiérrez"
    u_marcos.save()

    u_elena, _ = User.objects.get_or_create(username='elena_gastronomia', email='elena@esteli.com')
    u_elena.set_password('protagonista123')
    u_elena.es_protagonista = True
    u_elena.es_turista = False
    u_elena.first_name = "Elena"
    u_elena.last_name = "Torres"
    u_elena.save()

    # 🏙️ 2. Crear Ciudades Creativas
    print("🏙️ Creando ciudades creativas...")
    
    masaya = Ciudad.objects.create(
        nombre="Masaya",
        descripcion="La Cuna del Folklore Nicaragüense. Ciudad de flores, marimbas, mitos y del circuito precolombino de San Juan de Oriente.",
        imagen_portada="ciudades/portadas/masaya_portada.jpg",
        latitud_centro=11.9744,
        longitud_centro=-86.0942
    )

    esteli = Ciudad.objects.create(
        nombre="Estelí",
        descripcion="La Ciudad de los Murales. Famosa por su producción de tabaco de clase mundial, su naturaleza montañosa y su arte mural urbano.",
        imagen_portada="ciudades/portadas/esteli_portada.jpg",
        latitud_centro=13.0919,
        longitud_centro=-86.3538
    )

    leon = Ciudad.objects.create(
        nombre="León",
        descripcion="La Ciudad Universitaria e Histórica. Rica en arquitectura colonial, hogar de la Basílica Catedral y del gran poeta Rubén Darío.",
        imagen_portada="ciudades/portadas/leon_portada.jpg",
        latitud_centro=12.4379,
        longitud_centro=-86.8780
    )

    # 🗺️ 3. Crear Circuitos Creativos
    print("🗺️ Creando circuitos creativos...")

    c_masaya = CircuitoCreativo.objects.create(
        ciudad=masaya,
        nombre="Ruta del Barro y la Tradición precolombina",
        descripcion="Un recorrido mágico por los talleres de San Juan de Oriente y el icónico Mercado de Artesanías de Masaya.",
        distancia_km=12.5,
        duracion_estimada="3 horas",
        dificultad="Baja"
    )

    c_esteli = CircuitoCreativo.objects.create(
        ciudad=esteli,
        nombre="Sendero de los Murales Históricos y del Café",
        descripcion="Descubre la historia del norte de Nicaragua a través de murales artísticos y degusta café especial esteliano.",
        distancia_km=4.2,
        duracion_estimada="2 horas",
        dificultad="Baja"
    )

    c_leon = CircuitoCreativo.objects.create(
        ciudad=leon,
        nombre="Circuito Poético y Revolucionario",
        descripcion="Recorrido colonial que conecta la gran catedral con museos históricos y casas de insignes poetas.",
        distancia_km=3.0,
        duracion_estimada="1.5 horas",
        dificultad="Baja"
    )

    # 📍 4. Crear Puntos de Interés
    print("📍 Creando puntos de interés (paradas de circuitos)...")

    # Puntos de Masaya
    p_mercado = PuntoInteres.objects.create(
        circuito=c_masaya,
        nombre="Mercado de Artesanías de Masaya",
        descripcion="Edificio de estilo neogótico tardío donde se congregan artesanos de todo el departamento.",
        categoria="Cultural",
        latitud=11.9735,
        longitud=-86.0920,
        imagen="puntos/imagenes/mercado_masaya.jpg",
        audio_guia="puntos/audios/mercado_masaya.mp3",
        saberes_populares="Aquí se tocan las marimbas de arco de madera de chiquirín y se venden las famosas hamacas tejidas a mano por familias del barrio San Juan.",
        orden=1
    )

    p_taller_sjo = PuntoInteres.objects.create(
        circuito=c_masaya,
        nombre="Taller Escuela de Cerámica Precolombina Valentín",
        descripcion="Taller tradicional en San Juan de Oriente que mantiene vivas las técnicas de torneado y pulido indígena.",
        categoria="Taller Artesanal",
        latitud=11.9056,
        longitud=-86.0745,
        imagen="puntos/imagenes/taller_valentin.jpg",
        audio_guia="puntos/audios/taller_valentin.mp3",
        visita_virtual_url="https://ejemplo.com/tours/taller-sjo",
        saberes_populares="Los diseños de la cerámica utilizan arcilla local y pigmentos minerales inspirados en la fauna del jaguar y el dios Quetzalcóatl.",
        orden=2
    )

    # Puntos de Estelí
    p_parque_esteli = PuntoInteres.objects.create(
        circuito=c_esteli,
        nombre="Parque Central 16 de Julio",
        descripcion="Punto neurálgico del arte urbano donde se inician las principales rutas de muralismo urbano.",
        categoria="Cultural",
        latitud=13.0921,
        longitud=-86.3536,
        imagen="puntos/imagenes/parque_esteli.jpg",
        orden=1
    )

    p_galeria_murales = PuntoInteres.objects.create(
        circuito=c_esteli,
        nombre="Mural 'El Canto a la Vida' en Barrio Sandino",
        descripcion="Uno de los murales colectivos más grandes e históricos pintado por niños y jóvenes locales.",
        categoria="Cultural",
        latitud=13.0880,
        longitud=-86.3580,
        imagen="puntos/imagenes/mural_canto_vida.jpg",
        audio_guia="puntos/audios/mural_canto_vida.mp3",
        saberes_populares="Este mural plasma la historia de paz y reconstrucción de la ciudad después de las guerras del siglo pasado, usando alegorías del campo y el norte.",
        orden=2
    )

    # Puntos de León
    p_catedral = PuntoInteres.objects.create(
        circuito=c_leon,
        nombre="Catedral de la Asunción de León",
        descripcion="Imponente catedral barroca-neoclásica, la más grande de Centroamérica. Alberga la tumba de Rubén Darío.",
        categoria="Historico",
        latitud=12.4349,
        longitud=-86.8791,
        imagen="puntos/imagenes/catedral_leon.jpg",
        visita_virtual_url="https://ejemplo.com/tours/catedral-leon",
        saberes_populares="La leyenda cuenta que los planos originales eran para la catedral de Lima, Perú, pero por un error de barcos llegaron a León, construyéndose así este coloso.",
        orden=1
    )

    p_museo_dario = PuntoInteres.objects.create(
        circuito=c_leon,
        nombre="Museo Archivo Rubén Darío",
        descripcion="La casa del siglo XIX donde vivió el gran reformador de la poesía castellana durante sus primeros 14 años de vida.",
        categoria="Historico",
        latitud=12.4355,
        longitud=-86.8833,
        imagen="puntos/imagenes/museo_dario.jpg",
        audio_guia="puntos/audios/museo_dario.mp3",
        saberes_populares="Conserva pertenencias íntimas del bardo, incluyendo el manuscrito original del poema 'A Margarita Debayle' y su máscara mortuoria.",
        orden=2
    )

    # 🧑‍🎨 5. Crear Perfiles de Protagonistas
    print("🧑‍🎨 Creando perfiles de protagonistas...")

    prot_marcos = Protagonista.objects.create(
        user=u_marcos,
        nombre_negocio="Cerámica Artística Ancestral Gutiérrez",
        descripcion="Taller familiar heredero de técnicas de alfarería precolombina de San Juan de Oriente. Elaboramos vasijas, platos pintados y réplicas de deidades.",
        ciudad=masaya,
        categoria="Artesania",
        telefono="+505 8888-7777",
        redes_sociales={"facebook": "https://facebook.com/ceramica.gutierrez.sjo", "whatsapp": "+50588887777"},
        verificado=True,
        punto_interes_asociado=p_taller_sjo
    )

    prot_elena = Protagonista.objects.create(
        user=u_elena,
        nombre_negocio="Comedor Tradicional El Sabor del Norte",
        descripcion="Ofrecemos platos emblemáticos de Estelí como la sopa de gallina con albóndigas, nacatamales tradicionales de maíz y rosquillas horneadas en leña.",
        ciudad=esteli,
        categoria="Gastronomia",
        telefono="+505 8444-2222",
        redes_sociales={"instagram": "https://instagram.com/sabor.delnorte.esteli"},
        verificado=True
    )

    # 🏺 6. Crear Productos y Servicios
    print("🏺 Creando productos emblemáticos...")

    # Productos de Marcos
    ProductoServicio.objects.create(
        protagonista=prot_marcos,
        nombre="Jarrón Jaguar Pintado a Mano",
        descripcion="Jarrón de arcilla roja pulida, con pintura de pigmentos minerales naturales representando los jaguares mitológicos nicaraos.",
        precio=1200.00,  # En Córdobas
        imagen="productos/jarron_jaguar.jpg",
        es_emblematico=True
    )

    ProductoServicio.objects.create(
        protagonista=prot_marcos,
        nombre="Taller Práctico de Moldeado en Torno",
        descripcion="Clase privada de 1 hora donde aprenderás a moldear tu propia pieza de barro en el torno de pie tradicional.",
        precio=350.00,
        imagen="productos/taller_torno.jpg",
        es_emblematico=False
    )

    # Productos de Elena
    ProductoServicio.objects.create(
        protagonista=prot_elena,
        nombre="Nacatamal Esteliano Especial",
        descripcion="Masa de maíz criollo aliñada con tocino, arroz, papas, pasas, ciruelas y carne de cerdo seleccionada envuelta en hojas de plátano.",
        precio=120.00,
        imagen="productos/nacatamal_esteliano.jpg",
        es_emblematico=True
    )

    # 📅 7. Crear Eventos
    print("📅 Creando eventos de la agenda...")

    # Evento de masaya (asociado al taller de Marcos)
    Evento.objects.create(
        ciudad=masaya,
        titulo="Feria y Taller de Barro Vivo de San Juan de Oriente",
        descripcion="Ven a presenciar demostraciones en vivo y moldea tu propia pieza tradicional con los artesanos del barro de los Pueblos Blancos.",
        fecha_inicio=timezone.now() + timedelta(days=5, hours=10),
        fecha_fin=timezone.now() + timedelta(days=5, hours=17),
        lugar="Plaza de San Juan de Oriente",
        latitud=11.9050,
        longitud=-86.0740,
        imagen="eventos/feria_barro.jpg",
        categoria="Taller",
        protagonista_organizador=prot_marcos
    )

    # Evento oficial de Estelí (sin protagonista directo, creado por alcaldía)
    Evento.objects.create(
        ciudad=esteli,
        titulo="Festival del Muralismo Urbano 'Pintando Estelí'",
        descripcion="Gran jornada de arte urbano donde más de 30 muralistas locales y nacionales plasmarán murales artísticos en vivo en las calles de la ciudad.",
        fecha_inicio=timezone.now() + timedelta(days=12, hours=9),
        fecha_fin=timezone.now() + timedelta(days=14, hours=18),
        lugar="Avenidas del Centro Histórico, Estelí",
        imagen="eventos/festival_muralismo.jpg",
        categoria="Cultural"
    )

    print("🎉 ¡Base de datos poblada exitosamente!")

if __name__ == '__main__':
    populate()
