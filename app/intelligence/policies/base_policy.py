"""
=====================================================

TalentAI World

Base Policy

Base class for TALIA intelligence policies.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from abc import ABC
from abc import abstractmethod


class BasePolicy(ABC):

    NAME = "Base Policy"

    DESCRIPTION = ""

    @abstractmethod
    def evaluate(

        self,

        mission,

        evidence_set,

        decision

    ):

        pass