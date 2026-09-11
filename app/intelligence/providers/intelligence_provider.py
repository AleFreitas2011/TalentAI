"""
=====================================================

TalentAI OS

Intelligence Provider

Purpose:
Defines the contract for all Intelligence Providers.

Every AI provider used by TALIA must implement
this interface.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from abc import ABC, abstractmethod


class IntelligenceProvider(ABC):

    @abstractmethod
    def analyze(self, prompt: str) -> str:
        """
        Receives a prompt and returns the AI response.
        """
        pass