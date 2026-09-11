"""
=====================================================

TalentAI World
Knowledge Gateway

Single access point to TalentAI Knowledge.

Responsible for retrieving information from
the knowledge layer.

Author:
TalentAI Team

=====================================================
"""


class KnowledgeGateway:

    NAME = "Knowledge Gateway"

    VERSION = "1.0"

    DESCRIPTION = "Gateway for TalentAI Knowledge"

    def __init__(self):

        pass

    def get_facts(
        self,
        facts
    ):

        return {
            "success": True,
            "knowledge": facts
        }