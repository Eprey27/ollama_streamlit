import streamlit as st
import requests
import os
import time
import json
import logging
from streamlit.delta_generator import DeltaGenerator
from typing import List, Tuple, Optional

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# URL de la API para interactuar con el modelo LLaMA3
CREATE_URL = "http://ollama:11434/api/create"
API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/api/generate")
TAGS_URL = "http://ollama:11434/api/tags"


class OllamaAPI:
    """Clase para interactuar con la API de Ollama"""

    @staticmethod
    def create_model(name: str, modelfile: str, retries: int = 5) -> bool:
        payload = {
            "name": name,
            "modelfile": modelfile
        }
        for i in range(retries):
            try:
                logging.debug(f"Iniciando la creación del modelo '{name}' con modelfile: {modelfile}")
                response = requests.post(CREATE_URL, json=payload)
                response.raise_for_status()
                return True
            except requests.exceptions.RequestException as e:
                logging.error(f"Request to create model '{name}' failed (attempt {i+1}/{retries}): {e}")
                time.sleep(5)  # Esperar 5 segundos antes de reintentar
        return False

    @staticmethod
    def check_connection() -> bool:
        try:
            response = requests.get("http://ollama:11434")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to connect to Ollama API: {e}")
            return False

    @staticmethod
    def get_available_models() -> List[str]:
        try:
            response = requests.get(TAGS_URL)
            response.raise_for_status()
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch models: {e}")
            return []

    @staticmethod
    def generate_response(model: str, prompt: str) -> requests.Response:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True  # Habilitar streaming
        }
        try:
            logging.debug(f"Sending prompt to model '{model}': {payload}")
            response = requests.post(API_URL, json=payload, stream=True)
            response.raise_for_status()  # Lanzará una excepción para códigos de estado 4xx/5xx
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise e


class ModelManager:
    """Clase para manejar la inicialización de modelos"""

    def __init__(self, api: OllamaAPI):
        self.api = api

    def initialize_models(self):
        st.write("Initializing models...")
        if not self.api.create_model("llama3", "FROM llama3"):
            st.error("Error: Could not create model 'llama3'.")
        if not self.api.create_model("mario", "FROM llama3\nSYSTEM You are mario from Super Mario Bros."):
            st.error("Error: Could not create model 'mario'.")


class ChatManager:
    """Clase para manejar el chat"""

    def __init__(self):
        if 'conversation' not in st.session_state:
            st.session_state.conversation = []

    def add_message(self, role: str, message: str):
        st.session_state.conversation.append((role, message))

    def display_conversation(self):
        st.write("## Chat History")
        for speaker, text in st.session_state.conversation:
            st.write(f"**{speaker}:** {text}")

    def get_user_input(self) -> Optional[str]:
        return st.text_input("You:", key="user_input")

    def display_response(self, model: str, response: requests.Response, response_container: DeltaGenerator):
        full_response = ""
        try:
            for line in response.iter_lines():
                if line:
                    part = line.decode('utf-8')
                    logging.debug(f"Received part: {part}")
                    response_data = json.loads(part)
                    token = response_data.get("response", "")
                    full_response += token
                    response_container.markdown(f"**{model}:** {full_response}")
        except ValueError as e:
            logging.error(f"Failed to parse JSON: {e}")
            response_container.error(f"Failed to parse JSON: {e}")

        return full_response


def main():
    st.title("Chat con Modelos LLaMA")

    api = OllamaAPI()
    model_manager = ModelManager(api)
    chat_manager = ChatManager()

    if api.check_connection():
        st.write("Connected to Ollama API.")
        model_manager.initialize_models()
    else:
        st.error("Failed to connect to Ollama API.")
        return

    available_models = api.get_available_models()
    selected_model = st.selectbox("Selecciona un modelo", available_models)

    user_input = chat_manager.get_user_input()

    if st.button("Send"):
        if user_input and selected_model:
            chat_manager.add_message("You", user_input)
            response_container = st.empty()  # Contenedor temporal para mostrar la respuesta en tiempo real
            try:
                response = api.generate_response(selected_model, user_input)
                full_response = chat_manager.display_response(selected_model, response, response_container)
                chat_manager.add_message(selected_model, full_response)
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

    chat_manager.display_conversation()


if __name__ == "__main__":
    main()
