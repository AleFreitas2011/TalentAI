"""
=====================================================

TalentAI World

Decision Confidence

Represents TALIA's confidence level.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from enum import Enum


class DecisionConfidence(Enum):
    """
    Confidence level associated with
    TALIA's final decision.
    """

    HIGH = "high"

    MEDIUM = "medium"

    LOW = "low"