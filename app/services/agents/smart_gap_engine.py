"""
=====================================================

Smart Gap Engine

Purpose:
Identify missing information that can increase the
candidate Match Score through intelligent validation.

Author:
TalentAI Team

=====================================================
"""


from datetime import datetime


class SmartGapEngine:

    VERSION = "1.0"

    def executar(self, candidato, vaga):

        print("🔍 Smart Gap Engine")

        score = candidato.score or 0

        needs_validation = False
        estimated_score = score

        if 75 <= score < 90:

            needs_validation = True
            estimated_score = min(score + 10, 95)

        return {

            "success": True,

            "agent": "SmartGapEngine",

            "version": self.VERSION,

            "timestamp": datetime.now().isoformat(),

            "current_match": score,

            "estimated_match": estimated_score,

            "needs_validation": needs_validation,

            "gaps": [],

            "questions": []

        }