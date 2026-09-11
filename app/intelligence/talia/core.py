"""
=====================================================

TalentAI World
TALIA Core

The brain of the TalentAI Intelligence Platform.

TALIA is responsible for orchestrating every
intelligence component inside TalentAI.

She does not execute business logic directly.

She coordinates:

- Knowledge
- Reasoning
- Discovery
- Recommendation
- Learning
- Explainability

Author:
TalentAI Team

=====================================================
"""
from datetime import datetime
from app.intelligence.talia.orchestrator import Orchestrator



class Talia:
    """
    TALIA is not an AI model.

    TALIA is the intelligence layer that coordinates
    knowledge, reasoning, learning and recommendations
    inside TalentAI.

    She is the single entry point for every
    intelligence operation.
    """

    NAME = "TALIA"

    VERSION = "1.0"

    DESCRIPTION = (
        "Central Intelligence Layer of TalentAI World"
    )

    def __init__(self):

        self.started_at = datetime.now()
        self.orchestrator = Orchestrator()
        

    def analyze_candidate(
        self,
        candidate,
        job,
        context=None
    ):

        return self.orchestrator.analyze_candidate(
            candidate,
            job,
            context
        )