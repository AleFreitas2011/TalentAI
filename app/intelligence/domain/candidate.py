"""
=====================================================

TalentAI World

Candidate Domain Model

Represents a candidate inside the TALIA OS domain.

This model contains only intrinsic candidate data.
Analysis results such as match score, risks, gaps
and recommendations belong to the intelligence
pipeline and must not be stored in this entity.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(slots=True)
class Candidate:
    """
    Official Candidate domain entity used by TALIA OS.

    A Candidate represents the person being analyzed
    independently from any specific Mission or Job.
    """

    # =================================================
    # IDENTIFICATION
    # =================================================

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    # =================================================
    # PERSONAL INFORMATION
    # =================================================

    full_name: str = ""

    email: str = ""

    phone: str = ""

    # =================================================
    # LOCATION
    # =================================================

    city: str = ""

    state: str = ""

    country: str = ""

    # =================================================
    # PROFESSIONAL IDENTITY
    # =================================================

    linkedin: str = ""

    nationality: str = ""