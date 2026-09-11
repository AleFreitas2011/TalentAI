"""
=====================================================

TalentAI World

Reasoning Engine

Coordinates TALIA reasoning process.

Author:
TalentAI Team

Version:
3.0

=====================================================
"""

from app.intelligence.policies.policy_engine import (
    PolicyEngine
)

from app.intelligence.missions.mission import (
    Mission
)

from app.intelligence.decision import (
    Decision
)


class ReasoningEngine:

    NAME = "Reasoning Engine"

    VERSION = "3.0"

    DESCRIPTION = (
        "Coordinates TALIA reasoning process."
    )

    def __init__(self):

        self.policy_engine = PolicyEngine()

    def analyze(
        self,
        mission: Mission,
        evidence_set
    ) -> Decision:
        """
        Executes TALIA reasoning pipeline.

        Mission
            ↓
        Policy Engine
            ↓
        Decision
        """

        return self.policy_engine.evaluate(

            mission,

            evidence_set

        )