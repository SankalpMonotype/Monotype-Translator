# CLAUDE.md — Monotype Translation Crew

Guidance for Claude Code when working on this repository. Read this on every session before touching code.

## What this project does

Translates English UI strings into 5 target languages — French (fr), German (de), Brazilian Portuguese (pt_BR), Japanese (ja), Latin American Spanish (es_ES) — for Monotype web properties (monotype.com, fonts.com, MyFonts, Monotype Fonts SaaS).

Input: Excel (.xlsx) or Word (.docx) files with English source text.
Output: Same file format with translations populated in per-language columns/sections.

## Architecture (current state — being refactored)

Four-agent sequential CrewAI pipeline:

1. **brand_analyst** — reads `knowledge/*.md` (brand guidelines, glossary, per-language guides, translation memory), produces a brand context document for downstream agents
2. **translator** — reads the source file via `read_excel_for_translation` / `read_docx_for_translation`, produces translations in JSON
3. **translation_reviewer** — receives translator output via context (no tools), critiques and returns corrected JSON
4. **production_manager** — writes reviewed translations back to Excel/Docx

Orchestrated in two places:
- `src/monotype_translation_crew/crew.py` — `MonotypeTranslationCrew` (Excel flow, `@CrewBase` decorator) and `DocxTranslationCrew` (Word flow, plain class)
- `src/monotype_translation_crew/config/tasks.yaml` — task descriptions
- `src/monotype_translation_crew/config/agents.yaml` — agent roles and backstories
- `src/monotype_translation_crew/config/docx_tasks.yaml` — Word-specific task variants

API surface in `src/monotype_translation_crew/api.py` (FastAPI) — upload, preview, translate, status, download endpoints. Deployed on HuggingFace Spaces.

## Critical constraints — DO NOT VIOLATE

### Per-language rule isolation
Language-specific rules MUST stay isolated per language. The single biggest source of translation quality bugs in this codebase is cross-language contamination — for example, Portuguese feminine-article rules leaking into Spanish output. When refactoring, prefer per-language fan-out (N parallel translation tasks, one per requested language) over single-prompt multi-language translation.

### Validators are guardrails, not suggestions
`tools/glossary_validator.py` and `tools/placeholder_validator.py` are deterministic safety nets that catch the model when it ignores prompt instructions. Do not bypass, weaken, or "make smarter with an LLM." If a validator rejects output, the right fix is to make the model produce correct output, not to relax the validator.

### Knowledge base is the source of truth
`knowledge/glossary.md`, `knowledge/brand_guidelines.md`, and `knowledge/*_guide.md` are the source of truth for translation rules. The brand_analyst step should retrieve from these files, not synthesize or summarize them. Lossy summarization in the analyst step is a known failure mode — the V3 benchmark improvements (49.9% → 59.2% exact match) came from making rules more specific and reducing summarization, not the reverse.

### Glossary import goes through `import_glossary.py`
When linguists update SharePoint glossary Excels, run `import_glossary.py` to merge into `knowledge/glossary.md`. Never hand-edit `glossary.md` for routine linguist updates. Always commit the `.bak` backup with the change so the previous state is recoverable.

## Files Claude Code should NEVER modify without explicit instruction

- `tools/excel_tools.py`, `tools/docx_tools.py` — battle-tested file I/O, complex format preservation
- `tools/glossary_validator.py`, `tools/placeholder_validator.py` — deterministic guardrails
- `api.py` — public API surface, contract with the frontend
- `knowledge/glossary.md` — modified only via `import_glossary.py`

If a refactor seems to require touching these, stop and propose the change separately first.

## Files that are safe to refactor

- `crew.py` — orchestration, expected to evolve as the architecture matures
- `config/tasks.yaml`, `config/docx_tasks.yaml` — prompt engineering surface, expected to evolve
- `config/agents.yaml` — agent backstories
- `import_glossary.py` — utility script, easy to extend

## Working style for this repo

1. **Read before editing.** When a session starts, read `CLAUDE.md`, then the files relevant to the request, before proposing any change.
2. **Plan, approve, execute.** For any change touching more than one file, show a plan first (file-level diff outline). Wait for approval before editing.
3. **Small commits.** One concern per commit. If a task touches `crew.py` and `tasks.yaml`, those are two commits, not one.
4. **Preserve behavior unless asked to change it.** If a refactor would change observable output (translation quality, file format, API response shape), call it out explicitly before doing it.
5. **No new dependencies without asking.** This project runs on HuggingFace Spaces with a fixed dependency set; new packages need explicit approval.

## Known issues being addressed

1. **Cross-language contamination** — Portuguese rules leaking into Spanish translations. Fix in progress: per-language fan-out.
2. **Brand guideline drift** — Spanish linguist reports translations not following the style guide. Same root cause as #1 (single-prompt multi-language translation + lossy brand_analyst synthesis).
3. **Per-language model gap** — Japanese exact-match rate (~46%) significantly below Portuguese (~69%) on V3 benchmarks. Fix planned: route Japanese to a different LiteLLM model.
4. **Translation memory not active** — `knowledge/tm/` folder exists but is empty. Fix planned: populate from linguist-approved translations, add exact-match lookup before the translator agent runs.

## Running locally

```bash
# Install dependencies
pip install -e .

# Run a translation against a sample Excel
python -m monotype_translation_crew.main translate \
  --excel input.xlsx \
  --target-languages fr,de,pt_BR,ja,es_ES

# Run the FastAPI server (for UI testing)
uvicorn monotype_translation_crew.api:app --reload
```

## Testing

Benchmark harness in `compare_translations.py` and `analyze_translation_gaps.py`. Always run against the linguist reference set before merging prompt or agent changes — quality regressions are easy to introduce and hard to spot in casual review.
