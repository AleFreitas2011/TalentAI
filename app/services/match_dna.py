def calcular_match_dna(dna_vaga, dna_cv):

    score = 0
    peso_total = 0

    # 🔧 MÓDULOS (peso alto)
    peso_modulo = 40

    if dna_vaga["modulos"]:
        peso_por_modulo = peso_modulo / len(dna_vaga["modulos"])
        peso_total += peso_modulo

        for m in dna_vaga["modulos"]:
            if m in dna_cv["modulos"]:
                score += peso_por_modulo

    # 🔄 PROCESSOS (peso médio)
    peso_processos = 20

    if dna_vaga["processos"]:
        peso_por_processo = peso_processos / len(dna_vaga["processos"])
        peso_total += peso_processos

        for p in dna_vaga["processos"]:
            if p in dna_cv["processos"]:
                score += peso_por_processo

    # ⚡ S4HANA (crítico)
    if dna_vaga["s4hana"]:
        peso_total += 20
        if dna_cv["s4hana"]:
            score += 20

    # 🇧🇷 FISCAL (crítico)
    if dna_vaga["fiscal"]:
        peso_total += 10
        if dna_cv["fiscal"]:
            score += 10

    # 🧠 SENIORIDADE
    peso_total += 10

    if dna_cv["senioridade"] == "senior":
        score += 10
    elif dna_cv["senioridade"] == "pleno":
        score += 7
    else:
        score += 3

    # 🔒 NORMALIZAÇÃO
    if peso_total == 0:
        return 0

    score_final = (score / peso_total) * 100

    if score_final > 100:
        score_final = 100

    return round(score_final, 2)