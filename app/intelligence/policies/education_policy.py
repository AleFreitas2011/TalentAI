"""
=====================================================

TalentAI World

Education Policy

Checks mandatory education requirements.

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


class EducationPolicy(

    RequirementPolicy

):

    NAME = "Education Policy"

    DESCRIPTION = (
        "Checks mandatory education."
    )

    EVIDENCE_TYPE = EvidenceType.EDUCATION

    REQUIREMENT_FIELD = "mandatory_education"

    ERROR_MESSAGE = (
        "Missing mandatory education: "
    )