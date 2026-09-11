"""
=====================================================

TalentAI
360 Hiring Intelligence

Consultant360 Agent

Responsável por gerar a análise executiva e consultiva
do candidato a partir da inteligência oficial da TALIA.

Author:
TalentAI Team

Version:
2.0

=====================================================
"""

from datetime import datetime


class Consultant360Agent:

    NAME = "Consultant360 Agent"
    VERSION = "2.0"
    DESCRIPTION = (
        "Gera análise executiva e recomendação consultiva "
        "do candidato."
    )
    ANALYSIS_NAME = "360 Hiring Intelligence"
    GENERATED_BY = "TALIA AI"

    # =====================================================
    # TALIA DECISION
    # =====================================================

    def _extrair_match_result(self, decision):

        if decision is None:
            return None

        return getattr(
            decision,
            "match_result",
            None
        )

    def _extrair_skills(self, decision):

        match_result = self._extrair_match_result(
            decision
        )

        if match_result is None:
            return [], []

        matched_skills = getattr(
            match_result,
            "matched_skills",
            {}
        ) or {}

        missing_skills = getattr(
            match_result,
            "missing_skills",
            {}
        ) or {}

        encontradas = []
        faltantes = []

        for categoria in (
            "mandatory",
            "unclassified",
            "nice_to_have"
        ):

            encontradas.extend(
                matched_skills.get(
                    categoria,
                    []
                )
            )

            faltantes.extend(
                missing_skills.get(
                    categoria,
                    []
                )
            )

        encontradas = list(
            dict.fromkeys(
                encontradas
            )
        )

        faltantes = list(
            dict.fromkeys(
                faltantes
            )
        )

        return encontradas, faltantes

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    def gerar_resumo(
        self,
        score,
        encontradas=None,
        faltantes=None
    ):

        encontradas = encontradas or []
        faltantes = faltantes or []

        if score >= 90:

            return (
                "Excelente aderência comprovada aos requisitos "
                "da vaga. O perfil apresenta forte alinhamento "
                "com a oportunidade."
            )

        if score >= 75:

            return (
                "Boa aderência comprovada à vaga. "
                "O perfil apresenta evidências relevantes, "
                "com alguns pontos que devem ser validados "
                "antes da apresentação ao cliente."
            )

        if encontradas:

            return (
                "O perfil apresenta evidências relevantes para "
                "a oportunidade, embora parte dos requisitos "
                "ainda não esteja comprovada no currículo. "
                "Recomenda-se avaliação dos gaps antes de uma "
                "decisão final."
            )

        return (
            "A aderência comprovada à vaga é limitada neste "
            "momento. Recomenda-se revisar os requisitos "
            "essenciais antes de avançar."
        )

    # =====================================================
    # STRENGTHS
    # =====================================================

    def gerar_pontos_fortes(
        self,
        candidato,
        encontradas=None
    ):

        pontos = []

        encontradas = encontradas or []

        for skill in encontradas:

            pontos.append(
                f"Evidência identificada: {skill}."
            )

        if candidato.anos_experiencia:

            pontos.append(
                f"Experiência profissional: "
                f"{candidato.anos_experiencia}."
            )

        if candidato.nivel_ingles:

            pontos.append(
                f"Inglês: {candidato.nivel_ingles}."
            )

        if candidato.nivel_espanhol:

            pontos.append(
                f"Espanhol: {candidato.nivel_espanhol}."
            )

        if candidato.modelo_trabalho:

            pontos.append(
                f"Modelo de trabalho: "
                f"{candidato.modelo_trabalho}."
            )

        return pontos

    # =====================================================
    # ATTENTION POINTS
    # =====================================================

    def gerar_pontos_atencao(
        self,
        candidato,
        faltantes=None
    ):

        pontos = []

        faltantes = faltantes or []

        for skill in faltantes:

            pontos.append(
                f"Requisito sem evidência suficiente: {skill}."
            )

        if not candidato.nivel_ingles:

            pontos.append(
                "Nível de inglês não informado."
            )

        if not candidato.disponibilidade:

            pontos.append(
                "Disponibilidade não informada."
            )

        if not candidato.taxa_candidato:

            pontos.append(
                "Taxa/hora ainda não cadastrada."
            )

        return pontos

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    def gerar_recomendacao(
        self,
        candidato,
        encontradas=None,
        faltantes=None
    ):

        score = candidato.score or 0

        encontradas = encontradas or []
        faltantes = faltantes or []

        quantidade_encontradas = len(
            encontradas
        )

        if score >= 90:

            return (
                "Recomendo a apresentação deste candidato ao "
                "cliente. O perfil demonstra excelente aderência "
                "comprovada aos requisitos da oportunidade."
            )

        if score >= 75:

            return (
                "O candidato apresenta boa aderência comprovada. "
                "Recomendo validar os pontos de atenção "
                "identificados antes do envio ao cliente."
            )

        if score >= 60:

            return (
                "O perfil possui aderência parcial e evidências "
                "relevantes. Recomendo avançar para screening "
                "ou entrevista técnica para validar os requisitos "
                "ainda não comprovados."
            )

        if quantidade_encontradas >= 3:

            return (
                "Apesar do Match comprovado estar abaixo de 60%, "
                "foram identificadas evidências relevantes para "
                "a oportunidade. Recomendo avançar para screening "
                "antes de descartar o perfil, validando os "
                "requisitos ainda não comprovados."
            )

        return (
            "Neste momento, as evidências identificadas são "
            "insuficientes para recomendar a apresentação ao "
            "cliente. Sugere-se revisar os requisitos essenciais "
            "da oportunidade."
        )

    # =====================================================
    # BUSINESS RISKS
    # =====================================================

    def gerar_riscos(
        self,
        candidato,
        faltantes=None
    ):

        riscos = []

        faltantes = faltantes or []

        if faltantes:

            riscos.append(
                "Existem requisitos da vaga sem evidência "
                "suficiente no currículo e que precisam ser "
                "validados com o candidato."
            )

        if not candidato.nivel_ingles:

            riscos.append(
                "O nível de inglês não foi informado e pode "
                "representar um risco para oportunidades "
                "internacionais."
            )

        if not candidato.disponibilidade:

            riscos.append(
                "A disponibilidade do candidato ainda precisa "
                "ser confirmada."
            )

        if not candidato.taxa_candidato:

            riscos.append(
                "A taxa comercial ainda não foi definida, "
                "podendo impactar a negociação com o cliente."
            )

        return riscos

    # =====================================================
    # INTERVIEW QUESTIONS
    # =====================================================

    def gerar_perguntas(
        self,
        candidato,
        faltantes=None
    ):

        perguntas = [
            "Qual foi o projeto mais relevante da sua carreira?",
            "Qual foi sua principal responsabilidade técnica?"
        ]

        faltantes = faltantes or []

        for skill in faltantes:

            perguntas.append(
                f"Você possui experiência prática com "
                f"{skill}? Pode descrever um projeto "
                f"em que utilizou esse conhecimento?"
            )

        if not candidato.nivel_ingles:

            perguntas.append(
                "Qual é o seu nível atual de inglês e você já "
                "atuou em projetos internacionais utilizando "
                "o idioma?"
            )

        return perguntas

    # =====================================================
    # EXECUTION
    # =====================================================

    def executar(
        self,
        candidato,
        vaga=None,
        decision=None
    ):

        if candidato is None:

            raise ValueError(
                "O candidato não pode ser None."
            )

        match_score = candidato.score or 0

        encontradas, faltantes = self._extrair_skills(
            decision
        )

        executive_summary = self.gerar_resumo(
            match_score,
            encontradas,
            faltantes
        )

        strengths = self.gerar_pontos_fortes(
            candidato,
            encontradas
        )

        attention_points = self.gerar_pontos_atencao(
            candidato,
            faltantes
        )

        recommendation = self.gerar_recomendacao(
            candidato,
            encontradas,
            faltantes
        )

        business_risks = self.gerar_riscos(
            candidato,
            faltantes
        )

        interview_questions = self.gerar_perguntas(
            candidato,
            faltantes
        )

        return {

            "success": True,

            "agent": self.NAME,

            "version": self.VERSION,

            "timestamp": datetime.now().isoformat(),

            "analysis": {

                "analysis_name": self.ANALYSIS_NAME,

                "generated_by": self.GENERATED_BY,

                "executive_summary": executive_summary,

                "recommendation": recommendation,

                "strengths": strengths,

                "attention_points": attention_points,

                "business_risks": business_risks,

                "interview_questions": interview_questions,

                "confidence_score": match_score,

                "matched_requirements": encontradas,

                "requirements_to_validate": faltantes

            }

        }