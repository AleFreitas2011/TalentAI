"""
=====================================================

TalentAI World

Talent Intelligence Analyst

Core intelligence engine responsible for analyzing
Candidate Intelligence against Demand Intelligence.

This engine does NOT apply business rules.

Its responsibility is to understand:

- Candidate Profile
- Demand Profile
- Technical Fit
- Experience Fit
- Seniority Fit
- Business Fit
- Language Fit
- Risks
- Strengths
- Gaps

The final business decision is made later by
the Policy Engine.

Author:
TalentAI Team

Version:
2.7

=====================================================
"""

from app.intelligence.match_result import MatchResult

from app.intelligence.engines.experience_engine import (
    ExperienceEngine
)

from app.intelligence.evidence.evidence_type import (
    EvidenceType
)

from app.intelligence.knowledge.knowledge_manager import (
    KnowledgeManager
)

from app.intelligence.domain.business_fit_status import (
    BusinessFitStatus
)


class TalentIntelligenceAnalyst:

    NAME = "Talent Intelligence Analyst"

    VERSION = "2.7"

    DESCRIPTION = (
        "Analyzes candidate intelligence "
        "against demand intelligence."
    )

    def __init__(self):

        self.experience_engine = ExperienceEngine()

    # =====================================================
    # TECHNICAL FIT
    # =====================================================

    def _calculate_technical_fit(
        self,
        mission,
        evidence_set
    ):
        """
        Calculates CORE technical adherence.

        Mandatory and unclassified requirements participate
        in Core Fit.

        Nice-to-have requirements are evaluated separately
        for explainability and never reduce Core Fit.

        ONE_OF groups are scored as one logical requirement.
        """

        demand_profile = getattr(
            mission,
            "demand_profile",
            None
        )

        empty_matched = {
            "mandatory": [],
            "unclassified": [],
            "nice_to_have": []
        }

        empty_missing = {
            "mandatory": [],
            "unclassified": [],
            "nice_to_have": []
        }

        if not demand_profile:
            return 0, empty_matched, empty_missing

        requirements = getattr(
            demand_profile,
            "technical_requirements",
            None
        )

        if requirements is None:
            return 0, empty_matched, empty_missing

        semantic_evidences = (
            getattr(
                evidence_set,
                "semantic_evidences",
                []
            )
            or []
        )

        semantic_index = {}

        validation_value = {
            "SUPPORTED": 1.0,
            "PARTIALLY_SUPPORTED": 0.5,
            "NOT_SUPPORTED": 0.0
        }

        validation_rank = {
            "SUPPORTED": 3,
            "PARTIALLY_SUPPORTED": 2,
            "NOT_SUPPORTED": 1
        }

        for semantic in semantic_evidences:

            if not isinstance(semantic, dict):
                continue

            # Seniority is evaluated independently.
            if (
                str(
                    semantic.get(
                        "category",
                        ""
                    )
                )
                .strip()
                .casefold()
                == "seniority"
            ):
                continue

            requirement_name = str(
                semantic.get(
                    "requirement",
                    ""
                )
            ).strip()

            if not requirement_name:
                continue

            key = requirement_name.casefold()

            validation = str(
                semantic.get(
                    "validation",
                    "NOT_SUPPORTED"
                )
            ).strip().upper()

            if validation not in validation_value:
                validation = "NOT_SUPPORTED"

            existing = semantic_index.get(key)

            if (
                existing is None
                or validation_rank[validation]
                > validation_rank[
                    existing["validation"]
                ]
            ):
                semantic_index[key] = {
                    "requirement": requirement_name,
                    "validation": validation,
                    "value": validation_value[validation],
                    "semantic": semantic
                }

        matched = {
            "mandatory": [],
            "unclassified": [],
            "nice_to_have": []
        }

        missing = {
            "mandatory": [],
            "unclassified": [],
            "nice_to_have": []
        }

        core_maximum_score = 0.0
        core_achieved_score = 0.0

        scored_requirement_keys = set()

        def classify_result(
            name,
            bucket,
            value
        ):

            if value > 0.0:

                if name not in matched[bucket]:
                    matched[bucket].append(name)

            else:

                if name not in missing[bucket]:
                    missing[bucket].append(name)

        def score_requirement(
            name,
            bucket,
            weight,
            contributes_to_core=True
        ):

            nonlocal core_maximum_score
            nonlocal core_achieved_score

            clean_name = str(
                name or ""
            ).strip()

            if not clean_name:
                return

            key = clean_name.casefold()

            if key in scored_requirement_keys:
                return

            scored_requirement_keys.add(key)

            semantic = semantic_index.get(key)

            value = (
                semantic["value"]
                if semantic is not None
                else 0.0
            )

            classify_result(
                clean_name,
                bucket,
                value
            )

            if not contributes_to_core:
                return

            core_maximum_score += weight

            core_achieved_score += (
                weight * value
            )

        atomic_requirements = getattr(
            requirements,
            "atomic_requirements",
            []
        ) or []

        for requirement in atomic_requirements:

            name = str(
                getattr(
                    requirement,
                    "name",
                    ""
                )
                or ""
            ).strip()

            if not name:
                continue

            importance = str(
                getattr(
                    requirement,
                    "importance",
                    ""
                )
                or ""
            ).strip().casefold()

            if importance == "mandatory":

                bucket = "mandatory"
                weight = 3.0
                contributes_to_core = True

            elif importance in {
                "nice_to_have",
                "nice-to-have",
                "nice to have",
                "optional",
                "preferred"
            }:

                bucket = "nice_to_have"
                weight = 1.0
                contributes_to_core = False

            else:

                bucket = "unclassified"
                weight = 2.0
                contributes_to_core = True

            score_requirement(
                name,
                bucket,
                weight,
                contributes_to_core
            )

        # =================================================
        # ONE_OF GROUPS
        # =================================================

        groups = getattr(
            requirements,
            "requirement_groups",
            []
        ) or []

        for group in groups:

            group_type = str(
                getattr(
                    group,
                    "group_type",
                    ""
                )
                or ""
            ).strip().upper()

            if group_type != "ONE_OF":
                continue

            alternatives = getattr(
                group,
                "alternatives",
                []
            ) or []

            alternative_details = []

            for alternative in alternatives:

                alternative_requirements = getattr(
                    alternative,
                    "requirements",
                    []
                ) or []

                values = []
                names = []

                for requirement in alternative_requirements:

                    name = str(
                        getattr(
                            requirement,
                            "name",
                            ""
                        )
                        or ""
                    ).strip()

                    if not name:
                        continue

                    names.append(name)

                    semantic = semantic_index.get(
                        name.casefold()
                    )

                    values.append(
                        semantic["value"]
                        if semantic is not None
                        else 0.0
                    )

                if not values:
                    continue

                alternative_details.append(
                    {
                        "name": str(
                            getattr(
                                alternative,
                                "name",
                                ""
                            )
                            or ""
                        ).strip(),
                        "requirements": names,
                        "score": (
                            sum(values)
                            / len(values)
                        )
                    }
                )

            if not alternative_details:
                continue

            best_alternative = max(
                alternative_details,
                key=lambda item: item["score"]
            )

            best_score = best_alternative["score"]

            group_name = str(
                getattr(
                    group,
                    "name",
                    ""
                )
                or ""
            ).strip() or "ONE_OF"

            alternative_name = (
                best_alternative.get(
                    "name",
                    ""
                )
            )

            display_name = (
                f"{group_name}: {alternative_name}"
                if alternative_name
                else group_name
            )

            group_mandatory = bool(
                getattr(
                    group,
                    "mandatory",
                    True
                )
            )

            if group_mandatory:

                bucket = "mandatory"
                weight = 3.0
                contributes_to_core = True

            else:

                bucket = "nice_to_have"
                weight = 1.0
                contributes_to_core = False

            classify_result(
                display_name,
                bucket,
                best_score
            )

            if contributes_to_core:

                core_maximum_score += weight

                core_achieved_score += (
                    weight * best_score
                )

        # =================================================
        # LEGACY FALLBACK
        # =================================================

        if not atomic_requirements:

            mandatory = (
                getattr(
                    requirements,
                    "mandatory",
                    []
                )
                or []
            )

            nice_to_have = (
                getattr(
                    requirements,
                    "nice_to_have",
                    []
                )
                or []
            )

            technologies = (
                getattr(
                    requirements,
                    "technologies",
                    []
                )
                or []
            )

            mandatory_keys = {
                str(item).strip().casefold()
                for item in mandatory
                if str(item).strip()
            }

            nice_keys = {
                str(item).strip().casefold()
                for item in nice_to_have
                if str(item).strip()
            }

            for name in mandatory:

                score_requirement(
                    name,
                    "mandatory",
                    3.0,
                    True
                )

            for name in nice_to_have:

                score_requirement(
                    name,
                    "nice_to_have",
                    1.0,
                    False
                )

            for name in technologies:

                clean_name = str(
                    name or ""
                ).strip()

                if not clean_name:
                    continue

                key = clean_name.casefold()

                if (
                    key in mandatory_keys
                    or key in nice_keys
                ):
                    continue

                score_requirement(
                    clean_name,
                    "unclassified",
                    2.0,
                    True
                )

        for bucket in matched:

            matched[bucket] = sorted(
                matched[bucket]
            )

        for bucket in missing:

            missing[bucket] = sorted(
                missing[bucket]
            )

        if core_maximum_score <= 0:

            technical_fit = 0

        else:

            technical_fit = round(
                (
                    core_achieved_score
                    / core_maximum_score
                )
                * 100
            )

        return (
            technical_fit,
            matched,
            missing
        )

    # =====================================================
    # TECHNICAL APPLICABILITY
    # =====================================================

    def _technical_is_required(
        self,
        mission
    ):

        demand_profile = getattr(
            mission,
            "demand_profile",
            None
        )

        if demand_profile is None:
            return False

        requirements = getattr(
            demand_profile,
            "technical_requirements",
            None
        )

        if requirements is None:
            return False

        atomic_requirements = getattr(
            requirements,
            "atomic_requirements",
            []
        ) or []

        for requirement in atomic_requirements:

            importance = str(
                getattr(
                    requirement,
                    "importance",
                    ""
                )
                or ""
            ).strip().casefold()

            if importance not in {
                "nice_to_have",
                "nice-to-have",
                "nice to have",
                "optional",
                "preferred"
            }:
                return True

        groups = getattr(
            requirements,
            "requirement_groups",
            []
        ) or []

        for group in groups:

            if bool(
                getattr(
                    group,
                    "mandatory",
                    True
                )
            ):
                return True

        mandatory = getattr(
            requirements,
            "mandatory",
            []
        ) or []

        if mandatory:
            return True

        technologies = getattr(
            requirements,
            "technologies",
            []
        ) or []

        nice_to_have = {
            str(item).strip().casefold()
            for item in (
                getattr(
                    requirements,
                    "nice_to_have",
                    []
                )
                or []
            )
            if str(item).strip()
        }

        for technology in technologies:

            clean_name = str(
                technology or ""
            ).strip()

            if (
                clean_name
                and clean_name.casefold()
                not in nice_to_have
            ):
                return True

        return False

    # =====================================================
    # EXPERIENCE FIT
    # =====================================================

    def _calculate_experience_fit(
        self,
        mission
    ):

        demand_profile = getattr(
            mission,
            "demand_profile",
            None
        )

        context = getattr(
            mission,
            "context",
            None
        )

        if not demand_profile or not context:

            return (
                0,
                {
                    "total_months": 0,
                    "total_years": 0.0,
                    "experience_count": 0,
                    "valid_periods": 0,
                    "merged_periods": 0,
                },
                None
            )

        historico = getattr(
            context,
            "historico_profissional",
            []
        ) or []

        experience_intelligence = (
            self.experience_engine.analyze(
                historico
            )
        )

        requirements = getattr(
            demand_profile,
            "technical_requirements",
            None
        )

        minimum_years = (
            getattr(
                requirements,
                "minimum_years_experience",
                None
            )
            if requirements is not None
            else None
        )

        if minimum_years is None:

            return (
                0,
                experience_intelligence,
                None
            )

        if minimum_years <= 0:

            return (
                100,
                experience_intelligence,
                minimum_years
            )

        candidate_years = (
            experience_intelligence.get(
                "total_years",
                0.0
            )
        )

        experience_fit = round(
            min(
                (
                    candidate_years
                    / minimum_years
                )
                * 100,
                100
            )
        )

        return (
            experience_fit,
            experience_intelligence,
            minimum_years
        )

    # =====================================================
    # SENIORITY FIT
    # =====================================================

    def _calculate_seniority_fit(
        self,
        mission,
        evidence_set
    ):
        """
        Calculates Seniority Fit from the semantic evidence
        produced for demand_profile.job_info.seniority.

        Seniority remains qualitative.

        No fixed years-of-experience mapping is invented.
        """

        demand_profile = getattr(
            mission,
            "demand_profile",
            None
        )

        if demand_profile is None:
            return 0.0, False, None

        job_info = getattr(
            demand_profile,
            "job_info",
            None
        )

        if job_info is None:
            return 0.0, False, None

        required_seniority = str(
            getattr(
                job_info,
                "seniority",
                ""
            )
            or ""
        ).strip()

        if not required_seniority:
            return 0.0, False, None

        semantic_evidences = (
            getattr(
                evidence_set,
                "semantic_evidences",
                []
            )
            or []
        )

        validation_scores = {
            "SUPPORTED": 100.0,
            "PARTIALLY_SUPPORTED": 50.0,
            "NOT_SUPPORTED": 0.0
        }

        validation_rank = {
            "SUPPORTED": 3,
            "PARTIALLY_SUPPORTED": 2,
            "NOT_SUPPORTED": 1
        }

        best_validation = "NOT_SUPPORTED"
        best_semantic = None

        for semantic in semantic_evidences:

            if not isinstance(semantic, dict):
                continue

            category = str(
                semantic.get(
                    "category",
                    ""
                )
            ).strip().casefold()

            if category != "seniority":
                continue

            validation = str(
                semantic.get(
                    "validation",
                    "NOT_SUPPORTED"
                )
            ).strip().upper()

            if validation not in validation_scores:
                validation = "NOT_SUPPORTED"

            if (
                best_semantic is None
                or validation_rank[validation]
                > validation_rank[best_validation]
            ):

                best_validation = validation
                best_semantic = semantic

        seniority_fit = (
            validation_scores[
                best_validation
            ]
        )

        return (
            seniority_fit,
            True,
            {
                "required_seniority": required_seniority,
                "validation": best_validation,
                "semantic": best_semantic
            }
        )

    # =====================================================
    # BUSINESS FIT
    # =====================================================

    def _calculate_business_fit(
        self,
        mission,
        evidence_set
    ):

        demand_profile = getattr(
            mission,
            "demand_profile",
            None
        )

        if not demand_profile:

            return (
                0.0,
                BusinessFitStatus.NOT_APPLICABLE,
                None,
                []
            )

        business_context = getattr(
            demand_profile,
            "business_context",
            None
        )

        if not business_context:

            return (
                0.0,
                BusinessFitStatus.NOT_APPLICABLE,
                None,
                []
            )

        demand_industry = getattr(
            business_context,
            "industry",
            ""
        )

        if not demand_industry:

            return (
                0.0,
                BusinessFitStatus.NOT_APPLICABLE,
                None,
                []
            )

        demand_industry = (
            KnowledgeManager.normalize_industry(
                demand_industry
            )
        )

        business_evidences = evidence_set.by_type(
            EvidenceType.BUSINESS
        )

        candidate_industries = []

        for evidence in business_evidences:

            value = evidence.value

            if not isinstance(value, dict):
                continue

            industry = value.get(
                "industry"
            )

            if not industry:
                continue

            normalized_industry = (
                KnowledgeManager.normalize_industry(
                    industry
                )
            )

            if normalized_industry:
                candidate_industries.append(
                    normalized_industry
                )

        candidate_industries = sorted(
            set(candidate_industries)
        )

        if not candidate_industries:

            return (
                0.0,
                BusinessFitStatus.NO_EVIDENCE,
                demand_industry,
                []
            )

        best_relationship = 0.0

        for candidate_industry in candidate_industries:

            relationship = (
                KnowledgeManager.get_industry_relationship(
                    demand_industry,
                    candidate_industry
                )
            )

            if relationship > best_relationship:
                best_relationship = relationship

        if best_relationship >= 1.0:

            business_fit = 100.0
            business_status = BusinessFitStatus.DIRECT

        elif best_relationship >= 0.75:

            business_fit = 80.0
            business_status = (
                BusinessFitStatus.RELATED_STRONG
            )

        elif best_relationship >= 0.50:

            business_fit = 60.0
            business_status = (
                BusinessFitStatus.RELATED_MODERATE
            )

        else:

            business_fit = 0.0
            business_status = (
                BusinessFitStatus.UNRELATED
            )

        return (
            business_fit,
            business_status,
            demand_industry,
            candidate_industries
        )

    # =====================================================
    # LANGUAGE FIT
    # =====================================================

    def _normalize_language_level(
        self,
        level
    ):

        if level is None:
            return None

        normalized = str(
            level
        ).strip().casefold()

        if not normalized:
            return None

        level_aliases = {
            "a1": 1,
            "beginner": 1,
            "basic": 1,
            "básico": 1,
            "basico": 1,
            "a2": 2,
            "elementary": 2,
            "pre-intermediate": 2,
            "b1": 3,
            "intermediate": 3,
            "intermediário": 3,
            "intermediario": 3,
            "b2": 4,
            "upper-intermediate": 4,
            "upper intermediate": 4,
            "c1": 5,
            "advanced": 5,
            "avançado": 5,
            "avancado": 5,
            "c2": 6,
            "fluent": 6,
            "fluente": 6,
            "proficient": 6,
            "native": 7,
            "nativo": 7,
            "native speaker": 7
        }

        return level_aliases.get(
            normalized
        )

    def _parse_language_requirement(
        self,
        language_requirement
    ):

        if language_requirement is None:
            return None, None

        if isinstance(
            language_requirement,
            dict
        ):

            language_name = str(
                language_requirement.get(
                    "language",
                    language_requirement.get(
                        "name",
                        ""
                    )
                )
                or ""
            ).strip()

            required_level = str(
                language_requirement.get(
                    "level",
                    language_requirement.get(
                        "proficiency",
                        ""
                    )
                )
                or ""
            ).strip()

            return (
                language_name or None,
                required_level or None
            )

        language_name = getattr(
            language_requirement,
            "language",
            None
        )

        if language_name is None:

            language_name = getattr(
                language_requirement,
                "name",
                None
            )

        if language_name is not None:

            required_level = getattr(
                language_requirement,
                "level",
                None
            )

            if required_level is None:

                required_level = getattr(
                    language_requirement,
                    "proficiency",
                    None
                )

            return (
                str(language_name).strip() or None,
                (
                    str(required_level).strip() or None
                    if required_level is not None
                    else None
                )
            )

        parts = str(
            language_requirement
        ).split(
            ":",
            1
        )

        language_name = parts[0].strip()

        required_level = None

        if len(parts) > 1:

            required_level = (
                parts[1].strip()
                or None
            )

        return (
            language_name or None,
            required_level
        )

    def _candidate_language_index(
        self,
        evidence_set
    ):

        language_evidences = evidence_set.by_type(
            EvidenceType.LANGUAGE
        )

        candidate_languages = {}

        for evidence in language_evidences:

            language_name = str(
                getattr(
                    evidence,
                    "title",
                    ""
                )
                or ""
            ).strip()

            if not language_name:
                continue

            value = getattr(
                evidence,
                "value",
                None
            )

            candidate_level = None

            if isinstance(value, dict):

                candidate_level = (
                    value.get("level")
                    or value.get("proficiency")
                )

            key = language_name.casefold()

            normalized_level = (
                self._normalize_language_level(
                    candidate_level
                )
            )

            existing = candidate_languages.get(
                key
            )

            if existing is None:

                candidate_languages[key] = {
                    "language": language_name,
                    "level": (
                        str(candidate_level).strip()
                        if candidate_level is not None
                        else None
                    ),
                    "normalized_level": normalized_level
                }

                continue

            existing_score = existing.get(
                "normalized_level"
            )

            if (
                normalized_level is not None
                and (
                    existing_score is None
                    or normalized_level > existing_score
                )
            ):

                candidate_languages[key] = {
                    "language": language_name,
                    "level": (
                        str(candidate_level).strip()
                        if candidate_level is not None
                        else None
                    ),
                    "normalized_level": normalized_level
                }

        return candidate_languages

    def _calculate_language_fit(
        self,
        mission,
        evidence_set
    ):

        demand_profile = getattr(
            mission,
            "demand_profile",
            None
        )

        if demand_profile is None:
            return 0.0, False, []

        technical_requirements = getattr(
            demand_profile,
            "technical_requirements",
            None
        )

        if technical_requirements is None:
            return 0.0, False, []

        demand_languages = getattr(
            technical_requirements,
            "languages",
            []
        ) or []

        parsed_requirements = []

        for language_requirement in demand_languages:

            (
                language_name,
                required_level
            ) = self._parse_language_requirement(
                language_requirement
            )

            if not language_name:
                continue

            parsed_requirements.append(
                {
                    "language": language_name,
                    "required_level": required_level
                }
            )

        if not parsed_requirements:
            return 0.0, False, []

        candidate_languages = (
            self._candidate_language_index(
                evidence_set
            )
        )

        language_scores = []
        language_details = []

        for requirement in parsed_requirements:

            language_name = requirement[
                "language"
            ]

            required_level = requirement[
                "required_level"
            ]

            candidate = candidate_languages.get(
                language_name.casefold()
            )

            if candidate is None:

                score = 0.0
                status = "NOT_EVIDENCED"
                candidate_level = None

            else:

                candidate_level = candidate.get(
                    "level"
                )

                if not required_level:

                    score = 100.0
                    status = "SUPPORTED"

                else:

                    required_score = (
                        self._normalize_language_level(
                            required_level
                        )
                    )

                    candidate_score = candidate.get(
                        "normalized_level"
                    )

                    if required_score is None:

                        score = 0.0
                        status = (
                            "REQUIREMENT_LEVEL_UNRESOLVED"
                        )

                    elif candidate_score is None:

                        score = 0.0
                        status = (
                            "CANDIDATE_LEVEL_NOT_EVIDENCED"
                        )

                    elif candidate_score >= required_score:

                        score = 100.0
                        status = "SUPPORTED"

                    else:

                        score = round(
                            (
                                candidate_score
                                / required_score
                            )
                            * 100,
                            2
                        )

                        status = (
                            "BELOW_REQUIRED_LEVEL"
                        )

            language_scores.append(
                score
            )

            language_details.append(
                {
                    "language": language_name,
                    "required_level": required_level,
                    "candidate_level": candidate_level,
                    "score": score,
                    "status": status
                }
            )

        language_fit = round(
            sum(language_scores)
            / len(language_scores),
            2
        )

        return (
            language_fit,
            True,
            language_details
        )

    # =====================================================
    # OVERALL MATCH
    # =====================================================

    def _calculate_overall_match(
        self,
        technical_fit,
        technical_required,
        experience_fit,
        minimum_years,
        seniority_fit,
        seniority_required,
        language_fit,
        language_required,
        business_fit,
        business_status
    ):

        dimensions = []

        if technical_required:

            dimensions.append(
                (technical_fit, 0.60)
            )

        if minimum_years is not None:

            dimensions.append(
                (experience_fit, 0.25)
            )

        if seniority_required:

            dimensions.append(
                (seniority_fit, 0.20)
            )

        if language_required:

            dimensions.append(
                (language_fit, 0.15)
            )

        business_applicable = (
            business_status
            not in {
                BusinessFitStatus.NOT_APPLICABLE,
                BusinessFitStatus.NO_EVIDENCE
            }
        )

        if business_applicable:

            dimensions.append(
                (business_fit, 0.15)
            )

        if not dimensions:
            return 0.0

        total_weight = sum(
            weight
            for _, weight in dimensions
        )

        if total_weight <= 0:
            return 0.0

        weighted_score = sum(
            score * weight
            for score, weight in dimensions
        )

        return round(
            weighted_score
            / total_weight
        )

    # =====================================================
    # MAIN ANALYSIS
    # =====================================================

    def analyze(
        self,
        mission,
        evidence_set
    ) -> MatchResult:

        print()
        print(
            "TALIA - TALENT INTELLIGENCE ANALYST"
        )
        print()

        result = MatchResult()

        # =================================================
        # TECHNICAL
        # =================================================

        technical_fit, matched, missing = (
            self._calculate_technical_fit(
                mission,
                evidence_set
            )
        )

        technical_required = (
            self._technical_is_required(
                mission
            )
        )

        # =================================================
        # EXPERIENCE
        # =================================================

        (
            experience_fit,
            experience_intelligence,
            minimum_years
        ) = self._calculate_experience_fit(
            mission
        )

        # =================================================
        # SENIORITY
        # =================================================

        (
            seniority_fit,
            seniority_required,
            seniority_detail
        ) = self._calculate_seniority_fit(
            mission,
            evidence_set
        )

        # =================================================
        # LANGUAGE
        # =================================================

        (
            language_fit,
            language_required,
            language_details
        ) = self._calculate_language_fit(
            mission,
            evidence_set
        )

        # =================================================
        # BUSINESS
        # =================================================

        (
            business_fit,
            business_status,
            demand_industry,
            candidate_industries
        ) = self._calculate_business_fit(
            mission,
            evidence_set
        )

        # =================================================
        # LANGUAGE EXPLAINABILITY
        # =================================================

        for language_detail in language_details:

            language_name = language_detail.get(
                "language"
            )

            required_level = language_detail.get(
                "required_level"
            )

            candidate_level = language_detail.get(
                "candidate_level"
            )

            status = language_detail.get(
                "status"
            )

            if required_level:

                result.evidences.append(
                    f"Required {language_name} proficiency: "
                    f"{required_level}"
                )

            else:

                result.evidences.append(
                    f"{language_name} is explicitly required "
                    f"by the demand."
                )

            if status == "NOT_EVIDENCED":

                result.gaps.append(
                    f"No direct evidence of {language_name} "
                    f"proficiency was found."
                )

            elif status == (
                "CANDIDATE_LEVEL_NOT_EVIDENCED"
            ):

                result.gaps.append(
                    f"{language_name} was identified, but "
                    f"no proficiency level was evidenced."
                )

            elif status == (
                "REQUIREMENT_LEVEL_UNRESOLVED"
            ):

                result.risks.append(
                    f"The required proficiency level for "
                    f"{language_name} could not be safely "
                    f"normalized."
                )

            elif status == "BELOW_REQUIRED_LEVEL":

                result.evidences.append(
                    f"Candidate {language_name} proficiency: "
                    f"{candidate_level}"
                )

                result.gaps.append(
                    f"Candidate {language_name} proficiency "
                    f"is below the demand requirement."
                )

            elif status == "SUPPORTED":

                if candidate_level:

                    result.evidences.append(
                        f"Candidate {language_name} proficiency: "
                        f"{candidate_level}"
                    )

                result.strengths.append(
                    f"Candidate {language_name} proficiency "
                    f"meets the demand requirement."
                )

        # =================================================
        # CORE TECHNICAL EXPLAINABILITY
        # =================================================

        for technology in matched["mandatory"]:

            result.strengths.append(
                f"Mandatory requirement matched: {technology}"
            )

            result.evidences.append(
                f"Candidate evidence supports mandatory "
                f"requirement: {technology}"
            )

        for technology in missing["mandatory"]:

            result.gaps.append(
                f"No direct evidence found for mandatory "
                f"requirement: {technology}"
            )

        for technology in matched["unclassified"]:

            result.strengths.append(
                f"Technical requirement matched: {technology}"
            )

            result.evidences.append(
                f"Candidate evidence supports: {technology}"
            )

        for technology in missing["unclassified"]:

            result.gaps.append(
                f"No direct evidence found for technical "
                f"requirement: {technology}"
            )

        # =================================================
        # DIFFERENTIAL EXPLAINABILITY
        # =================================================
        #
        # Missing differentials are deliberately NOT gaps.
        # =================================================

        for technology in matched["nice_to_have"]:

            result.strengths.append(
                f"Differential matched: {technology}"
            )

            result.evidences.append(
                f"Candidate evidence supports differential: "
                f"{technology}"
            )

        for technology in missing["nice_to_have"]:

            result.evidences.append(
                f"Differential not evidenced in CV: "
                f"{technology}"
            )

        # =================================================
        # EXPERIENCE EXPLAINABILITY
        # =================================================

        candidate_years = (
            experience_intelligence.get(
                "total_years",
                0.0
            )
        )

        valid_periods = (
            experience_intelligence.get(
                "valid_periods",
                0
            )
        )

        if valid_periods > 0:

            result.evidences.append(
                f"Proven chronological professional "
                f"experience: {candidate_years} years"
            )

        if minimum_years is not None:

            result.evidences.append(
                f"Minimum experience required by demand: "
                f"{minimum_years} years"
            )

            if candidate_years >= minimum_years:

                result.strengths.append(
                    f"Proven professional experience meets "
                    f"the minimum requirement."
                )

            else:

                result.gaps.append(
                    f"Proven professional experience is below "
                    f"the minimum requirement."
                )

        # =================================================
        # SENIORITY EXPLAINABILITY
        # =================================================

        if seniority_required and seniority_detail:

            required_seniority = (
                seniority_detail.get(
                    "required_seniority"
                )
            )

            validation = seniority_detail.get(
                "validation"
            )

            result.evidences.append(
                f"Required seniority: {required_seniority}"
            )

            if validation == "SUPPORTED":

                result.strengths.append(
                    f"Candidate evidence supports the required "
                    f"seniority: {required_seniority}"
                )

            elif validation == "PARTIALLY_SUPPORTED":

                result.gaps.append(
                    f"Candidate evidence only partially "
                    f"supports the required seniority: "
                    f"{required_seniority}"
                )

            else:

                result.gaps.append(
                    f"Required seniority was not sufficiently "
                    f"evidenced in the CV: "
                    f"{required_seniority}"
                )

        # =================================================
        # RESULT SCORES
        # =================================================

        result.technical_fit = technical_fit
        result.experience_fit = experience_fit
        result.seniority_fit = seniority_fit
        result.business_fit = business_fit

        # Legacy external compatibility.
        result.english_fit = language_fit

        result.matched_skills = matched
        result.missing_skills = missing

        # =================================================
        # OVERALL
        # =================================================

        result.overall_match = (
            self._calculate_overall_match(
                technical_fit,
                technical_required,
                experience_fit,
                minimum_years,
                seniority_fit,
                seniority_required,
                language_fit,
                language_required,
                business_fit,
                business_status
            )
        )

        print("=" * 60)
        print("TALIA OVERALL MATCH - REAL VALUES")
        print("=" * 60)
        print(
            "technical_fit      =",
            technical_fit
        )
        print(
            "technical_required =",
            technical_required
        )
        print(
            "experience_fit     =",
            experience_fit
        )
        print(
            "minimum_years      =",
            minimum_years
        )
        print(
            "seniority_fit      =",
            seniority_fit
        )
        print(
            "seniority_required =",
            seniority_required
        )
        print(
            "language_fit       =",
            language_fit
        )
        print(
            "language_required  =",
            language_required
        )
        print(
            "business_fit       =",
            business_fit
        )
        print(
            "business_status    =",
            business_status
        )
        print(
            "overall_match      =",
            result.overall_match
        )
        print("=" * 60)

        # =================================================
        # TEMPORARY NON-SCORING DIMENSIONS
        # =================================================
        #
        # These fields remain for MatchResult compatibility.
        # They do NOT participate in Overall Match.
        # =================================================

        result.communication_fit = 85
        result.leadership_fit = 90
        result.confidence = 95

        result.executive_summary = (
            "Candidate adherence was evaluated from "
            "validated demand and resume evidence."
        )

        # =================================================
        # BUSINESS EXPLAINABILITY
        # =================================================

        if demand_industry:

            result.evidences.append(
                f"Demand industry identified: "
                f"{demand_industry}"
            )

            result.evidences.append(
                f"Business fit status: "
                f"{business_status.value}"
            )

            if candidate_industries:

                result.evidences.append(
                    f"Candidate industry evidence: "
                    f"{', '.join(candidate_industries)}"
                )

                best_relationship = 0.0
                best_candidate_industry = None

                for candidate_industry in candidate_industries:

                    relationship = (
                        KnowledgeManager
                        .get_industry_relationship(
                            demand_industry,
                            candidate_industry
                        )
                    )

                    result.evidences.append(
                        f"Industry relationship: "
                        f"{demand_industry} -> "
                        f"{candidate_industry} = "
                        f"{relationship:.2f}"
                    )

                    if relationship > best_relationship:

                        best_relationship = relationship
                        best_candidate_industry = (
                            candidate_industry
                        )

                if business_fit >= 100:

                    result.strengths.append(
                        f"Candidate has direct industry "
                        f"experience in {demand_industry}."
                    )

                elif business_fit >= 80:

                    result.strengths.append(
                        f"Candidate has strongly related "
                        f"industry experience in "
                        f"{best_candidate_industry}."
                    )

                elif business_fit >= 60:

                    result.strengths.append(
                        f"Candidate has moderately related "
                        f"industry experience in "
                        f"{best_candidate_industry}."
                    )

                else:

                    result.gaps.append(
                        f"No relevant industry relationship "
                        f"was identified between candidate "
                        f"experience and demand industry: "
                        f"{demand_industry}."
                    )

            else:

                # NO_EVIDENCE does not affect Overall Match.
                result.evidences.append(
                    f"No direct candidate industry evidence "
                    f"was found for: {demand_industry}."
                )

        return result