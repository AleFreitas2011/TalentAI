"""
=====================================================

TalentAI World

Official Industries Knowledge

Defines the official industry vocabulary
recognized by TALIA.

This catalog provides normalized industry names,
aliases and semantic relationships used by
TALIA Intelligence Engines.

Author:
TalentAI Team

Version:
1.1

=====================================================
"""


# =====================================================
# OFFICIAL INDUSTRIES
# =====================================================
#
# Canonical industry vocabulary recognized by TALIA.
#
# Each official industry contains aliases that may
# appear in job descriptions, candidate profiles
# and other intelligence inputs.
# =====================================================

OFFICIAL_INDUSTRIES = {

    "Banking": [
        "bank",
        "banks",
        "banking",
        "financial institution"
    ],

    "Financial Services": [
        "financial services",
        "fintech",
        "finance"
    ],

    "Insurance": [
        "insurance",
        "insurer"
    ],

    "Healthcare": [
        "healthcare",
        "health care",
        "health"
    ],

    "Pharmaceutical": [
        "pharmaceutical",
        "pharma",
        "pharmaceuticals"
    ],

    "Retail": [
        "retail",
        "retailer"
    ],

    "Consumer Goods": [
        "consumer goods",
        "consumer products",
        "fmcg",
        "cpg"
    ],

    "Manufacturing": [
        "manufacturing",
        "manufacturer",
        "industrial manufacturing"
    ],

    "Automotive": [
        "automotive",
        "automobile",
        "automotive industry"
    ],

    "Technology": [
        "technology industry",
        "technology sector",
        "information technology industry",
        "information technology sector",
        "it services company",
        "technology company",
        "software company"
    ],

    "Telecommunications": [
        "telecommunications",
        "telecom",
        "telco"
    ],

    "Energy": [
        "energy",
        "utilities",
        "power"
    ],

    "Oil & Gas": [
        "oil and gas",
        "oil & gas",
        "o&g"
    ],

    "Logistics": [
        "logistics",
        "transportation",
        "supply chain"
    ],

    "Education": [
        "education",
        "educational",
        "edtech"
    ],

    "Government": [
        "government",
        "public sector",
        "government agency"
    ],

    "Food & Beverage": [
        "food and beverage",
        "food & beverage",
        "food industry",
        "beverage"
    ],

    "Media & Entertainment": [
        "media",
        "entertainment",
        "media and entertainment"
    ],

    "E-commerce": [
        "e-commerce",
        "ecommerce",
        "online commerce"
    ],

    "Professional Services": [
        "professional services",
        "consulting",
        "consultancy"
    ]

}


# =====================================================
# INDUSTRY RELATIONSHIPS
# =====================================================
#
# Defines semantic proximity between official
# industries recognized by TALIA.
#
# Relationships are directional.
#
# A relationship means that experience in one
# industry may provide relevant business context
# for another industry without being considered
# an exact industry match.
#
# Relationship strengths:
#
# 1.00 = exact industry match
# 0.75 = strongly related industry
# 0.50 = moderately related industry
#
# Exact matches are handled separately by TALIA
# Business Reasoning and therefore are not listed
# in this catalog.
#
# IMPORTANT:
#
# These values represent knowledge about semantic
# proximity between industries.
#
# They are NOT Business Fit scores.
#
# The Talent Intelligence reasoning layer decides
# how this knowledge affects candidate evaluation.
# =====================================================

INDUSTRY_RELATIONSHIPS = {

    "Banking": {
        "Financial Services": 0.75
    },

    "Financial Services": {
        "Banking": 0.75,
        "Insurance": 0.50
    },

    "Insurance": {
        "Financial Services": 0.50
    },

    "Pharmaceutical": {
        "Healthcare": 0.75
    },

    "Healthcare": {
        "Pharmaceutical": 0.50
    },

    "Retail": {
        "Consumer Goods": 0.50,
        "E-commerce": 0.75
    },

    "E-commerce": {
        "Retail": 0.75
    },

    "Consumer Goods": {
        "Retail": 0.50,
        "Food & Beverage": 0.50
    },

    "Food & Beverage": {
        "Consumer Goods": 0.50
    },

    "Automotive": {
        "Manufacturing": 0.75
    },

    "Manufacturing": {
        "Automotive": 0.50
    },

    "Oil & Gas": {
        "Energy": 0.75
    },

    "Energy": {
        "Oil & Gas": 0.50
    },

    "Technology": {
        "Telecommunications": 0.50
    },

    "Telecommunications": {
        "Technology": 0.50
    }

}