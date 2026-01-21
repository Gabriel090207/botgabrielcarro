import os
from flask import Flask, request
from dotenv import load_dotenv
import requests

from app.main import main  # vamos ajustar depois

load_dotenv()

ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")
ULTRAMSG_BASE_URL = os.getenv("ULTRAMSG_BASE_URL")

app = Flask(__name__)


def enviar_mensagem(numero, mensagem):
    url = f"{ULTRAMSG_BASE_URL}/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": numero,
        "body": mensagem
    }
    requests.post(url, data=payload)


@app.route("/webhook", methods=["POST"])
def receber_mensagem():
    data = request.json
    print("WEBHOOK RECEBIDO:", data)


    try:
        numero = data.get("from")
        texto = data.get("body")

        if not numero or not texto:
            return "OK", 200

        # aqui depois vamos chamar o motor do bot
        resposta = "Recebi sua mensagem 👍"

        enviar_mensagem(numero, resposta)

    except Exception as e:
        print("Erro:", e)

    return "OK", 200

# Render vai iniciar via Gunicorn

