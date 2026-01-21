import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

from app.main import conversar  # usa o motor real do bot

load_dotenv()

ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")
ULTRAMSG_BASE_URL = os.getenv("ULTRAMSG_BASE_URL")

app = Flask(__name__)


def enviar_mensagem(numero, mensagem):
    numero = numero.replace("@c.us", "")

    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"

    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": numero,
        "body": mensagem
    }

    response = requests.post(url, data=payload)
    print("ULTRAMSG RESPONSE:", response.status_code, response.text)


@app.route("/webhook", methods=["POST"])
def receber_mensagem():
    data = request.json
    print("WEBHOOK RECEBIDO:", data)

    try:
        if data.get("event_type") != "message_received":
            return "OK", 200

        mensagem_data = data.get("data", {})

        if mensagem_data.get("fromMe"):
            return "OK", 200

        numero = mensagem_data.get("from").replace("@c.us", "")
        texto = mensagem_data.get("body")

        if not numero or not texto:
            return "OK", 200

        resposta = conversar(texto)
        enviar_mensagem(numero, resposta)

    except Exception as e:
        print("ERRO NO WEBHOOK:", e)

    return "OK", 200
