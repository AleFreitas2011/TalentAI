from app.intelligence.confidence.confidence import (
    Confidence
)

from app.intelligence.confidence.confidence_level import (
    ConfidenceLevel
)


class ConfidenceEngine:

    @staticmethod
    def evaluate(score: float) -> Confidence:

        if score >= 0.90:

            level = ConfidenceLevel.VERY_HIGH

        elif score >= 0.75:

            level = ConfidenceLevel.HIGH

        elif score >= 0.50:

            level = ConfidenceLevel.MEDIUM

        elif score >= 0.25:

            level = ConfidenceLevel.LOW

        else:

            level = ConfidenceLevel.VERY_LOW

        return Confidence(
            score=score,
            level=level
        )