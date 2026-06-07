# Monotype AI UI String Translator — Workflow & Solution Overview

**Submitted by:** Sankalp Khandelwal (sankalp.khandelwal@monotype.com)  
**Live tool:** https://huggingface.co/spaces/Sankalp546/Monotype_Translator  
**Version:** 1.0 | **Status:** Live prototype, actively used by linguist teams

---

## What It Does

The Monotype AI Translator is a multi-agent AI pipeline that translates product UI strings from English into up to five languages simultaneously:

- 🇫🇷 French (fr-FR)
- 🇩🇪 German (de-DE)
- 🇧🇷 Brazilian Portuguese (pt-BR)
- 🇪🇸 Spanish — Castilian (es-ES)
- 🇯🇵 Japanese (ja-JP)

The tool enforces Monotype's brand glossary, per-language style guides, and UI-context rules (e.g. button label conciseness, confirmation dialog structure, placeholder formatting) — without the linguist needing to look these up manually.

---

## How It Works — Architecture

The pipeline runs four AI agents in sequence:

| Agent | Role |
|-------|------|
| **Brand Analyst** | Reads the source strings, identifies UI context (button, toast, dialog, heading, etc.), and flags terminology that must follow Monotype brand rules |
| **Translator** | Translates each string into the selected languages, applying the style guide and glossary for each |
| **Translation Reviewer** | Reviews each translation for accuracy, register, placeholder integrity, and brand compliance; corrects errors |
| **Production Manager** | Assembles the final output Excel file with one column per language |

All agents are powered by **OpenAI GPT-4.1** via the OpenAI API.

---

## Linguist Workflow — Step by Step

### 1. Prepare the input file
- Create an Excel file (`.xlsx`) with English source strings in **Column A**
- A header row (`English`) in row 1 is optional — the tool auto-detects and inserts one if missing
- No other formatting required

### 2. Upload and configure
- Go to the tool URL (link above)
- Upload the `.xlsx` file
- Select target languages by clicking the language chips — **highlighted (blue) = will be translated**
  - All five are selected by default; tap any chip to deselect it
- Optionally enable **"UI Optimisation"** toggle for UI-specific string rules (button labels, dialogs, empty states)

### 3. Run the translation
- Click **Translate**
- Progress is shown in real time (typically 2–5 minutes for ~100 strings)

### 4. Download output
- A translated `.xlsx` file is generated with:
  - Column A: original English strings
  - One column per selected language
- Download and review — the file is ready for linguist post-editing

---

## What the Tool Enforces Automatically

The AI agents reference language-specific style guides covering:

| Rule Category | Example |
|---------------|---------|
| Button label conciseness | "Activate all users" → `すべてのユーザーを有効化` (no trailing する) |
| Confirmation dialog structure | Consequence first, question second |
| Brand vocabulary | `ライブラリ` not `ライブラリー`; `função` not `papel`; `espacio de trabajo` not `área de trabajo` |
| Placeholder formatting | `{{count}}` preserved exactly; inner spaces stripped |
| Voice and register | Active voice for toast messages; formal `vous` in French; `tú` in Spanish |
| Untranslatable terms | Monotype, MyFonts, Mosaic, SkyFonts always remain in English |

---

## Current Capabilities & Limitations

| Capability | Status |
|------------|--------|
| Languages supported | FR, DE, pt-BR, es-ES, JA |
| Input format | Excel (.xlsx) only |
| Max strings per batch | ~100 strings (recommended); larger batches split automatically |
| Glossary enforcement | ✅ Built into agent knowledge base |
| Style guide enforcement | ✅ Per-language rules in markdown knowledge files |
| Translation Memory (TM) integration | ❌ Not yet — planned backlog item |
| SSO / internal auth | ❌ Not yet — currently open prototype |
| Hosting | HuggingFace Spaces (free tier) |
| API cost | OpenAI API — per-token billing |

---

## Technology Stack

- **AI Framework:** CrewAI (multi-agent orchestration)
- **LLM:** OpenAI GPT-4.1
- **Backend:** Python, FastAPI
- **Hosting:** HuggingFace Spaces
- **Input/Output:** openpyxl (Excel processing)
- **Knowledge base:** Markdown style guides per language + shared glossary

---

## Business Value

| Metric | Before | After |
|--------|--------|-------|
| Time to translate 100 strings (5 languages) | ~2–3 days (manual) | ~3–5 minutes |
| Consistency of brand terminology | Varies by linguist | Enforced by AI agents |
| Style guide lookup | Manual per string | Automated |
| Linguist role | Full translation | Post-editing + QA |

The tool does not replace linguists — it produces a **strong first draft** that linguists review, correct, and approve. This shifts their effort from translation to quality assurance, significantly reducing turnaround time.

---

## Next Steps / Roadmap

1. Collect feedback from all 5 language teams and refine style guides
2. Add Translation Memory (TM) integration to re-use previously approved strings
3. Evaluate hosting on Monotype internal infrastructure (requires IT support)
4. Add support for additional languages (es-419 Latin American Spanish, zh-CN, ko-KR)
5. Explore integration with the Monotype Fonts product localization pipeline
