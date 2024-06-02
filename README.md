# Proyecto de Chat con Modelos LLaMA

## Descripción

Este proyecto utiliza Docker para desplegar un servicio de chat que interactúa con modelos de lenguaje LLaMA3 a través de una interfaz de usuario construida con Streamlit. Los modelos se gestionan mediante la API de Ollama, permitiendo la creación, consulta y uso de modelos de lenguaje.

## Funcionalidades

- **Selección de Modelos**: La interfaz de usuario permite seleccionar entre los modelos disponibles para el chat.
- **Historial de Chat**: El historial de la conversación se muestra en la interfaz, manteniendo el contexto del chat.
- **Creación de Modelos**: El sistema puede crear modelos personalizados al iniciar la aplicación, basándose en la configuración proporcionada.
- **Streaming de Respuestas**: Las respuestas del modelo se muestran en tiempo real a medida que se generan, mejorando la experiencia del usuario.

## Requisitos

- Docker
- Docker Compose
- Conexión a Internet para descargar las imágenes de Docker y los modelos de lenguaje

## Instalación

1. **Clonar el repositorio**:

   ```sh
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. **Construir y levantar los servicios con Docker Compose**:

   ```sh
   docker-compose up --build
   ```

3. **Acceder a la aplicación Streamlit**:

   Abre un navegador web y navega a `http://localhost:8501`.

## Uso

### Inicialización de Modelos

Al iniciar la aplicación, se comprobará la conexión con la API de Ollama y se procederá a crear los modelos necesarios (por ejemplo, LLaMA3 y un modelo personalizado "Mario"). Este proceso se registra y cualquier error se mostrará en la interfaz de usuario.

### Interacción con la Interfaz de Usuario

- **Selección de Modelo**: En la interfaz de Streamlit, selecciona el modelo con el que deseas interactuar desde un menú desplegable.
- **Envío de Mensajes**: Introduce tu mensaje en el campo de texto y envíalo. La respuesta del modelo se mostrará en la interfaz en tiempo real, token por token.
- **Historial de Conversación**: El historial de la conversación se mantiene y se muestra en la interfaz, permitiendo una interacción continua y contextual.

### Debugging

Para ver los logs de los contenedores y solucionar problemas:

```sh
docker-compose logs -f
```

## Información General

### Estructura del Proyecto

- **Dockerfile**: Define la imagen de Docker para el servicio de Streamlit.
- **docker-compose.yml**: Define y configura los servicios Docker, incluyendo Ollama y Streamlit.
- **app.py**: Código principal de la aplicación Streamlit.
- **README.md**: Archivo de documentación.

### Logs y Debugging

El sistema está configurado para proporcionar logs detallados que ayudan en el debugging. Los logs de los servicios Docker pueden ser visualizados con el comando `docker-compose logs -f`. Esto incluye información sobre la creación de modelos, solicitudes a la API, y cualquier error que ocurra durante la ejecución.

### Mejoras Futuras

- **Autenticación y Autorización**: Añadir mecanismos de seguridad para proteger el acceso a la aplicación.
- **Almacenamiento Persistente**: Implementar almacenamiento persistente para los historiales de chat, permitiendo su consulta y análisis posterior.
- **Ampliación de la Interfaz**: Añadir más funcionalidades a la interfaz de usuario, como opciones de configuración avanzadas para los modelos y visualización de métricas.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un fork del repositorio, realiza tus cambios y envía un pull request. Asegúrate de que tu código sigue las buenas prácticas de desarrollo y que has probado tus cambios antes de enviarlos.  
