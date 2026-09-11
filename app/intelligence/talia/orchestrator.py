"""
=====================================================

TalentAI World

TALIA Orchestrator

Coordinates all TALIA intelligence components.

Every execution starts with a Mission.

Author:
TalentAI Team

Version:
3.0

=====================================================
"""

from app.intelligence.talia.reasoning import (
    Reasoning
)

from app.intelligence.missions.mission import (
    Mission
)


class Orchestrator:
    """
    TALIA Workflow Manager.

    Coordinates all intelligence components.
    """

    NAME = "Orchestrator"

    VERSION = "3.0"

    DESCRIPTION = (
        "Coordinates TALIA execution flow."
    )

    def __init__(self):

        self.reasoning = Reasoning()

    def execute(
        self,
        mission: Mission
    ):
        """
        Executes a TALIA Mission.
        """

        return self.reasoning.execute(
            mission
        )