"""
=====================================================

TalentAI OS

Oracle Official Knowledge

Official Oracle technologies, modules,
localizations and technical capabilities
recognized by TALIA.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

from app.intelligence.domain.technology import Technology


# =====================================================
# ORACLE TECHNOLOGIES
# =====================================================

ORACLE_TECHNOLOGIES = {

    # =================================================
    # ORACLE EBS / PLATFORM
    # =================================================

    "Oracle E-Business Suite": Technology(
        name="Oracle E-Business Suite",
        vendor="Oracle",
        category="ERP",
        aliases=[
            "oracle e-business suite",
            "oracle e business suite",
            "oracle ebs",
            "ebs"
        ]
    ),

    "Oracle EBS R12": Technology(
        name="Oracle EBS R12",
        vendor="Oracle",
        category="ERP",
        aliases=[
            "oracle ebs r12",
            "ebs r12",
            "oracle r12",
            "r12.1.3",
            "r12.2",
            "r12.2.x"
        ]
    ),

    # =================================================
    # FINANCIALS
    # =================================================

    "Oracle Receivables": Technology(
        name="Oracle Receivables",
        vendor="Oracle",
        category="Oracle EBS Module",
        aliases=[
            "oracle receivables",
            "accounts receivable",
            "receivables",
            "ar"
        ]
    ),

    "Oracle Payables": Technology(
        name="Oracle Payables",
        vendor="Oracle",
        category="Oracle EBS Module",
        aliases=[
            "oracle payables",
            "accounts payable",
            "payables",
            "ap"
        ]
    ),

    # =================================================
    # ORDER MANAGEMENT
    # =================================================

    "Oracle Order Management": Technology(
        name="Oracle Order Management",
        vendor="Oracle",
        category="Oracle EBS Module",
        aliases=[
            "oracle order management",
            "order management",
            "om"
        ]
    ),

    # =================================================
    # BILLING
    # =================================================

    "Oracle Billing": Technology(
        name="Oracle Billing",
        vendor="Oracle",
        category="Oracle EBS Capability",
        aliases=[
            "oracle billing",
            "billing",
            "faturamento"
        ]
    ),

    # =================================================
    # TAX
    # =================================================

    "Oracle E-Business Tax": Technology(
        name="Oracle E-Business Tax",
        vendor="Oracle",
        category="Oracle Tax",
        aliases=[
            "oracle e-business tax",
            "oracle e business tax",
            "e-business tax",
            "e business tax",
            "ebtax"
        ]
    ),

    "Oracle Latin Tax Engine": Technology(
        name="Oracle Latin Tax Engine",
        vendor="Oracle",
        category="Oracle Tax",
        aliases=[
            "oracle latin tax engine",
            "latin tax engine",
            "lte"
        ]
    ),

    # =================================================
    # BRAZIL LOCALIZATION
    # =================================================

    "Oracle Brazil Localization": Technology(
        name="Oracle Brazil Localization",
        vendor="Oracle",
        category="Oracle Localization",
        aliases=[
            "oracle brazil localization",
            "brazil localization",
            "brazilian localization",
            "localização brasil",
            "localizacao brasil",
            "localização brasileira",
            "localizacao brasileira"
        ]
    ),

    # =================================================
    # RECEBIMENTO INTEGRADO
    # =================================================

    "Oracle CLL_F189": Technology(
        name="Oracle CLL_F189",
        vendor="Oracle",
        category="Oracle Brazil Localization",
        aliases=[
            "oracle cll_f189",
            "cll_f189",
            "cll f189",
            "recebimento integrado",
            "recebimento fiscal integrado",
            "ri"
        ]
    ),

    # =================================================
    # EFD LOADER
    # =================================================

    "Oracle CLL_F369": Technology(
        name="Oracle CLL_F369",
        vendor="Oracle",
        category="Oracle Brazil Localization",
        aliases=[
            "oracle cll_f369",
            "cll_f369",
            "cll f369",
            "efd loader"
        ]
    ),

    # =================================================
    # CONTROLE DE TERCEIROS
    # =================================================

    "Oracle CLL_F513": Technology(
        name="Oracle CLL_F513",
        vendor="Oracle",
        category="Oracle Brazil Localization",
        aliases=[
            "oracle cll_f513",
            "cll_f513",
            "cll f513",
            "controle de terceiros"
        ]
    ),
}