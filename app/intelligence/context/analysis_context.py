"""
=====================================================

TalentAI World
Analysis Context

Contains every information required
for a TALIA analysis.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class AnalysisContext:
    """
    Complete context used by TALIA during
    candidate analysis.
    """

    texto_cv: str = ""

    perfil: dict = field(default_factory=dict)

    match: dict = field(default_factory=dict)

    historico_profissional: list = field(default_factory=list)