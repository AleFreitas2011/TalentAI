"""
=====================================================

TalentAI
TALIA Knowledge Language (TKL)

Knowledge Types

Defines the official types of knowledge
understood by TALIA.

Every Knowledge Object must belong to one
of these categories.

Author:
TalentAI Team

=====================================================
"""

from enum import Enum


class KnowledgeType(str, Enum):

    TECHNOLOGY = "technology"

    PLATFORM = "platform"

    MODULE = "module"

    BUSINESS_PROCESS = "business_process"

    LOCALIZATION = "localization"

    CERTIFICATION = "certification"

    PROGRAMMING_LANGUAGE = "programming_language"

    DATABASE = "database"

    CLOUD = "cloud"

    FRAMEWORK = "framework"

    TOOL = "tool"

    ROLE = "role"

    INDUSTRY = "industry"

    METHODOLOGY = "methodology"

    SOFT_SKILL = "soft_skill"

    LANGUAGE = "language"