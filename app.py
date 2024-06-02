import streamlit as st
import requests
import os
import time
import json
import logging
from streamlit.delta_generator import DeltaGenerator

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# URL de la API para interactuar con el modelo LLaMA3
CREATE_URL = "http://ollama:11434/api/create"
API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/api/generate")
TAGS_URL = "http://ollama:11434/api/tags"

# Función para crear un modelo
def create_model(name, modelfile):
    payload = {
        "name": name,
        "modelfile": modelfile
    }
    retries = 5
    for i in range(retries):
        try:
            logging.debug(f"Iniciando la creación del modelo '{name}' con modelfile: {modelfile}")
            response = requests.post(CREATE_URL, json=payload)
            response.raise_for_status()
            st.write(f"Model '{name}' created successfully.")
            return
        except requests.exceptions.RequestException as e:
            logging.error(f"Request to create model '{name}' failed (attempt {i+1}/{retries}): {e}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar
    st.error(f"Error: Could not create model '{name}' after {retries} attempts.")

# Crear los modelos al iniciar Streamlit
def initialize_models():
    st.write("Initializing models...")
    # create_model("llama3", "FROM llama3")
    create_model("mario", "FROM llama3\nSYSTEM You are mario from Super Mario Bros.")

# Verificar la conexión con Ollama y crear los modelos si es necesario
def check_ollama_connection():
    try:
        response = requests.get("http://ollama:11434")
        if response.status_code == 200:
            st.write("Connected to Ollama API.")
            initialize_models()
        else:
            st.error("Failed to connect to Ollama API.")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to Ollama API: {e}")

# Obtener la lista de modelos disponibles
def get_available_models():
    try:
        response = requests.get(TAGS_URL)
        response.raise_for_status()
        models = response.json().get("models", [])
        return [model["name"] for model in models]
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch models: {e}")
        return []

st.title("Chat con Modelos LLaMA")

# Verificar la conexión al inicio
check_ollama_connection()

# Obtener la lista de modelos disponibles
available_models = get_available_models()

# Seleccionar el modelo
selected_model = st.selectbox("Selecciona un modelo", available_models)

def get_response(model, prompt, response_container: DeltaGenerator):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True  # Habilitar streaming
    }
    try:
        logging.debug(f"Sending prompt to model '{model}': {payload}")
        response = requests.post(API_URL, json=payload, stream=True)
        response.raise_for_status()  # Lanzará una excepción para códigos de estado 4xx/5xx

        full_response = ""
        for line in response.iter_lines():
            if line:
                part = line.decode('utf-8')
                logging.debug(f"Received part: {part}")
                response_data = json.loads(part)
                token = response_data.get("response", "")
                full_response += token
                response_container.markdown(f"**{model}:** {full_response}")

        return full_response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        response_container.error(f"Request failed: {e}")
        return ""
    except ValueError as e:
        logging.error(f"Failed to parse JSON: {e}")
        response_container.error(f"Failed to parse JSON: {e}")
        return ""

# Mantener el historial del chat
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("You:", key="user_input")

if st.button("Send"):
    if user_input and selected_model:
        st.session_state.conversation.append(("You", user_input))
        response_container = st.empty()  # Contenedor temporal para mostrar la respuesta en tiempo real
        response = get_response(selected_model, user_input, response_container)
        st.session_state.conversation.append((selected_model, response))

# Mostrar el historial del chat
st.write("## Chat History")
for speaker, text in st.session_state.conversation:
    st.write(f"**{speaker}:** {text}")
