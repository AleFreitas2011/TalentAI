"""
=====================================================

TalentAI World

Experience Engine

Transforms structured professional history into
reliable experience intelligence.

Responsibilities

- Normalize professional experience dates
- Build professional timeline intervals
- Merge overlapping employment periods
- Calculate proven chronological experience
- Preserve conservative evidence principles

This engine does NOT calculate candidate-job fit.
Candidate-job comparison belongs to the
Talent Intelligence Analyst.

Author:
TalentAI Team

Version:
1.0

=====================================================
"""

import re

from datetime import datetime


class ExperienceEngine:

    NAME = "Experience Engine"

    VERSION = "1.0"

    DESCRIPTION = (
        "Calculates reliable professional experience "
        "from structured candidate history."
    )

    # =====================================================
    # MONTH MAP
    # =====================================================

    MONTHS = {
        # English
        "jan": 1,
        "january": 1,
        "feb": 2,
        "february": 2,
        "mar": 3,
        "march": 3,
        "apr": 4,
        "april": 4,
        "may": 5,
        "jun": 6,
        "june": 6,
        "jul": 7,
        "july": 7,
        "aug": 8,
        "august": 8,
        "sep": 9,
        "sept": 9,
        "september": 9,
        "oct": 10,
        "october": 10,
        "nov": 11,
        "november": 11,
        "dec": 12,
        "december": 12,

        # Portuguese
        "jan.": 1,
        "janeiro": 1,
        "fev": 2,
        "fev.": 2,
        "fevereiro": 2,
        "mar.": 3,
        "março": 3,
        "marco": 3,
        "abr": 4,
        "abr.": 4,
        "abril": 4,
        "mai": 5,
        "mai.": 5,
        "maio": 5,
        "jun.": 6,
        "junho": 6,
        "jul.": 7,
        "julho": 7,
        "ago": 8,
        "ago.": 8,
        "agosto": 8,
        "set": 9,
        "set.": 9,
        "setembro": 9,
        "out": 10,
        "out.": 10,
        "outubro": 10,
        "nov.": 11,
        "novembro": 11,
        "dez": 12,
        "dez.": 12,
        "dezembro": 12,
    }

    PRESENT_TERMS = {
        "present",
        "current",
        "currently",
        "presente",
        "atual",
        "até o momento",
        "ate o momento",
    }

    # =====================================================
    # DATE NORMALIZATION
    # =====================================================

    def _parse_date(
        self,
        value: str,
        is_end: bool = False
    ):
        """
        Converts a resume date into a (year, month) tuple.

        Supported examples:

        January 2022
        Jan 2022
        03/2019
        2019
        Present
        Atual

        Year-only dates are treated conservatively:

        start year -> January
        end year   -> December
        """

        if not value:
            return None

        normalized = (
            value
            .strip()
            .lower()
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized
        )

        # =================================================
        # PRESENT
        # =================================================

        if normalized in self.PRESENT_TERMS:

            now = datetime.now()

            return (
                now.year,
                now.month
            )

        # =================================================
        # MM/YYYY
        # =================================================

        numeric_match = re.fullmatch(
            r"(\d{1,2})[/-](\d{4})",
            normalized
        )

        if numeric_match:

            month = int(
                numeric_match.group(1)
            )

            year = int(
                numeric_match.group(2)
            )

            if 1 <= month <= 12:

                return (
                    year,
                    month
                )

            return None

        # =================================================
        # MONTH + YEAR
        # =================================================

        month_year_match = re.fullmatch(
            r"([a-záàâãéêíóôõúç.]+)\s+(\d{4})",
            normalized
        )

        if month_year_match:

            month_name = (
                month_year_match
                .group(1)
                .strip()
            )

            year = int(
                month_year_match.group(2)
            )

            month = self.MONTHS.get(
                month_name
            )

            if month:

                return (
                    year,
                    month
                )

            return None

        # =================================================
        # YEAR ONLY
        # =================================================

        year_match = re.fullmatch(
            r"\d{4}",
            normalized
        )

        if year_match:

            year = int(
                normalized
            )

            if is_end:

                return (
                    year,
                    12
                )

            return (
                year,
                1
            )

        return None

    # =====================================================
    # MONTH INDEX
    # =====================================================

    @staticmethod
    def _month_index(
        year: int,
        month: int
    ) -> int:
        """
        Converts year/month into a sequential month index.
        """

        return (
            year * 12
            + month
        )

    # =====================================================
    # BUILD INTERVALS
    # =====================================================

    def _build_intervals(
        self,
        historico: list
    ) -> list[tuple[int, int]]:
        """
        Converts professional history into valid
        chronological month intervals.
        """

        intervals = []

        for experiencia in historico:

            if not isinstance(
                experiencia,
                dict
            ):
                continue

            inicio = self._parse_date(
                experiencia.get(
                    "inicio",
                    ""
                ),
                is_end=False
            )

            fim = self._parse_date(
                experiencia.get(
                    "fim",
                    ""
                ),
                is_end=True
            )

            if not inicio or not fim:
                continue

            start_index = self._month_index(
                inicio[0],
                inicio[1]
            )

            end_index = self._month_index(
                fim[0],
                fim[1]
            )

            if end_index < start_index:
                continue

            intervals.append(
                (
                    start_index,
                    end_index
                )
            )

        return sorted(
            intervals
        )

    # =====================================================
    # MERGE OVERLAPPING INTERVALS
    # =====================================================

    @staticmethod
    def _merge_intervals(
        intervals: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """
        Merges overlapping or contiguous professional
        experience intervals.

        This prevents simultaneous jobs from being
        counted twice as chronological experience.
        """

        if not intervals:
            return []

        merged = [
            list(intervals[0])
        ]

        for start, end in intervals[1:]:

            last = merged[-1]

            if start <= last[1] + 1:

                last[1] = max(
                    last[1],
                    end
                )

            else:

                merged.append(
                    [start, end]
                )

        return [
            (
                start,
                end
            )
            for start, end in merged
        ]

    # =====================================================
    # CALCULATE MONTHS
    # =====================================================

    @staticmethod
    def _calculate_months(
        intervals: list[tuple[int, int]]
    ) -> int:
        """
        Calculates chronological months represented
        by merged intervals.
        """

        total = 0

        for start, end in intervals:

            total += (
                end
                - start
                + 1
            )

        return total

    # =====================================================
    # PUBLIC API
    # =====================================================

    def analyze(
        self,
        historico: list
    ) -> dict:
        """
        Produces professional experience intelligence.

        No candidate-job comparison occurs here.
        """

        if not historico:

            return {
                "total_months": 0,
                "total_years": 0.0,
                "experience_count": 0,
                "valid_periods": 0,
                "merged_periods": 0,
            }

        intervals = self._build_intervals(
            historico
        )

        merged = self._merge_intervals(
            intervals
        )

        total_months = self._calculate_months(
            merged
        )

        total_years = round(
            total_months / 12,
            1
        )

        return {
            "total_months": total_months,
            "total_years": total_years,
            "experience_count": len(
                historico
            ),
            "valid_periods": len(
                intervals
            ),
            "merged_periods": len(
                merged
            ),
        }