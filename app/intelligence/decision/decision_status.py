"""
=====================================================

TalentAI World

Decision Status

Represents TALIA's final reasoning status.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from enum import Enum


class DecisionStatus(Enum):
    """
    Final status produced by TALIA after
    evaluating all intelligence policies.
    """

    APPROVED = "approved"

    REVIEW = "review"

    REJECTED = "rejected"