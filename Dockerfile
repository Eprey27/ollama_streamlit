# Usar una imagen base de Python
FROM python:3.9-slim

# Instalar dependencias
RUN pip install streamlit requests

# Copiar la aplicación y el script de pull
COPY app.py /app/app.py
COPY pull_model.py /app/pull_model.py

# Establecer el directorio de trabajo
WORKDIR /app

# Ejecutar el script para descargar el modelo antes de iniciar Streamlit
RUN python pull_model.py

# Exponer el puerto de Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py"]
