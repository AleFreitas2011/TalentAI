import re


def extrair_telefone(texto):

    if not texto:
        return None

    # Procura telefones brasileiros
    padrao = r'(?:\+?55[\s.-]?)?(?:\(?\d{2}\)?[\s.-]?)?(?:9\d{4}[\s.-]?\d{4}|\d{4}[\s.-]?\d{4})'

    telefones = re.findall(padrao, texto)
    print("TELEFONES ENCONTRADOS:")
    print(telefones)

    if not telefones:
        return None

    celulares = []
    fixos = []

    for telefone in telefones:

        numero = re.sub(r"\D", "", telefone)

        # Remove código do país
        if numero.startswith("55"):
            numero = numero[2:]

        # Celular brasileiro = DDD + 9 + 8 dígitos
        if len(numero) == 11 and numero[2] == "9":
            celulares.append(numero)

        # Fixo = DDD + 8 dígitos
        elif len(numero) == 10:
            fixos.append(numero)

    # Prioriza celular
    if celulares:
        return celulares[0]

    # Se não houver celular, retorna fixo
    if fixos:
        return fixos[0]

    return None