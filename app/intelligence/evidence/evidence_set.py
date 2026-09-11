"""
=====================================================

TalentAI World
Evidence Set

Represents the complete set of evidences
generated during candidate analysis.

Author:
TalentAI Team

Version:
1.1

=====================================================
"""

from dataclasses import dataclass, field
from typing import Any

from app.intelligence.evidence.evidence import Evidence
from app.intelligence.evidence.evidence_type import EvidenceType


@dataclass(slots=True)
class EvidenceSet:

    evidences: list[Evidence] = field(default_factory=list)

    semantic_evidences: list[dict[str, Any]] = field(
        default_factory=list
    )

    # =====================================================
    # STANDARD EVIDENCE
    # =====================================================

    def add(
        self,
        evidence: Evidence
    ):

        self.evidences.append(evidence)

    # =====================================================
    # SEMANTIC REQUIREMENT EVIDENCE
    # =====================================================

    def add_semantic(
        self,
        evidence: dict[str, Any]
    ):

        if not isinstance(evidence, dict):
            return

        self.semantic_evidences.append(
            evidence
        )

    def get_semantic(
        self
    ) -> list[dict[str, Any]]:

        return self.semantic_evidences

    # =====================================================
    # STANDARD EVIDENCE QUERIES
    # =====================================================

    def by_type(
        self,
        evidence_type: EvidenceType
    ) -> list[Evidence]:

        return [

            evidence

            for evidence in self.evidences

            if evidence.type == evidence_type

        ]

    def get_all(self) -> list[Evidence]:

        return self.evidences

    def total(self) -> int:

        return len(self.evidences)