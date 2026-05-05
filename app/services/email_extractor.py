import re

def extrair_email(texto):
    texto = texto.lower()

    # 🔥 padrão normal de email
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", texto)
    if emails:
        return emails[0]

    # 🔥 email quebrado tipo: joao @ gmail . com
    texto_corrigido = texto.replace(" @ ", "@").replace(" . ", ".")
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", texto_corrigido)
    if emails:
        return emails[0]

    return "Não encontrado"


def extrair_telefone(texto):
    texto = texto.lower()

    # 🔥 remove emojis comuns
    texto = texto.replace("📱", "").replace("☎", "").replace("📞", "")

    telefones = re.findall(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", texto)

    if telefones:
        return telefones[0]

    return "Não encontrado"