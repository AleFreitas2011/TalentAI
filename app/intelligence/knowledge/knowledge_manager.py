"""
=====================================================

TalentAI World

Knowledge Manager

Central access point for TALIA's knowledge base.

Responsibilities

- Normalize technology names
- Resolve aliases
- Search official knowledge
- Extract technologies from text
- Expose knowledge to Intelligence Engines
- Normalize industry names
- Extract industries from text
- Resolve industry relationships

Author:
TalentAI Team

Version:
2.4

=====================================================
"""

import re

from app.intelligence.domain.technology import (
    Technology
)

from app.intelligence.knowledge.official.technologies import (
    OFFICIAL_TECHNOLOGIES
)

from app.intelligence.knowledge.official.industries import (
    OFFICIAL_INDUSTRIES,
    INDUSTRY_RELATIONSHIPS
)

from app.intelligence.knowledge.aliases.technology_aliases import (
    TECHNOLOGY_ALIASES
)


class KnowledgeManager:
    """
    Central access point for TALIA's official knowledge.
    """

    # =====================================================
    # NORMALIZATION
    # =====================================================

    @staticmethod
    def normalize(name: str) -> str:
        """
        Normalize a technology name and resolve it
        to TALIA's official technology name.
        """

        if not name:
            return ""

        normalized = name.strip().lower()

        # =================================================
        # ALIAS RESOLUTION
        # =================================================

        alias_match = TECHNOLOGY_ALIASES.get(
            normalized
        )

        if alias_match:
            return alias_match

        # =================================================
        # OFFICIAL NAME RESOLUTION
        # =================================================

        for official_name in OFFICIAL_TECHNOLOGIES:

            if official_name.lower() == normalized:
                return official_name

        # =================================================
        # UNKNOWN TECHNOLOGY
        # =================================================

        return normalized

    # =====================================================
    # EXISTS
    # =====================================================

    @staticmethod
    def exists(name: str) -> bool:
        """
        Check whether a technology exists.
        """

        official_name = KnowledgeManager.normalize(
            name
        )

        return official_name in OFFICIAL_TECHNOLOGIES

    # =====================================================
    # GET TECHNOLOGY
    # =====================================================

    @staticmethod
    def get_technology(
        name: str
    ) -> Technology | None:
        """
        Retrieve an official technology.
        """

        official_name = KnowledgeManager.normalize(
            name
        )

        return OFFICIAL_TECHNOLOGIES.get(
            official_name
        )

    # =====================================================
    # GET ALL TECHNOLOGIES
    # =====================================================

    @staticmethod
    def get_all_technologies() -> dict[str, Technology]:
        """
        Return the complete official technology catalog.
        """

        return OFFICIAL_TECHNOLOGIES

    # =====================================================
    # FIND TECHNOLOGIES
    # =====================================================

    @staticmethod
    def find_technologies(
        text: str
    ) -> list[Technology]:
        """
        Search all official technologies inside a text.

        Recognition rules:

        - Explicit official technology names are authoritative.
        - Explicit vendor-qualified aliases are authoritative.
        - Generic aliases for vendor-specific technologies
          require compatible vendor context.
        - Generic aliases must not create cross-vendor
          false positives.
        - Generic aliases without vendor context must not
          create certainty about a vendor-specific technology.

        Returns unique Technology objects.
        """

        if not text:
            return []

        found = {}

        # =================================================
        # VENDOR CONTEXT
        # =================================================

        known_vendors = {
            (
                getattr(
                    technology,
                    "vendor",
                    ""
                )
                or ""
            ).strip()
            for technology in OFFICIAL_TECHNOLOGIES.values()
            if (
                getattr(
                    technology,
                    "vendor",
                    ""
                )
                or ""
            ).strip()
        }

        vendors_in_text = {
            vendor
            for vendor in known_vendors
            if Technology._matches_term(
                vendor,
                text
            )
        }

        # =================================================
        # OFFICIAL TECHNOLOGIES
        # =================================================

        for official_name, technology in (
            OFFICIAL_TECHNOLOGIES.items()
        ):

            # ---------------------------------------------
            # OFFICIAL NAME
            # ---------------------------------------------

            if Technology._matches_term(
                technology.name,
                text
            ):

                found[official_name] = technology
                continue

            vendor = (
                getattr(
                    technology,
                    "vendor",
                    ""
                )
                or ""
            ).strip()

            vendor_present = (
                bool(vendor)
                and vendor in vendors_in_text
            )

            # ---------------------------------------------
            # TECHNOLOGY ALIASES
            # ---------------------------------------------

            for alias in technology.aliases:

                if not Technology._matches_term(
                    alias,
                    text
                ):
                    continue

                alias_has_vendor = (
                    bool(vendor)
                    and Technology._matches_term(
                        vendor,
                        alias
                    )
                )

                # Explicit vendor-qualified alias.
                if alias_has_vendor:

                    found[official_name] = technology
                    break

                # Vendor-neutral technology.
                if not vendor:

                    found[official_name] = technology
                    break

                # Generic alias for a vendor-specific
                # technology requires matching vendor
                # context in the source text.
                if vendor_present:

                    found[official_name] = technology
                    break

        # =================================================
        # GLOBAL TECHNOLOGY ALIASES
        # =================================================

        for alias, official_name in (
            TECHNOLOGY_ALIASES.items()
        ):

            technology = OFFICIAL_TECHNOLOGIES.get(
                official_name
            )

            if not technology:
                continue

            if not Technology._matches_term(
                alias,
                text
            ):
                continue

            vendor = (
                getattr(
                    technology,
                    "vendor",
                    ""
                )
                or ""
            ).strip()

            alias_has_vendor = (
                bool(vendor)
                and Technology._matches_term(
                    vendor,
                    alias
                )
            )

            vendor_present = (
                bool(vendor)
                and vendor in vendors_in_text
            )

            # Explicit vendor-qualified alias.
            if alias_has_vendor:

                found[official_name] = technology
                continue

            # Vendor-neutral technology.
            if not vendor:

                found[official_name] = technology
                continue

            # Generic alias requires matching vendor context.
            if vendor_present:

                found[official_name] = technology

        # =================================================
        # OVERLAP RESOLUTION
        # =================================================

        if "C++" in found and "C" in found:

            c_without_cpp = text.replace(
                "C++",
                " "
            ).replace(
                "c++",
                " "
            )

            if not Technology._matches_term(
                "C",
                c_without_cpp
            ):

                found.pop(
                    "C",
                    None
                )

        # =================================================
        # RETURN SORTED RESULT
        # =================================================

        return sorted(
            found.values(),
            key=lambda technology: technology.name
        )

    # =====================================================
    # NORMALIZE INDUSTRY
    # =====================================================

    @staticmethod
    def normalize_industry(
        name: str
    ) -> str:
        """
        Normalize an industry name and resolve aliases
        to TALIA's official industry name.
        """

        if not name:
            return ""

        normalized = (
            name
            .strip()
            .lower()
        )

        # =================================================
        # OFFICIAL INDUSTRY + ALIASES
        # =================================================

        for (
            official_name,
            aliases
        ) in OFFICIAL_INDUSTRIES.items():

            if official_name.lower() == normalized:

                return official_name

            for alias in aliases:

                if alias.lower() == normalized:

                    return official_name

        # =================================================
        # UNKNOWN INDUSTRY
        # =================================================

        return normalized

    # =====================================================
    # FIND INDUSTRIES
    # =====================================================

    @staticmethod
    def find_industries(
        text: str
    ) -> list[str]:
        """
        Search official industries and their aliases
        inside a text.

        Returns unique normalized industry names.
        """

        if not text:
            return []

        found = set()

        # =================================================
        # BOUNDARY-SAFE MATCHING
        # =================================================

        def matches_term(
            term: str,
            source_text: str
        ) -> bool:

            pattern = (
                r"(?<!\w)"
                + re.escape(term)
                + r"(?!\w)"
            )

            return bool(
                re.search(
                    pattern,
                    source_text,
                    flags=re.IGNORECASE
                )
            )

        # =================================================
        # OFFICIAL INDUSTRIES
        # =================================================

        for (
            official_name,
            aliases
        ) in OFFICIAL_INDUSTRIES.items():

            if matches_term(
                official_name,
                text
            ):

                found.add(
                    official_name
                )

                continue

            # =============================================
            # INDUSTRY ALIASES
            # =============================================

            for alias in aliases:

                if matches_term(
                    alias,
                    text
                ):

                    found.add(
                        official_name
                    )

                    break

        # =================================================
        # RETURN SORTED RESULT
        # =================================================

        return sorted(
            found
        )

    # =====================================================
    # GET INDUSTRY RELATIONSHIP
    # =====================================================

    @staticmethod
    def get_industry_relationship(
        source_industry: str,
        target_industry: str
    ) -> float:
        """
        Return the semantic relationship strength
        between two industries.

        Relationship direction:

        source_industry
            Industry required by the demand.

        target_industry
            Industry experience identified for
            the candidate.

        Returns:

        1.00
            Exact industry match.

        0.75 / 0.50
            Known semantic relationship.

        0.00
            No known relationship.

        IMPORTANT:

        This value represents knowledge about
        industry proximity.

        It is not a Business Fit score.
        """

        source = KnowledgeManager.normalize_industry(
            source_industry
        )

        target = KnowledgeManager.normalize_industry(
            target_industry
        )

        if not source or not target:

            return 0.0

        # =================================================
        # UNKNOWN INDUSTRIES
        # =================================================

        if source not in OFFICIAL_INDUSTRIES:

            return 0.0

        if target not in OFFICIAL_INDUSTRIES:

            return 0.0

        # =================================================
        # EXACT MATCH
        # =================================================

        if source == target:

            return 1.0

        # =================================================
        # SEMANTIC RELATIONSHIP
        # =================================================

        relationships = INDUSTRY_RELATIONSHIPS.get(
            source,
            {}
        )

        return float(
            relationships.get(
                target,
                0.0
            )
        )