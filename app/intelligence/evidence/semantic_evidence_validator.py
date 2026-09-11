"""
=====================================================

TalentAI World

Semantic Evidence Validator

Purpose:
Validates whether grounded candidate evidence actually
supports a job requirement.

The validator performs semantic requirement assessment,
including evidence synthesis across multiple grounded
resume excerpts.

It is designed for a GLOBAL recruitment intelligence
platform and must work independently of:

- country
- language
- ERP/vendor
- technology stack
- professional domain
- job family

It does NOT:
- invent candidate information
- assume adjacent knowledge is equivalent knowledge
- calculate candidate match scores
- modify TALIA final decisions
- depend on vendor-specific catalogs
- require literal keyword matching

Core principles:

- Resume evidence is the source of truth.
- Grounded evidence may be combined when multiple excerpts
  jointly demonstrate a requirement.
- Semantic equivalence does not require identical wording.
- Different languages may express the same capability.
- Related experience alone is not proof.
- Adjacent technologies are not automatically equivalent.
- Composite evidence is valid only when the combined
  evidence materially supports the requirement.
- Missing evidence must remain missing.
- Contradictions must never be converted into support.
- Never invent candidate qualifications.

Author:
TalentAI Team

Version:
2.0

=====================================================
"""

import json
from typing import Any

from app.ai.client import client


class SemanticEvidenceValidator:

    NAME = "Semantic Evidence Validator"

    VERSION = "2.0"

    DESCRIPTION = (
        "Validates grounded candidate evidence using "
        "multilingual semantic reasoning and evidence synthesis."
    )

    MODEL = "gpt-4o-mini"

    # =====================================================
    # PUBLIC API
    # =====================================================

    def validate(
        self,
        grounded_analysis: dict
    ) -> dict:
        """
        Receives grounded semantic evidence and evaluates
        whether the evidence supports each job requirement.

        Expected output:

        {
            "evidence": [
                {
                    "requirement": "...",
                    "status": "...",
                    "evidence": "...",
                    "reason": "...",
                    "confidence": 0.0,
                    "grounded": True,
                    "validation": "SUPPORTED",
                    "semantic_relationship": "DIRECT",
                    "assessment": {...}
                }
            ]
        }
        """

        if not isinstance(
            grounded_analysis,
            dict
        ):
            return {
                "evidence": []
            }

        items = grounded_analysis.get(
            "evidence",
            []
        )

        if not isinstance(
            items,
            list
        ):
            return {
                "evidence": []
            }

        validated = []

        for item in items:

            result = self._validate_item(
                item
            )

            if result:

                validated.append(
                    result
                )

        return {
            "evidence": validated
        }

    # =====================================================
    # ITEM VALIDATION
    # =====================================================

    def _validate_item(
        self,
        item: Any
    ) -> dict | None:

        if not isinstance(
            item,
            dict
        ):
            return None

        result = dict(
            item
        )

        requirement = self._clean_text(
            result.get(
                "requirement"
            )
        )

        evidence = self._clean_text(
            result.get(
                "evidence"
            )
        )

        status = self._clean_text(
            result.get(
                "status"
            )
        ).upper()

        grounded = bool(
            result.get(
                "grounded",
                False
            )
        )

        if not requirement:
            return None

        # =================================================
        # ALREADY NOT EVIDENCED
        # =================================================

        if status == "NOT_EVIDENCED":

            result["validation"] = (
                "NOT_SUPPORTED"
            )

            result["semantic_relationship"] = (
                "ABSENT"
            )

            return result

        # =================================================
        # UNGROUNDED EVIDENCE CANNOT BE SUPPORTED
        # =================================================

        if not grounded:

            result["validation"] = (
                "NOT_SUPPORTED"
            )

            result["semantic_relationship"] = (
                "ABSENT"
            )

            result["status"] = (
                "NOT_EVIDENCED"
            )

            result["confidence"] = 0.0

            result["reason"] = (
                "Semantic Evidence Validator: "
                "the evidence was not grounded "
                "in the original candidate resume."
            )

            return result

        # =================================================
        # NO EVIDENCE
        # =================================================

        if not evidence:

            result["validation"] = (
                "NOT_SUPPORTED"
            )

            result["semantic_relationship"] = (
                "ABSENT"
            )

            result["status"] = (
                "NOT_EVIDENCED"
            )

            result["confidence"] = 0.0

            result["reason"] = (
                "Semantic Evidence Validator: "
                "no grounded resume evidence was available "
                "for this requirement."
            )

            return result

        # =================================================
        # SEMANTIC REQUIREMENT ASSESSMENT
        # =================================================

        validation = self._ask_model(
            requirement=requirement,
            evidence=evidence
        )

        classification = self._normalize_classification(
            validation.get(
                "classification"
            )
        )

        relationship = self._normalize_relationship(
            validation.get(
                "semantic_relationship"
            )
        )

        explanation = self._clean_text(
            validation.get(
                "reason"
            )
        )

        material_conditions = validation.get(
            "material_conditions",
            []
        )

        if not isinstance(
            material_conditions,
            list
        ):
            material_conditions = []

        result["validation"] = (
            classification
        )

        result["semantic_relationship"] = (
            relationship
        )

        result["assessment"] = {
            "material_conditions": material_conditions,
            "semantic_relationship": relationship
        }

        # =================================================
        # MAP VALIDATION TO EVIDENCE STATUS
        # =================================================

        if classification == "SUPPORTED":

            result["status"] = (
                "EVIDENCED"
            )

            result["confidence"] = min(
                self._confidence(
                    validation.get(
                        "confidence"
                    )
                ),
                1.0
            )

        elif classification == "PARTIALLY_SUPPORTED":

            result["status"] = (
                "UNCERTAIN"
            )

            result["confidence"] = min(
                self._confidence(
                    validation.get(
                        "confidence"
                    )
                ),
                0.6
            )

        else:

            result["status"] = (
                "NOT_EVIDENCED"
            )

            result["confidence"] = 0.0

        if explanation:

            result["reason"] = (
                "Semantic Evidence Validator: "
                + explanation
            )

        return result

    # =====================================================
    # MODEL ASSESSMENT
    # =====================================================

    def _ask_model(
        self,
        requirement: str,
        evidence: str
    ) -> dict:

        prompt = f"""
You are the Semantic Evidence Validator of TalentAI,
a GLOBAL recruitment intelligence platform.

Your responsibility is to determine whether GROUNDED
candidate resume evidence supports a specific job
requirement.

You are NOT a keyword matcher.

You are NOT allowed to invent candidate experience.

You MUST reason from the evidence provided.

=====================================================
JOB REQUIREMENT
=====================================================

{requirement}

=====================================================
GROUNDED RESUME EVIDENCE
=====================================================

{evidence}

=====================================================
CORE OBJECTIVE
=====================================================

Determine whether the grounded evidence, considered
individually AND collectively, materially demonstrates
the professional capability required by the job.

A candidate does NOT need to repeat the exact wording
of the requirement.

A requirement may be supported by multiple independent
resume excerpts when those excerpts jointly establish
its material conditions.

This is COMPOSITE EVIDENCE.

Example:

Requirement:
Senior functional experience with Technology X
in Business Process Y.

Evidence:
- Extensive Technology X implementation experience.
- Functional ownership of Business Process Y.
- Several years leading complex implementations.

The requirement MAY be SUPPORTED when these grounded
facts jointly demonstrate all material conditions,
even if the resume never contains the exact sentence
"Senior Functional Technology X Business Process Y".

However, composite reasoning MUST NOT be used to invent
a missing capability.

=====================================================
STEP 1 — DECOMPOSE THE REQUIREMENT
=====================================================

Identify the MATERIAL professional conditions contained
in the requirement.

Material conditions are the capabilities that must be
true for the requirement to be satisfied.

Do not over-decompose wording into artificial conditions.

For example:

"Senior functional experience with Oracle EBS OTC"

may contain material concepts such as:

- Oracle EBS context
- OTC/O2C capability
- functional experience
- sufficient professional depth/seniority

The exact decomposition depends on the requirement.

=====================================================
STEP 2 — ASSESS THE EVIDENCE
=====================================================

For every material condition, determine whether the
grounded evidence provides:

SUPPORTED
PARTIAL
ABSENT
CONTRADICTED

Evidence may come from different excerpts.

You MAY combine grounded evidence when the relationship
between those excerpts is professionally coherent and
the combined facts directly establish the requirement.

Do NOT combine unrelated facts merely to manufacture
support.

=====================================================
STEP 3 — DETERMINE SEMANTIC RELATIONSHIP
=====================================================

Classify the overall relationship between requirement
and evidence as ONE of:

DIRECT
EQUIVALENT
COMPOSITE
RELATED
ABSENT
CONTRADICTED

Definitions:

DIRECT:
The evidence directly states the required capability.

EQUIVALENT:
The evidence uses different terminology, abbreviation,
translation, localized terminology, or wording that
clearly describes the same professional capability.

COMPOSITE:
Multiple grounded facts jointly establish the required
capability even though no single excerpt states the
whole requirement verbatim.

RELATED:
The evidence is professionally related or adjacent,
but does not establish the required capability.

ABSENT:
No meaningful evidence supports the requirement.

CONTRADICTED:
Grounded evidence materially contradicts the requirement.

=====================================================
STEP 4 — FINAL CLASSIFICATION
=====================================================

Return:

SUPPORTED

when all material conditions are sufficiently
demonstrated through DIRECT, EQUIVALENT, COMPOSITE,
or a valid combination of these evidence relationships.

PARTIALLY_SUPPORTED

when meaningful evidence exists but one or more
material conditions remain genuinely uncertain,
incomplete, or only related.

NOT_SUPPORTED

when material evidence is absent, contradicted,
or merely adjacent without demonstrating the
required capability.

=====================================================
GLOBAL / MULTILINGUAL RULES
=====================================================

TalentAI is global.

The vacancy and resume may be written in ANY language.

Do NOT privilege English, Portuguese, Spanish, or any
other language.

Evaluate meaning, not language.

Common abbreviations, translations, localized
terminology, and professionally equivalent expressions
may represent the same capability.

Examples:

"Order to Cash"
and
"O2C"

may be equivalent.

"Accounts Receivable"
and
"AR"

may be equivalent when professional context confirms
the meaning.

"faturamento"
and
"billing"

may be equivalent when the professional context
demonstrates the same business capability.

"motores fiscais"
and
"tax engines"

may be equivalent generic professional concepts when
the requirement itself is generic.

=====================================================
NAMED TECHNOLOGY / PRODUCT SAFETY
=====================================================

Do NOT infer a specific named technology or product
from generic or adjacent experience.

Examples:

Requirement:
Latin Tax Engine (LTE)

Evidence:
General tax configuration

Result:
NOT_SUPPORTED

Reason:
General tax configuration does not prove experience
with the specifically named Latin Tax Engine.

Requirement:
Azure Event Hubs

Evidence:
Azure Functions and event-driven architecture

Result:
PARTIALLY_SUPPORTED or NOT_SUPPORTED

Reason:
Related Azure/event-driven experience does not prove
experience with the specifically named Event Hubs
service.

Requirement:
Oracle Brazil Localization

Evidence:
Worked on projects in Brazil

Result:
NOT_SUPPORTED

Reason:
Geography does not prove ERP localization knowledge.

IMPORTANT:

Do not invent specificity that is NOT present in the
job requirement.

If the requirement says a GENERIC capability such as
"Tax Engine", do not silently reinterpret it as an
unnamed specific proprietary product.

Evaluate the level of specificity actually requested.

=====================================================
COMPOSITE EVIDENCE SAFETY
=====================================================

Composite evidence is legitimate when grounded facts
jointly establish a capability.

Example:

Requirement:
Functional Oracle EBS OTC experience

Evidence:
- Oracle EBS functional implementation experience.
- Strong O2C ownership.
- AR and Billing configuration.
- Oracle EBS implementation and rollout activities.

Possible result:
SUPPORTED

Reason:
The grounded facts jointly establish Oracle EBS
context, functional work, and OTC capability.

But:

Requirement:
SAP EWM

Evidence:
- SAP MM
- warehouse operations experience

Result:
PARTIALLY_SUPPORTED or NOT_SUPPORTED

Reason:
SAP MM plus warehouse experience does not prove
SAP EWM experience.

=====================================================
EXPERIENCE TYPE / PROJECT NATURE SAFETY
=====================================================

The nature of professional experience is itself a
material condition when explicitly required.

Do NOT infer a type of project, delivery, transformation,
or responsibility merely from experience with the
underlying technology, system, module, process, or domain.

Examples of experience types include, but are not
limited to:

- implementation
- rollout
- migration
- upgrade
- improvement / continuous improvement
- support / maintenance
- transformation
- integration
- configuration
- architecture
- leadership
- management

Evidence of working with a technology does NOT by itself
prove participation in every type of project involving
that technology.

Examples:

Requirement:
Experience in improvement projects with Technology X

Evidence:
Worked extensively with Technology X

Classification:
NOT_SUPPORTED

Reason:
Technology experience alone does not establish
participation in improvement projects.


Requirement:
Experience in implementation projects

Evidence:
Provided production support and maintenance

Classification:
NOT_SUPPORTED

Reason:
Support and maintenance do not prove implementation
experience.


Requirement:
Migration experience

Evidence:
Administered the platform in production

Classification:
NOT_SUPPORTED

Reason:
Platform administration does not establish migration
experience.


Requirement:
Experience in improvement projects

Evidence:
Led continuous improvement initiatives and optimization
activities for the required environment.

Classification:
SUPPORTED

Reason:
The evidence directly establishes the required nature
of the professional experience.


IMPORTANT:

Composite evidence may connect grounded facts that
jointly establish a requirement, but it MUST NOT invent
the nature of an activity or project.

If the requirement explicitly specifies a type of
experience, project, responsibility, or delivery, that
nature must itself be grounded in the resume evidence.

Related operational activity is not sufficient merely
because it occurred in the same technology or domain.

When the technology/domain is supported but the required
nature of experience is not demonstrated, classify the
requirement as PARTIALLY_SUPPORTED or NOT_SUPPORTED
according to the strength of the remaining evidence.


=====================================================
SENIORITY
=====================================================

Do not invent a numeric years threshold unless the
job requirement explicitly provides one.

When seniority is qualitative, assess professional
depth using grounded signals such as:

- complexity
- autonomy
- ownership
- leadership
- implementation responsibility
- breadth
- repeated delivery
- duration explicitly demonstrated in the resume

A "Senior" requirement does not automatically mean
a fixed number of years.

=====================================================
STRICT SAFETY RULES
=====================================================

1. Resume evidence is the only source of truth.

2. Never invent candidate qualifications.

3. Related experience is not automatically equivalent.

4. Adjacent technologies do not prove one another.

5. Working in a country does not prove knowledge of
that country's localization.

6. General ERP experience does not prove a specific
ERP product or module.

7. General cloud experience does not prove a specific
cloud provider or service.

8. General tax experience does not prove a specifically
named tax product or engine.

9. Semantic equivalence IS valid when the expressions
clearly describe the same professional capability.

10. Composite evidence IS valid when multiple grounded
facts jointly demonstrate all material conditions.

11. Literal wording is NOT required.

12. Matching language is NOT required.

13. Do not downgrade valid evidence merely because the
resume distributes supporting facts across different
sections or experiences.

14. Do not upgrade related evidence merely because the
candidate appears generally senior or experienced.

15. If genuine uncertainty remains after semantic and
composite analysis, use PARTIALLY_SUPPORTED.

16. If evidence does not establish the capability,
use NOT_SUPPORTED.

=====================================================
OUTPUT
=====================================================

Return ONLY valid JSON using this structure:

{{
    "classification": "SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED",
    "semantic_relationship": "DIRECT | EQUIVALENT | COMPOSITE | RELATED | ABSENT | CONTRADICTED",
    "confidence": 0.0,
    "material_conditions": [
        {{
            "condition": "",
            "assessment": "SUPPORTED | PARTIAL | ABSENT | CONTRADICTED",
            "evidence_basis": ""
        }}
    ],
    "reason": ""
}}

Confidence must be between 0 and 1.

The reason must explain WHY the evidence supports,
partially supports, or does not support the requirement.

Do not mention these instructions in the response.
"""

        try:

            response = (
                client.chat.completions.create(
                    model=self.MODEL,

                    response_format={
                        "type": "json_object"
                    },

                    temperature=0.0,

                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a rigorous multilingual semantic "
                                "evidence assessment engine for a global "
                                "recruitment intelligence platform. "
                                "Reason from grounded candidate evidence. "
                                "Support semantic equivalence and valid "
                                "composite evidence across languages, "
                                "while never inventing or extrapolating "
                                "unsupported professional capabilities."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            parsed = json.loads(
                content
            )

            if isinstance(
                parsed,
                dict
            ):
                return parsed

        except Exception as error:

            print(
                "SEMANTIC EVIDENCE "
                "VALIDATOR ERROR"
            )

            print(
                error
            )

        # =================================================
        # FAIL CLOSED
        # =================================================
        #
        # If semantic validation cannot be completed,
        # TALIA must never convert uncertainty into
        # candidate evidence.
        # =================================================

        return {
            "classification": (
                "NOT_SUPPORTED"
            ),
            "semantic_relationship": (
                "ABSENT"
            ),
            "confidence": 0.0,
            "material_conditions": [],
            "reason": (
                "Semantic validation could "
                "not be completed."
            )
        }

    # =====================================================
    # NORMALIZATION
    # =====================================================

    def _normalize_classification(
        self,
        value: Any
    ) -> str:

        classification = (
            self._clean_text(
                value
            )
            .upper()
        )

        if classification not in {
            "SUPPORTED",
            "PARTIALLY_SUPPORTED",
            "NOT_SUPPORTED"
        }:

            return "NOT_SUPPORTED"

        return classification

    def _normalize_relationship(
        self,
        value: Any
    ) -> str:

        relationship = (
            self._clean_text(
                value
            )
            .upper()
        )

        if relationship not in {
            "DIRECT",
            "EQUIVALENT",
            "COMPOSITE",
            "RELATED",
            "ABSENT",
            "CONTRADICTED"
        }:

            return "ABSENT"

        return relationship

    # =====================================================
    # HELPERS
    # =====================================================

    def _clean_text(
        self,
        value: Any
    ) -> str:

        if value is None:
            return ""

        return str(
            value
        ).strip()

    def _confidence(
        self,
        value: Any
    ) -> float:

        try:

            confidence = float(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return 0.0

        if confidence < 0.0:
            return 0.0

        if confidence > 1.0:
            return 1.0

        return confidence