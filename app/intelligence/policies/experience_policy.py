"""
=====================================================

TalentAI World

Experience Policy

Checks minimum professional experience.

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


class ExperiencePolicy(

    RequirementPolicy

):

    NAME = "Experience Policy"

    DESCRIPTION = (
        "Checks mandatory experience."
    )

    EVIDENCE_TYPE = EvidenceType.EXPERIENCE

    REQUIREMENT_FIELD = "mandatory_experience"

    ERROR_MESSAGE = (
        "Missing required experience: "
    )