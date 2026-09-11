"""
=====================================================

Recruiter Agent

Especialista em análise de candidatos sob a ótica
de um recrutador sênior.

Responsabilidades:

- Avaliar senioridade
- Avaliar aderência à vaga
- Identificar pontos fortes
- Identificar pontos de atenção
- Gerar recomendação

Author: TalentAI Team

=====================================================
"""

from datetime import datetime


class RecruiterAgent:

    NAME = "Recruiter Agent"
    VERSION = "1.0"

    def __init__(self):

        self.started_at = datetime.now()

    def status(self):

        return {

            "agent": self.NAME,

            "version": self.VERSION,

            "status": "ONLINE",

            "started_at": self.started_at.isoformat()

        }

    def identificar_competencia_principal(self, vaga):

        titulo = (vaga.titulo or "").upper()

        if "SAP FI" in titulo:
            return "SAP FI"

        if "SAP MM" in titulo:
            return "SAP MM"

        if "JAVA" in titulo:
            return "JAVA"

        if "PYTHON" in titulo:
            return "PYTHON"

        if "ORACLE" in titulo:
            return "ORACLE"

        return "NÃO IDENTIFICADA"

    def calcular_experiencia(self, candidato, competencia):

        texto = (candidato.texto_cv or "").upper()

        if competencia in texto:
            return "IDENTIFICADA"

        return "NÃO IDENTIFICADA"

    def analisar(
        self,
        candidato,
        vaga
    ):

        competencia = self.identificar_competencia_principal(vaga)

        experiencia = self.calcular_experiencia(
            candidato,
            competencia
        )

        return {

            "success": True,

            "agent": self.NAME,

            "version": self.VERSION,

            "analysis": {

                "primary_skill": competencia,

                "experience_found": experiencia,

                "calculated_seniority": None,

                "recommendation": "UNDER_REVIEW"

            }

        }