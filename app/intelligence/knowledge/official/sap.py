"""
=====================================================

TalentAI OS

SAP Official Knowledge

Official SAP technologies, modules, processes,
localizations and technical capabilities
recognized by TALIA.

Author:
TalentAI Team

Version:
2.0

=====================================================
"""

from app.intelligence.domain.technology import Technology


# =====================================================
# SAP TECHNOLOGIES
# =====================================================

SAP_TECHNOLOGIES = {

    # =================================================
    # SAP CORE / PLATFORMS
    # =================================================

    "SAP ECC": Technology(
        name="SAP ECC",
        vendor="SAP",
        category="ERP",
        aliases=[
            "sap ecc",
            "ecc"
        ]
    ),

    "SAP S/4HANA": Technology(
        name="SAP S/4HANA",
        vendor="SAP",
        category="ERP",
        aliases=[
            "sap s/4hana",
            "sap s4hana",
            "s/4hana",
            "s4hana",
            "s/4"
        ]
    ),

    # =================================================
    # SAP MODULES
    # =================================================

    "SAP SD": Technology(
        name="SAP SD",
        vendor="SAP",
        category="SAP Module",
        aliases=[
            "sap sd",
            "sd module",
            "sales and distribution"
        ]
    ),

    "SAP MM": Technology(
        name="SAP MM",
        vendor="SAP",
        category="SAP Module",
        aliases=[
            "sap mm",
            "materials management"
        ]
    ),

    "SAP FI": Technology(
        name="SAP FI",
        vendor="SAP",
        category="SAP Module",
        aliases=[
            "sap fi",
            "financial accounting"
        ]
    ),

    "SAP PP": Technology(
        name="SAP PP",
        vendor="SAP",
        category="SAP Module",
        aliases=[
            "sap pp",
            "production planning"
        ]
    ),

    # =================================================
    # SAP DEVELOPMENT
    # =================================================

    "ABAP": Technology(
        name="ABAP",
        vendor="SAP",
        category="Programming Language",
        aliases=[
            "abap",
            "sap abap"
        ]
    ),

    "SAP Fiori": Technology(
        name="SAP Fiori",
        vendor="SAP",
        category="Frontend",
        aliases=[
            "fiori",
            "sap fiori"
        ]
    ),

    # =================================================
    # ORDER TO CASH
    # =================================================

    "Order-to-Cash": Technology(
        name="Order-to-Cash",
        vendor="SAP",
        category="SAP Process",
        aliases=[
            "order to cash",
            "order-to-cash",
            "order 2 cash",
            "o2c",
            "otc"
        ]
    ),

    # =================================================
    # INTERCOMPANY
    # =================================================

    "SAP Intercompany": Technology(
        name="SAP Intercompany",
        vendor="SAP",
        category="SAP Process",
        aliases=[
            "sap intercompany",
            "intercompany",
            "inter-company",
            "intercompany sales",
            "intercompany procurement",
            "intercompany process",
            "intercompany processes"
        ]
    ),

    # =================================================
    # THIRD-PARTY SALES
    # =================================================

    "SAP Third-Party Sales": Technology(
        name="SAP Third-Party Sales",
        vendor="SAP",
        category="SAP Process",
        aliases=[
            "third party sales",
            "third-party sales",
            "third party sale",
            "third-party sale"
        ]
    ),

    # =================================================
    # PRICING
    # =================================================

    "SAP Pricing": Technology(
        name="SAP Pricing",
        vendor="SAP",
        category="SAP SD Capability",
        aliases=[
            "sap pricing",
            "pricing procedure",
            "pricing procedures",
            "pricing configuration",
            "pricing conditions"
        ]
    ),

    # =================================================
    # SAP DRC
    # =================================================

    "SAP DRC": Technology(
        name="SAP DRC",
        vendor="SAP",
        category="SAP Compliance",
        aliases=[
            "drc",
            "sap drc",
            "document and reporting compliance",
            "sap document and reporting compliance"
        ]
    ),
    # =================================================
    # ELECTRONIC INVOICING
    # =================================================

    "SAP Electronic Invoicing": Technology(
        name="SAP Electronic Invoicing",
        vendor="SAP",
        category="SAP Localization",
        aliases=[
            "sap electronic invoicing",
            "electronic invoicing",
            "electronic invoice",
            "e-invoicing",
            "e-invoice",
            "einvoicing",
            "einvoice",
            "nfe",
            "nf-e",
            "nf e"
        ]
    ),

    # =================================================
    # IDOC
    # =================================================

    "IDoc": Technology(
        name="IDoc",
        vendor="SAP",
        category="SAP Integration",
        aliases=[
            "idoc",
            "idocs",
            "intermediate document",
            "intermediate documents"
        ]
    ),

    # =================================================
    # 3PL
    # =================================================

    "3PL Integration": Technology(
        name="3PL Integration",
        vendor="SAP",
        category="SAP Integration",
        aliases=[
            "3pl",
            "3pl integration",
            "3pl integrations",
            "3pl interface",
            "3pl interfaces",
            "third party logistics",
            "third-party logistics"
        ]
    ),

    # =================================================
    # BRAZIL LOCALIZATION
    # =================================================

    "SAP Brazil Localization": Technology(
        name="SAP Brazil Localization",
        vendor="SAP",
        category="SAP Localization",
        aliases=[
            "sap brazil localization",
            "brazil localization",
            "brazilian localization",
            "localização brasil",
            "localizacao brasil"
        ]
    ),

    # =================================================
    # MEXICO LOCALIZATION
    # =================================================

    "SAP Mexico Localization": Technology(
        name="SAP Mexico Localization",
        vendor="SAP",
        category="SAP Localization",
        aliases=[
            "sap mexico localization",
            "mexico localization",
            "mexican localization",
            "localización méxico",
            "localizacion mexico"
        ]
    ),

    # =================================================
    # LATAM LOCALIZATION
    # =================================================

    "SAP LATAM Localization": Technology(
        name="SAP LATAM Localization",
        vendor="SAP",
        category="SAP Localization",
        aliases=[
            "sap latam localization",
            "latam localization",
            "latin america localization",
            "latin american localization",
            "localization latam"
        ]
    ),

}