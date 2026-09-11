"""
=====================================================

TalentAI World
Evidence Builder

Builds structured evidences from
candidate analysis.

Author:
TalentAI Team

Version:
2.6

=====================================================
"""

from app.intelligence.evidence.evidence import Evidence
from app.intelligence.evidence.evidence_set import EvidenceSet
from app.intelligence.evidence.evidence_type import EvidenceType

from app.intelligence.extractors.extractor_manager import (
    ExtractorManager
)

from app.intelligence.knowledge.knowledge_manager import (
    KnowledgeManager
)

from app.intelligence.providers.openai_intelligence_provider import (
    OpenAIIntelligenceProvider
)

from app.intelligence.evidence.semantic_evidence_grounder import (
    SemanticEvidenceGrounder
)

from app.intelligence.evidence.semantic_evidence_validator import (
    SemanticEvidenceValidator
)

from app.intelligence.evidence.semantic_evidence_resolver import (
    SemanticEvidenceResolver
)


class EvidenceBuilder:

    NAME = "Evidence Builder"

    VERSION = "2.6"

    DESCRIPTION = (
        "Builds structured evidences."
    )

    def __init__(self):

        self.extractor_manager = ExtractorManager()

        self.knowledge = KnowledgeManager()

        self.intelligence_provider = (
            OpenAIIntelligenceProvider()
        )

        self.semantic_grounder = (
            SemanticEvidenceGrounder()
        )

        self.semantic_validator = (
            SemanticEvidenceValidator()
        )

        self.semantic_resolver = (
            SemanticEvidenceResolver()
        )

    def build(
        self,
        candidate,
        job,
        context,
        demand_profile=None
    ) -> EvidenceSet:

        evidence_set = EvidenceSet()

        # =====================================================
        # LEGACY MATCH EVIDENCE
        # =====================================================

        match = context.match or {}

        score = match.get(
            "score"
        )

        if score is not None:

            evidence_set.add(

                Evidence(

                    type=EvidenceType.MATCH,

                    title="Candidate Match",

                    description=f"Legacy match score: {score}%",

                    confidence=1.0,

                    value=match

                )

            )

        # =====================================================
        # AI PROFILE
        # =====================================================

        perfil = context.perfil

        if perfil:

            evidence_set.add(

                Evidence(

                    type=EvidenceType.BUSINESS,

                    title="AI Profile",

                    description=str(perfil),

                    confidence=0.95,

                    value=perfil

                )

            )

        # =====================================================
        # INDUSTRY EVIDENCE
        # =====================================================

        if perfil:

            setores = perfil.get(
                "setores",
                ""
            )

            if setores:

                industries = self.knowledge.find_industries(
                    str(setores)
                )

                for industry in industries:

                    evidence_set.add(

                        Evidence(

                            type=EvidenceType.BUSINESS,

                            title="Industry Experience",

                            description=(
                                f"Industry identified: {industry}"
                            ),

                            confidence=0.95,

                            value={
                                "industry": industry
                            }

                        )

                    )

        # =====================================================
        # PROFESSIONAL HISTORY
        # =====================================================

        historico = context.historico_profissional

        if historico:

            evidence_set.add(

                Evidence(

                    type=EvidenceType.EXPERIENCE,

                    title="Professional History",

                    description=str(historico),

                    confidence=1.0,

                    value=historico

                )

            )

        # =====================================================
        # TECHNICAL SKILLS
        # =====================================================

        skills = self.extractor_manager.skills(
            context
        )

        for skill in skills:

            evidence_set.add(

                Evidence(

                    type=EvidenceType.TECHNICAL,

                    title=skill,

                    description=f"Technical skill identified: {skill}",

                    confidence=1.0,

                    value=skill

                )

            )

        # =====================================================
        # LANGUAGES
        # =====================================================

        languages = self.extractor_manager.languages(
            context
        )

        for language in languages:

            description = (
                f"Language identified: {language.name}"
            )

            if language.level:

                description += (
                    f" - Proficiency: {language.level}"
                )

            evidence_set.add(

                Evidence(

                    type=EvidenceType.LANGUAGE,

                    title=language.name,

                    description=description,

                    confidence=1.0,

                    value={
                        "name": language.name,
                        "level": language.level
                    }

                )

            )

        # =====================================================
        # SEMANTIC REQUIREMENT EVIDENCE
        # =====================================================
        #
        # Version 2.5 preserves the structural identity of each
        # DemandProfile requirement and introduces seniority as
        # an independent semantic demand dimension.
        #
        # Seniority is NOT converted into a fixed number of years.
        # It is evaluated by the existing semantic evidence
        # pipeline using grounded professional evidence.
        #
        # This layer still does NOT change technical fit,
        # overall match or decision.
        # =====================================================

        self._build_semantic_evidence(
            evidence_set=evidence_set,
            context=context,
            demand_profile=demand_profile
        )

        return evidence_set

    # =========================================================
    # SEMANTIC EVIDENCE PIPELINE
    # =========================================================

    def _build_semantic_evidence(
        self,
        evidence_set,
        context,
        demand_profile
    ):

        if demand_profile is None:
            return

        resume_text = str(
            context.texto_cv or ""
        ).strip()

        if not resume_text:
            return

        requirement_index = (
            self._semantic_requirement_index(
                demand_profile
            )
        )

        if not requirement_index:
            return

        requirements = [
            item["requirement"]
            for item in requirement_index.values()
        ]

        retrieval = (
            self.intelligence_provider
            .retrieve_candidate_evidence(
                resume_text=resume_text,
                requirements=requirements,
                max_candidates=3
            )
        )

        if not isinstance(
            retrieval,
            dict
        ):
            return

        retrieval_items = retrieval.get(
            "requirements",
            []
        )

        if not isinstance(
            retrieval_items,
            list
        ):
            return

        processed_keys = set()

        for retrieval_item in retrieval_items:

            if not isinstance(
                retrieval_item,
                dict
            ):
                continue

            requirement = str(
                retrieval_item.get(
                    "requirement",
                    ""
                )
            ).strip()

            if not requirement:
                continue

            requirement_key = (
                requirement.casefold()
            )

            metadata = requirement_index.get(
                requirement_key
            )

            if metadata is None:
                continue

            processed_keys.add(
                requirement_key
            )

            candidates = retrieval_item.get(
                "candidates",
                []
            )

            if not isinstance(
                candidates,
                list
            ):
                candidates = []

            validated_candidates = []
            grounded_excerpts = []

            for candidate_evidence in candidates:

                if not isinstance(
                    candidate_evidence,
                    dict
                ):
                    continue

                excerpt = str(
                    candidate_evidence.get(
                        "evidence",
                        ""
                    )
                ).strip()

                if not excerpt:
                    continue

                analysis = {
                    "evidence": [
                        {
                            "requirement": requirement,
                            "status": "UNCERTAIN",
                            "evidence": excerpt,
                            "reason": str(
                                candidate_evidence.get(
                                    "relevance_reason",
                                    ""
                                )
                            ).strip(),
                            "confidence": 0.5
                        }
                    ]
                }

                grounded = (
                    self.semantic_grounder.ground(
                        analysis,
                        resume_text
                    )
                )

                validated = (
                    self.semantic_validator.validate(
                        grounded
                    )
                )

                validated_candidates.append(
                    validated
                )

                grounded_excerpt = (
                    self._extract_grounded_excerpt(
                        grounded
                    )
                )

                if (
                    grounded_excerpt
                    and grounded_excerpt
                    not in grounded_excerpts
                ):
                    grounded_excerpts.append(
                        grounded_excerpt
                    )

            # -------------------------------------------------
            # COMPLEMENTARY GROUNDED EVIDENCE
            # -------------------------------------------------
            #
            # Seniority requires a broader professional context
            # than a normal atomic technical requirement. The
            # retriever can legitimately return different small
            # excerpts between executions, which previously made
            # Seniority oscillate between SUPPORTED and
            # PARTIALLY_SUPPORTED for the same CV.
            #
            # For seniority only, the complete CV is already the
            # authoritative grounded source. We therefore add one
            # deterministic composite candidate containing the
            # full resume text. The SemanticEvidenceValidator
            # remains responsible for the qualitative decision:
            # no fixed years threshold and no automatic seniority
            # promotion are introduced here.
            # -------------------------------------------------

            is_seniority = (
                self._clean_text(
                    metadata.get(
                        "category",
                        ""
                    )
                ).casefold()
                == "seniority"
            )

            if is_seniority:

                seniority_analysis = {
                    "evidence": [
                        {
                            "requirement": requirement,
                            "status": "UNCERTAIN",
                            "evidence": resume_text,
                            "reason": (
                                "Complete grounded professional "
                                "history supplied for stable "
                                "qualitative seniority assessment."
                            ),
                            "confidence": 1.0,
                            "grounded": True
                        }
                    ]
                }

                seniority_validated = (
                    self.semantic_validator.validate(
                        seniority_analysis
                    )
                )

                validated_candidates.append(
                    seniority_validated
                )

            elif len(grounded_excerpts) >= 2:

                combined_evidence = (
                    "\n\n".join(
                        grounded_excerpts
                    )
                )

                combined_analysis = {
                    "evidence": [
                        {
                            "requirement": requirement,
                            "status": "UNCERTAIN",
                            "evidence": combined_evidence,
                            "reason": (
                                "Complementary resume excerpts "
                                "grounded independently and "
                                "validated together."
                            ),
                            "confidence": 0.5,
                            "grounded": True
                        }
                    ]
                }

                combined_validated = (
                    self.semantic_validator.validate(
                        combined_analysis
                    )
                )

                validated_candidates.append(
                    combined_validated
                )

            # -------------------------------------------------
            # RESOLVE
            # -------------------------------------------------

            resolved = (
                self.semantic_resolver.resolve(
                    requirement,
                    validated_candidates
                )
            )

            if not isinstance(
                resolved,
                dict
            ):
                continue

            enriched = (
                self._enrich_semantic_result(
                    resolved=resolved,
                    metadata=metadata
                )
            )

            evidence_set.add_semantic(
                enriched
            )

        # =====================================================
        # REQUIREMENTS OMITTED BY RETRIEVER
        # =====================================================

        for requirement_key, metadata in (
            requirement_index.items()
        ):

            if requirement_key in processed_keys:
                continue

            resolved = (
                self.semantic_resolver.resolve(
                    metadata["requirement"],
                    []
                )
            )

            enriched = (
                self._enrich_semantic_result(
                    resolved=resolved,
                    metadata=metadata
                )
            )

            evidence_set.add_semantic(
                enriched
            )

    # =========================================================
    # STRUCTURAL REQUIREMENT INDEX
    # =========================================================

    def _semantic_requirement_index(
        self,
        demand_profile
    ) -> dict:

        index = {}

        technical_requirements = getattr(
            demand_profile,
            "technical_requirements",
            None
        )

        # =====================================================
        # TECHNICAL REQUIREMENTS
        # =====================================================

        if technical_requirements is not None:

            # -------------------------------------------------
            # NORMAL ATOMIC REQUIREMENTS
            # -------------------------------------------------

            atomic_requirements = getattr(
                technical_requirements,
                "atomic_requirements",
                []
            )

            for requirement in atomic_requirements:

                name = self._clean_text(
                    getattr(
                        requirement,
                        "name",
                        ""
                    )
                )

                if not name:
                    continue

                key = name.casefold()

                item = self._ensure_requirement_entry(
                    index=index,
                    key=key,
                    requirement=requirement
                )

                self._add_structure(
                    item=item,
                    structure={
                        "scope": "atomic",
                        "group_id": None,
                        "group_name": None,
                        "group_type": None,
                        "group_mandatory": None,
                        "alternative_id": None,
                        "alternative_name": None
                    }
                )

            # -------------------------------------------------
            # LOGICAL REQUIREMENT GROUPS
            # -------------------------------------------------

            groups = getattr(
                technical_requirements,
                "requirement_groups",
                []
            )

            for group in groups:

                group_id = self._clean_text(
                    getattr(
                        group,
                        "group_id",
                        ""
                    )
                )

                group_name = self._clean_text(
                    getattr(
                        group,
                        "name",
                        ""
                    )
                )

                group_type = self._clean_text(
                    getattr(
                        group,
                        "group_type",
                        ""
                    )
                )

                group_mandatory = bool(
                    getattr(
                        group,
                        "mandatory",
                        True
                    )
                )

                alternatives = getattr(
                    group,
                    "alternatives",
                    []
                )

                for alternative in alternatives:

                    alternative_id = self._clean_text(
                        getattr(
                            alternative,
                            "alternative_id",
                            ""
                        )
                    )

                    alternative_name = self._clean_text(
                        getattr(
                            alternative,
                            "name",
                            ""
                        )
                    )

                    alternative_requirements = getattr(
                        alternative,
                        "requirements",
                        []
                    )

                    for requirement in (
                        alternative_requirements
                    ):

                        name = self._clean_text(
                            getattr(
                                requirement,
                                "name",
                                ""
                            )
                        )

                        if not name:
                            continue

                        key = name.casefold()

                        item = (
                            self._ensure_requirement_entry(
                                index=index,
                                key=key,
                                requirement=requirement
                            )
                        )

                        self._add_structure(
                            item=item,
                            structure={
                                "scope": "group",
                                "group_id": group_id or None,
                                "group_name": group_name or None,
                                "group_type": group_type or None,
                                "group_mandatory": (
                                    group_mandatory
                                ),
                                "alternative_id": (
                                    alternative_id or None
                                ),
                                "alternative_name": (
                                    alternative_name or None
                                )
                            }
                        )

        # =====================================================
        # SENIORITY REQUIREMENT
        # =====================================================
        #
        # Seniority belongs to job_info rather than
        # technical_requirements.
        #
        # It is represented as an independent semantic category.
        # The original seniority value is preserved exactly as
        # interpreted by DemandEngine.
        #
        # No fixed number of years is inferred here.
        # =====================================================

        job_info = getattr(
            demand_profile,
            "job_info",
            None
        )

        if job_info is not None:

            seniority = self._clean_text(
                getattr(
                    job_info,
                    "seniority",
                    ""
                )
            )

            if seniority:

                requirement = (
                    f"Seniority: {seniority}"
                )

                key = requirement.casefold()

                if key not in index:

                    index[key] = {
                        "requirement_id": "job_seniority",
                        "requirement": requirement,
                        "category": "seniority",
                        "importance": "mandatory",
                        "source": (
                            "demand_profile.job_info.seniority"
                        ),
                        "description": (
                            "Professional seniority level required "
                            "by the job demand. The level must be "
                            "assessed qualitatively from grounded "
                            "candidate evidence without inventing "
                            "a fixed years-of-experience threshold."
                        ),
                        "structures": [
                            {
                                "scope": "seniority",
                                "group_id": None,
                                "group_name": None,
                                "group_type": None,
                                "group_mandatory": None,
                                "alternative_id": None,
                                "alternative_name": None
                            }
                        ]
                    }

        return index

    # =========================================================
    # REQUIREMENT ENTRY
    # =========================================================

    def _ensure_requirement_entry(
        self,
        index,
        key,
        requirement
    ) -> dict:

        existing = index.get(
            key
        )

        if existing is not None:
            return existing

        item = {
            "requirement_id": self._clean_text(
                getattr(
                    requirement,
                    "requirement_id",
                    ""
                )
            ),
            "requirement": self._clean_text(
                getattr(
                    requirement,
                    "name",
                    ""
                )
            ),
            "category": self._clean_text(
                getattr(
                    requirement,
                    "category",
                    "technical"
                )
            ) or "technical",
            "importance": self._clean_text(
                getattr(
                    requirement,
                    "importance",
                    "mandatory"
                )
            ) or "mandatory",
            "source": self._clean_text(
                getattr(
                    requirement,
                    "source",
                    ""
                )
            ),
            "description": self._clean_text(
                getattr(
                    requirement,
                    "description",
                    ""
                )
            ),
            "structures": []
        }

        index[key] = item

        return item

    # =========================================================
    # STRUCTURE REGISTRATION
    # =========================================================

    def _add_structure(
        self,
        item,
        structure
    ):

        structures = item.setdefault(
            "structures",
            []
        )

        identity = (
            structure.get("scope"),
            structure.get("group_id"),
            structure.get("alternative_id")
        )

        for existing in structures:

            existing_identity = (
                existing.get("scope"),
                existing.get("group_id"),
                existing.get("alternative_id")
            )

            if existing_identity == identity:
                return

        structures.append(
            structure
        )

    # =========================================================
    # RESULT ENRICHMENT
    # =========================================================

    def _enrich_semantic_result(
        self,
        resolved,
        metadata
    ) -> dict:

        enriched = dict(
            resolved
        )

        enriched["requirement_id"] = (
            metadata.get(
                "requirement_id",
                ""
            )
        )

        enriched["requirement"] = (
            metadata.get(
                "requirement",
                enriched.get(
                    "requirement",
                    ""
                )
            )
        )

        enriched["category"] = (
            metadata.get(
                "category",
                "technical"
            )
        )

        enriched["importance"] = (
            metadata.get(
                "importance",
                "mandatory"
            )
        )

        enriched["source"] = (
            metadata.get(
                "source",
                ""
            )
        )

        enriched["description"] = (
            metadata.get(
                "description",
                ""
            )
        )

        enriched["structures"] = [
            dict(structure)
            for structure in metadata.get(
                "structures",
                []
            )
        ]

        return enriched

    # =========================================================
    # GROUNDED EXCERPT EXTRACTION
    # =========================================================

    def _extract_grounded_excerpt(
        self,
        grounded_analysis
    ) -> str:

        if not isinstance(
            grounded_analysis,
            dict
        ):
            return ""

        items = grounded_analysis.get(
            "evidence",
            []
        )

        if not isinstance(
            items,
            list
        ):
            return ""

        for item in items:

            if not isinstance(
                item,
                dict
            ):
                continue

            if not bool(
                item.get(
                    "grounded",
                    False
                )
            ):
                continue

            excerpt = self._clean_text(
                item.get(
                    "evidence",
                    ""
                )
            )

            if excerpt:
                return excerpt

        return ""

    # =========================================================
    # HELPERS
    # =========================================================

    def _clean_text(
        self,
        value
    ) -> str:

        if value is None:
            return ""

        return str(
            value
        ).strip()