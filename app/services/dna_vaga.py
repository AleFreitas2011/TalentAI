def gerar_dna_vaga(descricao):

    texto = descricao.lower()

    dna = {
        "modulos": [],
        "processos": [],
        "integracoes": [],
        "fiscal": False,
        "s4hana": False
    }

    modulos = ["mm", "sd", "fi", "co", "pp", "wm", "ewm"]

    for m in modulos:
        if m in texto:
            dna["modulos"].append(m)

    if "p2p" in texto:
        dna["processos"].append("p2p")

    if "otc" in texto:
        dna["processos"].append("otc")

    if "idoc" in texto:
        dna["integracoes"].append("idoc")

    if "drc" in texto:
        dna["integracoes"].append("drc")

    if "3pl" in texto:
        dna["integracoes"].append("3pl")

    if any(x in texto for x in ["tax", "fiscal", "nf"]):
        dna["fiscal"] = True

    if "s4hana" in texto or "s/4hana" in texto:
        dna["s4hana"] = True

    return dna