import re

def gerar_dna_cv(texto):

    texto = texto.lower()

    dna = {
        "modulos": [],
        "processos": [],
        "projetos": [],
        "integracoes": [],
        "fiscal": False,
        "s4hana": False,
        "senioridade": "junior"
    }

    # 🔧 módulos SAP
    for m in ["mm", "sd", "fi", "wm", "ewm"]:
        if m in texto:
            dna["modulos"].append(m)

    # 🔄 processos
    if "p2p" in texto or "procure to pay" in texto:
        dna["processos"].append("p2p")

    if "procurement" in texto:
        dna["processos"].append("procurement")

    # 🚀 projetos
    for p in ["rollout", "implementation", "greenfield", "brownfield"]:
        if p in texto:
            dna["projetos"].append(p)

    # 🔗 integração
    if "idoc" in texto:
        dna["integracoes"].append("idoc")

    if "interface" in texto:
        dna["integracoes"].append("interface")

    # 🇧🇷 fiscal
    if any(x in texto for x in ["tax", "fiscal", "nf", "nota fiscal"]):
        dna["fiscal"] = True

    # ⚡ S4
    if "s4hana" in texto or "s/4hana" in texto:
        dna["s4hana"] = True

    # 🧠 senioridade
    anos = re.findall(r"(\d+)\s+(years|anos)", texto)
    if anos:
        max_anos = max([int(a[0]) for a in anos])
        if max_anos >= 10:
            dna["senioridade"] = "senior"
        elif max_anos >= 5:
            dna["senioridade"] = "pleno"

    return dna