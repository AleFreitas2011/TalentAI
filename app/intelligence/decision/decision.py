"""
=====================================================

TalentAI World

Decision

Represents TALIA's official reasoning result.

Author:
TalentAI Team

Version:
2.1

=====================================================
"""

from dataclasses import dataclass, field

from app.intelligence.decision.decision_status import (
    DecisionStatus
)

from app.intelligence.decision.decision_confidence import (
    DecisionConfidence
)

from app.intelligence.match_result import MatchResult


@dataclass(slots=True)
class Decision:
    """
    Represents TALIA's final reasoning outcome.

    The Decision object is progressively enriched
    by the Policy Engine as each policy evaluates
    the candidate against the current mission.

    This is the official output of TALIA's
    reasoning process.
    """

    # =====================================================
    # MATCH RESULT
    # =====================================================

    match_result: MatchResult | None = None

    overall_match: float = 0.0

    technical_fit: float = 0.0

    experience_fit: float = 0.0

    executive_summary: str = ""

    # =====================================================
    # DECISION
    # =====================================================

    status: DecisionStatus = DecisionStatus.REVIEW

    confidence: DecisionConfidence = (
        DecisionConfidence.LOW
    )

    recommendation: str = ""

    explanation: str = ""

    # =====================================================
    # ANALYSIS
    # =====================================================

    strengths: list[str] = field(
        default_factory=list
    )

    gaps: list[str] = field(
        default_factory=list
    )

    risks: list[str] = field(
        default_factory=list
    )

    # =====================================================
    # POLICIES
    # =====================================================

    satisfied_policies: list[str] = field(
        default_factory=list
    )

    failed_policies: list[str] = field(
        default_factory=list
    )