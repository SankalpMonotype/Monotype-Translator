"""Unit tests for glossary_validator.validate_glossary."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from monotype_translation_crew.tools.glossary_validator import (
    validate_glossary,
    _parse_glossary,
    _term_in_english,
    _split_approved,
    KNOWN_WRONG,
)

# ---------------------------------------------------------------------------
# Glossary path used for all tests
# ---------------------------------------------------------------------------
_GLOSSARY = os.path.join(os.path.dirname(__file__), "..", "knowledge", "glossary.md")


# ---------------------------------------------------------------------------
# _split_approved
# ---------------------------------------------------------------------------

def test_split_approved_single():
    assert _split_approved("police") == ["police"]

def test_split_approved_slash():
    forms = _split_approved("Police / police de caractères")
    assert "police" in forms
    assert "police de caractères" in forms

def test_split_approved_strips_optional_plural():
    forms = _split_approved("tag(s)")
    assert "tag" in forms

def test_split_approved_strips_backtick_noise():
    forms = _split_approved("`Leiturabilidade` ⚠️")
    assert "leiturabilidade" in forms

def test_split_approved_skips_empty():
    assert _split_approved("") == []
    assert _split_approved("  ") == []


# ---------------------------------------------------------------------------
# _term_in_english
# ---------------------------------------------------------------------------

def test_term_word_boundary_single():
    assert _term_in_english("tag", "add a tag to this font")
    assert not _term_in_english("tag", "tagging is disabled")  # partial word — no match

def test_term_phrase_match():
    assert _term_in_english("unable to", "unable to delete the user")
    assert not _term_in_english("unable to", "we are unable")  # phrase not present

def test_term_case_insensitive():
    assert _term_in_english("font", "Font-Cache settings")


# ---------------------------------------------------------------------------
# _parse_glossary
# ---------------------------------------------------------------------------

def test_parse_glossary_returns_dict():
    approved = _parse_glossary(_GLOSSARY)
    assert isinstance(approved, dict)
    assert len(approved) > 0

def test_parse_glossary_fr_font():
    approved = _parse_glossary(_GLOSSARY)
    forms = approved.get(("font", "fr"), [])
    assert any("police" in f for f in forms)

def test_parse_glossary_de_font():
    approved = _parse_glossary(_GLOSSARY)
    forms = approved.get(("font", "de"), [])
    # Both "schrift" and "font" are listed in the glossary
    assert "font" in forms or any("font" in f for f in forms)

def test_parse_glossary_pt_br_seat():
    approved = _parse_glossary(_GLOSSARY)
    forms = approved.get(("seat (licence unit)", "pt_BR"), []) or \
            approved.get(("seat", "pt_BR"), [])
    assert forms  # should exist

def test_parse_glossary_missing_file():
    approved = _parse_glossary("/nonexistent/path/glossary.md")
    assert approved == {}


# ---------------------------------------------------------------------------
# validate_glossary — NO violation expected
# ---------------------------------------------------------------------------

def _entry(row, english, **langs):
    return {"row_index": row, "english": english, **langs}


def test_no_violation_when_approved_present():
    # French "tag" stays as "tag" — correct
    violations = validate_glossary(
        [_entry(5, "Add a tag", fr="Ajouter un tag")],
        glossary_path=_GLOSSARY,
    )
    assert violations == []


def test_no_violation_approved_missing_but_known_wrong_absent():
    # Missing approved form, but no known-wrong form either → no flag
    violations = validate_glossary(
        [_entry(5, "Add a tag", fr="Ajouter une note")],
        glossary_path=_GLOSSARY,
    )
    assert violations == []


def test_no_violation_empty_entries():
    assert validate_glossary([], glossary_path=_GLOSSARY) == []


def test_no_violation_no_english():
    violations = validate_glossary(
        [{"row_index": 1, "fr": "Bonjour"}],
        glossary_path=_GLOSSARY,
    )
    assert violations == []


def test_no_violation_non_target_lang_skipped():
    # "zh" is not a target language — should never be checked
    violations = validate_glossary(
        [_entry(1, "Add a tag", zh="添加标签")],
        glossary_path=_GLOSSARY,
    )
    assert violations == []


# ---------------------------------------------------------------------------
# validate_glossary — violations expected
# ---------------------------------------------------------------------------

def test_violation_fr_tag_etiquette():
    # "tag" English → French "étiquette" is wrong
    violations = validate_glossary(
        [_entry(3, "Add a tag", fr="Ajouter une étiquette")],
        glossary_path=_GLOSSARY,
    )
    assert len(violations) == 1
    v = violations[0]
    assert v["row_index"] == 3
    assert v["lang"] == "fr"
    assert v["english_term"] == "tag"
    assert "étiquette" in v["found_text"]
    assert v["severity"] == "HIGH"


def test_no_violation_fr_view_voir_glossary_conflict():
    # "Voir" is in KNOWN_WRONG for (view, fr) — BUT the glossary also approves "Voir"
    # alongside "Afficher". Since the approved form IS present, condition (3) is
    # skipped and no violation fires. This is intentional: the 3-condition design
    # prevents false positives when a form is simultaneously glossary-approved and
    # known-wrong in a narrower style context.
    violations = validate_glossary(
        [_entry(7, "View all fonts", fr="Voir toutes les polices")],
        glossary_path=_GLOSSARY,
    )
    assert violations == []


def test_violation_pt_br_unable_to():
    # Portuguese "Unable to" → "Incapaz de" is wrong
    violations = validate_glossary(
        [_entry(12, "Unable to delete user", pt_BR="Incapaz de excluir o usuário")],
        glossary_path=_GLOSSARY,
    )
    assert len(violations) == 1
    v = violations[0]
    assert v["lang"] == "pt_BR"
    assert "incapaz de" in v["found_text"].lower()


def test_violation_includes_expected_translation():
    violations = validate_glossary(
        [_entry(3, "Add a tag", fr="Ajouter une étiquette")],
        glossary_path=_GLOSSARY,
    )
    assert violations[0]["expected_translation"]  # non-empty approved form string


def test_violation_uses_canonical_lang_aliases():
    # Entry uses alias key "portuguese" instead of "pt_BR"
    violations = validate_glossary(
        [_entry(9, "Unable to delete user", portuguese="Incapaz de excluir o usuário")],
        glossary_path=_GLOSSARY,
    )
    assert any(v["lang"] == "pt_BR" for v in violations)


def test_multiple_entries_violations_and_clean():
    entries = [
        _entry(1, "Add a tag", fr="Ajouter une étiquette"),           # violation — étiquette
        _entry(2, "Unable to delete user", pt_BR="Incapaz de excluir o usuário"),  # violation
        _entry(3, "Save font", fr="Enregistrer la police"),            # clean — no violation
    ]
    violations = validate_glossary(entries, glossary_path=_GLOSSARY)
    rows_with_violations = {v["row_index"] for v in violations}
    assert 1 in rows_with_violations
    assert 2 in rows_with_violations
    assert 3 not in rows_with_violations


def test_violation_missing_glossary_still_fires_known_wrong():
    # If the glossary is missing the approved table is empty, but KNOWN_WRONG checks
    # (conditions 1+2) still fire — the validator degrades gracefully rather than going silent.
    # expected_translation falls back to "(see style guide)" since no approved form is known.
    entries = [_entry(1, "Add a tag", fr="Ajouter une étiquette")]
    violations = validate_glossary(entries, glossary_path="/no/such/glossary.md")
    assert len(violations) == 1
    assert violations[0]["expected_translation"] == "(see style guide)"
