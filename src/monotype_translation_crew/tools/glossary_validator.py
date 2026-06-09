"""
Post-translation glossary spot-checker.

Parses knowledge/glossary.md to build an approved-translation lookup, then
checks each translated entry for HIGH-CONFIDENCE violations: only flags when
(1) the English source contains a known glossary term, (2) the translation is
missing the approved form, AND (3) the translation contains a known-wrong
alternative.  All three conditions must be true to avoid false positives.
"""
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Column header → canonical lang code
# ---------------------------------------------------------------------------
_HEADER_TO_LANG: dict[str, str] = {
    "french":               "fr",
    "german":               "de",
    "portuguese (pt-br)":   "pt_BR",
    "portuguese":           "pt_BR",
    "japanese":             "ja",
    "spanish (es-es)":      "es_ES",
    "spanish":              "es_ES",
    "english":              "en",
}

# Lang codes whose entries the validator checks (skips "en")
_TARGET_LANGS = {"fr", "de", "pt_BR", "ja", "es_ES"}

# Entry key aliases → canonical lang code (mirrors excel_tools._LANG_KEY_ALIASES)
_ENTRY_LANG_ALIASES: dict[str, str] = {
    "fr": "fr", "french": "fr",
    "de": "de", "german": "de",
    "pt_br": "pt_BR", "pt-br": "pt_BR", "pt": "pt_BR", "portuguese": "pt_BR",
    "ja": "ja", "japanese": "ja",
    "es_es": "es_ES", "es-es": "es_ES", "es-419": "es_ES", "es": "es_ES", "spanish": "es_ES",
}

# ---------------------------------------------------------------------------
# Hardcoded known-wrong table
# Format: (english_term_lower, canonical_lang_code) → [wrong substrings (lower)]
# Only add entries where we have HIGH confidence it's always wrong in this product.
# ---------------------------------------------------------------------------
KNOWN_WRONG: dict[tuple[str, str], list[str]] = {
    # French: "tag" must stay as "tag" — never translate to "étiquette" or "balise"
    ("tag", "fr"):          ["étiquette", "etiquette", "balise"],
    # French: standalone view/show action label must be "Afficher" — "Voir" is wrong
    ("view", "fr"):         ["voir"],
    # German: in compound-word UI strings "Font" stays as "Font" — "Schrift" is wrong
    ("font", "de"):         ["schrift"],
    # Portuguese: system-inability error prefix must be "Não foi possível" — "Incapaz de" is wrong
    ("unable to", "pt_BR"): ["incapaz de"],
}

# ---------------------------------------------------------------------------
# Glossary parsing helpers
# ---------------------------------------------------------------------------

def _clean_cell(raw: str) -> str:
    """Strip markdown formatting noise from a glossary cell."""
    text = raw.strip()
    # Remove backticks
    text = text.replace("`", "")
    # Remove *(keep as-is)* and similar italic annotations
    text = re.sub(r'\*[^*]*\*', '', text)
    # Remove warning emoji and similar symbols
    text = re.sub(r'[⚠️✅❌]', '', text)
    return text.strip()


def _split_approved(cell: str) -> list[str]:
    """
    Split a glossary cell into individual approved forms.
    e.g. "Police / police de caractères" → ["police", "police de caractères"]
    Strips optional plural markers like (s), (en), (ren).
    """
    forms = [_clean_cell(part) for part in cell.split("/")]
    result = []
    for form in forms:
        if not form:
            continue
        # Strip optional plural suffixes: (s), (en), (ren), (es), etc.
        base = re.sub(r'\([a-zäöüé]+\)$', '', form, flags=re.IGNORECASE).strip()
        if base:
            result.append(base.lower())
    return result


def _is_separator_row(cells: list[str]) -> bool:
    """Return True if this is the |---|---| divider line."""
    return all(re.fullmatch(r'-+', c.strip().lstrip(':').rstrip(':')) or not c.strip()
               for c in cells)


def _parse_glossary(glossary_path: str) -> dict[tuple[str, str], list[str]]:
    """
    Parse all markdown tables in glossary.md and return:
        {(english_term_lower, lang_code): [approved_form_lower, ...]}

    Only entries for TARGET_LANGS are returned (English column is the key, not a value).
    """
    path = Path(glossary_path)
    if not path.is_absolute():
        path = Path.cwd() / path

    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")
    approved: dict[tuple[str, str], list[str]] = {}

    col_langs: list[str | None] = []   # column index → lang code (None = skip)
    en_col: int | None = None

    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            # Reset on any non-table line
            col_langs = []
            en_col = None
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]

        if _is_separator_row(cells):
            continue

        # If we have no column map yet, treat this as a header row
        if not col_langs:
            col_langs = []
            for cell in cells:
                lang = _HEADER_TO_LANG.get(cell.lower())
                if lang == "en":
                    en_col = len(col_langs)
                col_langs.append(lang)
            continue

        # Data row
        if en_col is None or en_col >= len(cells):
            continue

        raw_english = _clean_cell(cells[en_col])
        if not raw_english or raw_english.lower() in ("n/a", "-", ""):
            continue

        # Use the base form (strip optional plurals) as the dict key
        english_key = re.sub(r'\s*\([a-zäöüé/ ]+\)', '', raw_english, flags=re.IGNORECASE).strip().lower()
        if not english_key:
            continue

        for col_idx, lang in enumerate(col_langs):
            if lang is None or lang == "en" or lang not in _TARGET_LANGS:
                continue
            if col_idx >= len(cells):
                continue
            raw = _clean_cell(cells[col_idx])
            if not raw or raw.lower() in ("n/a", "-", ""):
                continue
            forms = _split_approved(raw)
            if not forms:
                continue
            key = (english_key, lang)
            existing = approved.get(key, [])
            for f in forms:
                if f not in existing:
                    existing.append(f)
            approved[key] = existing

    return approved


# ---------------------------------------------------------------------------
# Match helpers
# ---------------------------------------------------------------------------

def _term_in_english(term_lower: str, english_lower: str) -> bool:
    """
    Return True if `term_lower` appears in `english_lower` as a whole-word match
    (or whole-phrase match for multi-word terms). Case-insensitive.
    """
    if " " in term_lower:
        return term_lower in english_lower.lower()
    return bool(re.search(r'\b' + re.escape(term_lower) + r'\b', english_lower, re.IGNORECASE))


def _any_form_in_translation(forms: list[str], translation_lower: str) -> bool:
    """Return True if at least one approved form appears (case-insensitive substring)."""
    return any(f in translation_lower for f in forms if f)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_glossary(
    entries: list[dict],
    glossary_path: str = "knowledge/glossary.md",
) -> list[dict]:
    """
    Scan each translated string for known glossary violations.
    Returns a list of violation dicts:
        {row_index, lang, english_term, expected_translation, found_text, severity}

    Only flags HIGH-CONFIDENCE violations where:
    1. The English source contains the KNOWN_WRONG term (exact word/phrase match)
    2. The target language translation DOES contain a known wrong alternative
    3. (When the term is in the glossary) the approved form is NOT present in the
       translation — prevents false positives when the approved and wrong forms overlap.

    Conditions 1+2 are always required. Condition 3 is only applied when the
    glossary has an approved form for that (term, lang) pair; if the term is not
    in the glossary, conditions 1+2 alone are sufficient for a high-confidence flag.
    """
    approved = _parse_glossary(glossary_path)

    # Flatten approved into a dict keyed by (term_lower, lang_code) for fast lookup
    approved_lookup: dict[tuple[str, str], list[str]] = {}
    for (term, lang), forms in approved.items():
        approved_lookup[(term, lang)] = forms

    violations: list[dict] = []

    for entry in entries:
        row_index = entry.get("row_index")

        # Resolve English source — may be stored under "english", "en", or "English"
        english = (
            entry.get("english")
            or entry.get("en")
            or entry.get("English")
            or ""
        )
        if not english:
            continue
        english_lower = str(english).lower()

        # Check each language present in this entry
        for raw_key, value in entry.items():
            if not value or raw_key in {"row_index", "english", "en", "English", "reviewer_note"}:
                continue
            lang = _ENTRY_LANG_ALIASES.get(raw_key.lower())
            if lang is None or lang not in _TARGET_LANGS:
                continue

            translation_lower = str(value).lower()

            # Drive the check from KNOWN_WRONG — covers both glossary and non-glossary terms
            for (term_lower, wrong_lang), wrong_forms in KNOWN_WRONG.items():
                if wrong_lang != lang:
                    continue

                # Condition 1: English source must contain the term
                if not _term_in_english(term_lower, english_lower):
                    continue

                # Condition 2: translation must contain a known-wrong alternative
                found_wrong = next(
                    (wf for wf in wrong_forms if wf in translation_lower), None
                )
                if found_wrong is None:
                    continue

                # Condition 3 (when glossary has an approved form): approved form
                # must be ABSENT from the translation — prevents false positives when
                # a form is simultaneously "approved" and "known wrong" in different
                # style contexts (e.g. "Voir" approved in general, wrong as standalone label).
                approved_forms = approved_lookup.get((term_lower, lang), [])
                if approved_forms and _any_form_in_translation(approved_forms, translation_lower):
                    continue

                violations.append({
                    "row_index": row_index,
                    "lang": lang,
                    "english_term": term_lower,
                    "expected_translation": " / ".join(approved_forms) if approved_forms else "(see style guide)",
                    "found_text": str(value)[:120],
                    "severity": "HIGH",
                })

    return violations
