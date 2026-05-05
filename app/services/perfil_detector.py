def detectar_perfil(texto):

    texto = texto.lower()

    if "sap" in texto:
        return "sap"

    if any(x in texto for x in ["python", "java", "react", "node"]):
        return "dev"

    return "geral"