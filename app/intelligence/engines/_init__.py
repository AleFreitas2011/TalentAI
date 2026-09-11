"""
=====================================================

TalentAI OS

Knowledge Manager

Central Knowledge Access Layer

Responsibilities

- Manage TALIA Knowledge Base
- Search Official Knowledge
- Normalize Aliases
- Register New Discoveries
- Provide Knowledge to Intelligence Engines

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from app.intelligence.knowledge.official.technologies import (
    OFFICIAL_TECHNOLOGIES
)

from app.intelligence.knowledge.aliases.technology_aliases import (
    TECHNOLOGY_ALIASES
)

from app.intelligence.knowledge.learning.pending_technologies import (
    PENDING_TECHNOLOGIES
)


class KnowledgeManager:
    """
    Central access point for TALIA Knowledge Base.
    """

    # =====================================================
    # Normalize Technology
    # =====================================================

    def normalize_technology(self, technology_name: str) -> str:
        """
        Converts aliases into the official technology name.
        """

        if not technology_name:
            return ""

        key = technology_name.strip().lower()

        return TECHNOLOGY_ALIASES.get(
            key,
            technology_name.strip()
        )

    # =====================================================
    # Technology Exists
    # =====================================================

    def technology_exists(self, technology_name: str) -> bool:
        """
        Checks whether a technology exists
        in the official catalog.
        """

        technology = self.normalize_technology(
            technology_name
        )

        return technology in OFFICIAL_TECHNOLOGIES

    # =====================================================
    # Get Technology
    # =====================================================

    def get_technology(self, technology_name: str):
        """
        Returns an official technology object.
        """

        technology = self.normalize_technology(
            technology_name
        )

        return OFFICIAL_TECHNOLOGIES.get(
            technology
        )

    # =====================================================
    # Register Discovery
    # =====================================================

    def register_discovery(self, technology_name: str):
        """
        Registers a new technology for review.
        """

        technology = self.normalize_technology(
            technology_name
        )

        if technology in OFFICIAL_TECHNOLOGIES:
            return

        if technology in PENDING_TECHNOLOGIES:

            PENDING_TECHNOLOGIES[
                technology
            ]["occurrences"] += 1

            return

        PENDING_TECHNOLOGIES[technology] = {

            "name": technology,

            "occurrences": 1,

            "status": "Pending Review"

        }