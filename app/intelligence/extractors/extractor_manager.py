"""
=====================================================

TalentAI World
Extractor Manager

Coordinates all TALIA extractors.

Author:
TalentAI Team

Version:
1.1

=====================================================
"""

from app.intelligence.extractors.skill_extractor import (
    SkillExtractor
)

from app.intelligence.extractors.language_extractor import (
    LanguageExtractor
)


class ExtractorManager:

    NAME = "Extractor Manager"

    VERSION = "1.1"

    DESCRIPTION = (
        "Coordinates TALIA extractors."
    )

    def __init__(self):

        self.skill_extractor = SkillExtractor()

        self.language_extractor = LanguageExtractor()

        #
        # Future extractors
        #

        # self.certification_extractor = CertificationExtractor()
        # self.education_extractor = EducationExtractor()
        # self.softskill_extractor = SoftSkillExtractor()

    def skills(
        self,
        context
    ):

        return self.skill_extractor.extract(
            context
        )

    def languages(
        self,
        context
    ):

        return self.language_extractor.extract(
            context
        )

    #
    # Future methods
    #

    # def certifications(self, context):
    #     return self.certification_extractor.extract(context)

    # def education(self, context):
    #     return self.education_extractor.extract(context)

    # def soft_skills(self, context):
    #     return self.softskill_extractor.extract(context)