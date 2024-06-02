# Usar una imagen base de Python
FROM python:3.9-slim

# Instalar dependencias
RUN pip install streamlit requests

# Copiar la aplicación
COPY app.py /app/app.py

# Establecer el directorio de trabajo
WORKDIR /app

# Exponer el puerto de Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "app.py"]
