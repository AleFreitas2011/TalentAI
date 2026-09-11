"""
=====================================================

TalentAI World

Mandatory Skill Policy

=====================================================
"""

from app.intelligence.evidence.evidence_type import (
    EvidenceType
)

from app.intelligence.policies.requirement_policy import (
    RequirementPolicy
)


class MandatorySkillPolicy(

    RequirementPolicy

):

    NAME = "Mandatory Skill Policy"

    DESCRIPTION = "Checks mandatory skills."

    EVIDENCE_TYPE = EvidenceType.TECHNICAL

    REQUIREMENT_FIELD = "mandatory_skills"

    ERROR_MESSAGE = "Missing mandatory skills: "