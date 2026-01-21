from collections import deque

# Histórico simples de conversa (simula um cliente)
historico = deque(maxlen=15)

def adicionar_mensagem(role, content):
    historico.append({
        "role": role,
        "content": content
    })

def obter_historico():
    return list(historico)

def limpar_historico():
    historico.clear()


estado = {
    "carro": None,
    "entrada": None
}

def set_carro(nome):
    estado["carro"] = nome

def get_carro():
    return estado["carro"]

def set_entrada(valor):
    estado["entrada"] = valor

def get_entrada():
    return estado["entrada"]

# -----------------------------
# ESTÁGIO DA CONVERSA
# -----------------------------
estagio = "inicio"

def set_estagio(novo):
    global estagio
    estagio = novo

def get_estagio():
    return estagio
