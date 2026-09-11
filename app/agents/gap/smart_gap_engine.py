from app.agents.base.base_agent import BaseAgent


class SmartGapEngine(BaseAgent):

    NAME = "Smart Gap Engine"
    VERSION = "2.0"

    def executar(self, candidato, vaga):

        score = candidato.score or 0

        needs_validation = False
        estimated_score = score

        if 75 <= score < 90:
            needs_validation = True
            estimated_score = min(score + 10, 95)

        return self.success({
            "current_match": score,
            "estimated_match": estimated_score,
            "needs_validation": needs_validation,
            "gaps": [],
            "questions": []
        })