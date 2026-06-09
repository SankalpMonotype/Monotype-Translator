"""Unit tests for _normalise_translation in excel_tools."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from monotype_translation_crew.tools.excel_tools import _normalise_translation


# ---------------------------------------------------------------------------
# 1. Smart/curly apostrophes -> straight apostrophe
# ---------------------------------------------------------------------------

def test_right_curly_apostrophe_replaced():
    # U+2019 RIGHT SINGLE QUOTATION MARK -> ASCII apostrophe
    assert _normalise_translation("l’utilisateur", "fr") == "l'utilisateur"

def test_left_curly_apostrophe_replaced():
    # U+2018 LEFT SINGLE QUOTATION MARK -> ASCII apostrophe
    assert _normalise_translation("isn‘t", "en") == "isn't"

def test_both_curly_apostrophes_in_one_string():
    assert _normalise_translation("c’est l‘idée", "fr") == "c'est l'idée"

def test_straight_apostrophe_unchanged():
    assert _normalise_translation("l'utilisateur", "fr") == "l'utilisateur"


# ---------------------------------------------------------------------------
# 2. Smart/curly double quotes -> straight double quotes
# ---------------------------------------------------------------------------

def test_left_double_quote_replaced():
    # U+201C -> ASCII "
    assert _normalise_translation('“hello”', "de") == '"hello"'

def test_right_double_quote_replaced():
    assert _normalise_translation('say “no”', "fr") == 'say "no"'

def test_guillemets_preserved():
    # «» must NOT be touched
    assert _normalise_translation("«consulta»", "es_ES") == "«consulta»"

def test_guillemets_with_curly_in_same_string():
    # Mixed: curly quotes normalised, guillemets preserved
    result = _normalise_translation('«hola» “mundo”', "es_ES")
    assert result == '«hola» "mundo"'


# ---------------------------------------------------------------------------
# 3. Japanese fullwidth bracket normalisation
# ---------------------------------------------------------------------------

def test_ja_plain_number_parentheses():
    assert _normalise_translation("結果(42)", "ja") == "結果（42）"

def test_ja_number_with_counter_kanji():
    assert _normalise_translation("(5件)", "ja") == "（5件）"

def test_ja_number_with_comma():
    assert _normalise_translation("(1,200件)", "ja") == "（1,200件）"

def test_ja_angle_bracket_placeholder():
    assert _normalise_translation("(<count>件)", "ja") == "（<count>件）"

def test_ja_double_brace_placeholder():
    assert _normalise_translation("({{count}}件)", "ja") == "（{{count}}件）"

def test_ja_double_brace_without_counter():
    assert _normalise_translation("({{n}})", "ja") == "（{{n}}）"

def test_ja_fullwidth_brackets_unchanged():
    # Already fullwidth — should remain as-is
    assert _normalise_translation("（42件）", "ja") == "（42件）"

def test_non_ja_parentheses_unchanged():
    # ASCII parentheses in non-Japanese languages must NOT be widened
    assert _normalise_translation("(42件)", "fr") == "(42件)"
    assert _normalise_translation("(42件)", "de") == "(42件)"


# ---------------------------------------------------------------------------
# 4. Trailing whitespace strip
# ---------------------------------------------------------------------------

def test_trailing_spaces_stripped():
    assert _normalise_translation("Bonjour   ", "fr") == "Bonjour"

def test_trailing_tab_stripped():
    assert _normalise_translation("Hallo\t", "de") == "Hallo"

def test_trailing_mixed_whitespace_stripped():
    assert _normalise_translation("texto  \t  ", "es_ES") == "texto"

def test_internal_whitespace_untouched():
    # Only trailing whitespace is stripped; internal spaces must remain
    assert _normalise_translation("a b  c", "de") == "a b  c"

def test_no_trailing_whitespace_unchanged():
    assert _normalise_translation("clean", "fr") == "clean"


# ---------------------------------------------------------------------------
# Pre-existing rules — regression guard
# ---------------------------------------------------------------------------

def test_ellipsis_normalised():
    assert _normalise_translation("Attendre…", "fr") == "Attendre..."

def test_placeholder_spacing_normalised():
    assert _normalise_translation("Bonjour {{ name }}", "fr") == "Bonjour {{name}}"

def test_fr_nbsp_before_question_mark():
    assert _normalise_translation("Êtes-vous sûr ?", "fr") == "Êtes-vous sûr ?"

def test_fr_nbsp_before_colon():
    assert _normalise_translation("Résultat :", "fr") == "Résultat :"

def test_nbsp_untouched_in_non_fr():
    # Non-French: non-breaking space before ? must NOT be changed
    assert _normalise_translation("texto ?", "es_ES") == "texto ?"
