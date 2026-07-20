import pytest
from monotype_translation_crew.api import _merge_per_language_results


def test_merge_into_empty_base():
    result = _merge_per_language_results(
        base=[],
        additions=[{"row_index": 0, "english": "Save", "es_ES": "Guardar"}],
    )
    assert len(result) == 1
    assert result[0]["row_index"] == 0
    assert result[0]["es_ES"] == "Guardar"


def test_merge_adds_lang_to_existing_row():
    result = _merge_per_language_results(
        base=[{"row_index": 0, "english": "Save", "es_ES": "Guardar"}],
        additions=[{"row_index": 0, "english": "Save", "pt_BR": "Salvar"}],
    )
    assert len(result) == 1
    assert result[0]["es_ES"] == "Guardar"
    assert result[0]["pt_BR"] == "Salvar"
    assert result[0]["english"] == "Save"


def test_merge_creates_new_row_when_missing():
    result = _merge_per_language_results(
        base=[{"row_index": 0, "english": "Save", "es_ES": "Guardar"}],
        additions=[{"row_index": 1, "english": "Cancel", "es_ES": "Cancelar"}],
    )
    assert len(result) == 2
    assert result[0]["row_index"] == 0
    assert result[1]["row_index"] == 1


def test_merge_excludes_reviewer_note():
    result = _merge_per_language_results(
        base=[],
        additions=[{
            "row_index": 0,
            "english": "Save",
            "es_ES": "Guardar",
            "reviewer_note": "double-check register",
        }],
    )
    assert "reviewer_note" not in result[0]
    assert result[0]["es_ES"] == "Guardar"


def test_merge_returns_sorted_by_row_index():
    result = _merge_per_language_results(
        base=[],
        additions=[
            {"row_index": 2, "english": "Delete", "es_ES": "Eliminar"},
            {"row_index": 0, "english": "Save", "es_ES": "Guardar"},
            {"row_index": 1, "english": "Cancel", "es_ES": "Cancelar"},
        ],
    )
    assert [e["row_index"] for e in result] == [0, 1, 2]


def test_merge_skips_entries_without_row_index():
    result = _merge_per_language_results(
        base=[],
        additions=[
            {"english": "Save", "es_ES": "Guardar"},         # no row_index → dropped
            {"row_index": 1, "english": "Cancel", "es_ES": "Cancelar"},
        ],
    )
    assert len(result) == 1
    assert result[0]["row_index"] == 1
