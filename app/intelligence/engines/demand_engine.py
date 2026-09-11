"""
=====================================================

TalentAI OS

Demand Engine

Purpose:
Transforms a job description into a
structured DemandProfile.

This engine is responsible for understanding
a hiring demand before any candidate analysis.

Author:
TalentAI Team

Version:
1.4

=====================================================
"""

import re

from app.intelligence.demand_profile import (
    DemandProfile,
    AtomicRequirement,
    RequirementAlternative,
    RequirementGroup
)

from app.intelligence.providers.openai_intelligence_provider import (
    OpenAIIntelligenceProvider
)

from app.intelligence.knowledge.employment_terms import (
    SENIORITY,
    WORK_MODEL,
    EMPLOYMENT_TYPE
)

from app.intelligence.knowledge.knowledge_manager import (
    KnowledgeManager
)


class DemandEngine:

    NAME = "Demand Engine"

    VERSION = "1.4"

    DESCRIPTION = (
        "Converts job descriptions into "
        "Demand Profiles."
    )

    def __init__(self):

        self.knowledge = KnowledgeManager()

        self.intelligence_provider = (
            OpenAIIntelligenceProvider()
        )

    def analyze(
        self,
        job_description: str
    ) -> DemandProfile:

        profile = DemandProfile()

        # =================================================
        # EXISTING DETERMINISTIC INTELLIGENCE
        # =================================================

        self._extract_job_information(
            profile,
            job_description
        )

        self._extract_requirements(
            profile,
            job_description
        )

        self._extract_experience_requirement(
            profile,
            job_description
        )

        self._extract_language_requirements(
            profile,
            job_description
        )

        self._extract_business_context(
            profile,
            job_description
        )

        # =================================================
        # SEMANTIC DEMAND INTELLIGENCE
        # =================================================

        semantic_analysis = {}

        try:
            semantic_analysis = (
                self.intelligence_provider.analyze_demand(
                    job_description
                )
                or {}
            )

        except Exception as error:
            print(
                "DEMAND ENGINE SEMANTIC ANALYSIS ERROR:",
                error
            )
            semantic_analysis = {}

        # =================================================
        # SEMANTIC JOB INFORMATION
        # =================================================

        semantic_job_title = (
            semantic_analysis.get("job_title")
            or ""
        )

        semantic_seniority = (
            semantic_analysis.get("seniority")
            or ""
        )

        if semantic_job_title:
            profile.job_info.title = semantic_job_title

        if semantic_seniority:
            profile.job_info.seniority = semantic_seniority

        # =================================================
        # SEMANTIC REQUIREMENTS
        # =================================================

        semantic_mandatory = (
            semantic_analysis.get("mandatory")
            or []
        )

        semantic_nice_to_have = (
            semantic_analysis.get("nice_to_have")
            or []
        )

        semantic_technologies = (
            semantic_analysis.get("technologies")
            or []
        )

        valid_mandatory = [
            item.strip()
            for item in semantic_mandatory
            if isinstance(item, str)
            and item.strip()
        ]

        valid_nice_to_have = [
            item.strip()
            for item in semantic_nice_to_have
            if isinstance(item, str)
            and item.strip()
        ]

        valid_semantic_technologies = [
            item.strip()
            for item in semantic_technologies
            if isinstance(item, str)
            and item.strip()
        ]

        if valid_mandatory:
            profile.technical_requirements.mandatory = (
                valid_mandatory
            )

        if valid_nice_to_have:
            profile.technical_requirements.nice_to_have = (
                valid_nice_to_have
            )

        existing_technologies = (
            profile.technical_requirements.technologies
        )

        profile.technical_requirements.technologies = list(
            dict.fromkeys(
                existing_technologies
                + valid_semantic_technologies
            )
        )

        # =================================================
        # ATOMIC REQUIREMENTS
        # =================================================

        atomic_requirements = []

        for requirement in valid_mandatory:
            atomic_requirements.append(
                AtomicRequirement(
                    name=requirement,
                    category="technical",
                    importance="mandatory",
                    source="semantic_demand_analysis"
                )
            )

        for requirement in valid_nice_to_have:
            atomic_requirements.append(
                AtomicRequirement(
                    name=requirement,
                    category="technical",
                    importance="nice_to_have",
                    source="semantic_demand_analysis"
                )
            )

        profile.technical_requirements.atomic_requirements = (
            atomic_requirements
        )

        # =================================================
        # REQUIREMENT GROUPS
        # =================================================
        #
        # Alternative requirements are represented as
        # logical groups instead of independent atomic
        # requirements.
        #
        # The semantic provider defines whether each group
        # is mandatory or nice-to-have.
        # =================================================

        structured_groups = []

        raw_groups = (
            semantic_analysis.get("requirement_groups")
            or []
        )

        for raw_group in raw_groups:

            if not isinstance(raw_group, dict):
                continue

            # =============================================
            # GROUP TYPE
            # =============================================

            group_type = str(
                raw_group.get("type")
                or "ONE_OF"
            ).strip().upper()

            if group_type != "ONE_OF":
                continue

            # =============================================
            # GROUP IMPORTANCE
            # =============================================

            group_importance = str(
                raw_group.get("importance")
                or "mandatory"
            ).strip().casefold()

            if group_importance in {
                "nice_to_have",
                "nice-to-have",
                "nice to have",
                "optional",
                "preferred",
                "desirable",
                "differential"
            }:
                group_importance = "nice_to_have"
                group_mandatory = False

            else:
                group_importance = "mandatory"
                group_mandatory = True

            # =============================================
            # ALTERNATIVES
            # =============================================

            raw_alternatives = (
                raw_group.get("alternatives")
                or []
            )

            alternatives = []

            for raw_alternative in raw_alternatives:

                if not isinstance(raw_alternative, dict):
                    continue

                alternative_name = str(
                    raw_alternative.get("name")
                    or ""
                ).strip()

                raw_requirements = (
                    raw_alternative.get("requirements")
                    or []
                )

                alternative_requirements = []

                for requirement in raw_requirements:

                    if not isinstance(requirement, str):
                        continue

                    clean_requirement = (
                        requirement.strip()
                    )

                    if not clean_requirement:
                        continue

                    alternative_requirements.append(
                        AtomicRequirement(
                            name=clean_requirement,
                            category="technical",
                            importance=group_importance,
                            source="semantic_requirement_group"
                        )
                    )

                if not alternative_requirements:
                    continue

                alternatives.append(
                    RequirementAlternative(
                        name=alternative_name,
                        requirements=alternative_requirements
                    )
                )

            if not alternatives:
                continue

            # =============================================
            # STRUCTURED GROUP
            # =============================================

            structured_groups.append(
                RequirementGroup(
                    name="Alternative Requirement Group",
                    group_type=group_type,
                    alternatives=alternatives,
                    mandatory=group_mandatory
                )
            )

        # =================================================
        # REMOVE DUPLICATE ATOMIC REQUIREMENTS
        # =================================================
        #
        # A requirement represented inside an alternative
        # group must not also be evaluated independently.
        #
        # This protects TALIA against double counting when
        # semantic extraction accidentally returns the same
        # requirement both as an atomic requirement and as
        # part of a ONE_OF group.
        # =================================================

        grouped_requirement_names = set()

        for group in structured_groups:

            for alternative in group.alternatives:

                for requirement in alternative.requirements:

                    normalized_name = (
                        requirement.name
                        .strip()
                        .casefold()
                    )

                    if normalized_name:
                        grouped_requirement_names.add(
                            normalized_name
                        )

        if grouped_requirement_names:

            atomic_requirements = [
                requirement
                for requirement in atomic_requirements
                if (
                    requirement.name
                    .strip()
                    .casefold()
                    not in grouped_requirement_names
                )
            ]

            profile.technical_requirements.atomic_requirements = (
                atomic_requirements
            )    

        profile.technical_requirements.requirement_groups = (
            structured_groups
        )
        # =================================================
        # EXPERIENCE
        # =================================================

        semantic_minimum_years = (
            semantic_analysis.get(
                "minimum_years_experience"
            )
        )

        if (
            profile.technical_requirements.minimum_years_experience
            is None
            and isinstance(
                semantic_minimum_years,
                (int, float)
            )
        ):
            profile.technical_requirements.minimum_years_experience = (
                float(semantic_minimum_years)
            )

                # =================================================
        # LANGUAGES
        # =================================================
        #
        # Semantic demand analysis is authoritative for
        # language requirements.
        #
        # The deterministic extractor may identify any
        # language mentioned anywhere in the demand text,
        # including optional / nice-to-have sections.
        #
        # The semantic provider, however, understands the
        # requirement context and returns in "languages"
        # only languages that belong to actual demand
        # requirements.
        #
        # Therefore semantic languages replace, rather than
        # merge with, the deterministic language list.
        # =================================================

        semantic_languages = (
            semantic_analysis.get("languages")
            or []
        )

        profile.technical_requirements.languages = (
            self._normalize_semantic_languages(
                semantic_languages
            )
        )

        # =================================================
        # BUSINESS CONTEXT
        # =================================================

        semantic_business_context = (
            semantic_analysis.get("business_context")
            or {}
        )

        if isinstance(semantic_business_context, dict):

            semantic_industry = (
                semantic_business_context.get("industry")
                or ""
            )

            semantic_project_type = (
                semantic_business_context.get("project_type")
                or ""
            )

            semantic_business_problem = (
                semantic_business_context.get(
                    "business_problem"
                )
                or ""
            )

            if (
                not profile.business_context.industry
                and semantic_industry
            ):
                profile.business_context.industry = (
                    semantic_industry
                )

            if semantic_project_type:
                profile.business_context.project_type = (
                    semantic_project_type
                )

            if semantic_business_problem:
                profile.business_context.business_problem = (
                    semantic_business_problem
                )

        # =================================================
        # AI ANALYSIS METADATA
        # =================================================

        missing_information = (
            semantic_analysis.get("missing_information")
            or []
        )

        profile.ai_analysis.missing_information = [
            item
            for item in missing_information
            if isinstance(item, str)
        ]

        # =================================================
        # EXECUTIVE SUMMARY
        # =================================================

        self._generate_summary(
            profile
        )

        return profile
   
    # =====================================================
    # PRIVATE METHODS
    # =====================================================

    def _extract_job_information(
        self,
        profile: DemandProfile,
        text: str
    ):
        """
        Extracts basic job information from the
        job description.

        Uses the TalentAI Knowledge Base.
        """

        lower_text = text.lower()

        # -------------------------------------------------
        # Seniority
        # -------------------------------------------------

        for level, keywords in SENIORITY.items():

            if any(
                keyword in lower_text
                for keyword in keywords
            ):

                profile.job_info.seniority = level
                break

        # -------------------------------------------------
        # Work Model
        # -------------------------------------------------

        for model, keywords in WORK_MODEL.items():

            if any(
                keyword in lower_text
                for keyword in keywords
            ):

                profile.job_info.work_model = model
                break

        # -------------------------------------------------
        # Employment Type
        # -------------------------------------------------

        for employment, keywords in EMPLOYMENT_TYPE.items():

            if any(
                keyword in lower_text
                for keyword in keywords
            ):

                profile.job_info.employment_type = employment
                break

        # -------------------------------------------------
        # Job Title
        # -------------------------------------------------

        for line in text.splitlines():

            line = line.strip()

            if len(line) > 5:

                profile.job_info.title = line
                break

    # =====================================================
    # REQUIREMENTS
    # =====================================================

    def _extract_requirements(
        self,
        profile: DemandProfile,
        text: str
    ):
        """
        Extracts technical requirements from the
        job description.

        Identifies:

        - All technologies
        - Explicit mandatory requirements
        - Explicit nice-to-have requirements

        TALIA does not assume that a technology
        is mandatory unless the job description
        explicitly indicates it.
        """

        technologies = self.knowledge.find_technologies(
            text
        )

        # =================================================
        # ALL IDENTIFIED TECHNOLOGIES
        # =================================================

        profile.technical_requirements.technologies = [

            technology.name

            for technology in technologies
        ]

        # =================================================
        # CLASSIFICATION MARKERS
        # =================================================

        mandatory_markers = (

            "mandatory",
            "required",
            "must have",
            "must-have",

            "obrigatório",
            "obrigatória",
            "obrigatorio",
            "obrigatoria",
            "requisito obrigatório",
            "requisito obrigatória",
            "requisito obrigatorio",
            "requisito obrigatoria"

        )

        nice_to_have_markers = (

            "nice to have",
            "nice-to-have",
            "preferred",
            "desirable",

            "desejável",
            "desejáveis",
            "diferencial",
            "diferenciais",
            "preferencial"

        )

        mandatory = []

        nice_to_have = []

        # =================================================
        # SEGMENT-BY-SEGMENT CLASSIFICATION
        # =================================================
        #
        # A single line may contain multiple requirement
        # categories, for example:
        #
        # Required: C++, Linux. Nice to have: Android.
        #
        # TALIA therefore classifies each marker-delimited
        # segment independently instead of assuming that
        # one marker applies to the entire line.
        # =================================================

        all_markers = (
            mandatory_markers
            + nice_to_have_markers
        )

        marker_pattern = (
            r"("
            + "|".join(
                re.escape(marker)
                for marker in sorted(
                    all_markers,
                    key=len,
                    reverse=True
                )
            )
            + r")\s*:?"
        )

        segments = re.split(
            marker_pattern,
            text,
            flags=re.IGNORECASE
        )

        current_category = None

        for segment in segments:

            clean_segment = segment.strip()

            if not clean_segment:
                continue

            lower_segment = clean_segment.lower()

            if lower_segment in mandatory_markers:

                current_category = "mandatory"
                continue

            if lower_segment in nice_to_have_markers:

                current_category = "nice_to_have"
                continue

            if current_category is None:
                continue

            segment_technologies = (
                self.knowledge.find_technologies(
                    clean_segment
                )
            )

            names = [
                technology.name
                for technology in segment_technologies
            ]

            if current_category == "mandatory":

                mandatory.extend(
                    names
                )

            elif current_category == "nice_to_have":

                nice_to_have.extend(
                    names
                )

        # =================================================
        # REMOVE DUPLICATES
        # =================================================

        profile.technical_requirements.mandatory = sorted(
            set(mandatory)
        )

        profile.technical_requirements.nice_to_have = sorted(
            set(nice_to_have)
        )

    # =====================================================
    # EXPERIENCE REQUIREMENT
    # =====================================================

    def _extract_experience_requirement(
        self,
        profile: DemandProfile,
        text: str
    ):
        """
        Extracts minimum years of professional
        experience explicitly required by the demand.

        TALIA remains conservative:

        If the job description does not explicitly
        define a minimum experience requirement,
        the value remains None.
        """

        if not text:

            return

        patterns = [

            # -------------------------------------------------
            # English
            # -------------------------------------------------

            r"(?:minimum|min\.?|at least)\s+"
            r"(?:of\s+)?"
            r"(\d+(?:\.\d+)?)\s*\+?\s*years?",

            r"(\d+(?:\.\d+)?)\s*\+\s*years?"
            r"(?:\s+of)?\s+experience",

            r"(\d+(?:\.\d+)?)\s+years?"
            r"(?:\s+of)?\s+experience",

            # -------------------------------------------------
            # Portuguese
            # -------------------------------------------------

            r"(?:mínimo|minimo|pelo menos)\s+"
            r"(?:de\s+)?"
            r"(\d+(?:[.,]\d+)?)\s+anos?",

            r"(\d+(?:[.,]\d+)?)\s*\+\s*anos?"
            r"(?:\s+de)?\s+experiência",

            r"(\d+(?:[.,]\d+)?)\s+anos?"
            r"(?:\s+de)?\s+experiência",

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if not match:

                continue

            value = (
                match
                .group(1)
                .replace(",", ".")
            )

            try:

                years = float(
                    value
                )

            except ValueError:

                continue

            if years < 0:

                continue

            profile.technical_requirements.minimum_years_experience = (
                years
            )

            return

    # =====================================================
    # LANGUAGE REQUIREMENTS
    # =====================================================

    def _normalize_semantic_languages(
        self,
        semantic_languages
    ):
        """
        Normalizes semantic language requirements into
        the canonical DemandProfile contract.

        Examples:

        Inglês avançado
        -> English:ADVANCED

        English: Fluent
        -> English:FLUENT

        Inglês avançado + Inglês fluente
        -> English:ADVANCED

        When the semantic provider returns multiple
        acceptable proficiency levels for the same
        language, TALIA keeps the minimum explicit
        proficiency as the hiring threshold.
        """

        if not semantic_languages:
            return []

        language_aliases = {

            "English": (
                "english",
                "inglês",
                "ingles"
            ),

            "Spanish": (
                "spanish",
                "espanhol",
                "español"
            ),

            "Portuguese": (
                "portuguese",
                "português",
                "portugues"
            )
        }

        proficiency_levels = {

            "native or bilingual proficiency": "NATIVE",
            "native speaker": "NATIVE",
            "native": "NATIVE",
            "nativo": "NATIVE",
            "nativa": "NATIVE",

            "full professional proficiency": "FLUENT",
            "proficient": "FLUENT",
            "proficiente": "FLUENT",
            "fluency": "FLUENT",
            "fluent": "FLUENT",
            "fluente": "FLUENT",
            "c2": "FLUENT",

            "professional working proficiency": "ADVANCED",
            "advanced": "ADVANCED",
            "avançado": "ADVANCED",
            "avançada": "ADVANCED",
            "avancado": "ADVANCED",
            "avancada": "ADVANCED",
            "c1": "ADVANCED",

            "upper intermediate": "INTERMEDIATE",
            "upper-intermediate": "INTERMEDIATE",
            "intermediate": "INTERMEDIATE",
            "intermediário": "INTERMEDIATE",
            "intermediária": "INTERMEDIATE",
            "intermediario": "INTERMEDIATE",
            "intermediaria": "INTERMEDIATE",
            "b2": "INTERMEDIATE",
            "b1": "INTERMEDIATE",

            "pre-intermediate": "BASIC",
            "pre intermediate": "BASIC",
            "elementary": "BASIC",
            "beginner": "BASIC",
            "basic": "BASIC",
            "básico": "BASIC",
            "básica": "BASIC",
            "basico": "BASIC",
            "basica": "BASIC",
            "a2": "BASIC",
            "a1": "BASIC"
        }

        level_rank = {
            "BASIC": 1,
            "INTERMEDIATE": 2,
            "ADVANCED": 3,
            "FLUENT": 4,
            "NATIVE": 5
        }

        normalized = {}

        for raw_item in semantic_languages:

            if not isinstance(raw_item, str):
                continue

            clean_item = raw_item.strip()

            if not clean_item:
                continue

            lower_item = clean_item.casefold()

            language_name = None

            for canonical_name, aliases in (
                language_aliases.items()
            ):

                language_found = any(
                    re.search(
                        r"(?<!\w)"
                        + re.escape(alias.casefold())
                        + r"(?!\w)",
                        lower_item,
                        flags=re.IGNORECASE
                    )
                    for alias in aliases
                )

                if language_found:
                    language_name = canonical_name
                    break

            if not language_name:
                continue

            level = None

            levels = sorted(
                proficiency_levels.items(),
                key=lambda item: len(item[0]),
                reverse=True
            )

            for alias, normalized_level in levels:

                pattern = (
                    r"(?<!\w)"
                    + re.escape(alias.casefold())
                    + r"(?!\w)"
                )

                if re.search(
                    pattern,
                    lower_item,
                    flags=re.IGNORECASE
                ):
                    level = normalized_level
                    break

            existing_level = normalized.get(
                language_name
            )

            if existing_level is None:
                normalized[language_name] = level or ""
                continue

            if not level:
                continue

            if not existing_level:
                normalized[language_name] = level
                continue

            if (
                level_rank.get(level, 999)
                < level_rank.get(existing_level, 999)
            ):
                normalized[language_name] = level

        result = []

        for language_name, level in normalized.items():

            if level:
                result.append(
                    f"{language_name}:{level}"
                )
            else:
                result.append(
                    language_name
                )

        return sorted(
            set(result)
        )

    # =====================================================
    # LANGUAGE REQUIREMENTS
    # =====================================================

    def _extract_language_requirements(
        self,
        profile: DemandProfile,
        text: str
    ):
        """
        Extracts language requirements and
        proficiency levels from the demand.

        The result remains compatible with the
        current DemandProfile languages field.

        Examples:

        English Level: Fluent
        -> English:FLUENT

        Inglês: Avançado
        -> English:ADVANCED
        """

        if not text:

            return

        language_aliases = {

            "English": (
                "english",
                "inglês",
                "ingles"
            ),

            "Spanish": (
                "spanish",
                "espanhol",
                "español"
            ),

            "Portuguese": (
                "portuguese",
                "português",
                "portugues"
            )
        }

        proficiency_levels = {

            "native": "NATIVE",
            "native speaker": "NATIVE",
            "native or bilingual proficiency": "NATIVE",
            "nativo": "NATIVE",
            "nativa": "NATIVE",

            "fluent": "FLUENT",
            "fluency": "FLUENT",
            "fluente": "FLUENT",
            "full professional proficiency": "FLUENT",
            "c2": "FLUENT",

            "advanced": "ADVANCED",
            "avançado": "ADVANCED",
            "avançada": "ADVANCED",
            "professional working proficiency": "ADVANCED",
            "c1": "ADVANCED",

            "upper intermediate": "INTERMEDIATE",
            "upper-intermediate": "INTERMEDIATE",
            "intermediate": "INTERMEDIATE",
            "intermediário": "INTERMEDIATE",
            "intermediária": "INTERMEDIATE",
            "b2": "INTERMEDIATE",
            "b1": "INTERMEDIATE",

            "elementary": "BASIC",
            "beginner": "BASIC",
            "basic": "BASIC",
            "básico": "BASIC",
            "básica": "BASIC",
            "a2": "BASIC",
            "a1": "BASIC"
        }

        found_languages = []

        segments = re.split(
            r"[\n\r;,|/]+",
            text
        )

        for segment in segments:

            clean_segment = segment.strip()

            if not clean_segment:

                continue

            lower_segment = clean_segment.lower()

            for language_name, aliases in (
                language_aliases.items()
            ):

                language_found = any(

                    re.search(
                        r"(?<!\w)"
                        + re.escape(alias)
                        + r"(?!\w)",
                        lower_segment,
                        flags=re.IGNORECASE
                    )

                    for alias in aliases

                )

                if not language_found:

                    continue

                level = ""

                levels = sorted(
                    proficiency_levels.items(),
                    key=lambda item: len(item[0]),
                    reverse=True
                )

                for alias, normalized_level in levels:

                    pattern = (
                        r"(?<!\w)"
                        + re.escape(alias)
                        + r"(?!\w)"
                    )

                    if re.search(
                        pattern,
                        lower_segment,
                        flags=re.IGNORECASE
                    ):

                        level = normalized_level
                        break

                if level:

                    found_languages.append(
                        f"{language_name}:{level}"
                    )

                else:

                    found_languages.append(
                        language_name
                    )

        profile.technical_requirements.languages = sorted(
            set(found_languages)
        )

    # =====================================================
    # BUSINESS CONTEXT
    # =====================================================

    def _extract_business_context(
        self,
        profile: DemandProfile,
        text: str
    ):
        """
        Extracts business and project context.

        Future TALIA intelligence layer.
        """

        industries = self.knowledge.find_industries(
            text
        )

        if industries:

            profile.business_context.industry = industries[0]

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    def _generate_summary(
        self,
        profile: DemandProfile
    ):
        """
        Generates the executive summary
        for the demand.

        Future TALIA intelligence layer.
        """

        pass