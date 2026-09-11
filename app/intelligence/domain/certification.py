"""
=====================================================

TalentAI World

Certification Domain Model

Represents a professional certification recognized
by TALIA OS.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Certification:
    """
    Official professional certification used by TALIA OS.

    A Certification represents a credential independently
    from a Candidate, Job or Mission.
    """

    name: str

    issuer: str = ""

    credential_id: str = ""

    expiration_date: str = ""