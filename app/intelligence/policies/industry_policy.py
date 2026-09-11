"""
=====================================================

TalentAI World

Industry Policy

Checks mandatory industry experience.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from app.intelligence.evidence.evidence_type import (
    EvidenceType
)

from app.intelligence.policies.requirement_policy import (
    RequirementPolicy
)


class IndustryPolicy(

    RequirementPolicy

):

    NAME = "Industry Policy"

    DESCRIPTION = (
        "Checks mandatory industry experience."
    )

    EVIDENCE_TYPE = EvidenceType.BUSINESS

    REQUIREMENT_FIELD = "mandatory_industries"

    ERROR_MESSAGE = (
        "Missing industry experience: "
    )