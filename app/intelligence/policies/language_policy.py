"""
=====================================================

TalentAI World

Language Policy

Validates mandatory language requirements
against candidate language evidence.

Author:
TalentAI Team

Version:
2.0

=====================================================
"""

from app.intelligence.evidence.evidence_type import (
    EvidenceType
)

from app.intelligence.decision.decision_status import (
    DecisionStatus
)

from app.intelligence.policies.base_policy import (
    BasePolicy
)


class LanguagePolicy(BasePolicy):

    NAME = "Language Policy"

    VERSION = "2.0"

    DESCRIPTION = (
        "Validates mandatory language requirements."
    )

    # =====================================================
    # PROFICIENCY SCALE
    # =====================================================

    PROFICIENCY_SCALE = {
        "BASIC": 1,
        "INTERMEDIATE": 2,
        "ADVANCED": 3,
        "FLUENT": 4,
        "NATIVE": 5
    }

    # =====================================================
    # EVALUATION
    # =====================================================

    def evaluate(
        self,
        mission,
        evidence_set,
        decision
    ):
        """
        Validates language requirements defined by
        Demand Intelligence against candidate evidence.

        A language requirement with a proficiency level
        requires evidence of the same or a higher level.

        A language requirement without a proficiency
        level requires only evidence of the language.
        """

        # =================================================
        # DEMAND REQUIREMENTS
        # =================================================

        demand_profile = getattr(
            mission,
            "demand_profile",
            None
        )

        if demand_profile is None:
            return decision

        technical_requirements = getattr(
            demand_profile,
            "technical_requirements",
            None
        )

        if technical_requirements is None:
            return decision

        language_requirements = getattr(
            technical_requirements,
            "languages",
            []
        ) or []

        if not language_requirements:
            return decision

        # =================================================
        # CANDIDATE LANGUAGE EVIDENCE
        # =================================================

        language_evidences = evidence_set.by_type(
            EvidenceType.LANGUAGE
        )

        candidate_languages = {}

        for evidence in language_evidences:

            language_name = (
                evidence.title
                .strip()
                .upper()
            )

            level = ""

            if isinstance(
                evidence.value,
                dict
            ):

                level = str(
                    evidence.value.get(
                        "level",
                        ""
                    )
                ).strip().upper()

            candidate_languages[
                language_name
            ] = level

        # =================================================
        # REQUIREMENT VALIDATION
        # =================================================

        missing_languages = []

        insufficient_languages = []

        satisfied_languages = []

        for requirement in language_requirements:

            parts = str(
                requirement
            ).split(
                ":",
                1
            )

            required_language = (
                parts[0]
                .strip()
                .upper()
            )

            required_level = ""

            if len(parts) > 1:

                required_level = (
                    parts[1]
                    .strip()
                    .upper()
                )

            # ---------------------------------------------
            # LANGUAGE NOT FOUND
            # ---------------------------------------------

            if required_language not in candidate_languages:

                missing_languages.append(
                    required_language
                )

                continue

            candidate_level = candidate_languages[
                required_language
            ]

            # ---------------------------------------------
            # NO PROFICIENCY REQUIRED
            # ---------------------------------------------

            if not required_level:

                satisfied_languages.append(
                    required_language
                )

                continue

            # ---------------------------------------------
            # CANDIDATE LEVEL NOT PROVEN
            # ---------------------------------------------

            if not candidate_level:

                insufficient_languages.append(
                    (
                        required_language,
                        required_level,
                        ""
                    )
                )

                continue

            required_score = self.PROFICIENCY_SCALE.get(
                required_level
            )

            candidate_score = self.PROFICIENCY_SCALE.get(
                candidate_level
            )

            if (
                required_score is None
                or candidate_score is None
            ):

                insufficient_languages.append(
                    (
                        required_language,
                        required_level,
                        candidate_level
                    )
                )

                continue

            # ---------------------------------------------
            # PROFICIENCY COMPARISON
            # ---------------------------------------------

            if candidate_score >= required_score:

                satisfied_languages.append(
                    required_language
                )

            else:

                insufficient_languages.append(
                    (
                        required_language,
                        required_level,
                        candidate_level
                    )
                )

        # =================================================
        # POLICY RESULT
        # =================================================

        if (
            missing_languages
            or insufficient_languages
        ):

            decision.status = DecisionStatus.REJECTED

            if self.NAME not in decision.failed_policies:

                decision.failed_policies.append(
                    self.NAME
                )

            for language in missing_languages:

                decision.risks.append(
                    f"Required language not evidenced: "
                    f"{language}."
                )

            for (
                language,
                required_level,
                candidate_level
            ) in insufficient_languages:

                if candidate_level:

                    decision.risks.append(
                        f"{language} proficiency below requirement: "
                        f"{candidate_level} versus "
                        f"{required_level} required."
                    )

                else:

                    decision.risks.append(
                        f"{language} proficiency level not evidenced; "
                        f"{required_level} required."
                    )

            return decision

        # =================================================
        # POLICY SATISFIED
        # =================================================

        if self.NAME not in decision.satisfied_policies:

            decision.satisfied_policies.append(
                self.NAME
            )

        if satisfied_languages:

            decision.strengths.append(
                "All required language requirements satisfied."
            )

        return decision