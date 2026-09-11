"""
=====================================================

TalentAI OS

Technology Normalizer

Normalizes technology names before they
reach the Knowledge Layer.

Responsibilities

- Normalize text
- Resolve aliases
- Produce canonical technology names

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from app.intelligence.knowledge.aliases.technology_aliases import (
    TECHNOLOGY_ALIASES
)


class TechnologyNormalizer:
    """
    Normalizes technology names.
    """

    @staticmethod
    def normalize(name: str) -> str:
        """
        Normalize a technology name.
        """

        if not name:
            return ""

        normalized = name.strip().lower()

        return TECHNOLOGY_ALIASES.get(
            normalized,
            normalized
        )