from enum import Enum


class EvidenceType(str, Enum):

    TECHNICAL = "technical"

    EXPERIENCE = "experience"

    LANGUAGE = "language"

    CERTIFICATION = "certification"

    EDUCATION = "education"

    SOFT_SKILL = "soft_skill"

    BUSINESS = "business"

    RISK = "risk"

    MATCH = "match"