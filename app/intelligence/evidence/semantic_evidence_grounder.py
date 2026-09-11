"""
=====================================================

TalentAI World

Semantic Evidence Grounder

Purpose:
Grounds semantic candidate evidence against the
original resume text before it can become official
TALIA technical evidence.

Principles:

- AI may discover candidate evidence
- Resume remains the source of truth
- Evidence must be traceable to the resume
- Related knowledge is not direct proof
- Never calculate match scores
- Never invent candidate information
- Vendor and technology agnostic

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

import re
import unicodedata
from typing import Any


class SemanticEvidenceGrounder:

    NAME = "Semantic Evidence Grounder"

    VERSION = "1.0"

    DESCRIPTION = (
        "Validates whether semantic evidence is "
        "grounded in the original resume."
    )

    # =====================================================
    # PUBLIC API
    # =====================================================

    def ground(
        self,
        analysis: dict,
        resume_text: str
    ) -> dict:
        """
        Grounds AI-generated evidence against the
        original resume.

        Input:

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

        Output preserves the same structure and adds:

            grounded: bool

        This class does NOT decide semantic equivalence
        between technologies.

        Its responsibility is narrower:

        If AI claims that a piece of resume text is
        evidence, that evidence must actually be traceable
        to the original resume.
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

        normalized_resume = self._normalize(
            resume_text
        )

        grounded_items = []

        for item in items:

            grounded_item = self._ground_item(
                item,
                normalized_resume
            )

            if grounded_item:

                grounded_items.append(
                    grounded_item
                )

        return {
            "evidence": grounded_items
        }

    # =====================================================
    # ITEM GROUNDING
    # =====================================================

    def _ground_item(
        self,
        item: Any,
        normalized_resume: str
    ) -> dict | None:

        if not isinstance(item, dict):
            return None

        result = dict(
            item
        )

        requirement = self._clean_text(
            result.get(
                "requirement"
            )
        )

        status = self._clean_text(
            result.get(
                "status"
            )
        ).upper()

        evidence = self._clean_text(
            result.get(
                "evidence"
            )
        )

        if not requirement:
            return None

        # =================================================
        # NON-EVIDENCED ITEMS
        # =================================================

        if status == "NOT_EVIDENCED":

            result["grounded"] = True

            return result

        # =================================================
        # CLAIMED EVIDENCE MUST EXIST
        # =================================================

        if not evidence:

            result["status"] = "NOT_EVIDENCED"

            result["confidence"] = 0.0

            result["grounded"] = False

            result["reason"] = (
                "Semantic Evidence Grounder: evidence "
                "was claimed but no resume excerpt "
                "was supplied."
            )

            return result

        # =================================================
        # TRACE EVIDENCE TO RESUME
        # =================================================

        evidence_grounded = self._is_traceable(
            evidence,
            normalized_resume
        )

        if evidence_grounded:

            result["grounded"] = True

            return result

        # =================================================
        # UNTRACEABLE EVIDENCE
        # =================================================

        result["status"] = "UNCERTAIN"

        result["confidence"] = min(
            self._normalize_confidence(
                result.get(
                    "confidence"
                )
            ),
            0.5
        )

        result["grounded"] = False

        original_reason = self._clean_text(
            result.get(
                "reason"
            )
        )

        result["reason"] = (
            "Semantic Evidence Grounder: the supplied "
            "evidence could not be reliably traced to "
            "the original resume."
        )

        if original_reason:

            result["reason"] += (
                f" Original reason: {original_reason}"
            )

        return result

    # =====================================================
    # TRACEABILITY
    # =====================================================

    def _is_traceable(
        self,
        evidence: str,
        normalized_resume: str
    ) -> bool:
        """
        Checks whether the evidence supplied by AI can
        be traced back to the resume.

        Exact normalized containment is preferred.

        A conservative token-overlap fallback exists
        because PDF extraction may introduce whitespace,
        punctuation and line-break differences.
        """

        if not evidence or not normalized_resume:

            return False

        normalized_evidence = self._normalize(
            evidence
        )

        if not normalized_evidence:

            return False

        # =================================================
        # EXACT NORMALIZED CONTAINMENT
        # =================================================

        if normalized_evidence in normalized_resume:

            return True

        # =================================================
        # CONSERVATIVE TOKEN OVERLAP
        # =================================================

        evidence_tokens = self._meaningful_tokens(
            normalized_evidence
        )

        if len(evidence_tokens) < 4:

            return False

        resume_tokens = set(
            self._meaningful_tokens(
                normalized_resume
            )
        )

        if not resume_tokens:

            return False

        matched_tokens = sum(
            1
            for token in evidence_tokens
            if token in resume_tokens
        )

        coverage = (
            matched_tokens
            / len(evidence_tokens)
        )

        return coverage >= 0.85

    # =====================================================
    # NORMALIZATION
    # =====================================================

    def _normalize(
        self,
        value: Any
    ) -> str:

        text = self._clean_text(
            value
        )

        if not text:

            return ""

        text = unicodedata.normalize(
            "NFKD",
            text
        )

        text = "".join(
            character
            for character in text
            if not unicodedata.combining(
                character
            )
        )

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9+#._/-]+",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # =====================================================
    # TOKENIZATION
    # =====================================================

    def _meaningful_tokens(
        self,
        text: str
    ) -> list[str]:

        tokens = re.findall(
            r"[a-z0-9+#._/-]+",
            text
        )

        return [
            token
            for token in tokens
            if len(token) >= 2
        ]

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