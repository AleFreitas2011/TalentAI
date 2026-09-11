"""
=====================================================

TalentAI World

Semantic Evidence Resolver

Purpose:
Resolves multiple validated evidence candidates
for the same requirement and selects the strongest
available evidence.

This component is deterministic.

It does NOT:
- call AI providers
- read resumes
- retrieve evidence
- validate semantic entailment
- calculate candidate match
- modify TALIA decisions

Resolution priority:

1. SUPPORTED
2. PARTIALLY_SUPPORTED
3. NOT_SUPPORTED

Confidence is used only as a secondary criterion
inside the same validation class.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from typing import Any


class SemanticEvidenceResolver:

    NAME = "Semantic Evidence Resolver"

    VERSION = "1.0"

    DESCRIPTION = (
        "Selects the strongest validated evidence "
        "for a requirement."
    )

    VALIDATION_PRIORITY = {
        "SUPPORTED": 3,
        "PARTIALLY_SUPPORTED": 2,
        "NOT_SUPPORTED": 1
    }

    # =====================================================
    # PUBLIC API
    # =====================================================

    def resolve(
        self,
        requirement: str,
        validated_candidates: list
    ) -> dict:
        """
        Selects the strongest validated evidence
        candidate for one requirement.

        Validation class has priority over confidence.

        Example:

        SUPPORTED 0.70

        always wins over:

        PARTIALLY_SUPPORTED 0.95
        """

        requirement = self._clean_text(
            requirement
        )

        candidates = self._extract_candidates(
            validated_candidates
        )

        if not candidates:

            return self._empty_result(
                requirement
            )

        ranked = sorted(
            candidates,
            key=self._ranking_key,
            reverse=True
        )

        winner = dict(
            ranked[0]
        )

        winner["requirement"] = (
            requirement
            or self._clean_text(
                winner.get(
                    "requirement"
                )
            )
        )

        winner["resolved"] = True

        winner["candidate_count"] = len(
            candidates
        )

        return winner

    # =====================================================
    # CANDIDATE EXTRACTION
    # =====================================================

    def _extract_candidates(
        self,
        validated_candidates: Any
    ) -> list[dict]:

        if not isinstance(
            validated_candidates,
            list
        ):
            return []

        extracted = []

        for candidate in validated_candidates:

            if not isinstance(
                candidate,
                dict
            ):
                continue

            # ---------------------------------------------
            # Validator output:
            #
            # {
            #     "evidence": [
            #         {...}
            #     ]
            # }
            # ---------------------------------------------

            evidence_items = candidate.get(
                "evidence"
            )

            if isinstance(
                evidence_items,
                list
            ):

                for item in evidence_items:

                    if isinstance(
                        item,
                        dict
                    ):

                        extracted.append(
                            dict(item)
                        )

                continue

            # ---------------------------------------------
            # Also accepts a direct evidence dictionary.
            # ---------------------------------------------

            if (
                "validation" in candidate
                or "status" in candidate
            ):

                extracted.append(
                    dict(candidate)
                )

        return extracted

    # =====================================================
    # RANKING
    # =====================================================

    def _ranking_key(
        self,
        candidate: dict
    ) -> tuple:

        validation = self._clean_text(
            candidate.get(
                "validation"
            )
        ).upper()

        priority = (
            self.VALIDATION_PRIORITY.get(
                validation,
                0
            )
        )

        confidence = self._confidence(
            candidate.get(
                "confidence"
            )
        )

        grounded = bool(
            candidate.get(
                "grounded",
                False
            )
        )

        evidence = self._clean_text(
            candidate.get(
                "evidence"
            )
        )

        # Validation class is always the primary factor.
        #
        # Grounding and confidence are secondary.
        #
        # Evidence length is only a final deterministic
        # tie-breaker and never changes semantic class.

        return (
            priority,
            int(grounded),
            confidence,
            len(evidence)
        )

    # =====================================================
    # EMPTY RESULT
    # =====================================================

    def _empty_result(
        self,
        requirement: str
    ) -> dict:

        return {
            "requirement": requirement,
            "status": "NOT_EVIDENCED",
            "evidence": "",
            "reason": (
                "Semantic Evidence Resolver: "
                "no validated evidence candidates "
                "were available."
            ),
            "confidence": 0.0,
            "grounded": False,
            "validation": "NOT_SUPPORTED",
            "resolved": True,
            "candidate_count": 0
        }

    # =====================================================
    # HELPERS
    # =====================================================

    def _clean_text(
        self,
        value: Any
    ) -> str:

        if value is None:
            return ""

        return str(
            value
        ).strip()

    def _confidence(
        self,
        value: Any
    ) -> float:

        try:

            confidence = float(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return 0.0

        if confidence < 0.0:
            return 0.0

        if confidence > 1.0:
            return 1.0

        return confidence