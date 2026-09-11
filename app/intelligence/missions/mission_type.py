"""
=====================================================

TalentAI World

Mission Type

=====================================================
"""

from enum import Enum


class MissionType(str, Enum):

    CANDIDATE_ANALYSIS = "CANDIDATE_ANALYSIS"

    TALENT_SEARCH = "TALENT_SEARCH"

    JOB_CREATION = "JOB_CREATION"

    CANDIDATE_COMPARISON = "CANDIDATE_COMPARISON"

    CLIENT_PRESENTATION = "CLIENT_PRESENTATION"

    INTERVIEW_PREPARATION = "INTERVIEW_PREPARATION"