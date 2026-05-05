import re

def gerar_resumo_cv(texto):
    if not texto:
        return ""

    texto = texto.lower()
    texto = re.sub(r'\s+', ' ', texto)

    # 🔥 SKILLS IMPORTANTES
    palavras = [
        # SAP
        "sap", "mm", "sd", "fi", "co", "wm", "ewm", "s4hana",

        # ORACLE
        "oracle", "ar", "ap", "financials", "erp", "cloud",

        # PROCESSOS
        "p2p", "otc", "order to cash", "procure to pay",
        "logistics", "supply chain",

        # PROJETOS
        "implementation", "rollout", "support", "upgrade",
        "go-live", "migration",

        # FISCAL
        "tax", "fiscal", "brazil", "invoice", "nf-e",

        # SENIORIDADE
        "lead", "manager", "consultant", "specialist"
    ]

    encontrados = []

    for p in palavras:
        if p in texto:
            encontrados.append(p)

    # 🔥 REMOVE DUPLICADOS
    encontrados = list(set(encontrados))

    # 🔥 SE NÃO ENCONTRAR NADA
    if not encontrados:
        return texto[:200]

    # 🔥 MONTA FRASE INTELIGENTE
    principais = ", ".join(encontrados[:5])

    resumo = f"Profissional com experiência em {principais}, atuando em projetos e sustentação de sistemas."

    return resumo