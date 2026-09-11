"""
=====================================================

TalentAI OS

Confidence Levels

Author:
TalentAI Team

=====================================================
"""

from enum import Enum


class ConfidenceLevel(str, Enum):

    VERY_LOW = "very_low"

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    VERY_HIGH = "very_high"