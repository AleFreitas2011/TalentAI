"""
=====================================================

TalentAI OS
Candidate Profile

Purpose:
Represents the Candidate Intelligence model used
throughout the TalentAI platform.

This is NOT a database model.
It is the central domain object shared by all AI engines.

Author:
TalentAI Team

=====================================================
"""

from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from uuid import uuid4


# =====================================================
# PERSONAL INFORMATION
# =====================================================

@dataclass
class PersonalInfo:

    full_name: str = ""
    email: str = ""
    phone: str = ""

    city: str = ""
    state: str = ""
    country: str = ""

    linkedin: str = ""

    nationality: str = ""


# =====================================================
# AI ANALYSIS
# =====================================================

@dataclass
class AIAnalysis:

    executive_summary: str = ""

    match_score: float = 0.0

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)

    observations: List[str] = field(default_factory=list)


# =====================================================
# DOCUMENT INFORMATION
# =====================================================

@dataclass
class DocumentInfo:

    original_filename: str = ""

    original_cv: str = ""

    extracted_text: str = ""

    language: str = "pt-BR"

# =====================================================
# METADATA
# =====================================================

@dataclass
class Metadata:

    created_at: datetime = field(default_factory=datetime.now)

    updated_at: datetime = field(default_factory=datetime.now)

    source: str = "pdf"

    status: str = "imported"    


# =====================================================
# MAIN OBJECT
# =====================================================

@dataclass
class CandidateProfile:

    candidate_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    personal_info: PersonalInfo = field(
        default_factory=PersonalInfo
    )

    ai_analysis: AIAnalysis = field(
        default_factory=AIAnalysis
    )

    document: DocumentInfo = field(
        default_factory=DocumentInfo
    )

    metadata: Metadata = field(
        default_factory=Metadata
    )