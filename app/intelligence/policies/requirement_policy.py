"""
=====================================================

TalentAI World

Requirement Policy

Base implementation for requirement policies.

Author:
TalentAI Team

Version:
2.0

=====================================================
"""

from app.intelligence.decision.decision_status import (
    DecisionStatus
)

from app.intelligence.policies.base_policy import (
    BasePolicy
)


class RequirementPolicy(BasePolicy):

    EVIDENCE_TYPE = None

    REQUIREMENT_FIELD = ""

    ERROR_MESSAGE = ""

    def evaluate(

        self,

        mission,

        evidence_set,

        decision

    ):

        requirements = getattr(

            mission,

            self.REQUIREMENT_FIELD,

            []

        )

        if not requirements:

            return decision

        evidences = evidence_set.by_type(

            self.EVIDENCE_TYPE

        )

        found = {

            evidence.title.upper()

            for evidence in evidences

        }

        missing = []

        for item in requirements:

            if item.upper() not in found:

                missing.append(item)

        if missing:

            decision.status = DecisionStatus.REJECTED

            decision.failed_policies.append(

                self.NAME

            )

            decision.risks.append(

                self.ERROR_MESSAGE +

                ", ".join(missing)

            )

        else:

            decision.satisfied_policies.append(

                self.NAME

            )

            decision.strengths.append(

                f"All required items found for {self.NAME}."

            )

        return decision