"""
=====================================================

TalentAI OS

Official Technology Catalog

Purpose:
Central catalog of all official technologies
recognized by TALIA.

Responsibilities

- Aggregate all technology catalogs
- Provide a single technology source
- Keep Intelligence Engines independent
- Standardize technology access

Author:
TalentAI Team

Version:
1.1

=====================================================
"""

from app.intelligence.knowledge.official.sap import (
    SAP_TECHNOLOGIES
)
from app.intelligence.knowledge.official.embedded import (
    EMBEDDED_TECHNOLOGIES
)

# Future catalogs
#
from app.intelligence.knowledge.official.oracle import ORACLE_TECHNOLOGIES
# from app.intelligence.knowledge.official.microsoft import MICROSOFT_TECHNOLOGIES
# from app.intelligence.knowledge.official.salesforce import SALESFORCE_TECHNOLOGIES
# from app.intelligence.knowledge.official.cloud import CLOUD_TECHNOLOGIES
# from app.intelligence.knowledge.official.databases import DATABASE_TECHNOLOGIES
# from app.intelligence.knowledge.official.frameworks import FRAMEWORK_TECHNOLOGIES


# =====================================================
# OFFICIAL TECHNOLOGY CATALOG
# =====================================================

OFFICIAL_TECHNOLOGIES = {}

OFFICIAL_TECHNOLOGIES.update(
    SAP_TECHNOLOGIES
)

OFFICIAL_TECHNOLOGIES.update(
    EMBEDDED_TECHNOLOGIES
)

# Future
#
OFFICIAL_TECHNOLOGIES.update(
    ORACLE_TECHNOLOGIES
)

# OFFICIAL_TECHNOLOGIES.update(MICROSOFT_TECHNOLOGIES)
# OFFICIAL_TECHNOLOGIES.update(SALESFORCE_TECHNOLOGIES)
# OFFICIAL_TECHNOLOGIES.update(CLOUD_TECHNOLOGIES)
# OFFICIAL_TECHNOLOGIES.update(DATABASE_TECHNOLOGIES)
# OFFICIAL_TECHNOLOGIES.update(FRAMEWORK_TECHNOLOGIES)