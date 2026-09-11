"""
=====================================================

TalentAI World
Evidence

Represents a single piece of evidence
identified during candidate analysis.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from dataclasses import dataclass
from typing import Any

...

@dataclass(slots=True)
class Evidence:

    type: EvidenceType

    title: str

    description: str

    confidence: float = 1.0

    value: Any = None