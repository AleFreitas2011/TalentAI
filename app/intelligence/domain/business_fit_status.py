"""
=====================================================

TalentAI World

Business Fit Status

Represents the semantic result of TALIA
business-context reasoning.

A Business Fit score alone is not sufficient
to explain the meaning of the analysis.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from enum import Enum


class BusinessFitStatus(str, Enum):
    """
    Semantic classification of Business Fit.

    DIRECT
        Candidate has direct experience in the
        demand industry.

    RELATED_STRONG
        Candidate has experience in an industry
        strongly related to the demand industry.

    RELATED_MODERATE
        Candidate has experience in an industry
        moderately related to the demand industry.

    UNRELATED
        Candidate industry evidence exists, but
        no relevant relationship with the demand
        industry was identified.

    NO_EVIDENCE
        The demand has an industry, but TALIA
        found no candidate industry evidence.

    NOT_APPLICABLE
        The demand does not define an industry,
        so Business Fit is not applicable.
    """

    DIRECT = "DIRECT"

    RELATED_STRONG = "RELATED_STRONG"

    RELATED_MODERATE = "RELATED_MODERATE"

    UNRELATED = "UNRELATED"

    NO_EVIDENCE = "NO_EVIDENCE"

    NOT_APPLICABLE = "NOT_APPLICABLE"