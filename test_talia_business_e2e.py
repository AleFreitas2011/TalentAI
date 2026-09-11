"""
TalentAI World

TALIA Business Intelligence
End-to-End Integration Test

Flow:

Demand
    ↓
Demand Engine
    ↓
Mission
    ↓
TALIA Kernel
    ↓
Evidence Builder
    ↓
Knowledge Layer
    ↓
Business Reasoning
    ↓
Explainability
    ↓
Decision
"""

from app.intelligence.talia.kernel import TaliaKernel

from app.intelligence.missions.mission import Mission

from app.intelligence.domain.candidate import Candidate

from app.intelligence.domain.job import Job

from app.intelligence.context.analysis_context import (
    AnalysisContext
)

from app.intelligence.engines.demand_engine import (
    DemandEngine
)


# =====================================================
# JOB
# =====================================================

job = Job(
    title="Senior SAP Consultant",
    description=(
        "Senior SAP consultant for a global "
        "pharmaceutical company."
    )
)


# =====================================================
# CANDIDATE
# =====================================================

candidate = Candidate(
    full_name="Healthcare Test Candidate"
)


# =====================================================
# ANALYSIS CONTEXT
# =====================================================

context = AnalysisContext(

    texto_cv=(
        "Senior SAP consultant with 10 years of "
        "experience working with healthcare companies."
    ),

    perfil={
        "nome": "Healthcare Test Candidate",
        "titulo_profissional": "Senior SAP Consultant",
        "anos_experiencia": "10",
        "localizacao": "",
        "idiomas": "",
        "setores": "healthcare",
        "resumo": (
            "Senior SAP consultant with extensive "
            "healthcare industry experience."
        ),
    },

    match={},

    historico_profissional=[]
)


# =====================================================
# DEMAND INTELLIGENCE
# =====================================================

demand_profile = DemandEngine().analyze(
    job.description
)


# =====================================================
# TALIA MISSION
# =====================================================

mission = Mission(
    candidate=candidate,
    job=job,
    demand_profile=demand_profile,
    context=context
)


# =====================================================
# TALIA KERNEL
# =====================================================

result = TaliaKernel().execute(
    mission
)


# =====================================================
# RESULT
# =====================================================

decision = result["decision"]

match_result = decision.match_result


print()
print("========================================")
print("TALIA BUSINESS INTELLIGENCE E2E TEST")
print("========================================")

print(
    "MISSION STATUS:",
    result["mission"].status
)

print(
    "DEMAND INDUSTRY:",
    result["mission"]
    .demand_profile
    .business_context
    .industry
)

print(
    "BUSINESS FIT:",
    match_result.business_fit
)

print(
    "OVERALL MATCH:",
    match_result.overall_match
)

print(
    "TECHNICAL FIT:",
    match_result.technical_fit
)

print(
    "EXPERIENCE FIT:",
    match_result.experience_fit
)

print(
    "ENGLISH FIT:",
    match_result.english_fit
)

print(
    "DEMAND TECHNOLOGIES:",
    demand_profile.technical_requirements.technologies
)

print(
    "MANDATORY:",
    demand_profile.technical_requirements.mandatory
)

print(
    "MINIMUM YEARS:",
    demand_profile.technical_requirements.minimum_years_experience
)

print(
    "LANGUAGES:",
    demand_profile.technical_requirements.languages
)

print(
    "STRENGTHS:",
    decision.strengths
)

print(
    "GAPS:",
    decision.gaps
)

print(
    "EVIDENCES:",
    match_result.evidences
)

print(
    "BUSINESS EVIDENCE:",
    [
        (
            evidence.title,
            evidence.value
        )
        for evidence
        in result["evidence_set"].evidences
        if getattr(
            evidence.type,
            "value",
            ""
        ) == "business"
    ]
)

print("========================================")