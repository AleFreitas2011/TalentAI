"""
=====================================================

TalentAI World

Language Extractor

Extracts language proficiency from
candidate information.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

import re

from app.intelligence.domain.language import (
    Language
)


class LanguageExtractor:

    NAME = "Language Extractor"

    VERSION = "1.0"

    DESCRIPTION = (
        "Extracts language proficiency."
    )

    # =====================================================
    # PROFICIENCY LEVELS
    # =====================================================

    PROFICIENCY_LEVELS = {

        "native": "NATIVE",
        "native speaker": "NATIVE",
        "native or bilingual proficiency": "NATIVE",
        "nativo": "NATIVE",
        "nativa": "NATIVE",

        "fluent": "FLUENT",
        "fluency": "FLUENT",
        "fluente": "FLUENT",
        "full professional proficiency": "FLUENT",
        "c2": "FLUENT",

        "advanced": "ADVANCED",
        "avançado": "ADVANCED",
        "avançada": "ADVANCED",
        "professional working proficiency": "ADVANCED",
        "c1": "ADVANCED",

        "upper intermediate": "INTERMEDIATE",
        "upper-intermediate": "INTERMEDIATE",
        "intermediate": "INTERMEDIATE",
        "intermediário": "INTERMEDIATE",
        "intermediária": "INTERMEDIATE",
        "b2": "INTERMEDIATE",
        "b1": "INTERMEDIATE",

        "elementary": "BASIC",
        "beginner": "BASIC",
        "basic": "BASIC",
        "básico": "BASIC",
        "básica": "BASIC",
        "a2": "BASIC",
        "a1": "BASIC"
    }

    # =====================================================
    # LANGUAGE ALIASES
    # =====================================================

    LANGUAGE_ALIASES = {

        "English": (
            "english",
            "inglês",
            "ingles"
        ),

        "Spanish": (
            "spanish",
            "espanhol",
            "español"
        ),

        "Portuguese": (
            "portuguese",
            "português",
            "portugues"
        )
    }

    # =====================================================
    # LEVEL NORMALIZATION
    # =====================================================

    def _normalize_level(
        self,
        text
    ) -> str:

        normalized_text = text.lower()

        levels = sorted(
            self.PROFICIENCY_LEVELS.items(),
            key=lambda item: len(item[0]),
            reverse=True
        )

        for alias, normalized_level in levels:

            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                normalized_text,
                flags=re.IGNORECASE
            ):

                return normalized_level

        return ""

    # =====================================================
    # EXTRACTION
    # =====================================================

    def extract(
        self,
        context
    ) -> list[Language]:

        perfil = str(
            getattr(
                context,
                "perfil",
                ""
            )
        )

        historico = str(
            getattr(
                context,
                "historico_profissional",
                ""
            )
        )

        texto = str(
            getattr(
                context,
                "texto_cv",
                ""
            )
        )

        source = "\n".join(
            [
                perfil,
                historico,
                texto
            ]
        )

        found_languages = []

        # =================================================
        # SEGMENT-BASED EXTRACTION
        # =================================================
        #
        # Language proficiency must be associated with
        # the correct language.
        #
        # Example:
        #
        # English: Fluent
        # Spanish: Intermediate
        #
        # Each segment is analyzed independently so that
        # proficiency levels do not contaminate each other.
        # =================================================

        segments = re.split(
            r"[\n\r;,|/]+",
            source
        )

        for segment in segments:

            clean_segment = segment.strip()

            if not clean_segment:
                continue

            lower_segment = clean_segment.lower()

            for language_name, aliases in (
                self.LANGUAGE_ALIASES.items()
            ):

                language_found = any(
                    re.search(
                        r"(?<!\w)"
                        + re.escape(alias)
                        + r"(?!\w)",
                        lower_segment,
                        flags=re.IGNORECASE
                    )
                    for alias in aliases
                )

                if not language_found:
                    continue

                level = self._normalize_level(
                    clean_segment
                )

                found_languages.append(
                    Language(
                        name=language_name,
                        level=level
                    )
                )

        # =================================================
        # REMOVE DUPLICATES
        # =================================================

        unique_languages = {}

        for language in found_languages:

            current = unique_languages.get(
                language.name
            )

            if current is None:

                unique_languages[
                    language.name
                ] = language

                continue

            # Preserve an identified proficiency level
            # instead of replacing it with an empty one.

            if (
                not current.level
                and language.level
            ):

                unique_languages[
                    language.name
                ] = language

        return sorted(
            unique_languages.values(),
            key=lambda language: language.name
        )