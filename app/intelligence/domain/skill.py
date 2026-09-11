"""
=====================================================

TalentAI World

Skill Domain Model

Represents a professional skill recognized
by TALIA OS.

A Skill describes a capability demonstrated
or required within the intelligence domain.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Skill:
    """
    Official professional skill used by TALIA OS.

    A Skill represents a capability independently
    from a Candidate, Job or Mission.
    """

    name: str

    category: str = ""

    level: str = ""