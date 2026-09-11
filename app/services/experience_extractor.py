"""
=====================================================

TalentAI World

Experience Extractor

Responsible for extracting structured professional
experience from candidate resumes.

Principles:

- Extract facts only
- Never invent professional history
- Preserve original resume evidence
- Identify professional periods conservatively
- Respect resume sections
- Support global resume layouts
- Prepare experience data for TALIA Intelligence

Author:
TalentAI Team

Version:
2.0

=====================================================
"""

import re


# =====================================================
# DATE PATTERNS
# =====================================================

MONTHS = (
    r"jan(?:uary|eiro)?|"
    r"feb(?:ruary|ruary|vereiro)?|"
    r"mar(?:ch|ço)?|"
    r"apr(?:il)?|abr(?:il)?|"
    r"may|mai(?:o)?|"
    r"jun(?:e|ho)?|"
    r"jul(?:y|ho)?|"
    r"aug(?:ust)?|ago(?:sto)?|"
    r"sep(?:tember)?|set(?:embro)?|"
    r"oct(?:ober)?|out(?:ubro)?|"
    r"nov(?:ember|embro)?|"
    r"dec(?:ember)?|dez(?:embro)?"
)

PRESENT_TERMS = (
    r"present|current|currently|"
    r"presente|atual|até o momento|"
    r"actualidad"
)

DATE_TOKEN = (
    rf"(?:"
    rf"(?:{MONTHS})[\s./-]+\d{{4}}"
    rf"|"
    rf"\d{{1,2}}[/-]\d{{4}}"
    rf"|"
    rf"\d{{4}}"
    rf")"
)

DATE_RANGE_PATTERN = re.compile(
    rf"(?P<start>{DATE_TOKEN})"
    rf"\s*"
    rf"(?:-|–|—|to|até|a)"
    rf"\s*"
    rf"(?P<end>{DATE_TOKEN}|{PRESENT_TERMS})",
    re.IGNORECASE
)


# =====================================================
# SECTION DEFINITIONS
# =====================================================

EXPERIENCE_SECTIONS = {
    "experience",
    "professional experience",
    "work experience",
    "employment history",
    "professional history",
    "career history",
    "work history",
    "experiência",
    "experiencia",
    "experiência profissional",
    "experiencia profissional",
    "histórico profissional",
    "historico profissional",
    "experiencia laboral",
    "experiencia profesional",
}

STOP_SECTIONS = {
    "education",
    "academic background",
    "academic education",
    "academic history",
    "formação",
    "formacao",
    "formação acadêmica",
    "formacao academica",
    "educação",
    "educacao",
    "educación",

    "certifications",
    "certification",
    "certificações",
    "certificacoes",
    "certificaciones",

    "skills",
    "technical skills",
    "core competencies",
    "competencies",
    "competências",
    "competencias",
    "habilidades",

    "languages",
    "idiomas",

    "courses",
    "training",
    "cursos",

    "projects",
    "projetos",

    "awards",
    "publications",
    "references",
}


# =====================================================
# HELPERS
# =====================================================

def _clean_line(line: str) -> str:
    """
    Normalizes whitespace while preserving
    resume information.
    """

    if not line:
        return ""

    return re.sub(
        r"\s+",
        " ",
        line
    ).strip()


def _normalize_section(line: str) -> str:
    """
    Normalizes a possible section title.
    """

    line = _clean_line(line)

    line = line.strip(
        " :|-–—"
    )

    return line.lower()


def _extract_date_range(line: str):
    """
    Extracts a date range from a line.

    Returns:
        (start, end)

    If no reliable range exists:
        ("", "")
    """

    if not line:
        return "", ""

    match = DATE_RANGE_PATTERN.search(
        line
    )

    if not match:
        return "", ""

    return (
        _clean_line(
            match.group("start")
        ),
        _clean_line(
            match.group("end")
        )
    )


def _remove_date_range(line: str) -> str:
    """
    Removes the detected date range from a line.
    """

    if not line:
        return ""

    return _clean_line(
        DATE_RANGE_PATTERN.sub(
            "",
            line,
            count=1
        )
    ).strip(
        " |-–—,"
    )


def _is_experience_section(line: str) -> bool:

    return (
        _normalize_section(line)
        in EXPERIENCE_SECTIONS
    )


def _is_stop_section(line: str) -> bool:

    return (
        _normalize_section(line)
        in STOP_SECTIONS
    )


def _is_bullet(line: str) -> bool:
    """
    Detects common bullet formats.
    """

    if not line:
        return False

    stripped = line.lstrip()

    return stripped.startswith(
        (
            "•",
            "●",
            "▪",
            "■",
            "◦",
            "○",
            "- ",
            "* ",
        )
    )


def _clean_bullet(line: str) -> str:
    """
    Removes only the visual bullet marker.
    """

    if not line:
        return ""

    return re.sub(
        r"^[\s•●▪■◦○*-]+",
        "",
        line
    ).strip()


def _looks_like_description(line: str) -> bool:
    """
    Conservative detection of lines that are more
    likely to be activity descriptions than headers.
    """

    if not line:
        return False

    if _is_bullet(line):
        return True

    words = line.split()

    if len(words) > 18:
        return True

    return False


def _split_role_company(header: str):
    """
    Attempts to split role and company from a
    professional experience header.

    Supported examples:

    Senior Consultant | Accenture

    Senior Consultant - Accenture

    Senior Consultant — Accenture

    Conservative principle:
    when uncertain, preserve the text as role instead
    of inventing a company.
    """

    header = _clean_line(header)

    if not header:
        return "", ""

    # -------------------------------------------------
    # PRIMARY SEPARATOR: |
    # -------------------------------------------------

    if "|" in header:

        parts = [
            _clean_line(part)
            for part in header.split("|", 1)
        ]

        cargo = parts[0]

        empresa = (
            parts[1]
            if len(parts) > 1
            else ""
        )

        return cargo, empresa

    # -------------------------------------------------
    # SECONDARY SEPARATORS
    # -------------------------------------------------

    for separator in (
        " — ",
        " – ",
        " - ",
    ):

        if separator in header:

            parts = header.split(
                separator,
                1
            )

            left = _clean_line(
                parts[0]
            )

            right = _clean_line(
                parts[1]
            )

            # Avoid aggressive guessing.
            # Only split reasonably short headers.

            if (
                left
                and right
                and len(left.split()) <= 12
                and len(right.split()) <= 12
            ):

                return left, right

    # -------------------------------------------------
    # UNCERTAIN HEADER
    # -------------------------------------------------

    return header, ""


def _build_experience(
    header_line: str,
    start: str,
    end: str,
    description_lines: list[str]
):
    """
    Builds one professional experience while
    preserving the original evidence.
    """

    header_without_date = _remove_date_range(
        header_line
    )

    cargo, empresa = _split_role_company(
        header_without_date
    )

    descricao_parts = []

    for line in description_lines:

        cleaned = _clean_bullet(
            line
        )

        if cleaned:
            descricao_parts.append(
                cleaned
            )

    descricao = " ".join(
        descricao_parts
    ).strip()

    evidencia_parts = [
        header_line
    ]

    evidencia_parts.extend(
        description_lines
    )

    evidencia_original = "\n".join(
        evidencia_parts
    ).strip()

    return {
        "empresa": empresa,
        "cargo": cargo,
        "inicio": start,
        "fim": end,
        "descricao": descricao,
        "evidencia_original": evidencia_original,
    }


# =====================================================
# PUBLIC API
# =====================================================

def extrair_historico_profissional(
    texto: str
) -> list[dict]:
    """
    Extracts structured professional history.

    Contract preserved:

    [
        {
            "empresa": "",
            "cargo": "",
            "inicio": "",
            "fim": "",
            "descricao": "",
            "evidencia_original": ""
        }
    ]

    Strategy:

    1. Detect professional experience section when present.
    2. Stop before Education, Certifications, Skills, etc.
    3. Identify professional blocks using explicit date ranges.
    4. Preserve role/company/date information from the header.
    5. Aggregate activity lines until the next experience.
    6. Never create experiences from non-professional sections.
    """

    if not texto:
        return []

    lines = [
        _clean_line(line)
        for line in texto.splitlines()
    ]

    lines = [
        line
        for line in lines
        if line
    ]

    if not lines:
        return []

    # =================================================
    # FIND EXPERIENCE SECTION
    # =================================================

    experience_start = None

    for index, line in enumerate(lines):

        if _is_experience_section(line):

            experience_start = (
                index + 1
            )

            break

    # -------------------------------------------------
    # If an explicit experience section exists,
    # restrict extraction to that section.
    #
    # If it does not exist, use the whole document
    # conservatively, but stop at known non-work
    # sections.
    # -------------------------------------------------

    if experience_start is None:

        working_lines = lines

    else:

        working_lines = lines[
            experience_start:
        ]

    # =================================================
    # CUT AT FIRST STOP SECTION
    # =================================================

    scoped_lines = []

    for line in working_lines:

        if _is_stop_section(line):
            break

        scoped_lines.append(
            line
        )

    if not scoped_lines:
        return []

    # =================================================
    # IDENTIFY EXPERIENCE HEADERS
    # =================================================

    header_indexes = []

    for index, line in enumerate(
        scoped_lines
    ):

        inicio, fim = _extract_date_range(
            line
        )

        if not inicio:
            continue

        # A bullet containing a date is normally an
        # activity/certification detail, not a new job.

        if _is_bullet(line):
            continue

        # Very long narrative lines are unlikely to be
        # professional headers.

        if (
            _looks_like_description(line)
            and "|" not in line
        ):
            continue

        header_indexes.append(
            index
        )

    # =================================================
    # BUILD EXPERIENCES
    # =================================================

    historico = []

    for position, header_index in enumerate(
        header_indexes
    ):

        header_line = scoped_lines[
            header_index
        ]

        inicio, fim = _extract_date_range(
            header_line
        )

        if not inicio:
            continue

        # ---------------------------------------------
        # DESCRIPTION RANGE
        # ---------------------------------------------

        description_start = (
            header_index + 1
        )

        if (
            position + 1
            < len(header_indexes)
        ):

            description_end = (
                header_indexes[
                    position + 1
                ]
            )

        else:

            description_end = len(
                scoped_lines
            )

        description_lines = scoped_lines[
            description_start:
            description_end
        ]

        # ---------------------------------------------
        # REMOVE ACCIDENTAL SECTION TITLES
        # ---------------------------------------------

        description_lines = [
            line
            for line in description_lines
            if not _is_stop_section(line)
            and not _is_experience_section(line)
        ]

        experiencia = _build_experience(
            header_line=header_line,
            start=inicio,
            end=fim,
            description_lines=description_lines
        )

        historico.append(
            experiencia
        )

    return historico