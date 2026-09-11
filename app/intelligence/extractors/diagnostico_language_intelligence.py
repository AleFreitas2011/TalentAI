"""
=====================================================

TalentAI World

Language Intelligence Diagnostic

Diagnóstico controlado:

Candidate CV
-> LanguageExtractor
-> EvidenceBuilder

Job
-> DemandEngine
-> DemandProfile

Candidate Language x Demand Language

Não altera banco de dados.
Não executa TALIA.
Não grava nenhuma informação.

=====================================================
"""

from app.db import SessionLocal
from app.models import Candidato, Vaga

from app.intelligence.context.analysis_context import (
    AnalysisContext
)

from app.intelligence.extractors.extractor_manager import (
    ExtractorManager
)

from app.intelligence.evidence.evidence_builder import (
    EvidenceBuilder
)

from app.intelligence.evidence.evidence_type import (
    EvidenceType
)

from app.intelligence.engines.demand_engine import (
    DemandEngine
)


CANDIDATE_ID = 142
JOB_ID = 31


def section(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def safe_value(obj, attribute, default=""):

    return getattr(
        obj,
        attribute,
        default
    )


def main():

    db = SessionLocal()

    try:

        # =====================================================
        # REAL DATABASE RECORDS
        # =====================================================

        candidato = (
            db.query(Candidato)
            .filter(
                Candidato.id == CANDIDATE_ID
            )
            .first()
        )

        vaga = (
            db.query(Vaga)
            .filter(
                Vaga.id == JOB_ID
            )
            .first()
        )

        if candidato is None:

            raise RuntimeError(
                f"Candidato {CANDIDATE_ID} nao encontrado."
            )

        if vaga is None:

            raise RuntimeError(
                f"Vaga {JOB_ID} nao encontrada."
            )

        texto_cv = str(
            candidato.texto_cv or ""
        )

        # =====================================================
        # 1. CANDIDATE CV
        # =====================================================

        section("1. CANDIDATE CV")

        print(
            "CANDIDATE ID:",
            candidato.id
        )

        print(
            "CV LENGTH:",
            len(texto_cv)
        )

        print(
            "HAS ENGLISH:",
            any(
                token in texto_cv.casefold()
                for token in (
                    "inglês",
                    "ingles",
                    "english",
                )
            )
        )

        print()
        print("LANGUAGE LINES:")

        for line in texto_cv.splitlines():

            normalized = line.casefold()

            if any(
                token in normalized
                for token in (
                    "idioma",
                    "language",
                    "inglês",
                    "ingles",
                    "english",
                    "português",
                    "portugues",
                    "espanhol",
                    "spanish",
                    "italiano",
                    "italian",
                )
            ):

                print(
                    " ",
                    repr(
                        line.strip()
                    )
                )

        # =====================================================
        # 2. ANALYSIS CONTEXT
        # =====================================================

        context = AnalysisContext(
            texto_cv=texto_cv
        )

        section("2. ANALYSIS CONTEXT")

        context_text = str(
            safe_value(
                context,
                "texto_cv",
                ""
            )
            or ""
        )

        print(
            "CONTEXT CV LENGTH:",
            len(context_text)
        )

        print(
            "CONTEXT HAS ENGLISH:",
            any(
                token in context_text.casefold()
                for token in (
                    "inglês",
                    "ingles",
                    "english",
                )
            )
        )

        # =====================================================
        # 3. LANGUAGE EXTRACTOR
        # =====================================================

        section("3. CANDIDATE LANGUAGE EXTRACTOR")

        extractor_manager = (
            ExtractorManager()
        )

        languages = (
            extractor_manager.languages(
                context
            )
        )

        print(
            "LANGUAGES FOUND:",
            len(languages)
        )

        for language in languages:

            print(
                "LANGUAGE:",
                repr(language.name),
                "| LEVEL:",
                repr(language.level)
            )

        # =====================================================
        # 4. LANGUAGE EVIDENCE
        # =====================================================

        section("4. CANDIDATE LANGUAGE EVIDENCE")

        builder = EvidenceBuilder()

        evidence_set = builder.build(
            candidate=candidato,
            job=vaga,
            context=context,
            demand_profile=None
        )

        language_evidences = (
            evidence_set.by_type(
                EvidenceType.LANGUAGE
            )
        )

        print(
            "LANGUAGE EVIDENCE COUNT:",
            len(language_evidences)
        )

        for evidence in language_evidences:

            print(
                "TITLE:",
                repr(
                    safe_value(
                        evidence,
                        "title",
                        None
                    )
                )
            )

            print(
                "VALUE:",
                repr(
                    safe_value(
                        evidence,
                        "value",
                        None
                    )
                )
            )

        # =====================================================
        # 5. REAL JOB DATA
        # =====================================================

        section("5. REAL JOB DATA")

        print(
            "JOB ID:",
            vaga.id
        )

        print(
            "TITLE:",
            repr(
                safe_value(
                    vaga,
                    "titulo",
                    ""
                )
            )
        )

        print(
            "DESCRIPTION:",
            repr(
                safe_value(
                    vaga,
                    "descricao",
                    ""
                )
            )
        )

        print(
            "KEYWORDS:",
            repr(
                safe_value(
                    vaga,
                    "palavras_chave",
                    ""
                )
            )
        )

        # =====================================================
        # 6. BUILD DEMAND TEXT
        # =====================================================

        title = str(
            safe_value(
                vaga,
                "titulo",
                ""
            )
            or ""
        )

        description = str(
            safe_value(
                vaga,
                "descricao",
                ""
            )
            or ""
        )

        keywords = str(
            safe_value(
                vaga,
                "palavras_chave",
                ""
            )
            or ""
        )

        demand_text = "\n".join(
            part
            for part in (
                title,
                description,
                keywords
            )
            if part
        )

        section("6. DEMAND TEXT")

        print(
            "DEMAND TEXT LENGTH:",
            len(demand_text)
        )

        print(
            "DEMAND HAS ENGLISH REQUIREMENT:",
            any(
                token in demand_text.casefold()
                for token in (
                    "inglês",
                    "ingles",
                    "english",
                )
            )
        )

        # =====================================================
        # 7. DEMAND ENGINE
        # =====================================================

        section("7. DEMAND PROFILE")

        demand_engine = DemandEngine()

        demand_profile = demand_engine.analyze(
            demand_text
        )

        technical_requirements = safe_value(
            demand_profile,
            "technical_requirements",
            None
        )

        demand_languages = (
            safe_value(
                technical_requirements,
                "languages",
                []
            )
            or []
        )

        print(
            "DEMAND LANGUAGES RAW:",
            repr(demand_languages)
        )

        print()
        print("DEMAND LANGUAGE ITEMS:")

        if not demand_languages:

            print("  NONE")

        for language_requirement in demand_languages:

            print(
                "TYPE:",
                type(
                    language_requirement
                ).__name__
            )

            print(
                "REPR:",
                repr(
                    language_requirement
                )
            )

            print(
                "NAME:",
                repr(
                    safe_value(
                        language_requirement,
                        "name",
                        None
                    )
                )
            )

            print(
                "LANGUAGE:",
                repr(
                    safe_value(
                        language_requirement,
                        "language",
                        None
                    )
                )
            )

            print(
                "LEVEL:",
                repr(
                    safe_value(
                        language_requirement,
                        "level",
                        None
                    )
                )
            )

            print(
                "PROFICIENCY:",
                repr(
                    safe_value(
                        language_requirement,
                        "proficiency",
                        None
                    )
                )
            )

            print("-" * 50)

        # =====================================================
        # 8. SIDE-BY-SIDE
        # =====================================================

        section("8. CANDIDATE X DEMAND")

        print("CANDIDATE LANGUAGES:")

        for language in languages:

            print(
                " ",
                repr(language.name),
                "/",
                repr(language.level)
            )

        print()
        print("DEMAND LANGUAGES:")

        if demand_languages:

            for language_requirement in demand_languages:

                print(
                    " ",
                    repr(
                        language_requirement
                    )
                )

        else:

            print("  NONE")

        # =====================================================
        # END
        # =====================================================

        section("9. DIAGNOSTIC COMPLETE")

        print(
            "No database changes were made."
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()