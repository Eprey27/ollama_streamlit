import requests
import json
import logging
import time

# Configurar logging
logging.basicConfig(filename='/app/pull_model.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL de la API para descargar el modelo
PULL_URL = "http://ollama:11434/api/pull"

def pull_model(model_name):
    payload = {
        "name": model_name
    }
    retries = 5
    for i in range(retries):
        try:
            logging.info(f"Iniciando la descarga del modelo '{model_name}' desde {PULL_URL}")
            response = requests.post(PULL_URL, json=payload, stream=True)
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    log_entry = json.loads(line)
                    logging.info(log_entry)
                    print(log_entry)
            logging.info(f"Modelo '{model_name}' descargado exitosamente.")
            return
        except requests.exceptions.RequestException as e:
            logging.error(f"Falló la solicitud (intento {i+1}/{retries}): {e}")
            print(f"Request failed (attempt {i+1}/{retries}): {e}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar
    logging.error(f"Error: No se pudo descargar el modelo '{model_name}' después de {retries} intentos.")

if __name__ == "__main__":
    pull_model("llama3")
