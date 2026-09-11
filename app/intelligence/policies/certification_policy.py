"""
=====================================================

TalentAI World

Language Policy

=====================================================
"""

from app.intelligence.evidence.evidence_type import (
    EvidenceType
)

from app.intelligence.policies.requirement_policy import (
    RequirementPolicy
)


class LanguagePolicy(

    RequirementPolicy

):

    NAME = "Language Policy"

    DESCRIPTION = "Checks mandatory languages."

    EVIDENCE_TYPE = EvidenceType.LANGUAGE

    REQUIREMENT_FIELD = "mandatory_languages"

    ERROR_MESSAGE = "Missing mandatory languages: "