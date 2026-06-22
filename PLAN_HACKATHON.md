# 🇳🇮 Reto Hackatón: Circuitos Creativos de la Red Nacional de Ciudades Creativas

Este es tu documento de ruta para el Hackatón. El objetivo es mantenerte enfocado en los requisitos clave del reto y asegurar que el Backend con **Django Rest Framework (DRF)** proporcione todo lo necesario para el Frontend.

---

## 🎯 ¿Qué vamos a conseguir? (El MVP)
Una plataforma web/móvil que permita:
1. **Ver las 10 Ciudades Creativas** de Nicaragua (Estelí, León, Nagarote, Managua, Masaya, Granada, San Juan de Oriente, Juigalpa, Matagalpa y Bluefields).
2. **Explorar Mapas Interactivos** de sus Circuitos Creativos (rutas turísticas culturales).
3. **Escuchar Audios y ver Contenido Inmersivo** sobre puntos de interés (saberes populares, historia, naturaleza).
4. **Consultar una Agenda de Actividades** (talleres de barro, ferias de artesanía, expo-ventas locales).
5. **Ver un Directorio de Protagonistas** (los artesanos y MIPYMES que dan vida a las ciudades) con sus productos y servicios.

---

## 🗄️ Modelos de Base de Datos Propuestos (`models.py`)

A grandes rasgos, implementaremos los siguientes modelos:
- **Ciudad:** Las 10 ciudades creativas oficiales con su información y centro geográfico.
- **CircuitoCreativo:** Rutas temáticas dentro de una ciudad (ej. *Ruta de las Flores*, *Circuito Histórico*).
- **PuntoInteres:** Paradas físicas dentro de un circuito (ej. *Taller de Cerámica de Don Valentín* en San Juan de Oriente). Contiene coordenadas, descripción, audio-guía (URL) e información de saberes populares.
- **Protagonista:** Perfil del artesano/emprendedor verificado.
- **ProductoServicio:** Productos emblemáticos que ofrece un protagonista.
- **Evento:** Actividades culturales, ferias, talleres con fecha, hora, lugar y organizador.

---

## 🔗 Rutas del API (Endpoints)

Estas son las rutas principales que usará el frontend para consumir datos:
*   `GET /api/ciudades/` -> Lista de ciudades con sus imágenes y coordenadas principales.
*   `GET /api/ciudades/<id>/circuitos/` -> Circuitos turísticos de esa ciudad.
*   `GET /api/circuitos/<id>/` -> Detalle de un circuito con la lista de sus puntos de interés ordenada para pintar el mapa.
*   `GET /api/puntos-interes/<id>/` -> Audio-guías, fotos y leyendas del punto específico.
*   `GET /api/eventos/` -> Agenda del mes. Se puede filtrar por ciudad: `/api/eventos/?ciudad=<id>` o por categoría `/api/eventos/?categoria=taller`.
*   `GET /api/protagonistas/` -> Directorio de artesanos locales.
*   `GET /api/protagonistas/<id>/` -> Perfil, redes, contacto y su catálogo de productos.
*   `POST /api/auth/register/` y `/api/auth/login/` -> Registro e inicio de sesión con JWT para turistas y protagonistas.

---

## 🚀 Fases del Desarrollo

1.  **Fase 1: Estructura y Modelos (Models & DB)**: Crear el proyecto django `CodeCore` e implementar el archivo `models.py`.
2.  **Fase 2: Consola de Administración (Django Admin)**: Personalizar el panel de administración para poder registrar ciudades, circuitos, eventos y artesanos rápidamente durante la presentación con el jurado.
3.  **Fase 3: Serializadores y Vistas (DRF API)**: Crear la lógica para exponer los JSONs que el frontend va a consumir.
4.  **Fase 4: Semilla de Datos (Data Seeding)**: Crear un script para cargar datos reales de ciudades como *Granada*, *Masaya* o *Estelí* de inmediato para no presentar un proyecto vacío.
5.  **Fase 5: Conectar Frontend**: Probar y asegurar que la comunicación con el frontend (CORS, URLs, Métodos) funcione al 100%.

---

## ❓ Preguntas para Iniciar
Para arrancar el desarrollo de inmediato, indícame:
1. ¿Usaremos coordenadas flotantes simples (latitud/longitud) para no complicar el despliegue del hackatón, o necesitas GIS especializado (GeoDjango)? *(Se recomienda flotantes simples para desarrollo ágil)*
2. ¿Usamos SQLite para empezar rápido, o PostgreSQL?
3. ¿Las imágenes y audios se guardarán de forma local en la carpeta `/media/` o los subiremos a un servicio como Cloudinary?

**¡Listo para comenzar a codificar los modelos en cuanto me des luz verde!** 🇳🇮🚀
