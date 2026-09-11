"""
=====================================================

TalentAI World

TALIA Reasoning

Coordinates TALIA reasoning engines.

Author:
TalentAI Team

Version:
4.0

=====================================================
"""

from app.intelligence.reasoning.candidate_reasoning import (
    CandidateReasoning
)

from app.intelligence.missions.mission import (
    Mission
)


class Reasoning:

    NAME = "Reasoning"

    VERSION = "4.0"

    DESCRIPTION = (
        "Coordinates TALIA reasoning engines."
    )

    def __init__(self):

        self.candidate_reasoning = CandidateReasoning()

    def execute(
        self,
        mission: Mission
    ):
        """
        Executes TALIA reasoning for a Mission.
        """

        return self.candidate_reasoning.execute(
            mission
        )