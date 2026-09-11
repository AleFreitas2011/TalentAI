"""
=====================================================

TalentAI World

TALIA

Chief Talent Intelligence Officer

Central Intelligence Entry Point

Author:
TalentAI Team

Version:
3.2

=====================================================
"""

from datetime import datetime

from app.intelligence.talia.kernel import (
    TaliaKernel
)

from app.intelligence.missions.mission_builder import (
    MissionBuilder
)

from app.intelligence.domain.candidate import (
    Candidate
)

from app.intelligence.domain.job import (
    Job
)

from app.intelligence.engines.demand_engine import (
    DemandEngine
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

    VERSION = "3.2"

    DESCRIPTION = (
        "Central Intelligence Entry Point."
    )

    def __init__(self, kernel=None):

        self.kernel = kernel or TaliaKernel()

        self.mission_builder = MissionBuilder()

        self.demand_engine = DemandEngine()

        #
        # Legacy Agents
        # Temporary during migration
        #

        self.recruiter = RecruiterAgent()

        self.smart_gap = SmartGapEngine()

        self.consultant360 = Consultant360Agent()

        self.started_at = datetime.now()

    # =====================================================
    # STATUS
    # =====================================================

    def status(self):

        return {

            "assistant": self.NAME,

            "title": self.TITLE,

            "version": self.VERSION,

            "status": "ONLINE",

            "started_at": self.started_at.isoformat()

        }

    def _build_domain_candidate(
        self,
        candidato,
        context
    ) -> Candidate:
        """
        Converts the application candidate model
        into TALIA's official Candidate domain model.
        """

        perfil = getattr(
            context,
            "perfil",
            {}
        ) or {}

        return Candidate(

            full_name=perfil.get(
                "nome",
                ""
            ),

            email=getattr(
                candidato,
                "email",
                ""
            ) or "",

            phone=getattr(
                candidato,
                "telefone",
                ""
            ) or ""

        )

    def _build_domain_job(
        self,
        vaga
    ) -> Job:
        """
        Converts the application job model
        into TALIA's official Job domain model.
        """

        cliente = getattr(
            vaga,
            "cliente",
            None
        )

        client_name = ""

        if cliente:
            client_name = getattr(
                cliente,
                "empresa",
                ""
            ) or ""

        return Job(

            code=str(
                getattr(
                    vaga,
                    "id",
                    ""
                ) or ""
            ),

            title=getattr(
                vaga,
                "titulo",
                ""
            ) or "",

            description=getattr(
                vaga,
                "descricao",
                ""
            ) or "",

            client_name=client_name

        )

    # =====================================================
    # OFFICIAL MATCH
    # =====================================================

    def _extract_official_match(
        self,
        kernel_result
    ):
        """
        Extracts the official Overall Match produced by
        TALIA OS.

        The Kernel result contains the official Decision
        object inside the "decision" key.

        No score is recalculated here.
        """

        if not isinstance(kernel_result, dict):
            return None

        official_decision = kernel_result.get(
            "decision"
        )

        if official_decision is None:
            return None

        overall_match = getattr(
            official_decision,
            "overall_match",
            None
        )

        if overall_match is not None:
            return overall_match

        match_result = getattr(
            official_decision,
            "match_result",
            None
        )

        if match_result is None:
            return None

        return getattr(
            match_result,
            "overall_match",
            None
        )

    # =====================================================
    # CANDIDATE ANALYSIS
    # =====================================================

    def analisar_candidato(
        self,
        candidato,
        vaga,
        context
    ):

        print("\n" + "=" * 60)
        print(self.NAME)
        print(self.TITLE)
        print(f"Version {self.VERSION}")
        print("=" * 60)

        # =================================================
        # TALIA OS
        # =================================================

        domain_candidate = self._build_domain_candidate(
            candidato,
            context
        )

        domain_job = self._build_domain_job(
            vaga
        )

        # =====================================================
        # DEMAND INTELLIGENCE
        # =====================================================

        demand_text = "\n".join(
            filter(
                None,
                [
                    getattr(vaga, "titulo", "") or "",
                    getattr(vaga, "descricao", "") or "",
                    getattr(vaga, "palavras_chave", "") or ""
                ]
            )
        )

        demand_profile = self.demand_engine.analyze(
            demand_text
        )

        # =====================================================
        # MISSION
        # =====================================================

        mission = self.mission_builder.build(

            candidate=domain_candidate,

            job=domain_job,

            demand_profile=demand_profile,

            context=context

        )

        print()
        print("🚨 TALIA 3.2 VAI ENTRAR NO KERNEL 🚨")
        print("KERNEL CLASS:", self.kernel.__class__)
        print("KERNEL MODULE:", self.kernel.__class__.__module__)
        print()

        kernel_result = self.kernel.execute(
            mission
        )

        print()
        print("🚨 TALIA 3.2 VOLTOU DO KERNEL 🚨")
        print("RETURN TYPE:", type(kernel_result))
        print()

        # =================================================
        # OFFICIAL MATCH SOURCE
        # =================================================

        official_match = self._extract_official_match(
            kernel_result
        )

        if official_match is not None:

            print(
                "🎯 TALIA OFFICIAL OVERALL MATCH:",
                official_match
            )

            #
            # Temporary compatibility bridge.
            #
            # Legacy agents still consume candidato.score.
            # They must receive TALIA OS official Overall Match,
            # not the stale score previously stored in the model.
            #
            # Database persistence remains the responsibility
            # of candidate_processor.
            #

            candidato.score = official_match

        else:

            print(
                "⚠️ TALIA OFFICIAL OVERALL MATCH "
                "NOT AVAILABLE"
            )

        # =================================================
        # LEGACY AGENTS
        # Temporary compatibility layer
        # =================================================

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

            vaga,

            decision=kernel_result.get(
                "decision"
            )
            if isinstance(
                kernel_result,
                dict
            )
            else None

        )

        # =================================================
        # RESPONSE
        # =================================================

        return {

            "success": True,

            "agent": self.NAME,

            "version": self.VERSION,

            "timestamp": datetime.now().isoformat(),

            "candidate_id": candidato.id,

            "candidate_name": candidato.nome_arquivo,

            "status": "ANALYZED",

            #
            # TALIA OS
            #

            "mission_id": mission.id,

            "decision": kernel_result,

            "overall_match": official_match,

            #
            # Legacy
            #

            "recommendation": recruiter[
                "analysis"
            ][
                "recommendation"
            ],

            "agents": {

                "recruiter": recruiter,

                "smart_gap": smart_gap,

                "consultant360": consultant360

            }

        }