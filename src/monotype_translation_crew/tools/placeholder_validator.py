"""
Placeholder integrity checker for translated strings.

Extracts every placeholder token from the English source and verifies it appears
exactly once in each language translation.  Only reports "missing" and
"duplicated" — positional re-ordering (valid in many languages) is allowed.
"""
import re

# ---------------------------------------------------------------------------
# Placeholder extraction
# ---------------------------------------------------------------------------

# Order matters: double-brace MUST be matched before single-brace so that
# {{name}} is not split into two single-brace tokens.
_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("double_brace", re.compile(r'\{\{[^}]+\}\}')),
    # Single-brace: only match when NOT preceded/followed by another brace,
    # so {{...}} does not accidentally also match as {... or ...}.
    ("single_brace", re.compile(r'(?<!\{)\{[^{}]+\}(?!\})')),
    ("printf",       re.compile(r'%[0-9]*\$?[sd]')),
    ("positional",   re.compile(r'<\d+>')),
]

# Lang keys to skip when iterating entry fields
_META_KEYS = frozenset({"row_index", "english", "en", "English", "reviewer_note"})

# Lang-code aliases (mirrors excel_tools._LANG_KEY_ALIASES)
_LANG_ALIASES: dict[str, str] = {
    "fr": "fr", "french": "fr",
    "de": "de", "german": "de",
    "pt_br": "pt_BR", "pt-br": "pt_BR", "pt": "pt_BR", "portuguese": "pt_BR",
    "ja": "ja", "japanese": "ja",
    "es_es": "es_ES", "es-es": "es_ES", "es-419": "es_ES", "es": "es_ES", "spanish": "es_ES",
}

_TARGET_LANGS = frozenset({"fr", "de", "pt_BR", "ja", "es_ES"})


def extract_placeholders(text: str) -> list[str]:
    """
    Return all placeholder tokens found in *text*, in the order they appear.

    Double-brace tokens are extracted first (and their positions masked) so
    that the single-brace pattern cannot re-match the same characters.
    """
    remaining = text
    tokens: list[tuple[int, str]] = []  # (start_pos_in_original, token)

    # Extract double-brace first, masking matched spans
    for m in _PATTERNS[0][1].finditer(remaining):
        tokens.append((m.start(), m.group()))

    # Build a masked copy: replace double-brace tokens with spaces of equal length
    # so subsequent patterns cannot overlap with already-found tokens
    masked = list(remaining)
    for _, tok in tokens:
        for m in _PATTERNS[0][1].finditer(remaining):
            if m.group() == tok:
                for i in range(m.start(), m.end()):
                    masked[i] = ' '
    masked_str = ''.join(masked)

    # Extract remaining pattern types against the masked string
    for name, pattern in _PATTERNS[1:]:
        for m in pattern.finditer(masked_str):
            tokens.append((m.start(), m.group()))

    # Return tokens sorted by their position in the original string
    tokens.sort(key=lambda t: t[0])
    return [tok for _, tok in tokens]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_placeholders(entries: list[dict]) -> list[dict]:
    """
    For each entry, extract all placeholders from the English source using:
    - {{variable_name}}  double-brace
    - {variable_name}    single-brace (not double-brace)
    - %s, %d, %1$s       printf-style
    - <0>, <1>           positional

    Then verify each placeholder appears exactly once in each translated string.

    Returns a list of violations:
        {row_index, lang, english, placeholder, issue}
    where issue is "missing" or "duplicated".
    """
    violations: list[dict] = []

    for entry in entries:
        row_index = entry.get("row_index")

        english = (
            entry.get("english")
            or entry.get("en")
            or entry.get("English")
            or ""
        )
        if not english:
            continue

        source_placeholders = extract_placeholders(str(english))
        if not source_placeholders:
            continue  # no placeholders — nothing to check

        # Build expected count per unique placeholder from the source
        expected: dict[str, int] = {}
        for ph in source_placeholders:
            expected[ph] = expected.get(ph, 0) + 1

        for raw_key, value in entry.items():
            if not value or raw_key in _META_KEYS:
                continue
            lang = _LANG_ALIASES.get(raw_key.lower())
            if lang is None or lang not in _TARGET_LANGS:
                continue

            translation = str(value)

            for ph, expected_count in expected.items():
                actual_count = translation.count(ph)
                if actual_count < expected_count:
                    violations.append({
                        "row_index": row_index,
                        "lang": lang,
                        "english": str(english)[:120],
                        "placeholder": ph,
                        "issue": "missing",
                    })
                elif actual_count > expected_count:
                    violations.append({
                        "row_index": row_index,
                        "lang": lang,
                        "english": str(english)[:120],
                        "placeholder": ph,
                        "issue": "duplicated",
                    })

    return violations
