"""
=====================================================

TalentAI World

Mission

Represents a TALIA mission.

A Mission is the central object that flows
through the entire TALIA OS pipeline.

Author:
TalentAI Team

Version:
2.0

=====================================================
"""

from dataclasses import dataclass, field

from datetime import datetime

from uuid import uuid4

from app.intelligence.missions.mission_type import MissionType

from app.intelligence.missions.mission_priority import (
    MissionPriority
)

from app.intelligence.domain.job import (
    Job
)

from app.intelligence.domain.candidate import (
    Candidate
)

from app.intelligence.demand_profile import (
    DemandProfile
)

from app.intelligence.context.analysis_context import (
    AnalysisContext
)


@dataclass(slots=True)
class Mission:
    """
    Represents a TALIA mission.

    Every TALIA execution starts with a Mission.

    Mission
        ↓
    Evidence
        ↓
    Reasoning
        ↓
    Decision
    """

    # =====================================================
    # IDENTIFICATION
    # =====================================================

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    # =====================================================
    # METADATA
    # =====================================================

    type: MissionType = (
        MissionType.CANDIDATE_ANALYSIS
    )

    priority: MissionPriority = (
        MissionPriority.NORMAL
    )

    status: str = "CREATED"

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # =====================================================
    # DOMAIN OBJECTS
    # =====================================================

    candidate: Candidate | None = None

    job: Job | None = None

    demand_profile: DemandProfile | None = None

    context: AnalysisContext | None = None

    # =====================================================
    # OPTIONAL INFORMATION
    # =====================================================
    
    language: str = "English"

    notes: str = ""

    # =====================================================
    # HELPERS
    # =====================================================

    def start(self):

        self.status = "RUNNING"

    def finish(self):

        self.status = "FINISHED"

    def fail(self):

        self.status = "FAILED"