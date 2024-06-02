import requests
import json

# URL de la API para descargar el modelo
PULL_URL = "http://ollama:11434/api/pull"

def pull_model(model_name):
    payload = {
        "name": model_name
    }
    try:
        response = requests.post(PULL_URL, json=payload, stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                print(json.loads(line))
        print("Model pulled successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    pull_model("llama3")
