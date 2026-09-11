from dataclasses import dataclass

from app.intelligence.missions.mission_type import MissionType


@dataclass(frozen=True, slots=True)
class MissionContext:

    mission: MissionType

    language: str = "pt-BR"

    explain: bool = True

    confidence: bool = True