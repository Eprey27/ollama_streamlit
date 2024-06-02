import streamlit as st
import requests
import os

# URL de la API para interactuar con el modelo LLaMA3
API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/api/generate")

st.title("Chat con LLaMA3")

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
