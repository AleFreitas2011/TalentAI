"""
=====================================================

TalentAI World

Hiring Intelligence

Match Result

Represents TALIA intelligent analysis.

Author:
TalentAI Team

Version:
2.2

=====================================================
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class MatchResult:

    #
    # Overall Analysis
    #

    overall_match: float = 0.0

    confidence: float = 0.0

    #
    # Detailed Scores
    #

    technical_fit: float = 0.0

    business_fit: float = 0.0

    experience_fit: float = 0.0

    seniority_fit: float = 0.0

    communication_fit: float = 0.0

    leadership_fit: float = 0.0

    #
    # Legacy compatibility:
    # TALIA evaluates languages globally, while existing
    # application layers still expose english_fit.
    #

    english_fit: float = 0.0

    certification_fit: float = 0.0

    #
    # Technical Requirement Analysis
    #

    matched_skills: dict[str, list[str]] = field(
        default_factory=dict
    )

    missing_skills: dict[str, list[str]] = field(
        default_factory=dict
    )

    #
    # Explainability
    #

    strengths: list[str] = field(
        default_factory=list
    )

    gaps: list[str] = field(
        default_factory=list
    )

    evidences: list[str] = field(
        default_factory=list
    )

    risks: list[str] = field(
        default_factory=list
    )

    #
    # Executive Output
    #

    recommendation: str = ""

    executive_summary: str = ""