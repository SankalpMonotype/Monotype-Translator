# Monotype Translation Crew — Backlog

Known gaps and improvements identified in the audit (2026-05-25).
Items are grouped by priority. None are blocking for current use.

---

## 🔴 High Priority

### 1. Agent execution limits
**Files:** `src/monotype_translation_crew/crew.py`  
**Issue:** No `max_iter` or `max_execution_time` set on any agent — a stuck agent loops indefinitely.  
**Fix:** Add `max_iter=10` / `max_execution_time=720` to brand_analyst; `max_iter=5` / `max_execution_time=600` to translator; `max_iter=3` / `max_execution_time=300` to reviewer; `max_iter=5` / `max_execution_time=120` to production_manager.

### 2. Concurrent job race condition
**Files:** `src/monotype_translation_crew/crew.py`, `src/monotype_translation_crew/api.py`  
**Issue:** All jobs write reviewed translations to the same `outputs/reviewed_translations.json`. Two simultaneous uploads overwrite each other's data.  
**Fix:** Use `threading.local()` in `crew.py` to store a per-job ID; derive the output filename as `reviewed_translations_{job_id}.json`; set the context from `api.py` before calling `kickoff()`.

### 3. No retry on failed translation batch
**Files:** `src/monotype_translation_crew/api.py` — `_run_job()` around line 1583  
**Issue:** A transient LLM or network error on any batch immediately marks the whole job failed with no retry.  
**Fix:** Wrap `crew().kickoff()` in a retry loop (2 attempts, 5 s pause between) before propagating the exception.

---

## 🟠 Medium Priority

### 4. German dialog forms missing from review checklist
**Files:** `src/monotype_translation_crew/config/tasks.yaml` — `review_task`  
**Issue:** `translation_task` defines 4 distinct German dialog patterns but `review_task` never checks them — incorrect dialog forms pass review undetected.  
**Fix:** Add a `[ ] German dialog forms` checkpoint to the review checklist covering all four patterns (notification / short label / confirmation body / affirmation button).

### 5. No tone selection in the UI
**Files:** `src/monotype_translation_crew/api.py` — configure view HTML (~line 449)  
**Issue:** `tone` defaults to `"informal"` hardcoded in JS (`selectedTone = 'informal'`). There is no toggle to switch to formal tone before starting a job.  
**Fix:** Add a two-option toggle (Informal / Formal) in the configure screen between the length toggle and the Start button; wire it to `selectedTone`.

### 6. Malformed JSON not recovered
**Files:** `src/monotype_translation_crew/api.py` — `_extract_json_array()` (~line 1273)  
**Issue:** If the LLM returns JSON with a missing comma or unescaped quote, `json.loads` raises and the batch silently fails (falls back to English copy).  
**Fix:** Add basic JSON repair before parsing — strip trailing commas, attempt truncation at last `}` if loads fails, log the raw output on failure for debugging.

---

## 🟡 Low Priority

### 7. Outputs folder grows indefinitely
**Files:** `src/monotype_translation_crew/api.py` — `lifespan` startup  
**Issue:** Every job writes translated `.xlsx` / `.zip` and a `.md` report to `outputs/`. No cleanup policy — 120+ files already present.  
**Fix:** On server startup, delete output files older than 30 days.

### 8. Unpinned major version ranges
**Files:** `pyproject.toml`  
**Issue:** `crewai[tools] >=0.175.0,<1.0.0` and `litellm >=1.0.0` — a future minor release can introduce breaking changes and auto-upgrade will pick it up.  
**Fix:** After testing a known-good version, pin to a narrow range (e.g. `>=0.185,<0.190`).

### 9. Filename sanitisation
**Files:** `src/monotype_translation_crew/api.py` — `start_translation()` (~line 1118)  
**Issue:** Uploaded filenames with `/`, `\`, `*`, or `?` pass through directly into the path `uploads/{job_id}_{fname}`.  
**Fix:** Apply `re.sub(r'[^\w\-. ]', '_', fname)` before constructing `safe_name`.

### 10. Merged cell handling
**Files:** `src/monotype_translation_crew/tools/excel_tools.py` — `read_excel_for_translation()`  
**Issue:** openpyxl silently drops data in merged cells (value only in the top-left cell). No warning surfaced to the user.  
**Fix:** Detect merged cell ranges on the header row and warn in the return value if any language column is part of a merge.

---

## ✅ Completed (reference)

| Item | Commit |
|------|--------|
| 5 per-language knowledge files (ja, pt_BR, es_ES, fr, de) | bfaadbd |
| Mandatory glossary-first lookup in translation_task | bfaadbd |
| Verbatim glossary reproduction in brand_context_task | bfaadbd |
| PT-BR linguist terminology applied | 3810cf7 |
| ES-ES linguist terminology applied | 4721572 |
| 7 new Japanese quality rules | 0a3d278 |
| Template variable dummy fix (foundry, name) | fd40335, a10c5fd |
