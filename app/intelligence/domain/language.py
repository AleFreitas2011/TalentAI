"""
=====================================================

TalentAI World

Language Domain Model

Represents a language proficiency recognized
by TALIA OS.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Language:
    """
    Official language proficiency used by TALIA OS.

    A Language represents a language and the
    proficiency level associated with it.
    """

    name: str

    level: str = ""