def normalizar(texto):

    if not texto:
        return ""

    texto = texto.lower()

    mapa = {
        "s/4hana": "s4hana",
        "node.js": "nodejs",
        "node js": "nodejs",
        "c sharp": "c#",
        "procure to pay": "p2p"
    }

    for k, v in mapa.items():
        texto = texto.replace(k, v)

    return texto