import streamlit as st
import requests
import os
import time

# URL de la API para interactuar con el modelo LLaMA3
CREATE_URL = "http://ollama:11434/api/create"
API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/api/generate")

# Función para crear un modelo
def create_model(name, modelfile):
    payload = {
        "name": name,
        "modelfile": modelfile
    }
    retries = 5
    for i in range(retries):
        try:
            response = requests.post(CREATE_URL, json=payload)
            response.raise_for_status()
            st.write(f"Model '{name}' created successfully.")
            return
        except requests.exceptions.RequestException as e:
            st.error(f"Request to create model '{name}' failed (attempt {i+1}/{retries}): {e}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar
    st.error(f"Error: Could not create model '{name}' after {retries} attempts.")

# Crear los modelos al iniciar Streamlit
def initialize_models():
    st.write("Initializing models...")
    create_model("llama3", "FROM llama3")
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

st.title("Chat con LLaMA3 y Mario")

# Verificar la conexión al inicio
check_ollama_connection()

def get_response(prompt):
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False  # Ajusta esto según tus necesidades
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Lanzará una excepción para códigos de estado 4xx/5xx
        st.write(f"Raw response: {response.text}")  # Imprime la respuesta completa para depuración
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return ""
    except ValueError as e:
        st.error(f"Failed to parse JSON: {e}")
        return ""

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("You:", key="user_input")

if st.button("Send"):
    if user_input:
        st.session_state.conversation.append(("You", user_input))
        response = get_response(user_input)
        st.session_state.conversation.append(("LLaMA3", response))

for speaker, text in st.session_state.conversation:
    st.write(f"**{speaker}:** {text}")
