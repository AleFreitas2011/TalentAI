import re

def extrair_telefone(texto):

    if not texto:
        return None

    # remove tudo que não for número
    numeros = re.sub(r"\D", "", texto)

    # remove código do país (55) se existir
    if numeros.startswith("55"):
        numeros = numeros[2:]

    # procura número com DDD (11 dígitos)
    match = re.search(r"\d{11}", numeros)

    if match:
        return match.group(0)

    return None