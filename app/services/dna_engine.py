from .perfil_detector import detectar_perfil
from .normalizer import normalizar

from .sap.dna_sap import gerar_dna_sap
from .sap.match_sap import match_sap


def analisar_candidato(texto_cv, descricao_vaga):

    texto_cv = normalizar(texto_cv)
    descricao_vaga = normalizar(descricao_vaga)

    perfil = detectar_perfil(descricao_vaga)

    if perfil == "sap":

        dna_cv = gerar_dna_sap(texto_cv)
        dna_vaga = gerar_dna_sap(descricao_vaga)

        score = match_sap(dna_vaga, dna_cv)

        return {
            "score": score,
            "skills": dna_cv["modulos"] + dna_cv["processos"],
            "perfil": "sap"
        }

    return {
        "score": 0,
        "skills": [],
        "perfil": "geral"
    }