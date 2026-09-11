"""
Custom exceptions.
"""

class TalentAIException(Exception):
    """Base exception for TalentAI."""
    pass


class CandidateException(TalentAIException):
    pass


class RecruiterException(TalentAIException):
    pass


class PricingException(TalentAIException):
    pass