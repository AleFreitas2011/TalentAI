from dataclasses import dataclass

from app.intelligence.confidence.confidence_level import (
    ConfidenceLevel
)


@dataclass(frozen=True, slots=True)
class Confidence:

    score: float

    level: ConfidenceLevel

    explanation: str = ""