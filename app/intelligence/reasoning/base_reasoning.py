"""
=====================================================

TalentAI OS

Base Reasoning

Defines the contract for all TALIA reasoning
engines.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from abc import ABC, abstractmethod

from app.intelligence.missions.mission_context import MissionContext


class BaseReasoning(ABC):
    """
    Base class for every TALIA reasoning engine.
    """

    @abstractmethod
    def execute(
        self,
        context: MissionContext,
        facts: dict
    ):
        """
        Execute the reasoning process.
        """
        raise NotImplementedError