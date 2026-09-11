"""
=====================================================

Candidate Reasoning

Responsible for candidate reasoning.

Transforms mission evidence into
business decisions.

Author:
TalentAI Team

Version:
3.0

=====================================================
"""

from app.intelligence.evidence.evidence_builder import (
    EvidenceBuilder
)

from app.intelligence.reasoning.reasoning_engine import (
    ReasoningEngine
)

from app.intelligence.missions.mission import (
    Mission
)


class CandidateReasoning:

    NAME = "Candidate Reasoning"

    VERSION = "3.0"

    DESCRIPTION = (
        "Candidate reasoning engine."
    )

    def __init__(self):

        self.evidence_builder = EvidenceBuilder()

        self.reasoning_engine = ReasoningEngine()

    def execute(
        self,
        mission: Mission
    ):

        #
        # Build structured evidences
        #

        evidence_set = self.evidence_builder.build(

            mission.candidate,

            mission.job,

            mission.context,

            mission.demand_profile

        )

        #
        # Execute reasoning pipeline
        #

        decision = self.reasoning_engine.analyze(

            mission,

            evidence_set

        )

        return {

            "success": True,

            "candidate": getattr(
                mission.candidate,
                "full_name",
                ""
            ),

            "job": getattr(
                mission.job,
                "title",
                ""
            ),

            #
            # Mission ID only.
            # The Mission object itself must not
            # be returned because it is not JSON serializable.
            #

            "mission_id": getattr(
                mission,
                "id",
                None
            ),

            "decision": decision,

            "evidence_set": evidence_set,

            "context": mission.context

        }