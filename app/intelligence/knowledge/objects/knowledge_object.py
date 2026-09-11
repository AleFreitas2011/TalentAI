"""
=====================================================

TalentAI
TALIA Knowledge Language (TKL)

Knowledge Object

Represents a canonical concept understood
by TALIA.

Knowledge Objects are immutable domain
entities and form the foundation of the
Knowledge Layer.

Author:
TalentAI Team

=====================================================
"""

from dataclasses import dataclass, field

from app.intelligence.knowledge.types.knowledge_type import KnowledgeType


@dataclass(frozen=True)
class KnowledgeObject:

    id: str

    name: str

    canonical_name: str

    type: KnowledgeType

    description: str = ""

    aliases: list[str] = field(default_factory=list)

    relationships: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)