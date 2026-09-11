"""
=====================================================

TalentAI World

Business Fit Semantic Status Test

Validates all semantic states produced by
TALIA Business Intelligence.

=====================================================
"""

from types import SimpleNamespace

from app.intelligence.engines.talent_intelligence_analyst import (
    TalentIntelligenceAnalyst
)

from app.intelligence.evidence.evidence import (
    Evidence
)

from app.intelligence.evidence.evidence_set import (
    EvidenceSet
)

from app.intelligence.evidence.evidence_type import (
    EvidenceType
)

from app.intelligence.domain.business_fit_status import (
    BusinessFitStatus
)


analyst = TalentIntelligenceAnalyst()


# =====================================================
# HELPERS
# =====================================================

def create_mission(industry=None):

    business_context = SimpleNamespace(
        industry=industry
    )

    demand_profile = SimpleNamespace(
        business_context=business_context
    )

    return SimpleNamespace(
        demand_profile=demand_profile
    )


def create_evidence_set(industries):

    evidences = []

    for industry in industries:

        evidences.append(
            Evidence(
                type=EvidenceType.BUSINESS,
                title="Industry Experience",
                description="",
                confidence=0.95,
                value={
                    "industry": industry
                }
            )
        )

    return EvidenceSet(
        evidences
    )


# =====================================================
# TEST CASES
# =====================================================

cases = [

    (
        "DIRECT",
        "Pharmaceutical",
        ["Pharmaceutical"],
        100.0,
        BusinessFitStatus.DIRECT
    ),

    (
        "RELATED_STRONG",
        "Pharmaceutical",
        ["Healthcare"],
        80.0,
        BusinessFitStatus.RELATED_STRONG
    ),

    (
        "RELATED_MODERATE",
        "Healthcare",
        ["Pharmaceutical"],
        60.0,
        BusinessFitStatus.RELATED_MODERATE
    ),

    (
        "UNRELATED",
        "Pharmaceutical",
        ["Banking"],
        0.0,
        BusinessFitStatus.UNRELATED
    ),

    (
        "NO_EVIDENCE",
        "Pharmaceutical",
        [],
        0.0,
        BusinessFitStatus.NO_EVIDENCE
    ),

    (
        "NOT_APPLICABLE",
        None,
        ["Healthcare"],
        0.0,
        BusinessFitStatus.NOT_APPLICABLE
    ),
]


# =====================================================
# EXECUTION
# =====================================================

print()
print("========================================")
print("TALIA BUSINESS FIT STATUS TEST")
print("========================================")

all_passed = True


for (
    name,
    demand_industry,
    candidate_industries,
    expected_score,
    expected_status
) in cases:

    mission = create_mission(
        demand_industry
    )

    evidence_set = create_evidence_set(
        candidate_industries
    )

    (
        score,
        status,
        normalized_demand,
        normalized_candidates
    ) = analyst._calculate_business_fit(
        mission,
        evidence_set
    )

    passed = (
        score == expected_score
        and status == expected_status
    )

    if not passed:

        all_passed = False

    print()
    print(name)

    print(
        "SCORE:",
        score
    )

    print(
        "STATUS:",
        status.value
    )

    print(
        "DEMAND:",
        normalized_demand
    )

    print(
        "CANDIDATE:",
        normalized_candidates
    )

    print(
        "RESULT:",
        "PASS" if passed else "FAIL"
    )


print()
print("========================================")

print(
    "FINAL RESULT:",
    "ALL TESTS PASSED"
    if all_passed
    else "TEST FAILURE"
)

print("========================================")


if not all_passed:

    raise SystemExit(1)
