"""
=====================================================

TalentAI

Executive Briefing Agent

Responsável por gerar o briefing executivo
apresentado pela TALIA no Dashboard.

Author:
TalentAI Team

Version:
1.2

=====================================================
"""

from datetime import datetime


class ExecutiveBriefingAgent:

    NAME = "Executive Briefing Agent"
    VERSION = "1.2"
    DESCRIPTION = "Generates the executive dashboard briefing."

    def __init__(self):

        self.generated_at = datetime.now()

    def build(
        self,
        total_vagas,
        vagas_novas,
        total_candidatos,
        entrevistas_hoje,
        matches_90,
        media_match,
        language="en-US"
    ):
        """
        Gera o briefing executivo da TALIA
        de acordo com o idioma selecionado.
        """

        is_pt = language == "pt-BR"

        # ==========================================
        # GREETING
        # ==========================================

        hour = datetime.now().hour

        if is_pt:

            if hour < 12:
                greeting = "Bom dia, Alessandra."

            elif hour < 18:
                greeting = "Boa tarde, Alessandra."

            else:
                greeting = "Boa noite, Alessandra."

        else:

            if hour < 12:
                greeting = "Good morning, Alessandra."

            elif hour < 18:
                greeting = "Good afternoon, Alessandra."

            else:
                greeting = "Good evening, Alessandra."

        # ==========================================
        # SUMMARY
        # ==========================================

        if is_pt:

            summary = (
                "Já analisei a atividade de recrutamento de hoje."
            )

        else:

            summary = (
                "I've already analyzed today's recruitment activity."
            )

        # ==========================================
        # EXECUTIVE INSIGHTS
        # ==========================================

        insights = []

        if matches_90 >= 3:

            if is_pt:

                insights.append({
                    "title": "Candidatos com Alta Aderência Prontos",
                    "description": (
                        f"Você possui atualmente {matches_90} candidatos "
                        "com match de 90% ou superior. "
                        "Esses perfis devem ser priorizados para apresentação aos clientes."
                    )
                })

            else:

                insights.append({
                    "title": "High-Match Candidates Ready",
                    "description": (
                        f"You currently have {matches_90} candidates "
                        "with a match score of 90% or higher. "
                        "These profiles should be prioritized for client submission."
                    )
                })

        if entrevistas_hoje > 0:

            if is_pt:

                insights.append({
                    "title": "Entrevistas Agendadas para Hoje",
                    "description": (
                        f"Existem {entrevistas_hoje} entrevista(s) "
                        "agendada(s) para hoje que requerem atenção."
                    )
                })

            else:

                insights.append({
                    "title": "Interviews Scheduled Today",
                    "description": (
                        f"There are {entrevistas_hoje} interview(s) "
                        "scheduled for today that require attention."
                    )
                })

        if total_vagas > 20:

            if is_pt:

                insights.append({
                    "title": "Alto Volume de Vagas Ativas",
                    "description": (
                        f"Existem atualmente {total_vagas} vagas ativas. "
                        "Considere priorizar as posições mais críticas."
                    )
                })

            else:

                insights.append({
                    "title": "High Volume of Active Jobs",
                    "description": (
                        f"There are currently {total_vagas} active jobs. "
                        "Consider prioritizing the most critical positions."
                    )
                })

        if vagas_novas > 0:

            if is_pt:

                insights.append({
                    "title": "Demanda Ativa de Recrutamento",
                    "description": (
                        f"Existem {vagas_novas} oportunidades ativas de recrutamento "
                        "que requerem atenção no pipeline."
                    )
                })

            else:

                insights.append({
                    "title": "Active Recruitment Demand",
                    "description": (
                        f"There are {vagas_novas} active recruitment "
                        "opportunities requiring pipeline attention."
                    )
                })

        if media_match < 50 and total_candidatos > 0:

            if is_pt:

                insights.append({
                    "title": "Oportunidade de Alinhamento de Talentos",
                    "description": (
                        f"O match médio atual dos candidatos é de "
                        f"{media_match:.2f}%. "
                        "Revisar os critérios de busca pode melhorar a aderência geral dos perfis."
                    )
                })

            else:

                insights.append({
                    "title": "Talent Alignment Opportunity",
                    "description": (
                        f"The current average candidate match is "
                        f"{media_match:.2f}%. "
                        "Reviewing sourcing criteria may improve overall alignment."
                    )
                })

        if not insights:

            if is_pt:

                insights.append({
                    "title": "Pipeline de Recrutamento Estável",
                    "description": (
                        "Sua operação de recrutamento está estável no momento, "
                        "sem alertas críticos que exijam ação imediata."
                    )
                })

            else:

                insights.append({
                    "title": "Recruitment Pipeline Stable",
                    "description": (
                        "Your recruitment operation is currently stable "
                        "with no critical alerts requiring immediate action."
                    )
                })

        # ==========================================
        # AI RECOMMENDATION
        # ==========================================

        if matches_90 > 0:

            if is_pt:

                recommendation = (
                    f"Priorize os {matches_90} candidato(s) com alta aderência "
                    "que já estão prontos para revisão e apresentação. "
                    "Comece pelas vagas ativas que apresentam maior alinhamento "
                    "entre os requisitos e os candidatos disponíveis."
                )

            else:

                recommendation = (
                    f"Prioritize the {matches_90} high-match candidate(s) "
                    "currently ready for review and submission. "
                    "Start with active positions that already have strong "
                    "candidate alignment."
                )

        elif total_vagas > 0:

            if is_pt:

                recommendation = (
                    "Concentre os esforços de sourcing nas vagas ativas com "
                    "menor cobertura de candidatos e fortaleça o pipeline de talentos "
                    "antes de iniciar novas buscas."
                )

            else:

                recommendation = (
                    "Focus sourcing efforts on active positions with the "
                    "lowest candidate coverage and strengthen the talent "
                    "pipeline before opening additional searches."
                )

        else:

            if is_pt:

                recommendation = (
                    "Seu pipeline de recrutamento está estável no momento. "
                    "Continue monitorando a disponibilidade de talentos e "
                    "as próximas demandas."
                )

            else:

                recommendation = (
                    "Your recruitment pipeline is currently stable. "
                    "Continue monitoring talent availability and upcoming demand."
                )

        # ==========================================
        # METRICS
        # ==========================================

        if is_pt:

            metrics = [

                {
                    "value": total_vagas,
                    "label": "Vagas Ativas"
                },

                {
                    "value": matches_90,
                    "label": "Prontos para Apresentação"
                },

                {
                    "value": f"{media_match:.2f}%",
                    "label": "Match Médio"
                }

            ]

            executive_title = "Chief AI Recruiter"

        else:

            metrics = [

                {
                    "value": total_vagas,
                    "label": "Active Jobs"
                },

                {
                    "value": matches_90,
                    "label": "Ready to Submit"
                },

                {
                    "value": f"{media_match:.2f}%",
                    "label": "Average Match"
                }

            ]

            executive_title = "Chief AI Recruiter"

        # ==========================================
        # RETURN
        # ==========================================

        return {

            "status": "Online",

            "executive_title": executive_title,

            "greeting": greeting,

            "summary": summary,

            "metrics": metrics,

            "insights": insights,

            "recommendation": recommendation

        }