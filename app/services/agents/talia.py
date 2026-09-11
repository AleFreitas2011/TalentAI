"""
=====================================================

TalentAI World

TALIA

Chief Talent Intelligence Officer

Central Intelligence Entry Point

Author:
TalentAI Team

Version:
3.0

=====================================================
"""

from datetime import datetime

from app.intelligence.talia.kernel import (
    TaliaKernel
)

from app.services.agents.smart_gap_engine import (
    SmartGapEngine
)

from app.services.agents.recruiter_agent import (
    RecruiterAgent
)

from app.services.agents.consultant360.consultant360_agent import (
    Consultant360Agent
)


class Talia:

    NAME = "TALIA"

    TITLE = "Chief Talent Intelligence Officer"

    VERSION = "3.0"

    def __init__(self, kernel=None):

        self.kernel = kernel or TaliaKernel()

        #
        # Legacy Agents
        # (Temporary during migration)
        #

        self.recruiter = RecruiterAgent()

        self.smart_gap = SmartGapEngine()

        self.consultant360 = Consultant360Agent()

        self.started_at = datetime.now()

    def status(self):

        return {

            "assistant": self.NAME,

            "title": self.TITLE,

            "version": self.VERSION,

            "status": "ONLINE",

            "started_at": self.started_at.isoformat()

        }

    def analisar_candidato(

        self,

        candidato,

        vaga,

        context

    ):

        print("\n" + "=" * 60)
        print(f"{self.NAME}")
        print(self.TITLE)
        print(f"Version {self.VERSION}")
        print("=" * 60)

        #
        # TALIA OS
        #

        decision = self.kernel.execute(

            candidate=candidato,

            job=vaga,

            context=context

        )

        #
        # Legacy Agents
        # (Temporary compatibility layer)
        #

        recruiter = self.recruiter.analisar(

            candidato,

            vaga

        )

        smart_gap = self.smart_gap.executar(

            candidato,

            vaga

        )

        consultant360 = self.consultant360.executar(

            candidato,

            vaga

        )

        return {

            "success": True,

            "agent": self.NAME,

            "version": self.VERSION,

            "timestamp": datetime.now().isoformat(),

            "candidate_id": candidato.id,

            "candidate_name": candidato.nome_arquivo,

            "status": "ANALYZED",

            #
            # NEW TALIA OS
            #

            "decision": decision,

            #
            # Legacy (temporary)
            #

            "recommendation": recruiter["analysis"]["recommendation"],

            "agents": {

                "recruiter": recruiter,

                "smart_gap": smart_gap,

                "consultant360": consultant360

            }

        }