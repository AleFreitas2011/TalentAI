"""
=====================================================

TalentAI World

Technology Vendor Context Regression Test

Purpose:
Protect technology recognition against
cross-vendor false positives.

This test validates that generic business or
localization terminology does not incorrectly
identify technologies from another vendor.

=====================================================
"""

from app.intelligence.knowledge.knowledge_manager import (
    KnowledgeManager
)


knowledge = KnowledgeManager()


# =====================================================
# TEST HELPER
# =====================================================

def run_case(
    name,
    text,
    expected_present=None,
    expected_absent=None
):

    expected_present = expected_present or []
    expected_absent = expected_absent or []

    technologies = knowledge.find_technologies(
        text
    )

    found = [
        technology.name
        for technology in technologies
    ]

    present_ok = all(
        technology in found
        for technology in expected_present
    )

    absent_ok = all(
        technology not in found
        for technology in expected_absent
    )

    passed = present_ok and absent_ok

    print()
    print(name)
    print("TEXT:", text)
    print("FOUND:", found)
    print("EXPECTED PRESENT:", expected_present)
    print("EXPECTED ABSENT:", expected_absent)
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
# 1. EXPLICIT SAP
#
# Explicit SAP terminology must continue to identify
# SAP technologies.
# -----------------------------------------------------

results.append(
    run_case(
        name="EXPLICIT SAP",
        text=(
            "Senior SAP consultant with "
            "SAP Brazil Localization and "
            "SAP Electronic Invoicing."
        ),
        expected_present=[
            "SAP Brazil Localization",
            "SAP Electronic Invoicing"
        ]
    )
)


# -----------------------------------------------------
# 2. ORACLE CONTEXT
#
# Generic localization and invoicing terminology
# inside an explicit Oracle context must not create
# SAP-specific technologies.
# -----------------------------------------------------

results.append(
    run_case(
        name="ORACLE CONTEXT",
        text=(
            "Senior Oracle EBS consultant with "
            "Brazil Localization, electronic invoicing, "
            "Latin Tax Engine and e-Business Tax."
        ),
        expected_absent=[
            "SAP Brazil Localization",
            "SAP Electronic Invoicing"
        ]
    )
)


# -----------------------------------------------------
# 3. CROSS-VENDOR
#
# An explicitly named SAP technology must still be
# recognized even when Oracle also appears.
# -----------------------------------------------------

results.append(
    run_case(
        name="CROSS-VENDOR",
        text=(
            "Integration between "
            "SAP Electronic Invoicing "
            "and Oracle EBS."
        ),
        expected_present=[
            "SAP Electronic Invoicing"
        ]
    )
)


# -----------------------------------------------------
# 4. SAP CONTEXT + GENERIC ALIAS
#
# Generic Brazil Localization terminology may resolve
# to SAP when SAP context is explicitly present.
# -----------------------------------------------------

results.append(
    run_case(
        name="SAP CONTEXT WITH GENERIC ALIAS",
        text=(
            "Senior SAP consultant with "
            "Brazil Localization experience."
        ),
        expected_present=[
            "SAP Brazil Localization"
        ]
    )
)


# -----------------------------------------------------
# 5. NO VENDOR CONTEXT
#
# Generic terminology alone must not create certainty
# about a vendor-specific technology.
# -----------------------------------------------------

results.append(
    run_case(
        name="NO VENDOR CONTEXT",
        text=(
            "Experience with Brazil Localization "
            "and electronic invoicing."
        ),
        expected_absent=[
            "SAP Brazil Localization",
            "SAP Electronic Invoicing"
        ]
    )
)


# =====================================================
# FINAL RESULT
# =====================================================

print()
print("========================================")
print("TECHNOLOGY VENDOR CONTEXT REGRESSION")
print("========================================")

if all(results):

    print("FINAL RESULT: ALL TESTS PASSED")

else:

    print("FINAL RESULT: TEST FAILURE")

    raise SystemExit(1)

print("========================================")