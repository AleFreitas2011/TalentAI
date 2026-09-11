"""
=====================================================

TalentAI World

Evidence Guard

Purpose:
Validates AI-generated candidate evidence before
it can be consumed by TALIA reasoning.

Principles:

- Evidence must be grounded in the resume
- Related evidence is not confirmed evidence
- Inference cannot become proof
- Never calculate match scores
- Never invent candidate information
- Domain-independent validation

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from typing import Any


class EvidenceGuard:

    NAME = "Evidence Guard"

    VERSION = "1.0"

    DESCRIPTION = (
        "Validates semantic evidence before it enters "
        "TALIA reasoning."
    )

    VALID_STATUSES = {
        "EVIDENCED",
        "UNCERTAIN",
        "NOT_EVIDENCED",
    }

    # Language that indicates the conclusion
    # depends on inference rather than direct proof.
    INFERENCE_MARKERS = (
        "suggests",
        "suggesting",
        "indicates",
        "indicating",
        "likely",
        "probably",
        "presumably",
        "may imply",
        "could imply",
        "appears to",
        "seems to",
        "aligns with",
        "related to",
        "similar to",
        "consistent with",
    )

    # =====================================================
    # PUBLIC API
    # =====================================================

    def validate(
        self,
        analysis: dict
    ) -> dict:
        """
        Validates an AI evidence response.

        Expected input:

        {
            "evidence": [
                {
                    "requirement": "",
                    "status": "",
                    "evidence": "",
                    "reason": "",
                    "confidence": 0.0
                }
            ]
        }

        Returns the same structure with guarded statuses.
        """

        if not isinstance(analysis, dict):

            return {
                "evidence": []
            }

        items = analysis.get(
            "evidence",
            []
        )

        if not isinstance(items, list):

            return {
                "evidence": []
            }

        guarded = []

        for item in items:

            validated = self._validate_item(
                item
            )

            if validated:

                guarded.append(
                    validated
                )

        return {
            "evidence": guarded
        }

    # =====================================================
    # ITEM VALIDATION
    # =====================================================

    def _validate_item(
        self,
        item: Any
    ) -> dict | None:

        if not isinstance(item, dict):
            return None

        requirement = self._clean_text(
            item.get("requirement")
        )

        status = self._clean_text(
            item.get("status")
        ).upper()

        evidence = self._clean_text(
            item.get("evidence")
        )

        reason = self._clean_text(
            item.get("reason")
        )

        confidence = self._normalize_confidence(
            item.get("confidence")
        )

        if not requirement:
            return None

        if status not in self.VALID_STATUSES:

            status = "UNCERTAIN"

            confidence = min(
                confidence,
                0.5
            )

        # =================================================
        # RULE 1
        # EVIDENCED REQUIRES ACTUAL EVIDENCE
        # =================================================

        if (
            status == "EVIDENCED"
            and not evidence
        ):

            status = "NOT_EVIDENCED"

            confidence = 0.0

            reason = (
                "Evidence Guard: the requirement was marked "
                "EVIDENCED but no resume evidence was supplied."
            )

        # =================================================
        # RULE 2
        # INFERENCE CANNOT BECOME CONFIRMED EVIDENCE
        # =================================================

        if (
            status == "EVIDENCED"
            and self._contains_inference_marker(reason)
        ):

            status = "UNCERTAIN"

            confidence = min(
                confidence,
                0.5
            )

            reason = (
                "Evidence Guard: related evidence exists, "
                "but the original analysis relied on "
                "inference rather than direct proof. "
                f"Original reason: {reason}"
            )

        # =================================================
        # RULE 3
        # NOT_EVIDENCED CANNOT HAVE POSITIVE CONFIDENCE
        # =================================================

        if status == "NOT_EVIDENCED":

            confidence = 0.0

        # =================================================
        # RULE 4
        # UNCERTAIN IS NEVER FULL CONFIDENCE
        # =================================================

        if status == "UNCERTAIN":

            confidence = min(
                confidence,
                0.5
            )

        return {
            "requirement": requirement,
            "status": status,
            "evidence": evidence,
            "reason": reason,
            "confidence": confidence,
        }

    # =====================================================
    # INFERENCE DETECTION
    # =====================================================

    def _contains_inference_marker(
        self,
        text: str
    ) -> bool:

        if not text:
            return False

        normalized = text.lower()

        return any(
            marker in normalized
            for marker in self.INFERENCE_MARKERS
        )

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

    def _normalize_confidence(
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