"""
=====================================================

TalentAI World

Mission Priority

=====================================================
"""

from enum import Enum


class MissionPriority(str, Enum):

    LOW = "LOW"

    NORMAL = "NORMAL"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"