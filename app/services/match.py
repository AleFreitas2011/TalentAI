import re


def normalizar(texto):
    texto = texto.lower()

    # 🔥 padronizações inteligentes
    texto = texto.replace("s/4hana", "s4hana")
    texto = texto.replace("procure to pay", "p2p")

    # remove caracteres especiais
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)

    # remove espaços duplicados
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


def calcular_match(vaga, texto_cv):

    texto_cv = normalizar(texto_cv)

    obrigatorios = [
        "sap", "mm", "s4hana", "p2p",
        "fiscal", "tax", "brazil"
    ]

    importantes = [
        "integration", "idoc", "interface",
        "rollout", "implementation",
        "customizing", "config",
        "procurement", "supply chain"
    ]

    encontrados = []
    faltantes = []

    score = 0
    max_score = 0

    # 🔥 OBRIGATÓRIOS (peso alto)
    for p in obrigatorios:
        max_score += 10
        if p in texto_cv:
            score += 10
            encontrados.append(p)
        else:
            faltantes.append(p)

    # 🔥 IMPORTANTES (peso médio)
    for p in importantes:
        max_score += 5
        if p in texto_cv:
            score += 5
            encontrados.append(p)

    # 🔥 BÔNUS (experiência)
    if "years" in texto_cv or "anos" in texto_cv:
        score += 10
        max_score += 10

    # 🔥 cálculo final
    score_final = int((score / max_score) * 100) if max_score else 0

    # 🔒 limite
    score_final = min(score_final, 100)

    return {
        "score": score_final,
        "encontradas": list(set(encontrados)),
        "faltantes": faltantes
    }