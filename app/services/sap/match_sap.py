def match_sap(vaga, cv):

    score = 0

    # =========================
    # 📦 MÓDULOS
    # =========================
    match_modulos = set(vaga["modulos"]) & set(cv["modulos"])
    score += len(match_modulos) * 25

    # =========================
    # 🔄 PROCESSOS
    # =========================
    match_processos = set(vaga["processos"]) & set(cv["processos"])
    score += len(match_processos) * 20

    # =========================
    # 🔗 INTEGRAÇÕES
    # =========================
    match_integracoes = set(vaga["integracoes"]) & set(cv["integracoes"])
    score += len(match_integracoes) * 15

    # =========================
    # 🇧🇷 FISCAL
    # =========================
    if vaga["fiscal"] and cv["fiscal"]:
        score += 10

    # =========================
    # 🚀 S/4HANA
    # =========================
    if vaga["s4hana"] and cv["s4hana"]:
        score += 10

    return min(score, 100)