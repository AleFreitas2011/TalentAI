"""
=====================================================

TalentAI OS
Demand Profile

Purpose:
Represents the Demand Intelligence model used
throughout the TalentAI platform.

This is NOT a database model.
It is the central domain object shared by all
TalentAI Intelligence Engines.

Author:
TalentAI Team

Version:
1.1

=====================================================
"""

from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from uuid import uuid4


# =====================================================
# JOB INFORMATION
# =====================================================

@dataclass
class JobInfo:

    job_code: str = ""

    title: str = ""

    client_name: str = ""

    project_name: str = ""

    business_area: str = ""

    seniority: str = ""

    employment_type: str = ""

    work_model: str = ""

    project_duration: str = ""

    country: str = ""

    state: str = ""

    city: str = ""

    timezone: str = ""

    primary_language: str = "English"


# =====================================================
# BUSINESS CONTEXT
# =====================================================

@dataclass
class BusinessContext:

    business_problem: str = ""

    project_type: str = ""

    industry: str = ""

    criticality: str = ""

    priority: str = ""

    goals: List[str] = field(default_factory=list)


# =====================================================
# STRUCTURED REQUIREMENT INTELLIGENCE
# =====================================================

@dataclass
class AtomicRequirement:
    """
    Represents one indivisible requirement.

    Examples:

    Oracle EBS R12
    Accounts Receivable
    Billing
    CLL_F189
    English

    Atomic requirements allow TALIA to reason about
    individual requirements instead of treating a
    compound sentence as one technical skill.
    """

    requirement_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""

    category: str = "technical"

    importance: str = "mandatory"

    source: str = ""

    description: str = ""


@dataclass
class RequirementAlternative:
    """
    Represents one complete alternative or track
    inside a logical requirement group.

    Example:

    OtC Track:
        - AR
        - Billing
        - Latin Tax Engine

    PtP Track:
        - RI
        - CLL_F189
        - Localização Brasil
    """

    alternative_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""

    requirements: List[AtomicRequirement] = field(
        default_factory=list
    )


@dataclass
class RequirementGroup:
    """
    Represents logical relationships between
    alternative requirement tracks.

    Example:

        OtC Track
            OR
        PtP Track

    group_type = "ONE_OF"

    ONE_OF means that satisfying one complete
    alternative is sufficient to satisfy the group.
    """

    group_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""

    group_type: str = "ONE_OF"

    alternatives: List[RequirementAlternative] = field(
        default_factory=list
    )

    mandatory: bool = True


# =====================================================
# TECHNICAL REQUIREMENTS
# =====================================================

@dataclass
class Requirements:

    # -------------------------------------------------
    # EXISTING FIELDS
    #
    # Preserved for backward compatibility with the
    # current TalentAI pipeline.
    # -------------------------------------------------

    mandatory: List[str] = field(default_factory=list)

    nice_to_have: List[str] = field(default_factory=list)

    technologies: List[str] = field(default_factory=list)

    certifications: List[str] = field(default_factory=list)

    languages: List[str] = field(default_factory=list)

    soft_skills: List[str] = field(default_factory=list)

    minimum_years_experience: float | None = None

    # -------------------------------------------------
    # STRUCTURED REQUIREMENT INTELLIGENCE
    #
    # Additive representation used by the new semantic
    # demand/evidence architecture.
    # -------------------------------------------------

    atomic_requirements: List[AtomicRequirement] = field(
        default_factory=list
    )

    requirement_groups: List[RequirementGroup] = field(
        default_factory=list
    )


# =====================================================
# DEMAND AI ANALYSIS
# =====================================================

@dataclass
class DemandAIAnalysis:

    executive_summary: str = ""

    complexity: str = ""

    confidence: float = 0.0

    missing_information: List[str] = field(default_factory=list)

    risks: List[str] = field(default_factory=list)

    reasoning: List[str] = field(default_factory=list)


# =====================================================
# METADATA
# =====================================================

@dataclass
class Metadata:

    created_at: datetime = field(
        default_factory=datetime.now
    )

    updated_at: datetime = field(
        default_factory=datetime.now
    )

    source: str = "manual"

    status: str = "created"


# =====================================================
# MAIN OBJECT
# =====================================================

@dataclass
class DemandProfile:

    demand_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    job_info: JobInfo = field(
        default_factory=JobInfo
    )

    business_context: BusinessContext = field(
        default_factory=BusinessContext
    )

    technical_requirements: Requirements = field(
        default_factory=Requirements
    )

    ai_analysis: DemandAIAnalysis = field(
        default_factory=DemandAIAnalysis
    )

    metadata: Metadata = field(
        default_factory=Metadata
    )