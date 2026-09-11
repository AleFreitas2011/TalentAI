"""
=====================================================

TalentAI World

Mission Builder

Creates TALIA missions.

Author:
TalentAI Team

Version:
2.0

=====================================================
"""

from app.intelligence.missions.mission import Mission

from app.intelligence.missions.mission_type import (
    MissionType
)

from app.intelligence.missions.mission_priority import (
    MissionPriority
)


class MissionBuilder:

    NAME = "Mission Builder"

    VERSION = "2.0"

    DESCRIPTION = (
        "Creates TALIA missions."
    )

    def build(
        self,
        candidate=None,
        job=None,
        demand_profile=None,
        context=None,
        mission_type=MissionType.CANDIDATE_ANALYSIS,
        priority=MissionPriority.NORMAL
    ) -> Mission:

   
        """
        Creates a TALIA Mission.

        Every execution inside TALIA starts
        by creating a Mission.
        """

        mission = Mission(

            type=mission_type,

            priority=priority,

            candidate=candidate,

            job=job,

            demand_profile=demand_profile,

            context=context

        )

        return mission