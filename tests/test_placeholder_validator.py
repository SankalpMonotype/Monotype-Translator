"""Unit tests for placeholder_validator.validate_placeholders and extract_placeholders."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from monotype_translation_crew.tools.placeholder_validator import (
    extract_placeholders,
    validate_placeholders,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _entry(row, english, **langs):
    return {"row_index": row, "english": english, **langs}


# ---------------------------------------------------------------------------
# extract_placeholders — pattern coverage
# ---------------------------------------------------------------------------

class TestExtractPlaceholders:
    def test_double_brace(self):
        assert extract_placeholders("Hello {{name}}!") == ["{{name}}"]

    def test_single_brace(self):
        assert extract_placeholders("Hello {name}!") == ["{name}"]

    def test_double_brace_not_also_single(self):
        # {{name}} must produce ONE token, not two or three
        tokens = extract_placeholders("{{name}} is here")
        assert tokens == ["{{name}}"]

    def test_printf_s(self):
        assert extract_placeholders("Hello %s") == ["%s"]

    def test_printf_d(self):
        assert extract_placeholders("%d items") == ["%d"]

    def test_printf_positional_printf(self):
        assert extract_placeholders("%1$s and %2$s") == ["%1$s", "%2$s"]

    def test_positional_angle_bracket(self):
        assert extract_placeholders("<0> of <1>") == ["<0>", "<1>"]

    def test_mixed_placeholders(self):
        tokens = extract_placeholders("{{count}} items: {name} (<0>)")
        assert "{{count}}" in tokens
        assert "{name}" in tokens
        assert "<0>" in tokens
        assert len(tokens) == 3

    def test_no_placeholders(self):
        assert extract_placeholders("No placeholders here.") == []

    def test_empty_string(self):
        assert extract_placeholders("") == []

    def test_multiple_same_placeholder(self):
        # If the same placeholder appears twice in the source, both are returned
        tokens = extract_placeholders("{{n}} of {{n}}")
        assert tokens.count("{{n}}") == 2

    def test_order_preserved(self):
        tokens = extract_placeholders("{{a}} then {b} then <0>")
        assert tokens == ["{{a}}", "{b}", "<0>"]

    def test_single_brace_with_spaces_in_name(self):
        # {company name} is a real Monotype placeholder
        assert extract_placeholders("{company name}") == ["{company name}"]

    def test_double_brace_with_spaces_in_name(self):
        assert extract_placeholders("{{division name}}") == ["{{division name}}"]


# ---------------------------------------------------------------------------
# validate_placeholders — no violation expected
# ---------------------------------------------------------------------------

class TestNoViolations:
    def test_clean_double_brace(self):
        entries = [_entry(1, "Hello {{name}}!", fr="Bonjour {{name}} !")]
        assert validate_placeholders(entries) == []

    def test_clean_single_brace(self):
        entries = [_entry(2, "Delete {item}?", de="Löschen {item}?")]
        assert validate_placeholders(entries) == []

    def test_clean_printf(self):
        entries = [_entry(3, "Found %d results", fr="Résultats trouvés : %d")]
        assert validate_placeholders(entries) == []

    def test_clean_positional(self):
        entries = [_entry(4, "<0> of <1> used", de="<0> von <1> verwendet")]
        assert validate_placeholders(entries) == []

    def test_reordered_placeholders_ok(self):
        # Positional re-ordering is valid — only presence matters, not order
        entries = [_entry(5, "{{a}} then {{b}}", fr="{{b}} puis {{a}}")]
        assert validate_placeholders(entries) == []

    def test_no_placeholders_in_source(self):
        entries = [_entry(6, "Save font", fr="Enregistrer la police")]
        assert validate_placeholders(entries) == []

    def test_empty_entries(self):
        assert validate_placeholders([]) == []

    def test_no_english_field(self):
        violations = validate_placeholders([{"row_index": 1, "fr": "Bonjour {{name}}"}])
        assert violations == []

    def test_non_target_lang_skipped(self):
        entries = [{"row_index": 1, "english": "Hi {{name}}", "zh": "{{name}}缺失"}]
        assert validate_placeholders(entries) == []

    def test_multiple_same_placeholder_present_in_both(self):
        # Source has {{n}} twice; translation also has it twice — no violation
        entries = [_entry(7, "{{n}} of {{n}}", fr="{{n}} sur {{n}}")]
        assert validate_placeholders(entries) == []


# ---------------------------------------------------------------------------
# validate_placeholders — missing placeholder
# ---------------------------------------------------------------------------

class TestMissingViolations:
    def test_missing_double_brace(self):
        entries = [_entry(10, "Hello {{name}}!", fr="Bonjour !")]
        violations = validate_placeholders(entries)
        assert len(violations) == 1
        v = violations[0]
        assert v["row_index"] == 10
        assert v["lang"] == "fr"
        assert v["placeholder"] == "{{name}}"
        assert v["issue"] == "missing"

    def test_missing_single_brace(self):
        entries = [_entry(11, "Delete {item}?", de="Löschen?")]
        violations = validate_placeholders(entries)
        assert any(v["placeholder"] == "{item}" and v["issue"] == "missing" for v in violations)

    def test_missing_printf(self):
        entries = [_entry(12, "Found %d items", fr="Résultats trouvés")]
        violations = validate_placeholders(entries)
        assert any(v["placeholder"] == "%d" and v["issue"] == "missing" for v in violations)

    def test_missing_positional(self):
        entries = [_entry(13, "<0> of <1>", de="von")]
        violations = validate_placeholders(entries)
        missing = {v["placeholder"] for v in violations if v["issue"] == "missing"}
        assert "<0>" in missing
        assert "<1>" in missing

    def test_missing_one_of_two_placeholders(self):
        entries = [_entry(14, "{{a}} and {{b}}", fr="{{a}} et quelque chose")]
        violations = validate_placeholders(entries)
        missing = [v for v in violations if v["issue"] == "missing"]
        assert len(missing) == 1
        assert missing[0]["placeholder"] == "{{b}}"

    def test_missing_across_multiple_languages(self):
        entries = [_entry(15, "Hi {{name}}", fr="Bonjour", de="Hallo")]
        violations = validate_placeholders(entries)
        langs = {v["lang"] for v in violations}
        assert "fr" in langs
        assert "de" in langs

    def test_violation_contains_english_snippet(self):
        entries = [_entry(16, "Hello {{name}}!", fr="Bonjour !")]
        v = validate_placeholders(entries)[0]
        assert "{{name}}" in v["english"]

    def test_missing_one_of_repeated_placeholder(self):
        # Source has {{n}} twice; translation has it only once → "missing" (count 1 < 2)
        entries = [_entry(17, "{{n}} of {{n}}", fr="{{n}} sur quelque chose")]
        violations = validate_placeholders(entries)
        assert any(v["placeholder"] == "{{n}}" and v["issue"] == "missing" for v in violations)


# ---------------------------------------------------------------------------
# validate_placeholders — duplicated placeholder
# ---------------------------------------------------------------------------

class TestDuplicatedViolations:
    def test_duplicated_double_brace(self):
        entries = [_entry(20, "Hi {{name}}", fr="{{name}} Bonjour {{name}}")]
        violations = validate_placeholders(entries)
        assert any(v["placeholder"] == "{{name}}" and v["issue"] == "duplicated" for v in violations)

    def test_duplicated_printf(self):
        entries = [_entry(21, "Found %d items", de="%d Ergebnisse, %d gesamt")]
        violations = validate_placeholders(entries)
        assert any(v["placeholder"] == "%d" and v["issue"] == "duplicated" for v in violations)

    def test_duplicated_positional(self):
        entries = [_entry(22, "<0> selected", fr="<0> et <0> sélectionnés")]
        violations = validate_placeholders(entries)
        assert any(v["placeholder"] == "<0>" and v["issue"] == "duplicated" for v in violations)


# ---------------------------------------------------------------------------
# validate_placeholders — alias key resolution
# ---------------------------------------------------------------------------

class TestAliasKeys:
    def test_portuguese_alias(self):
        entries = [{"row_index": 5, "english": "Hi {{name}}", "portuguese": "Olá"}]
        violations = validate_placeholders(entries)
        assert len(violations) == 1
        assert violations[0]["lang"] == "pt_BR"

    def test_pt_br_dash_alias(self):
        entries = [{"row_index": 6, "english": "{count} left", "pt-br": "restantes"}]
        violations = validate_placeholders(entries)
        assert violations[0]["lang"] == "pt_BR"

    def test_german_alias(self):
        entries = [{"row_index": 7, "english": "{{n}} items", "german": "Elemente"}]
        v = validate_placeholders(entries)
        assert v[0]["lang"] == "de"

    def test_en_field_as_source(self):
        # Entry uses "en" key instead of "english"
        entries = [{"row_index": 8, "en": "Hello {{name}}", "fr": "Bonjour"}]
        violations = validate_placeholders(entries)
        assert len(violations) == 1
        assert violations[0]["placeholder"] == "{{name}}"
