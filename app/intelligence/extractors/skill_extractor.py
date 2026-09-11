"""
=====================================================

TalentAI World

Skill Extractor

Extracts technical skills from
candidate information using
TALIA's official Knowledge Manager.

Author:
TalentAI Team

Version:
3.0

=====================================================
"""

from app.intelligence.knowledge.knowledge_manager import (
    KnowledgeManager
)


class SkillExtractor:

    NAME = "Skill Extractor"

    VERSION = "3.0"

    DESCRIPTION = (
        "Extracts technical skills."
    )

    def __init__(self):

        self.knowledge = KnowledgeManager()

    def extract(
        self,
        context
    ) -> list[str]:

        perfil = str(
            getattr(
                context,
                "perfil",
                ""
            )
        )

        historico = str(
            getattr(
                context,
                "historico_profissional",
                ""
            )
        )

        texto = str(
            getattr(
                context,
                "texto_cv",
                ""
            )
        )

        source = "\n".join(
            [
                perfil,
                historico,
                texto
            ]
        )

        found = []

        for technology in self.knowledge.get_all_technologies().values():

            if technology.matches(source):

                found.append(
                    technology.name
                )

        return sorted(
            set(found)
        )