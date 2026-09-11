"""
=====================================================

TalentAI World

TALIA Kernel

Central execution engine for TALIA OS.

Every intelligence request must pass
through the Kernel.

Author:
TalentAI Team

Version:
2.0

=====================================================
"""

from app.intelligence.talia.orchestrator import (
    Orchestrator
)

from app.intelligence.missions.mission import (
    Mission
)


class TaliaKernel:

    NAME = "TALIA Kernel"

    VERSION = "2.0"

    DESCRIPTION = (
        "Central Intelligence Runtime."
    )

    def __init__(self):

        self.orchestrator = Orchestrator()

    def execute(
        self,
        mission: Mission
    ):
        """
        Executes a TALIA Mission.

        Every request inside TALIA starts
        with a Mission.
        """

        mission.start()

        decision = self.orchestrator.execute(
            mission
        )

        mission.finish()

        return decision