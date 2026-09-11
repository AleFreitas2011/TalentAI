"""
=====================================================

TalentAI OS

Technology Domain Model

Represents an official technology recognized
by TALIA.

Author:
TalentAI Team

Version:
2.1

=====================================================
"""

import re

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Technology:
    """
    Official technology recognized by TALIA.
    """

    name: str

    vendor: str

    category: str

    aliases: list[str] = field(default_factory=list)

    # =====================================================
    # TERM MATCHING
    # =====================================================

    @staticmethod
    def _matches_term(
        term: str,
        text: str
    ) -> bool:
        """
        Checks whether a technology term exists in text
        using safe token boundaries.
        """

        if not term or not text:
            return False

        term = term.strip().lower()
        text = text.strip().lower()

        if not term or not text:
            return False

        escaped_term = re.escape(
            term
        )

        pattern = (
            r"(?<!\w)"
            + escaped_term
            + r"(?!\w)"
        )

        return (
            re.search(
                pattern,
                text
            )
            is not None
        )

    # =====================================================
    # PUBLIC MATCH
    # =====================================================

    def matches(
        self,
        text: str
    ) -> bool:
        """
        Checks whether a text matches this technology
        using its official name or registered aliases.
        """

        if not text:
            return False

        if self._matches_term(
            self.name,
            text
        ):
            return True

        for alias in self.aliases:

            if self._matches_term(
                alias,
                text
            ):
                return True

        return False