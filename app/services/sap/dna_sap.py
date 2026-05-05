def gerar_dna_sap(texto):

    texto = texto.lower()

    dna = {
        "modulos": [],
        "processos": [],
        "integracoes": [],
        "fiscal": False,
        "s4hana": False
    }

    # =========================
    # 📦 MÓDULOS SAP
    # =========================
    if "mm" in texto:
        dna["modulos"].append("mm")

    if "sd" in texto:
        dna["modulos"].append("sd")

    if "fi" in texto:
        dna["modulos"].append("fi")

    if "wm" in texto or "ewm" in texto:
        dna["modulos"].append("wm")

    # =========================
    # 🔄 PROCESSOS
    # =========================
    if "p2p" in texto:
        dna["processos"].append("p2p")

    if "otc" in texto:
        dna["processos"].append("otc")

    # =========================
    # 🔗 INTEGRAÇÕES
    # =========================
    if "idoc" in texto:
        dna["integracoes"].append("idoc")

    if "drc" in texto:
        dna["integracoes"].append("drc")

    if "3pl" in texto:
        dna["integracoes"].append("3pl")

    # =========================
    # 🇧🇷 FISCAL
    # =========================
    if any(x in texto for x in ["tax", "fiscal", "nf"]):
        dna["fiscal"] = True

    # =========================
    # 🚀 S/4HANA
    # =========================
    if "s4hana" in texto or "s/4hana" in texto:
        dna["s4hana"] = True

    return dna