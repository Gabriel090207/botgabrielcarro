import os
from dotenv import load_dotenv
from openai import OpenAI

from app.prompts import PROMPT_BASE
from app.regras import CARROS, calcular_parcelas
from app.memory import (
    adicionar_mensagem,
    obter_historico,
    set_carro,
    get_carro,
    set_entrada,
    get_entrada,
    set_estagio,
    get_estagio,
)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ================= UTILIDADES =================

def conversar(mensagem):
    adicionar_mensagem("user", mensagem)

    mensagens = [
        {"role": "system", "content": PROMPT_BASE},
        *obter_historico()
    ]

    resposta = client.responses.create(
        model="gpt-4.1-mini",
        input=mensagens
    )

    texto = resposta.output_text
    adicionar_mensagem("assistant", texto)
    return texto


def extrair_numero(texto):
    numeros = "".join(c for c in texto if c.isdigit())
    return int(numeros) if numeros else None


def falou_valor(texto):
    return any(p in texto for p in ["valor", "preço", "custa", "avista", "à vista"])


def falou_parcelado(texto):
    return any(p in texto for p in ["parcelado", "financiado", "financiamento"])


# ================= MAIN =================

def main():
    print("Bot iniciado. Digite algo:")

    while True:
        texto = input("> ").strip()
        texto_lower = texto.lower()

        if texto_lower in ["sair", "exit"]:
            break

        # -------- FOTO / VÍDEO --------
        if any(p in texto_lower for p in ["foto", "fotos", "video", "vídeo"]):
            print("Já já vou enviar 🚗")
            continue

        # -------- DETECTA CARRO --------
        for nome in CARROS:
            if nome in texto_lower:
                set_carro(nome)
                set_estagio("carro_definido")

        carro = get_carro()
        estagio = get_estagio()

        # -------- VALOR PARCELADO (PRIORIDADE ALTA) --------
        if carro and falou_parcelado(texto_lower) and estagio != "aguardando_entrada":
            set_estagio("aguardando_entrada")
            print("Perfeito. Qual valor de entrada você pretende dar?")
            continue

        # -------- CAPTURA ENTRADA --------
        if estagio == "aguardando_entrada":
            entrada = extrair_numero(texto_lower)
            if entrada:
                set_entrada(entrada)
            else:
                print("Me diga apenas o valor da entrada para eu simular.")
                continue

        entrada = get_entrada()

        # -------- SIMULAÇÃO AUTOMÁTICA --------
        if carro and entrada and estagio != "simulacao_enviada":
            if entrada < 2000:
                print("O valor mínimo de entrada é de R$ 2.000, mas podemos avaliar outras opções.")
                continue

            parcelas = calcular_parcelas(CARROS[carro], entrada)

            resposta = "As parcelas ficam assim:\n"
            for k in ["60x", "48x", "36x", "24x", "12x"]:
                resposta += f"{k} de R$ {parcelas[k]}\n"

            print(resposta)
            set_estagio("simulacao_enviada")
            continue

        # -------- VALOR À VISTA --------
        if carro and falou_valor(texto_lower):
            print(f"O valor à vista é R$ {CARROS[carro]}.")
            continue

        # -------- PÓS SIMULAÇÃO --------
        if estagio == "simulacao_enviada":
            print(
                "Assim fica mais tranquilo. "
                "Você prefere vir até a loja ou fazer a compra à distância?"
            )
            set_estagio("direcionamento")
            continue

        # -------- FECHAMENTO --------
        if estagio == "direcionamento" and any(
            p in texto_lower for p in ["loja", "ir", "pessoalmente", "distância", "distancia", "online"]
        ):
            print(
                "Perfeito. Para darmos andamento na sua compra, "
                "vou precisar de uma foto da sua identidade ou CNH "
                "e um comprovante de residência."
            )
            set_estagio("documentos")
            continue

        # -------- FLUXO NORMAL (IA) --------
        resposta = conversar(texto)
        print(resposta)


if __name__ == "__main__":
    main()
