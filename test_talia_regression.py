"""
=====================================================

TalentAI World

TALIA Regression Test

Validates the adaptive Overall Match behavior
after Business Intelligence integration.

=====================================================
"""

from app.intelligence.domain.business_fit_status import (
    BusinessFitStatus
)

from app.intelligence.engines.talent_intelligence_analyst import (
    TalentIntelligenceAnalyst
)


analyst = TalentIntelligenceAnalyst()


# =====================================================
# TEST HELPER
# =====================================================

def run_case(
    name,
    technical_fit,
    technical_required,
    experience_fit,
    minimum_years,
    english_fit,
    english_required,
    business_fit,
    business_status,
    expected
):

    result = analyst._calculate_overall_match(
        technical_fit,
        technical_required,
        experience_fit,
        minimum_years,
        english_fit,
        english_required,
        business_fit,
        business_status
    )

    passed = result == expected

    print()
    print(name)
    print("OVERALL MATCH:", result)
    print("EXPECTED:", expected)
    print(
        "RESULT:",
        "PASS" if passed else "FAIL"
    )

    return passed


# =====================================================
# REGRESSION CASES
# =====================================================

results = []


# -----------------------------------------------------
# 1. TECHNICAL ONLY
#
# Only Technical is applicable.
# Expected: 88
# -----------------------------------------------------

results.append(
    run_case(
        name="TECHNICAL ONLY",
        technical_fit=88,
        technical_required=True,
        experience_fit=0,
        minimum_years=None,
        english_fit=0,
        english_required=False,
        business_fit=0,
        business_status=BusinessFitStatus.NOT_APPLICABLE,
        expected=88
    )
)


# -----------------------------------------------------
# 2. TECHNICAL + EXPERIENCE
#
# 88 * 0.60 + 100 * 0.25
# normalized by 0.85
#
# Expected: 92
# -----------------------------------------------------

results.append(
    run_case(
        name="TECHNICAL + EXPERIENCE",
        technical_fit=88,
        technical_required=True,
        experience_fit=100,
        minimum_years=5,
        english_fit=0,
        english_required=False,
        business_fit=0,
        business_status=BusinessFitStatus.NOT_APPLICABLE,
        expected=92
    )
)


# -----------------------------------------------------
# 3. TECHNICAL + EXPERIENCE + ENGLISH
#
# 88 * 0.60
# 100 * 0.25
# 100 * 0.15
#
# Expected: 93
# -----------------------------------------------------

results.append(
    run_case(
        name="TECHNICAL + EXPERIENCE + ENGLISH",
        technical_fit=88,
        technical_required=True,
        experience_fit=100,
        minimum_years=5,
        english_fit=100,
        english_required=True,
        business_fit=0,
        business_status=BusinessFitStatus.NOT_APPLICABLE,
        expected=93
    )
)


# -----------------------------------------------------
# 4. BUSINESS ONLY
#
# No technical, experience or English requirement.
#
# Business is the only applicable dimension.
#
# Expected: 80
# -----------------------------------------------------

results.append(
    run_case(
        name="BUSINESS ONLY",
        technical_fit=0,
        technical_required=False,
        experience_fit=0,
        minimum_years=None,
        english_fit=0,
        english_required=False,
        business_fit=80,
        business_status=BusinessFitStatus.RELATED_STRONG,
        expected=80
    )
)


# -----------------------------------------------------
# 5. BUSINESS NO EVIDENCE
#
# Business exists in the demand, but TALIA has no
# candidate industry evidence.
#
# Business must NOT artificially penalize the candidate.
#
# Technical remains the only applicable dimension.
#
# Expected: 90
# -----------------------------------------------------

results.append(
    run_case(
        name="BUSINESS NO EVIDENCE",
        technical_fit=90,
        technical_required=True,
        experience_fit=0,
        minimum_years=None,
        english_fit=0,
        english_required=False,
        business_fit=0,
        business_status=BusinessFitStatus.NO_EVIDENCE,
        expected=90
    )
)


# -----------------------------------------------------
# 6. BUSINESS UNRELATED
#
# Candidate industry evidence exists and is unrelated.
#
# Business therefore participates with score 0.
#
# Technical:
#     90 * 0.60 = 54
#
# Business:
#     0 * 0.15 = 0
#
# Normalized:
#     54 / 0.75 = 72
#
# Expected: 72
# -----------------------------------------------------

results.append(
    run_case(
        name="BUSINESS UNRELATED",
        technical_fit=90,
        technical_required=True,
        experience_fit=0,
        minimum_years=None,
        english_fit=0,
        english_required=False,
        business_fit=0,
        business_status=BusinessFitStatus.UNRELATED,
        expected=72
    )
)


# =====================================================
# FINAL RESULT
# =====================================================

print()
print("========================================")
print("TALIA OVERALL MATCH REGRESSION")
print("========================================")

if all(results):

    print("FINAL RESULT: ALL TESTS PASSED")

else:

    print("FINAL RESULT: TEST FAILURE")

    raise SystemExit(1)

print("========================================")