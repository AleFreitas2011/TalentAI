"""
=====================================================

TalentAI World

OpenAI Intelligence Provider

Provides semantic intelligence capabilities
for TALIA using OpenAI.

Principles:

- AI interprets information
- AI never fabricates evidence
- Related evidence is not confirmed evidence
- AI does not calculate TalentAI scores
- Structured output whenever required
- Provider remains independent from TALIA reasoning

Author:
TalentAI Team

Version:
1.3

=====================================================
"""

import json

from app.ai.client import client

from app.intelligence.providers.intelligence_provider import (
    IntelligenceProvider
)


class OpenAIIntelligenceProvider(IntelligenceProvider):

    NAME = "OpenAI Intelligence Provider"

    VERSION = "1.3"

    DESCRIPTION = (
        "Provides structured semantic intelligence "
        "for TalentAI."
    )

    MODEL = "gpt-4o-mini"

    # =====================================================
    # PROVIDER CONTRACT
    # =====================================================

    def analyze(
        self,
        prompt: str
    ) -> str:
        """
        Implements the official IntelligenceProvider
        contract.

        Receives a prompt and returns the raw AI response.
        """

        if not prompt:
            return ""

        try:

            response = client.chat.completions.create(

                model=self.MODEL,

                temperature=0.1,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are TALIA, the Talent "
                            "Intelligence layer of TalentAI. "
                            "Analyze information accurately "
                            "and never fabricate evidence."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            return content or ""

        except Exception as error:

            print("=" * 60)
            print("OPENAI INTELLIGENCE PROVIDER ERROR")
            print(error)
            print("=" * 60)

            return ""

    # =====================================================
    # INTERNAL JSON REQUEST
    # =====================================================

    def _request_json(
        self,
        system_prompt: str,
        user_prompt: str
    ) -> dict:

        try:

            response = client.chat.completions.create(

                model=self.MODEL,

                response_format={
                    "type": "json_object"
                },

                temperature=0.1,

                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            if not content:
                return {}

            data = json.loads(content)

            if not isinstance(data, dict):
                return {}

            return data

        except Exception as error:

            print("=" * 60)
            print("OPENAI INTELLIGENCE PROVIDER JSON ERROR")
            print(error)
            print("=" * 60)

            return {}

    # =====================================================
    # DEMAND ANALYSIS
    # =====================================================

    def analyze_demand(
        self,
        text: str
    ) -> dict:
        """
        Interprets a job description and extracts
        structured recruiting requirements.

        Requirements are represented atomically whenever
        they can be evaluated independently.

        Alternative requirement tracks are preserved in
        requirement_groups.

        Does not calculate candidate match scores.

        The analysis is domain-independent and does not
        require the technology to exist in TalentAI's
        official Knowledge Catalog.
        """

        if not text:
            return {}

        system_prompt = """
You are TALIA, the Talent Intelligence layer of TalentAI.

Your task is to interpret job requirements accurately.

You may analyze jobs from ANY professional domain,
industry, technology or country.

Do not depend on a predefined technology catalog.

STRICT RULES:

1. Use only information explicitly present in the job description.

2. Never invent requirements.

3. Never convert a nice-to-have requirement into mandatory.

4. Never convert a mandatory requirement into nice-to-have.

5. Preserve OR / AND requirement logic.

5A. Interpret requirement connectors according to their
semantic meaning in context, not merely as punctuation.

The following expressions commonly indicate alternative
ways of satisfying ONE requirement:

- A or B
- A ou B
- A and/or B
- A e/ou B
- A / B

When the job description uses these expressions to mean
that either option can satisfy the same requirement,
represent them as ONE_OF in "requirement_groups".

Do NOT create two independent mandatory requirements in
that case.

Example:

"Experience with Latin Tax Engine (LTE) / Tax Engine"

means that evidence of Latin Tax Engine OR Tax Engine can
satisfy the requirement.

It must therefore be represented as one ONE_OF group,
not as two independent mandatory requirements.

Example:

"Experience in implementation, rollout and/or
improvements of Oracle EBS"

means that experience in implementation OR rollout OR
improvements may satisfy that requirement when the wording
explicitly presents those project types as alternatives.

5B. A slash "/" is NOT automatically an atomic-requirement
separator.

Determine its meaning from the professional context.

Use "/" as a separator only when the description clearly
requires every listed capability independently.

Use ONE_OF when "/" expresses alternative names,
technologies, modules, approaches or acceptable ways of
satisfying the same requirement.

5C. Requirements belonging to a ONE_OF group must not also
appear as independent items in "mandatory" or
"nice_to_have".

5D. Each independent alternative clause must create its
OWN requirement group.

Never merge separate job requirements into the same
ONE_OF group merely because both contain alternative
logic.

Example:

"Experience with A / B"
"Experience in implementation, rollout and/or improvements"

represents TWO independent requirements.

Correct:

Group 1:
A OR B

Group 2:
implementation OR rollout OR improvements

Incorrect:

Group:
(A + B) OR (implementation + rollout + improvements)

A ONE_OF group represents alternative ways of satisfying
ONE semantic requirement only.

5E. Inside a ONE_OF group, each alternative must represent
one acceptable way of satisfying the requirement.

Example:

"A / B"

must become:

ONE_OF:
- Alternative A:
    requirement A
- Alternative B:
    requirement B

It must NOT become one alternative containing both A and B.

Example:

"implementation, rollout and/or improvements"

must become:

ONE_OF:
- implementation
- rollout
- improvements

when the wording means any one of these project types is
acceptable.

5F. Section headings define requirement importance.

Requirements under headings equivalent to:

- Diferenciais
- Desejáveis
- Nice to have
- Preferred
- Desirable
- Plus
- Optional

must be classified as nice_to_have unless the job
description explicitly says otherwise.

This classification applies to normal requirements,
languages and alternative requirement groups.

Do not discard a nice-to-have requirement merely because
it is also represented in another specialized field such
as "languages", "technologies", "certifications" or
"soft_skills".

Example:

"Diferenciais:
- Brazilian Tax Reform
- Order Management
- English"

must preserve those items as optional requirements.

Technical items belong in "nice_to_have".

English belongs in "nice_to_have" when it is optional.

Optional or nice-to-have languages MUST NOT be returned
in "languages".

The "languages" field is reserved only for explicitly
mandatory language requirements.

6. Preserve technologies and professional terminology.

7. Do not calculate candidate match scores.

8. Do not evaluate any candidate.

9. If information is missing, keep the corresponding field empty.

10. The "technologies" field must contain every explicitly
mentioned technology, platform, product, module,
programming language, framework, technical tool or
technical system found in the job description.

11. A technology may appear both in "mandatory" or
"nice_to_have" AND in "technologies". These fields have
different purposes.

12. Do not omit a technology from "technologies" merely
because it already appears inside a requirement.

13. Preserve technology names as written whenever possible.

14. "mandatory" and "nice_to_have" must contain STRINGS ONLY.

15. Never place dictionaries, objects, lists or structured
requirement groups inside "mandatory" or "nice_to_have".

16. Requirements must be ATOMIC whenever multiple
independently evaluable requirements are combined in one
sentence.

Example:

"Experience with Setup Fiscal / Latin Tax /
e-Business Tax"

must be represented as separate requirements such as:

"Experience with Setup Fiscal"
"Experience with Latin Tax"
"Experience with e-Business Tax"

Do not keep several independently required technologies,
modules, products or capabilities joined inside one
requirement when the job description clearly requires
each one separately.

Before atomicizing punctuation such as slash, comma,
semicolon or conjunction, first determine whether it
expresses independent requirements or alternative ways
of satisfying the same requirement.

If it expresses alternatives, preserve the logic in
"requirement_groups" instead of creating independent
atomic requirements.

17. Do NOT incorrectly split a single professional concept.

For example:

"Oracle EBS R12"
is one requirement.

"5 years of Oracle EBS experience"
is one experience requirement.

Atomicization means separating independently evaluable
requirements, not breaking meaningful concepts into words.

18. Alternative requirement logic MUST be represented
inside "requirement_groups".

Examples include:

- A OR B
- either A or B
- one of the following
- at least one of these tracks
- experience in one of these areas
- Track A OR Track B

19. An alternative requirement MUST NOT also remain as a
combined sentence inside "mandatory" or "nice_to_have".

20. When an alternative contains multiple requirements,
preserve the alternative as a COMPLETE TRACK.

Example:

(A + B + C) OR (D + E + F)

must NOT become:

A OR B OR C OR D OR E OR F.

It must become one ONE_OF group containing two complete
alternatives:

Alternative 1:
A, B, C

Alternative 2:
D, E, F

21. Every requirement inside an alternative must also be
atomic whenever it can be evaluated independently.

22. Do not create alternative logic unless the job
description explicitly expresses that logic.

23. Return valid JSON only.
"""

        user_prompt = f"""
Analyze the following job description.

Return exactly one JSON object using this structure:

{{
    "job_title": "",
    "seniority": "",
    "mandatory": [],
    "nice_to_have": [],
    "technologies": [],
    "certifications": [],
    "languages": [],
    "soft_skills": [],
    "minimum_years_experience": null,
    "requirement_groups": [],
    "business_context": {{
        "industry": "",
        "project_type": "",
        "business_problem": ""
    }},
    "missing_information": []
}}

FIELD DEFINITIONS:

"mandatory":

All explicitly mandatory professional requirements that
are NOT part of an alternative requirement group.

This field must contain strings only.

Requirements must be atomic whenever each component can
be evaluated independently.

Example:

Instead of:

[
    "Experience with Setup Fiscal / Latin Tax /
    e-Business Tax"
]

prefer:

[
    "Experience with Setup Fiscal",
    "Experience with Latin Tax",
    "Experience with e-Business Tax"
]

when the job description requires those capabilities
independently.

--------------------------------------------------

"nice_to_have":

All explicitly optional, desirable or preferred
requirements that are NOT part of an alternative
requirement group.

This field must contain strings only.

Apply the same atomic requirement rules used for
"mandatory".

--------------------------------------------------

"technologies":

All explicitly mentioned technologies, platforms,
products, modules, programming languages, frameworks,
technical tools and technical systems.

A technology can appear in both a normal requirement and
"technologies".

Do not omit technologies simply because they also appear
inside a requirement group.

--------------------------------------------------

""languages":

Human languages explicitly REQUIRED for the role.

This field contains mandatory language requirements only.

A language mentioned under "Diferenciais",
"Nice to have", "Preferred", "Desirable",
"Optional", "Plus" or equivalent sections must NOT
appear in "languages".

Instead, preserve that optional language requirement
inside "nice_to_have".

A language under "Requisitos", "Requirements",
"Mandatory", "Required", "Must have" or equivalent
sections must be returned in "languages".

Preserve an explicitly required proficiency level
whenever provided.

Examples:

"Diferenciais:
- Inglês para atuação em ambiente internacional"

must produce:

"nice_to_have": [
    "Inglês para atuação em ambiente internacional"
]

"languages": []

But:

"Requisitos:
- Inglês avançado para atuação em ambiente internacional"

must produce a mandatory language requirement in
"languages", preserving the advanced proficiency level.
--------------------------------------------------

"minimum_years_experience":

Minimum number of years explicitly required.

Return null if no minimum number is provided.

--------------------------------------------------

"requirement_groups":

Use this field ONLY for explicit alternative requirement
logic.

A requirement group represents ONE semantic job
requirement that can be satisfied through alternative
options.

Each independent job requirement with alternative logic
must create its OWN group.

Return requirement_groups as a LIST of group objects.

Each group must use this structure:

{{
    "type": "ONE_OF",
    "importance": "mandatory | nice_to_have",
    "alternatives": [
        {{
            "name": "",
            "requirements": []
        }}
    ]
}}

The "importance" field is REQUIRED for every group.

Use "mandatory" when the requirement belongs to a
mandatory or required section.

Use "nice_to_have" when the requirement belongs to a
desirable, preferred, optional, differential, plus or
nice-to-have section.

Never promote a nice-to-have requirement to mandatory.

Never downgrade a mandatory requirement to nice-to-have.

--------------------------------------------------

SIMPLE ALTERNATIVES:

When ONE requirement can be satisfied by A OR B, create
ONE group with TWO alternatives.

Example:

"Experience with Latin Tax Engine (LTE) / Tax Engine"

must become:

[
    {{
        "type": "ONE_OF",
        "importance": "mandatory",
        "alternatives": [
            {{
                "name": "Latin Tax Engine (LTE)",
                "requirements": [
                    "Experience with Latin Tax Engine (LTE)"
                ]
            }},
            {{
                "name": "Tax Engine",
                "requirements": [
                    "Experience with Tax Engine"
                ]
            }}
        ]
    }}
]

Each option is a separate alternative.

Do NOT return:

[
    {{
        "type": "ONE_OF",
        "importance": "mandatory",
        "alternatives": [
            {{
                "name": "Tax Engine",
                "requirements": [
                    "Experience with Latin Tax Engine (LTE)",
                    "Experience with Tax Engine"
                ]
            }}
        ]
    }}
]

because that would incorrectly require both technologies
inside the same alternative.

--------------------------------------------------

MULTIPLE OPTIONS:

When ONE requirement can be satisfied by A OR B OR C,
create ONE group with THREE alternatives.

Example:

"Experience in Oracle EBS implementation, rollout and/or
improvements"

must become:

[
    {{
        "type": "ONE_OF",
        "importance": "mandatory",
        "alternatives": [
            {{
                "name": "Implementation",
                "requirements": [
                    "Experience in Oracle EBS implementation"
                ]
            }},
            {{
                "name": "Rollout",
                "requirements": [
                    "Experience in Oracle EBS rollout"
                ]
            }},
            {{
                "name": "Improvements",
                "requirements": [
                    "Experience in Oracle EBS improvements"
                ]
            }}
        ]
    }}
]

--------------------------------------------------

SEPARATE REQUIREMENTS:

Never merge independent job requirements into the same
ONE_OF group.

Example:

Requirement 1:
"Experience with Latin Tax Engine (LTE) / Tax Engine"

Requirement 2:
"Experience in Oracle EBS implementation, rollout and/or
improvements"

must produce TWO separate group objects:

[
    {{
        "type": "ONE_OF",
        "importance": "mandatory",
        "alternatives": [
            {{
                "name": "Latin Tax Engine (LTE)",
                "requirements": [
                    "Experience with Latin Tax Engine (LTE)"
                ]
            }},
            {{
                "name": "Tax Engine",
                "requirements": [
                    "Experience with Tax Engine"
                ]
            }}
        ]
    }},
    {{
        "type": "ONE_OF",
        "importance": "mandatory",
        "alternatives": [
            {{
                "name": "Implementation",
                "requirements": [
                    "Experience in Oracle EBS implementation"
                ]
            }},
            {{
                "name": "Rollout",
                "requirements": [
                    "Experience in Oracle EBS rollout"
                ]
            }},
            {{
                "name": "Improvements",
                "requirements": [
                    "Experience in Oracle EBS improvements"
                ]
            }}
        ]
    }}
]

Do NOT merge these two groups.

--------------------------------------------------

COMPLETE ALTERNATIVE TRACKS:

An alternative may contain multiple requirements ONLY
when the job description explicitly defines complete
alternative tracks.

Example:

Track A requires:
A + B + C

OR

Track B requires:
D + E + F

In this specific case, preserve the complete tracks:

[
    {{
        "type": "ONE_OF",
        "importance": "mandatory",
        "alternatives": [
            {{
                "name": "Track A",
                "requirements": [
                    "A",
                    "B",
                    "C"
                ]
            }},
            {{
                "name": "Track B",
                "requirements": [
                    "D",
                    "E",
                    "F"
                ]
            }}
        ]
    }}
]

Do not confuse a simple A OR B requirement with complete
alternative tracks.

--------------------------------------------------

IMPORTANT:

Requirements represented inside a requirement_group must
NOT also appear independently inside "mandatory" or
"nice_to_have".

Do not flatten complete alternative tracks.

Do not merge separate alternative requirements.

Do not create alternative logic unless the job
description explicitly expresses alternative logic.
--------------------------------------------------

FINAL VALIDATION BEFORE RETURNING JSON:

Before returning the result, verify:

1. "mandatory" contains strings only.

2. "nice_to_have" contains strings only.

3. No alternative-track sentence remains in "mandatory"
or "nice_to_have".

4. Explicit OR / either / one-of / at-least-one-track
logic is represented in "requirement_groups".

5. Compound independently evaluable requirements have
been atomicized.

6. Alternative tracks remain grouped and have not been
flattened.

7. No requirement was invented.

8. Every requirement_group contains an "importance"
field with exactly "mandatory" or "nice_to_have".

9. Requirements from sections such as "Diferenciais",
"Preferred", "Desirable", "Nice to have", "Plus" or
equivalent remain nice_to_have, including when they are
represented as alternative groups.

10. No requirement represented inside a requirement_group
is duplicated as an independent item in "mandatory" or
"nice_to_have".

JOB DESCRIPTION:

{text}
"""

        return self._request_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

    # =====================================================
    # CANDIDATE EVIDENCE ANALYSIS
    # =====================================================

    def analyze_candidate_evidence(
        self,
        resume_text: str,
        requirements: list[str]
    ) -> dict:
        """
        Finds evidence for supplied requirements
        inside a candidate resume.

        Does not calculate match scores.

        Every conclusion must be grounded in explicit
        candidate resume evidence.
        """

        if not resume_text:
            return {}

        if not requirements:
            return {
                "evidence": []
            }

        requirements_json = json.dumps(
            requirements,
            ensure_ascii=False
        )

        system_prompt = """
You are TALIA, the Talent Intelligence layer of TalentAI.

Your task is strict candidate evidence analysis.

You may analyze candidates from ANY professional domain,
industry, technology or country.

You do not depend on a predefined technology catalog.

Your role is similar to an evidence auditor.

A related skill, product, technology, country, vendor,
module or professional context is NOT automatically proof
of the exact requirement.

STRICT RULES:

1. Use only evidence explicitly contained in the candidate
resume.

2. Never invent candidate experience.

3. Never infer an exact technology because another related
technology appears in the resume.

4. Never infer an exact product or module because the
candidate has experience with the same vendor.

5. Never infer an exact product version because another
version or product family appears in the resume.

6. Never infer localization knowledge merely because the
candidate worked in that country.

7. Never infer tax localization knowledge merely because
the candidate has general tax experience.

8. Never infer a specialized tax engine merely because the
candidate configured taxes or tax rules.

9. Oracle Cloud evidence does NOT prove an Oracle
E-Business Suite-specific requirement unless the resume
explicitly connects the experience to Oracle EBS.

10. Oracle EBS evidence does NOT automatically prove Oracle
Cloud experience.

11. Experience with tax configuration does NOT
automatically prove experience with Latin Tax Engine,
e-Business Tax, Brazilian Localization or another named
tax engine.

12. Experience working for a Brazilian client or in Brazil
does NOT automatically prove Oracle Brazil Localization.

13. Experience with Accounts Receivable does NOT
automatically prove Billing, Latin Tax Engine or another
adjacent module.

14. Experience with one module does NOT prove experience
with another module from the same ERP.

15. Do not mark EVIDENCED when the reasoning would require
words or ideas such as:

- suggests
- indicates
- likely
- probably
- presumably
- related to
- similar to
- may imply
- could imply

If such reasoning is necessary, the requirement is not
explicitly evidenced.

16. Semantic equivalence may be accepted only when two
terms clearly describe the same technology, skill,
capability or professional concept.

17. Semantic equivalence must not be used to transform a
general capability into a specific named product or module.

18. If the resume contains NO explicit evidence or mention
of the requirement, mark NOT_EVIDENCED.

19. Mark UNCERTAIN only when the resume contains explicit
related evidence, but that evidence is ambiguous,
incomplete, or insufficient to confirm the exact
requirement.

20. EVIDENCED requires clear resume evidence that directly
supports the requirement.

21. The language used to write the resume is NOT evidence
of candidate proficiency in that language.

22. For language requirements:

- no explicit language mention = NOT_EVIDENCED
- explicit language mention with insufficient proficiency
  information = UNCERTAIN
- explicit evidence satisfying the required proficiency
  level = EVIDENCED

23. Preserve the original resume evidence whenever
available.

24. Do not calculate match percentages.

25. Do not decide whether the candidate should be hired.

26. Evaluate every supplied requirement.

27. Return valid JSON only.
"""

        user_prompt = f"""
Analyze the candidate resume against every requirement below.

REQUIREMENTS:

{requirements_json}

For every requirement return one evidence object using
this structure:

{{
    "requirement": "",
    "status": "EVIDENCED | NOT_EVIDENCED | UNCERTAIN",
    "evidence": "",
    "reason": "",
    "confidence": 0.0
}}

STATUS DEFINITIONS:

EVIDENCED:

Use only when the resume contains clear and direct evidence
supporting the exact requirement or a genuine semantic
equivalent.

NOT_EVIDENCED:

Use when the resume contains no evidence supporting the
requirement.

Also use NOT_EVIDENCED when only a different technology,
module, product or unrelated capability is present.

UNCERTAIN:

Use only when explicit related evidence exists in the
resume, but the evidence is insufficiently specific to
confirm the exact requirement.

IMPORTANT EXAMPLES:

Candidate worked in Brazil
!=
Brazil Localization experience.

General tax configuration
!=
Latin Tax Engine.

General tax configuration
!=
e-Business Tax.

Oracle AR Cloud
!=
Oracle EBS AR unless EBS experience is separately
demonstrated.

Accounts Receivable
!=
Billing.

Oracle EBS
!=
every Oracle EBS module.

Resume written in English
!=
English proficiency.

The "evidence" field must contain the relevant original
resume evidence when available.

If no supporting evidence exists, return an empty string.

The "reason" field must explain the classification without
inventing connections between technologies.

The "confidence" field must be a number between 0.0 and 1.0
representing confidence in the classification.

Return exactly:

{{
    "evidence": []
}}

CANDIDATE RESUME:

{resume_text}
"""

        return self._request_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )


    # =====================================================
    # CANDIDATE EVIDENCE RETRIEVAL
    # =====================================================

    def retrieve_candidate_evidence(
        self,
        resume_text: str,
        requirements: list[str],
        max_candidates: int = 3
    ) -> dict:
        """
        Retrieves the strongest candidate resume excerpts
        potentially related to each supplied requirement.

        This method performs retrieval only.

        It does NOT:
        - decide whether a requirement is satisfied
        - classify evidence
        - calculate match scores
        - infer candidate qualifications
        - replace semantic validation

        The returned excerpts are candidates for later
        grounding and semantic validation.
        """

        if not resume_text:
            return {
                "requirements": []
            }

        if not requirements:
            return {
                "requirements": []
            }

        try:
            max_candidates = int(max_candidates)
        except (TypeError, ValueError):
            max_candidates = 3

        max_candidates = max(
            1,
            min(max_candidates, 5)
        )

        requirements_json = json.dumps(
            requirements,
            ensure_ascii=False
        )

        system_prompt = """
You are TALIA, the Talent Intelligence layer of TalentAI.

Your task is candidate evidence RETRIEVAL only.

You may analyze resumes from ANY professional domain,
industry, technology, vendor or country.

For each supplied job requirement, find the strongest
resume excerpts that may be relevant to that requirement.

IMPORTANT:

You are NOT deciding whether the candidate satisfies
the requirement.

Another component will validate the evidence later.

STRICT RULES:

1. Use only text explicitly contained in the resume.

2. Never invent, rewrite or manufacture resume evidence.

3. Preserve the original wording of the resume excerpt
as closely as possible.

4. Return the strongest and most specific evidence first.

5. Prefer excerpts that explicitly contain:
   - the exact requirement
   - an abbreviation
   - an expanded name
   - a product or version
   - a module name
   - a directly related professional activity

6. Search the ENTIRE resume before selecting evidence.

7. Do not stop after finding the first related passage.

8. If several passages exist, prefer the passage that is
most specific to the supplied requirement.

9. A passage may be returned even when it only appears
related. Validation belongs to another component.

10. Do not classify the evidence as supported,
unsupported, evidenced, uncertain or missing.

11. Do not calculate match percentages.

12. Do not decide whether the candidate should be hired.

13. Do not use outside knowledge to add facts that are
not written in the resume.

14. The language used to write the resume is not evidence
of language proficiency.

15. Evaluate every supplied requirement.

16. If no potentially relevant resume passage exists,
return an empty "candidates" list.

17. Return valid JSON only.
"""

        user_prompt = f"""
Retrieve resume evidence candidates for every job
requirement below.

REQUIREMENTS:

{requirements_json}

For every requirement return:

{{
    "requirement": "",
    "candidates": [
        {{
            "evidence": "",
            "relevance_reason": ""
        }}
    ]
}}

Return no more than {max_candidates} candidate excerpts
for each requirement.

ORDERING RULE:

The strongest and most specific candidate excerpt must
appear first.

IMPORTANT:

Do NOT decide whether an excerpt proves the requirement.

Do NOT use status labels such as:
- EVIDENCED
- UNCERTAIN
- NOT_EVIDENCED
- SUPPORTED
- NOT_SUPPORTED

The "evidence" value must come from the resume.

The "relevance_reason" must explain only why the passage
was retrieved, not whether it proves the requirement.

Return exactly this top-level structure:

{{
    "requirements": []
}}

CANDIDATE RESUME:

{resume_text}
"""

        result = self._request_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        if not isinstance(result, dict):
            return {
                "requirements": []
            }

        items = result.get(
            "requirements",
            []
        )

        if not isinstance(items, list):
            return {
                "requirements": []
            }

        normalized_items = []

        for item in items:

            if not isinstance(item, dict):
                continue

            requirement = str(
                item.get(
                    "requirement",
                    ""
                )
            ).strip()

            if not requirement:
                continue

            candidates = item.get(
                "candidates",
                []
            )

            if not isinstance(candidates, list):
                candidates = []

            normalized_candidates = []

            for candidate in candidates[
                :max_candidates
            ]:

                if not isinstance(
                    candidate,
                    dict
                ):
                    continue

                evidence = str(
                    candidate.get(
                        "evidence",
                        ""
                    )
                ).strip()

                relevance_reason = str(
                    candidate.get(
                        "relevance_reason",
                        ""
                    )
                ).strip()

                if not evidence:
                    continue

                normalized_candidates.append(
                    {
                        "evidence": evidence,
                        "relevance_reason": (
                            relevance_reason
                        )
                    }
                )

            normalized_items.append(
                {
                    "requirement": requirement,
                    "candidates": (
                        normalized_candidates
                    )
                }
            )

        return {
            "requirements": normalized_items
        }