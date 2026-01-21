CARROS = {
    "onix": 40900,
    "gol": 12900,
    "gol g3": 12900,
    "civic": 40900
}

def calcular_parcelas(valor_carro, entrada):
    valor_financiar = valor_carro - entrada

    if valor_financiar <= 0:
        return None

    valor_final = valor_financiar * 1.2

    return {
        "60x": round(valor_final / 60, 2),
        "48x": round(valor_final / 48, 2),
        "36x": round(valor_final / 36, 2),
        "24x": round(valor_final / 24, 2),
        "12x": round(valor_final / 12, 2),
    }
