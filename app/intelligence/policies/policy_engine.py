"""
=====================================================

TalentAI World

Policy Engine

Coordinates TALIA intelligence policies.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from app.intelligence.decision import Decision

from app.intelligence.policies.base_policy import BasePolicy

from app.intelligence.policies.mandatory_skill_policy import (
    MandatorySkillPolicy
)

from app.intelligence.policies.language_policy import (
    LanguagePolicy
)

from app.intelligence.engines.talent_intelligence_analyst import (
    TalentIntelligenceAnalyst
)


class PolicyEngine:

    NAME = "Policy Engine"

    VERSION = "1.0"

    DESCRIPTION = (
        "Coordinates TALIA intelligence policies."
    )

    def __init__(self):

        self.analyst = TalentIntelligenceAnalyst()

        self.policies = [

            MandatorySkillPolicy(),

            LanguagePolicy()

        ]

    def evaluate(
        self,
        mission,
        evidence_set
    ) -> Decision:
        """
        Executes all registered policies and produces
        the final TALIA decision.
        """

        print()
        print("🔥 POLICY ENGINE REAL ENTROU 🔥")
        print("ANALYST CLASS:", self.analyst.__class__)
        print("ANALYST MODULE:", self.analyst.__class__.__module__)
        print()

        decision = Decision()

        print("🔥 VAI CHAMAR ANALYST AGORA 🔥")

        match_result = self.analyst.analyze(
            mission,
            evidence_set
        )
        # =================================================
        # TRANSFER ANALYSIS TO DECISION
        # =================================================

        decision.match_result = match_result

        decision.overall_match = match_result.overall_match

        decision.technical_fit = match_result.technical_fit

        decision.experience_fit = match_result.experience_fit

        decision.executive_summary = (
            match_result.executive_summary
        )

        decision.recommendation = (
            match_result.recommendation
        )

        decision.strengths = match_result.strengths

        decision.gaps = match_result.gaps

        decision.risks = match_result.risks

        # =================================================
        # POLICY EVALUATION
        # =================================================

        for policy in self.policies:

            decision = policy.evaluate(
                mission,
                evidence_set,
                decision
            )

        return decision