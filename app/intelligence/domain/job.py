"""
=====================================================

TalentAI World

Job Domain Model

Represents a job opportunity inside the TALIA OS domain.

This model contains the intrinsic information required
to represent a Job independently from persistence,
analysis results and execution context.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(slots=True)
class Job:
    """
    Official Job domain entity used by TALIA OS.

    A Job represents an opportunity independently
    from database models, Missions and AI analysis.
    """

    # =================================================
    # IDENTIFICATION
    # =================================================

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    code: str = ""

    # =================================================
    # JOB INFORMATION
    # =================================================

    title: str = ""

    description: str = ""

    seniority: str = ""

    # =================================================
    # BUSINESS CONTEXT
    # =================================================

    client_name: str = ""

    project_name: str = ""

    # =================================================
    # ENGAGEMENT
    # =================================================

    employment_type: str = ""

    work_model: str = ""

    project_duration: str = ""

    # =================================================
    # LOCATION
    # =================================================

    country: str = ""

    state: str = ""

    city: str = ""

    timezone: str = ""

    # =================================================
    # LANGUAGE
    # =================================================

    primary_language: str = "English"