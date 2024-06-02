import streamlit as st
import requests
import os

# URL de la API para interactuar con el modelo LLaMA3
API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/predict")

st.title("Chat con LLaMA3")

def get_response(prompt):
    response = requests.post(API_URL, json={"prompt": prompt})
    return response.json().get("response", "")

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
