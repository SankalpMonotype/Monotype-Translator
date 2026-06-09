"""Unit tests for _filter_task_description (language-section filtering)."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
import yaml
from pathlib import Path
from monotype_translation_crew.api import _filter_task_description, _SECTION_TO_LANG

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TASKS_YAML = Path(__file__).parent.parent / "src" / "monotype_translation_crew" / "config" / "tasks.yaml"

def _load_translation_desc() -> str:
    data = yaml.safe_load(_TASKS_YAML.read_text(encoding="utf-8"))
    return data["translation_task"]["description"]

# Minimal synthetic description for structural tests
_SYNTHETIC = (
    "Preamble text that always stays.\n\n"
    "=== GLOBAL RULES (apply to ALL languages) ===\n\n"
    "Global rule A. Global rule B.\n\n"
    "=== FRENCH RULES (apply ONLY when translating to French — do NOT apply to other languages) ===\n\n"
    "French rule 1. French rule 2.\n\n"
    "=== GERMAN RULES (apply ONLY when translating to German — do NOT apply to other languages) ===\n\n"
    "German rule 1.\n\n"
    "=== PORTUGUESE (pt-BR) RULES (apply ONLY when translating to Portuguese — do NOT apply to other languages) ===\n\n"
    "Portuguese rule 1.\n\n"
    "=== SPANISH (es-ES) RULES (apply ONLY when translating to Spanish — do NOT apply to other languages) ===\n\n"
    "Spanish rule 1.\n\n"
    "=== JAPANESE RULES (apply ONLY when translating to Japanese — do NOT apply to other languages) ===\n\n"
    "Japanese rule 1.\n"
    "Output ONLY a valid JSON array. No preamble.\n"
)

ALL_5 = ["fr", "de", "pt_BR", "es_ES", "ja"]


# ---------------------------------------------------------------------------
# _SECTION_TO_LANG constants
# ---------------------------------------------------------------------------

def test_section_to_lang_has_all_five():
    assert set(_SECTION_TO_LANG.values()) == {"fr", "de", "pt_BR", "es_ES", "ja"}


# ---------------------------------------------------------------------------
# Structural tests on synthetic description
# ---------------------------------------------------------------------------

class TestSyntheticDescription:
    def test_all_languages_keeps_everything(self):
        result = _filter_task_description(_SYNTHETIC, ALL_5)
        for lang_section in ["FRENCH RULES", "GERMAN RULES", "PORTUGUESE", "SPANISH", "JAPANESE RULES"]:
            assert lang_section in result

    def test_global_always_kept(self):
        for lang in ALL_5:
            result = _filter_task_description(_SYNTHETIC, [lang])
            assert "GLOBAL RULES" in result

    def test_preamble_always_kept(self):
        for lang in ALL_5:
            result = _filter_task_description(_SYNTHETIC, [lang])
            assert "Preamble text that always stays" in result

    def test_json_footer_always_kept(self):
        for lang in ALL_5:
            result = _filter_task_description(_SYNTHETIC, [lang])
            assert "Output ONLY a valid JSON array" in result

    def test_single_lang_ja_removes_four_sections(self):
        result = _filter_task_description(_SYNTHETIC, ["ja"])
        assert "JAPANESE RULES" in result
        assert "FRENCH RULES" not in result
        assert "GERMAN RULES" not in result
        assert "PORTUGUESE" not in result
        assert "SPANISH" not in result

    def test_single_lang_fr_keeps_only_french(self):
        result = _filter_task_description(_SYNTHETIC, ["fr"])
        assert "FRENCH RULES" in result
        assert "GERMAN RULES" not in result
        assert "JAPANESE RULES" not in result

    def test_two_langs_fr_de(self):
        result = _filter_task_description(_SYNTHETIC, ["fr", "de"])
        assert "FRENCH RULES" in result
        assert "GERMAN RULES" in result
        assert "PORTUGUESE" not in result
        assert "SPANISH" not in result
        assert "JAPANESE RULES" not in result

    def test_three_langs(self):
        result = _filter_task_description(_SYNTHETIC, ["fr", "de", "pt_BR"])
        assert "FRENCH RULES" in result
        assert "GERMAN RULES" in result
        assert "PORTUGUESE" in result
        assert "SPANISH" not in result
        assert "JAPANESE RULES" not in result

    def test_no_sections_returns_unchanged(self):
        plain = "Just a plain description with no section headers."
        assert _filter_task_description(plain, ["fr"]) == plain

    def test_single_lang_reduces_length(self):
        full = _filter_task_description(_SYNTHETIC, ALL_5)
        one = _filter_task_description(_SYNTHETIC, ["ja"])
        assert len(one) < len(full)

    def test_content_within_kept_section_preserved(self):
        result = _filter_task_description(_SYNTHETIC, ["fr"])
        assert "French rule 1" in result
        assert "French rule 2" in result

    def test_content_within_removed_section_absent(self):
        result = _filter_task_description(_SYNTHETIC, ["fr"])
        assert "German rule 1" not in result
        assert "Japanese rule 1" not in result


# ---------------------------------------------------------------------------
# Integration tests against the real tasks.yaml
# ---------------------------------------------------------------------------

class TestRealTasksYaml:
    def setup_method(self):
        self.desc = _load_translation_desc()

    def test_all_six_headers_found(self):
        import re
        header_re = re.compile(r'^(?:===|---)\s+.+\s+(?:===|---)\s*$', re.MULTILINE)
        headers = header_re.findall(self.desc)
        assert len(headers) == 6, f"Expected 6 headers, found: {headers}"

    def test_json_footer_present_in_real_desc(self):
        assert "Output ONLY a valid JSON array." in self.desc

    def test_all_langs_keeps_full_length(self):
        result = _filter_task_description(self.desc, ALL_5)
        # Allow minor whitespace differences but length should be very close
        assert abs(len(result) - len(self.desc)) < 10

    def test_single_lang_ja_saves_at_least_50_percent(self):
        full = _filter_task_description(self.desc, ALL_5)
        one = _filter_task_description(self.desc, ["ja"])
        savings_pct = (len(full) - len(one)) / len(full) * 100
        assert savings_pct >= 50, f"Expected ≥50% savings, got {savings_pct:.1f}%"

    def test_single_lang_json_footer_preserved(self):
        for lang in ALL_5:
            result = _filter_task_description(self.desc, [lang])
            assert "Output ONLY a valid JSON array." in result, f"Footer missing for lang={lang}"

    def test_single_lang_global_rules_preserved(self):
        for lang in ALL_5:
            result = _filter_task_description(self.desc, [lang])
            assert "GLOBAL RULES" in result, f"GLOBAL section missing for lang={lang}"

    def test_single_lang_fr_contains_french_rules(self):
        result = _filter_task_description(self.desc, ["fr"])
        assert "FRENCH RULES" in result

    def test_single_lang_fr_no_german_rules(self):
        result = _filter_task_description(self.desc, ["fr"])
        assert "GERMAN RULES" not in result

    def test_single_lang_de_contains_german_rules(self):
        result = _filter_task_description(self.desc, ["de"])
        assert "GERMAN RULES" in result

    def test_single_lang_pt_br_contains_portuguese_rules(self):
        result = _filter_task_description(self.desc, ["pt_BR"])
        assert "PORTUGUESE" in result

    def test_single_lang_es_es_contains_spanish_rules(self):
        result = _filter_task_description(self.desc, ["es_ES"])
        assert "SPANISH" in result

    def test_single_lang_es_es_no_french_rules(self):
        result = _filter_task_description(self.desc, ["es_ES"])
        assert "FRENCH RULES" not in result

    def test_variable_placeholders_still_present(self):
        # CrewAI interpolates these from inputs — they must survive filtering
        result = _filter_task_description(self.desc, ["ja"])
        assert "{target_languages}" in result or "{target_languages_str}" in result or "{excel_path}" in result
