"""FastAPI web application for Monotype Translation Crew.

Exposes a single-page web UI where users can:
  - Upload an .xlsx file
  - Watch a progress indicator while the CrewAI pipeline runs
  - Download the translated Excel output
  - Browse a review table of all translated strings

Known limitation: reviewed_translations.json is a shared file in outputs/.
Running two jobs concurrently will cause the review data to be overwritten.
For single-user / small-team use this is fine.
"""

import asyncio
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

# ---------------------------------------------------------------------------
# File-format converters  (PDF / DOCX → translation-ready .xlsx)
# ---------------------------------------------------------------------------

_XLSX_HEADERS = ["English", "French", "German", "Portuguese (pt-BR)", "Japanese", "Spanish (es-419)"]


def _write_strings_xlsx(strings: list[str], xlsx_path: str) -> None:
    """Write a flat list of strings into a 6-column translation Excel."""
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Translations"
    ws.append(_XLSX_HEADERS)
    for s in strings:
        if s and s.strip():
            ws.append([s.strip(), "", "", "", "", ""])
    wb.save(xlsx_path)


def _pdf_to_xlsx(pdf_path: str, xlsx_path: str) -> None:
    import pdfplumber
    strings: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in (page.extract_tables() or []):
                for row in table:
                    for cell in row:
                        if cell and cell.strip():
                            strings.append(cell.strip())
            if not strings:                # fallback: raw text lines
                text = page.extract_text() or ""
                strings.extend(l.strip() for l in text.splitlines() if l.strip())
    if not strings:
        raise ValueError("No readable text found in the PDF.")
    _write_strings_xlsx(strings, xlsx_path)


def _docx_to_xlsx(docx_path: str, xlsx_path: str) -> None:
    from docx import Document
    doc = Document(docx_path)
    strings: list[str] = []
    seen: set[str] = set()
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                t = cell.text.strip()
                if t and t not in seen:
                    seen.add(t)
                    strings.append(t)
    if len(strings) < 2:        # no useful tables — fall back to paragraphs
        strings = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    if not strings:
        raise ValueError("No readable text found in the document.")
    _write_strings_xlsx(strings, xlsx_path)


def _convert_to_xlsx(src: Path, dst: Path) -> None:
    """Convert PDF or DOCX to a translation-ready .xlsx at *dst*."""
    ext = src.suffix.lower()
    if ext == ".pdf":
        _pdf_to_xlsx(str(src), str(dst))
    elif ext in (".docx", ".doc"):
        _docx_to_xlsx(str(src), str(dst))
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# ---------------------------------------------------------------------------
# Job store (in-memory; lost on server restart)
# ---------------------------------------------------------------------------
JOBS: dict[str, dict] = {}

# Thread pool — CrewAI is synchronous, so we run it off the event loop
_executor = ThreadPoolExecutor(max_workers=2)


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    Path("uploads").mkdir(exist_ok=True)
    Path("outputs").mkdir(exist_ok=True)
    yield


app = FastAPI(title="Monotype Translation Crew", version="1.0.0", lifespan=lifespan)


# ---------------------------------------------------------------------------
# Embedded single-page frontend
# ---------------------------------------------------------------------------

_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Monotype Translation Crew</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      --ink:    #0D0D0D;
      --paper:  #F8F6F2;
      --mist:   #F0EDE7;
      --border: #E3DFD9;
      --muted:  #73706A;
      --subtle: #B3B0AB;
    }
    html { background: var(--paper); }
    body { background: var(--paper); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; }
    .serif { font-family: Georgia, 'Times New Roman', serif; }

    /* ── Animations ── */
    @keyframes spin       { to { transform: rotate(360deg); } }
    @keyframes pulse-dot  { 0%,100% { opacity:1; box-shadow: 0 0 0 0 rgba(13,13,13,.3); }
                             50%    { opacity:.7; box-shadow: 0 0 0 4px rgba(13,13,13,0); } }
    @keyframes fade-up    { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
    @keyframes slide-up   { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
    @keyframes shimmer    { 0% { transform:translateX(-100%); } 100% { transform:translateX(400%); } }
    @keyframes draw-check { to { stroke-dashoffset: 0; } }

    .anim-fade-up  { animation: fade-up  .4s cubic-bezier(.16,1,.3,1) both; }
    .anim-slide-up { animation: slide-up .5s cubic-bezier(.16,1,.3,1) both; }

    /* ── Drop zone ── */
    #drop-zone { border: 1.5px dashed var(--border); transition: border-color .2s, background .2s; }
    #drop-zone:hover  { border-color: var(--muted); }
    #drop-zone.active { border-color: var(--ink) !important; border-style: solid !important; background: var(--mist) !important; }
    #drop-zone.active .drop-arrow { transform: translateY(-4px); }
    .drop-arrow { transition: transform .25s cubic-bezier(.16,1,.3,1); }

    /* ── Step indicators ── */
    .step .dot {
      width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
      border: 1.5px solid var(--border); background: transparent;
      transition: background .3s, border-color .3s;
      position: relative;
    }
    .step.active .dot {
      border-color: var(--ink); background: var(--ink);
      animation: pulse-dot 1.6s ease-in-out infinite;
    }
    .step.done .dot {
      border-color: var(--ink); background: var(--ink);
    }
    .step.done .dot::after {
      content: '';
      position: absolute; top: 50%; left: 50%;
      width: 3px; height: 5px;
      border-right: 1.5px solid white; border-bottom: 1.5px solid white;
      transform: translate(-65%, -65%) rotate(45deg);
    }
    .step .name { font-size: 12px; color: var(--subtle); transition: color .3s, font-weight .3s; }
    .step.active .name { color: var(--ink); font-weight: 500; }
    .step.done   .name { color: var(--muted); }

    /* ── Progress bar ── */
    #progress-bar { transition: width .8s cubic-bezier(.4,0,.2,1); position: relative; overflow: hidden; }
    #progress-bar::after {
      content: ''; position: absolute; top:0; left:0; height:100%; width:35%;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,.5), transparent);
      animation: shimmer 2.2s ease infinite;
    }

    /* ── Insight card ── */
    #insight-wrap { transition: opacity .35s ease; }

    /* ── Buttons ── */
    .btn-ink {
      background: var(--ink); color: white;
      border-radius: 12px; cursor: pointer;
      transition: background .15s, transform .1s;
      letter-spacing: .04em;
    }
    .btn-ink:hover:not(:disabled) { background: #2a2a2a; }
    .btn-ink:active:not(:disabled){ transform: scale(.98); }
    .btn-ink:disabled { opacity: .28; cursor: not-allowed; }

    .btn-ghost {
      border: 1px solid var(--border); color: var(--muted);
      border-radius: 12px; cursor: pointer;
      transition: background .15s;
      letter-spacing: .03em;
    }
    .btn-ghost:hover { background: var(--mist); }

    /* ── Review table ── */
    #review-thead th { background: var(--paper); border-bottom: 1px solid var(--border); position: sticky; top: 0; }
    #review-tbody tr:nth-child(even) { background: var(--paper); }
    #review-tbody tr:hover { background: #EEF0FF22; }
  </style>
</head>
<body style="background:var(--paper); min-height:100vh;">

<!-- ── Header ── -->
<header style="background:white; border-bottom:1px solid var(--border); position:sticky; top:0; z-index:10;">
  <div style="max-width:680px; margin:0 auto; padding:14px 24px; display:flex; align-items:center; justify-content:space-between;">
    <div id="logo-home" style="display:flex; align-items:center; gap:10px; cursor:pointer; user-select:none;" title="Back to home">
      <div style="width:26px; height:26px; background:var(--ink); border-radius:4px; display:flex; align-items:center; justify-content:center;">
        <span style="color:white; font-size:11px; font-weight:700; letter-spacing:-.01em;">M</span>
      </div>
      <span style="font-size:14px; font-weight:600; color:var(--ink); letter-spacing:-.01em;">Monotype</span>
    </div>
    <span style="font-size:11px; color:var(--subtle); letter-spacing:.08em; text-transform:uppercase;">Translation Crew</span>
  </div>
</header>

<main style="max-width:680px; margin:0 auto; padding:48px 24px 80px;">

  <!-- ══════════════════════════════════════════════════════ -->
  <!-- VIEW: UPLOAD                                           -->
  <!-- ══════════════════════════════════════════════════════ -->
  <div id="view-upload" class="anim-fade-up">

    <!-- Headline -->
    <h1 class="serif" style="font-size:3rem; line-height:1.08; color:var(--ink); margin-bottom:12px; letter-spacing:-.02em;">
      Translate your<br>UI strings.
    </h1>
    <p style="font-size:14px; color:var(--muted); line-height:1.65; max-width:460px; margin-bottom:36px;">
      Upload a file containing English source strings. The AI crew translates them into
      French, German, Portuguese, Japanese, and Spanish — guided by Monotype brand standards.
    </p>

    <!-- Drop zone -->
    <div id="drop-zone" style="border-radius:14px; padding:32px; cursor:pointer; background:white;">
      <div style="display:flex; align-items:center; gap:20px;">
        <!-- Icon -->
        <div class="drop-arrow" style="flex-shrink:0; width:52px; height:52px; border-radius:12px;
             background:var(--mist); display:flex; align-items:center; justify-content:center;">
          <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
            <path d="M11 14V4M11 4L8 7M11 4L14 7" stroke="var(--muted)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M3 16v1.5A1.5 1.5 0 004.5 19h13a1.5 1.5 0 001.5-1.5V16" stroke="var(--muted)" stroke-width="1.6" stroke-linecap="round"/>
          </svg>
        </div>
        <!-- Text -->
        <div>
          <p style="font-size:14px; font-weight:500; color:var(--ink); margin-bottom:4px;">
            Drop your file here
          </p>
          <p style="font-size:13px; color:var(--subtle); margin-bottom:8px;">
            or <button id="browse-btn" style="color:var(--ink); text-decoration:underline; text-underline-offset:3px;
               background:none; border:none; cursor:pointer; font-size:13px; font-weight:500; padding:0;">browse to upload</button>
          </p>
          <!-- Format badges -->
          <div style="display:flex; gap:5px; flex-wrap:wrap;">
            <span style="font-size:10px; padding:2px 7px; border-radius:4px; background:var(--mist); color:var(--muted); letter-spacing:.02em;">.xlsx</span>
            <span style="font-size:10px; padding:2px 7px; border-radius:4px; background:var(--mist); color:var(--muted); letter-spacing:.02em;">.pdf</span>
            <span style="font-size:10px; padding:2px 7px; border-radius:4px; background:var(--mist); color:var(--muted); letter-spacing:.02em;">.docx</span>
            <span style="font-size:10px; padding:2px 7px; border-radius:4px; background:var(--mist); color:var(--subtle); letter-spacing:.02em;">Max 10 MB</span>
          </div>
        </div>
      </div>
    </div>
    <input type="file" id="file-input" accept=".xlsx,.pdf,.docx,.doc" style="display:none;">

    <!-- File selected card -->
    <div id="file-card" style="display:none; margin-top:10px; padding:12px 16px; border-radius:12px;
         background:var(--mist); border:1px solid var(--border); align-items:center; gap:12px;">
      <div style="width:34px; height:34px; border-radius:8px; background:white; border:1px solid var(--border);
           display:flex; align-items:center; justify-content:center; flex-shrink:0;">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M8 1H3a1 1 0 00-1 1v10a1 1 0 001 1h8a1 1 0 001-1V6L8 1z" stroke="var(--muted)" stroke-width="1.2"/>
          <path d="M8 1v5h5" stroke="var(--muted)" stroke-width="1.2" stroke-linecap="round"/>
        </svg>
      </div>
      <div style="flex:1; min-width:0;">
        <p id="file-name" style="font-size:13px; font-weight:500; color:var(--ink); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;"></p>
        <p id="file-size" style="font-size:11px; color:var(--subtle); margin-top:2px;"></p>
      </div>
      <button id="remove-file" style="width:22px; height:22px; border-radius:50%; border:none; background:none;
              cursor:pointer; color:var(--subtle); display:flex; align-items:center; justify-content:center; padding:0;">
        <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
          <path d="M1 1l8 8M9 1L1 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </button>
    </div>

    <!-- CTA -->
    <button id="translate-btn" disabled class="btn-ink"
            style="width:100%; padding:14px; font-size:13px; font-weight:600; border:none;
                   margin-top:10px; letter-spacing:.05em; text-transform:uppercase;">
      Start Translation
    </button>

    <!-- Language tags -->
    <div style="display:flex; align-items:center; gap:8px; margin-top:20px; flex-wrap:wrap;">
      <span style="font-size:10px; color:var(--subtle); letter-spacing:.06em; text-transform:uppercase;">Translates to</span>
      <div style="display:flex; gap:5px;">
        <span style="font-size:11px; padding:3px 8px; border-radius:4px; background:var(--mist); color:var(--muted);">FR</span>
        <span style="font-size:11px; padding:3px 8px; border-radius:4px; background:var(--mist); color:var(--muted);">DE</span>
        <span style="font-size:11px; padding:3px 8px; border-radius:4px; background:var(--mist); color:var(--muted);">PT</span>
        <span style="font-size:11px; padding:3px 8px; border-radius:4px; background:var(--mist); color:var(--muted);">JA</span>
        <span style="font-size:11px; padding:3px 8px; border-radius:4px; background:var(--mist); color:var(--muted);">ES</span>
      </div>
    </div>
  </div>

  <!-- ══════════════════════════════════════════════════════ -->
  <!-- VIEW: PROCESSING                                       -->
  <!-- ══════════════════════════════════════════════════════ -->
  <div id="view-processing" style="display:none;" class="anim-fade-up">

    <!-- File row + elapsed -->
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:20px;">
      <div style="display:flex; align-items:center; gap:8px;">
        <svg width="12" height="14" viewBox="0 0 12 14" fill="none">
          <path d="M7 1H2a1 1 0 00-1 1v10a1 1 0 001 1h8a1 1 0 001-1V5L7 1z" stroke="var(--subtle)" stroke-width="1.2"/>
          <path d="M7 1v4h4" stroke="var(--subtle)" stroke-width="1.2" stroke-linecap="round"/>
        </svg>
        <span id="proc-filename" style="font-size:12px; font-weight:500; color:var(--muted);"></span>
      </div>
      <span id="elapsed-disp" style="font-size:12px; color:var(--subtle); font-variant-numeric:tabular-nums;"></span>
    </div>

    <!-- Progress bar -->
    <div style="margin-bottom:28px;">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
        <span id="progress-stage-label" style="font-size:12px; color:var(--muted); font-weight:500;">Initialising…</span>
        <span id="progress-pct" style="font-size:12px; color:var(--subtle); font-variant-numeric:tabular-nums; font-weight:500;">0%</span>
      </div>
      <div style="height:6px; background:var(--mist); border-radius:6px; overflow:hidden;">
        <div id="progress-bar" style="height:100%; background:var(--ink); width:2%; border-radius:6px;"></div>
      </div>
    </div>

    <!-- Two-column: stages + insight -->
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:32px; align-items:start;">

      <!-- Stages -->
      <div>
        <p style="font-size:10px; color:var(--subtle); letter-spacing:.1em; text-transform:uppercase; margin-bottom:16px; font-weight:600;">Progress</p>
        <div id="stage-list" style="display:flex; flex-direction:column; gap:12px;"></div>
      </div>

      <!-- Insight card -->
      <div>
        <p style="font-size:10px; color:var(--subtle); letter-spacing:.1em; text-transform:uppercase; margin-bottom:16px; font-weight:600;">Did you know</p>
        <div id="insight-wrap"
             style="background:white; border:1px solid var(--border); border-radius:14px; padding:20px; min-height:160px;">
          <p id="insight-title" style="font-size:12px; font-weight:600; color:var(--ink); margin-bottom:8px;"></p>
          <p id="insight-body"  style="font-size:12px; line-height:1.7; color:var(--muted);"></p>
          <div id="insight-dots" style="display:flex; gap:5px; margin-top:16px;"></div>
        </div>
      </div>
    </div>

    <p style="font-size:11px; color:var(--subtle); text-align:center; margin-top:32px; line-height:1.6;">
      This usually takes 3–8 minutes — you can leave this tab open.
    </p>
    <p id="job-id-disp" style="font-size:10px; color:var(--border); text-align:center; font-family:monospace; margin-top:6px;"></p>

    <div style="text-align:center; margin-top:20px;">
      <button id="cancel-btn" class="btn-ghost"
              style="padding:10px 32px; font-size:12px; font-weight:500;
                     letter-spacing:.05em; text-transform:uppercase; background:none;">
        Cancel Translation
      </button>
    </div>

  </div>

  <!-- ══════════════════════════════════════════════════════ -->
  <!-- VIEW: RESULTS                                          -->
  <!-- ══════════════════════════════════════════════════════ -->
  <div id="view-results" style="display:none;">

    <!-- Success headline -->
    <div style="text-align:center; margin-bottom:36px;" class="anim-slide-up">
      <div style="width:48px; height:48px; border-radius:50%; background:#F0FDF4; border:1px solid #BBF7D0;
           display:inline-flex; align-items:center; justify-content:center; margin-bottom:16px;">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path id="check-path" d="M4 10.5l4 4 8-8" stroke="#16A34A" stroke-width="1.75"
                stroke-linecap="round" stroke-linejoin="round"
                stroke-dasharray="20" stroke-dashoffset="20"
                style="animation: draw-check .5s .1s ease forwards;"/>
        </svg>
      </div>
      <h2 class="serif" style="font-size:2rem; color:var(--ink); letter-spacing:-.02em; margin-bottom:8px;">
        Translation complete.
      </h2>
      <p id="result-summary" style="font-size:14px; color:var(--muted);"></p>
    </div>

    <!-- Download CTA -->
    <div style="background:var(--ink); border-radius:16px; padding:20px 24px; display:flex;
         align-items:center; justify-content:space-between; gap:16px; margin-bottom:20px;">
      <div>
        <p style="font-size:13px; font-weight:600; color:white; margin-bottom:4px;">Download your translations</p>
        <p id="dl-filename" style="font-size:12px; color:rgba(255,255,255,.45);"></p>
      </div>
      <button id="download-btn"
              style="display:flex; align-items:center; gap:8px; padding:10px 20px; border-radius:10px;
                     background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.15);
                     color:white; font-size:12px; font-weight:600; cursor:pointer; white-space:nowrap;
                     letter-spacing:.04em; text-transform:uppercase; transition:background .15s;"
              onmouseover="this.style.background='rgba(255,255,255,.18)'"
              onmouseout="this.style.background='rgba(255,255,255,.1)'">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
          <path d="M6.5 1v8M3.5 6l3 3 3-3" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M1 10v1a1.5 1.5 0 001.5 1.5h8A1.5 1.5 0 0012 11v-1" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        Download
      </button>
    </div>

    <!-- Review table -->
    <div style="background:white; border:1px solid var(--border); border-radius:16px; overflow:hidden; margin-bottom:16px;">
      <div style="padding:16px 20px; border-bottom:1px solid var(--border); background:var(--paper);
           display:flex; align-items:center; justify-content:space-between; gap:12px;">
        <p style="font-size:11px; font-weight:700; color:var(--muted); letter-spacing:.07em; text-transform:uppercase; white-space:nowrap;">
          Review Translations
        </p>
        <input id="search-input" type="text" placeholder="Search strings…"
               style="font-size:12px; padding:7px 12px; border-radius:8px; border:1px solid var(--border);
                      background:white; color:var(--ink); width:180px; outline:none; transition:border-color .15s;"
               onfocus="this.style.borderColor='var(--muted)'" onblur="this.style.borderColor='var(--border)'"/>
      </div>
      <div style="overflow-x:auto; max-height:440px; overflow-y:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:12px;">
          <thead id="review-thead"></thead>
          <tbody id="review-tbody"></tbody>
        </table>
      </div>
      <p id="no-matches" style="display:none; text-align:center; font-size:12px; color:var(--subtle); padding:24px;">
        No matching strings.
      </p>
    </div>

    <button id="btn-new" class="btn-ghost"
            style="width:100%; padding:13px; font-size:12px; font-weight:500; background:none;
                   text-transform:uppercase; letter-spacing:.05em;">
      Translate another file
    </button>
  </div>

  <!-- ══════════════════════════════════════════════════════ -->
  <!-- VIEW: ERROR                                            -->
  <!-- ══════════════════════════════════════════════════════ -->
  <div id="view-error" style="display:none; text-align:center; padding:48px 0;" class="anim-fade-up">
    <div style="width:48px; height:48px; border-radius:50%; background:#FFF1F2; border:1px solid #FECDD3;
         display:inline-flex; align-items:center; justify-content:center; margin-bottom:16px;">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 7v3M10 13.5h.01M10 1L1.5 17h17L10 1z" stroke="#E11D48" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <h3 class="serif" style="font-size:1.75rem; color:var(--ink); letter-spacing:-.02em; margin-bottom:10px;">
      Translation failed.
    </h3>
    <p id="error-text" style="font-size:13px; color:var(--muted); max-width:380px; margin:0 auto 28px; line-height:1.6;"></p>
    <button id="btn-retry" class="btn-ink"
            style="padding:12px 32px; font-size:13px; font-weight:600; border:none; letter-spacing:.04em;">
      Try again
    </button>
  </div>

</main>

<script>
// ── Data ─────────────────────────────────────────────────────────────────────
const LANG_LABELS = {
  en: 'English', fr: 'French', de: 'German',
  pt_BR: 'Portuguese (pt-BR)', ja: 'Japanese', es_419: 'Spanish (es-419)'
};

const PIPELINE_STAGES = [
  { id: 'parse',   label: 'Parsing your file',              est: 0   },
  { id: 'brand',   label: 'Loading brand guidelines',        est: 8   },
  { id: 'context', label: 'Building translation context',    est: 22  },
  { id: 'fr',      label: 'Translating to French',           est: 70  },
  { id: 'de',      label: 'Adapting for German grammar',     est: 120 },
  { id: 'pt',      label: 'Localising for Portuguese',       est: 170 },
  { id: 'ja',      label: 'Localising for Japanese',         est: 220 },
  { id: 'es',      label: 'Translating to Spanish',          est: 270 },
  { id: 'review',  label: 'Reviewing all translations',      est: 320 },
  { id: 'report',  label: 'Generating production report',    est: 430 },
];

const INSIGHTS = [
  { title: 'Japanese script systems',
    body: 'Japanese UI strings are typically 40–60% shorter than English equivalents, despite blending three writing systems: Hiragana, Katakana, and Kanji.' },
  { title: 'French typographic convention',
    body: 'French typography requires a non-breaking space before double punctuation — colons, semicolons, question marks, and exclamation points — by convention.' },
  { title: 'German compound words',
    body: '"Zugriffsschlüssel" (access key) is a single compound noun. German combines words freely, which can significantly extend UI element widths.' },
  { title: 'Latin American Spanish',
    body: 'es-419 targets Latin America, not Spain. Vocabulary, formality register, and some grammar structures differ meaningfully from Castilian Spanish.' },
  { title: 'Brazilian Portuguese',
    body: 'Brazilian Portuguese (pt-BR) diverges substantially from European Portuguese in vocabulary, orthography, and everyday grammar structures.' },
  { title: 'The craft of localisation',
    body: 'True localisation adapts tone, cultural references, date formats, and sentence structure — not just individual vocabulary words.' },
  { title: 'Monotype type heritage',
    body: "Monotype's library holds over 150,000 fonts, spanning centuries of typographic history — from Garamond to Helvetica to bespoke brand typefaces." },
  { title: 'String length variance',
    body: 'The same phrase can be 30% longer in German and 50% shorter in Japanese. Good UI design accommodates text expansion in every language.' },
];

// ── State ─────────────────────────────────────────────────────────────────────
let selectedFile  = null;
let currentJobId  = null;
let pollTimer     = null;
let elapsedTimer  = null;
let insightTimer  = null;
let startedAt     = null;
let insightIdx    = 0;
let allRows       = [];

// ── DOM helpers ───────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);

function showEl(id, flex) {
  const el = $(id);
  el.style.display = flex ? 'flex' : 'block';
}
function hideEl(id) { $(id).style.display = 'none'; }

function switchView(name) {
  ['upload','processing','results','error'].forEach(v => hideEl('view-' + v));
  const el = $('view-' + name);
  el.style.display = 'block';
  el.classList.remove('anim-fade-up', 'anim-slide-up');
  void el.offsetWidth;
  el.classList.add('anim-fade-up');
}

function fmtBytes(b) {
  return b < 1024 ? b + ' B' : b < 1048576 ? (b/1024).toFixed(1) + ' KB' : (b/1048576).toFixed(1) + ' MB';
}

function esc(v) {
  return String(v ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── File handling ─────────────────────────────────────────────────────────────
const dropZone = $('drop-zone');
dropZone.addEventListener('dragover',  e => { e.preventDefault(); dropZone.classList.add('active'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('active'));
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('active');
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});
dropZone.addEventListener('click', e => { if (e.target.id !== 'browse-btn') $('file-input').click(); });
$('browse-btn').addEventListener('click', e => { e.stopPropagation(); $('file-input').click(); });
$('file-input').addEventListener('change', () => { if ($('file-input').files[0]) handleFile($('file-input').files[0]); });
$('remove-file').addEventListener('click', clearFile);

function handleFile(file) {
  const ok = /\.(xlsx|pdf|docx|doc)$/i.test(file.name);
  if (!ok) { alert('Please upload an .xlsx, .pdf, or .docx file.'); return; }
  if (file.size > 10 * 1024 * 1024) { alert('File must be smaller than 10 MB.'); return; }
  selectedFile = file;
  $('file-name').textContent = file.name;
  $('file-size').textContent = fmtBytes(file.size);
  hideEl('drop-zone');
  showEl('file-card', true);
  $('translate-btn').disabled = false;
}

function clearFile() {
  selectedFile = null; $('file-input').value = '';
  hideEl('file-card'); showEl('drop-zone');
  $('translate-btn').disabled = true;
}

// ── Start translation ──────────────────────────────────────────────────────────
$('translate-btn').addEventListener('click', startTranslation);

async function startTranslation() {
  if (!selectedFile) return;
  $('translate-btn').disabled = true;
  const fd = new FormData();
  fd.append('file', selectedFile);
  try {
    const res = await fetch('/api/translate', { method: 'POST', body: fd });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    currentJobId = data.job_id;
    startedAt    = Date.now();
    switchView('processing');
    $('proc-filename').textContent = selectedFile.name;
    $('job-id-disp').textContent   = 'job ' + currentJobId;
    initProcessingView();
    pollTimer = setInterval(pollStatus, 5000);
    pollStatus();
  } catch (err) {
    $('translate-btn').disabled = false;
    alert('Could not start: ' + err.message);
  }
}

// ── Processing view ────────────────────────────────────────────────────────────
function initProcessingView() {
  // Build stage list
  $('stage-list').innerHTML = PIPELINE_STAGES.map(s =>
    `<div id="step-${s.id}" class="step pending"
          style="display:flex; align-items:center; gap:10px;">
       <div class="dot"></div>
       <span class="name">${s.label}</span>
     </div>`
  ).join('');

  // Build insight dots
  $('insight-dots').innerHTML = INSIGHTS.map((_, i) =>
    `<div data-dot="${i}" style="width:5px; height:5px; border-radius:50%;
          background:${i === 0 ? 'var(--ink)' : 'var(--border)'}; transition:background .3s;"></div>`
  ).join('');

  showInsight(0);

  // Elapsed + stage advancement timer
  elapsedTimer = setInterval(() => {
    const sec = Math.floor((Date.now() - startedAt) / 1000);
    const m = Math.floor(sec / 60), s = sec % 60;
    $('elapsed-disp').textContent = m + 'm ' + String(s).padStart(2, '0') + 's';
    advanceStages(sec);
  }, 1000);

  // Rotate insights every 9 seconds
  insightTimer = setInterval(() => showInsight(insightIdx + 1), 9000);
}

function advanceStages(sec) {
  let activeIdx = 0;
  PIPELINE_STAGES.forEach((s, i) => { if (sec >= s.est) activeIdx = i; });

  PIPELINE_STAGES.forEach((s, i) => {
    const el = $('step-' + s.id);
    if (!el) return;
    const state = i < activeIdx ? 'done' : i === activeIdx ? 'active' : 'pending';
    el.className = 'step ' + state;
    el.style.cssText = 'display:flex; align-items:center; gap:10px;';
  });

  // Progress bar + label: 2% → 95%
  const maxEst = PIPELINE_STAGES[PIPELINE_STAGES.length - 1].est + 60;
  const pct = Math.min(95, 2 + (sec / maxEst) * 93);
  $('progress-bar').style.width = pct + '%';
  $('progress-pct').textContent = Math.round(pct) + '%';
  $('progress-stage-label').textContent = PIPELINE_STAGES[activeIdx].label;
}

function showInsight(idx) {
  insightIdx = ((idx % INSIGHTS.length) + INSIGHTS.length) % INSIGHTS.length;
  const wrap = $('insight-wrap');
  wrap.style.opacity = '0';
  setTimeout(() => {
    $('insight-title').textContent = INSIGHTS[insightIdx].title;
    $('insight-body').textContent  = INSIGHTS[insightIdx].body;
    document.querySelectorAll('[data-dot]').forEach(d => {
      d.style.background = parseInt(d.dataset.dot) === insightIdx ? 'var(--ink)' : 'var(--border)';
    });
    wrap.style.opacity = '1';
  }, 350);
}

// ── Poll status ────────────────────────────────────────────────────────────────
async function pollStatus() {
  try {
    const res = await fetch('/api/status/' + currentJobId);
    if (!res.ok) return;
    const data = await res.json();
    if (data.status === 'complete') {
      clearInterval(pollTimer); clearInterval(elapsedTimer); clearInterval(insightTimer);
      $('progress-bar').style.width = '100%';
      $('progress-pct').textContent = '100%';
      $('progress-stage-label').textContent = 'Complete';
      setTimeout(() => showResults(data), 800);
    } else if (data.status === 'failed') {
      clearInterval(pollTimer); clearInterval(elapsedTimer); clearInterval(insightTimer);
      switchView('error');
      $('error-text').textContent = data.error || 'An unknown error occurred.';
    } else if (data.status === 'cancelled') {
      clearInterval(pollTimer); clearInterval(elapsedTimer); clearInterval(insightTimer);
      resetUI();
    }
  } catch (_) { /* keep polling on transient errors */ }
}

// ── Results ────────────────────────────────────────────────────────────────────
function showResults(data) {
  switchView('results');
  const n = data.review_data ? data.review_data.length : '?';
  $('result-summary').textContent = n + ' string' + (n !== 1 ? 's' : '') + ' · 5 languages';
  $('dl-filename').textContent = (selectedFile ? selectedFile.name.replace('.xlsx', '') : 'file') + '_translated.xlsx';
  if (data.review_data && data.review_data.length > 0) {
    allRows = data.review_data;
    renderTable(allRows);
  }
}

$('download-btn').addEventListener('click', () => { window.location.href = '/api/download/' + currentJobId; });

function renderTable(rows) {
  if (!rows.length) return;
  const keys = Object.keys(rows[0]).filter(k => k !== 'row_index');

  $('review-thead').innerHTML =
    '<tr>' + keys.map(k =>
      '<th style="padding:10px 16px; text-align:left; font-size:11px; font-weight:600; ' +
      'color:var(--muted); letter-spacing:.07em; text-transform:uppercase; white-space:nowrap;">' +
      esc(LANG_LABELS[k] || k) + '</th>'
    ).join('') + '</tr>';

  $('review-tbody').innerHTML = rows.map((row, i) =>
    '<tr style="background:' + (i % 2 ? 'var(--paper)' : 'white') + ';">' +
    keys.map(k =>
      '<td style="padding:10px 16px; font-size:12px; color:var(--ink); ' +
      'max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; vertical-align:top;" ' +
      'title="' + esc(row[k]) + '">' + esc(row[k]) + '</td>'
    ).join('') + '</tr>'
  ).join('');

  hideEl('no-matches');
}

$('search-input').addEventListener('input', e => {
  const q = e.target.value.toLowerCase();
  const filtered = q ? allRows.filter(r => Object.values(r).some(v => String(v ?? '').toLowerCase().includes(q))) : allRows;
  renderTable(filtered);
  if (!filtered.length) showEl('no-matches');
  else hideEl('no-matches');
});

// ── Cancel translation ─────────────────────────────────────────────────────────
$('cancel-btn').addEventListener('click', cancelJob);

async function cancelJob() {
  if (!currentJobId) return;
  const btn = $('cancel-btn');
  btn.disabled = true;
  btn.textContent = 'Cancelling…';
  try {
    await fetch('/api/cancel/' + currentJobId, { method: 'DELETE' });
  } catch (_) { /* best-effort */ }
  [pollTimer, elapsedTimer, insightTimer].forEach(t => t && clearInterval(t));
  resetUI();
}

// ── Logo → home ────────────────────────────────────────────────────────────────
$('logo-home').addEventListener('click', () => {
  if (currentJobId) {
    // If a job is running, ask before cancelling
    if (!confirm('A translation is in progress. Cancel it and return to the upload screen?')) return;
    fetch('/api/cancel/' + currentJobId, { method: 'DELETE' }).catch(() => {});
  }
  [pollTimer, elapsedTimer, insightTimer].forEach(t => t && clearInterval(t));
  resetUI();
});

// ── Reset ──────────────────────────────────────────────────────────────────────
$('btn-new').addEventListener('click', resetUI);
$('btn-retry').addEventListener('click', resetUI);

function resetUI() {
  [pollTimer, elapsedTimer, insightTimer].forEach(t => t && clearInterval(t));
  currentJobId = null; selectedFile = null; startedAt = null; allRows = []; insightIdx = 0;
  $('file-input').value = '';
  if ($('search-input')) $('search-input').value = '';
  if ($('cancel-btn')) { $('cancel-btn').disabled = false; $('cancel-btn').textContent = 'Cancel Translation'; }
  hideEl('file-card'); showEl('drop-zone');
  $('translate-btn').disabled = true;
  switchView('upload');
}
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index():
    return _HTML


_ALLOWED_EXTS = {".xlsx", ".pdf", ".docx", ".doc"}


@app.post("/api/translate")
async def start_translation(file: UploadFile = File(...)):
    """Accept .xlsx / .pdf / .docx, convert if needed, kick off translation."""
    fname = file.filename or ""
    ext   = Path(fname).suffix.lower()
    if ext not in _ALLOWED_EXTS:
        raise HTTPException(status_code=400, detail="Supported formats: .xlsx, .pdf, .docx")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File must be smaller than 10 MB.")

    job_id    = uuid.uuid4().hex[:8]
    safe_name = f"{job_id}_{fname}"
    raw_path  = Path("uploads") / safe_name
    raw_path.write_bytes(contents)

    # Convert PDF / DOCX → xlsx so the crew can process it
    if ext != ".xlsx":
        xlsx_path = raw_path.with_suffix(".xlsx")
        try:
            _convert_to_xlsx(raw_path, xlsx_path)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"Could not parse file: {exc}")
        work_path = xlsx_path
    else:
        work_path = raw_path

    expected_output = Path("outputs") / f"{work_path.stem}_translated.xlsx"

    JOBS[job_id] = {
        "status": "pending",
        "input_file": fname,
        "upload_path": str(work_path),
        "output_path": str(expected_output),
        "created_at": datetime.now().isoformat(),
        "cancel_requested": False,
        "error": None,
        "review_data": None,
        "report": None,
    }

    loop = asyncio.get_running_loop()
    loop.run_in_executor(_executor, _run_job, job_id, str(work_path))

    return JSONResponse({"job_id": job_id, "status": "pending"})


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Return current job status plus review data when complete."""
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return JSONResponse({
        "job_id": job_id,
        "status": job["status"],
        "input_file": job["input_file"],
        "created_at": job["created_at"],
        "error": job["error"],
        "review_data": job["review_data"],
    })


@app.delete("/api/cancel/{job_id}")
async def cancel_job(job_id: str):
    """Mark a pending/running job as cancelled. The background thread will finish
    on its own but its result will be discarded."""
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job["status"] in ("complete", "failed"):
        raise HTTPException(status_code=400, detail="Job has already finished and cannot be cancelled.")
    job["cancel_requested"] = True
    job["status"] = "cancelled"
    return JSONResponse({"job_id": job_id, "status": "cancelled"})


@app.get("/api/download/{job_id}")
async def download(job_id: str):
    """Stream the translated Excel file to the browser."""
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job["status"] != "complete":
        raise HTTPException(status_code=400, detail="Translation is not complete yet.")

    output_path = Path(job["output_path"])
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found on disk.")

    download_name = f"{Path(job['input_file']).stem}_translated.xlsx"
    return FileResponse(
        path=str(output_path),
        filename=download_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# ---------------------------------------------------------------------------
# Background job runner
# ---------------------------------------------------------------------------

def _run_job(job_id: str, excel_path: str) -> None:
    """Run the full CrewAI pipeline in a background thread."""
    JOBS[job_id]["status"] = "running"
    try:
        from .crew import MonotypeTranslationCrew  # import here to keep startup fast

        MonotypeTranslationCrew().crew().kickoff(inputs={
            "excel_path": excel_path,
            "knowledge_dir": "knowledge",
        })

        # Snapshot review data immediately (shared file; capture before another job runs)
        review_path = Path("outputs/reviewed_translations.json")
        if review_path.exists():
            try:
                JOBS[job_id]["review_data"] = json.loads(review_path.read_text())
            except Exception:
                pass

        # Capture the latest production report
        reports = sorted(Path("outputs").glob("translation_report-*.md"))
        if reports:
            try:
                JOBS[job_id]["report"] = reports[-1].read_text()
            except Exception:
                pass

        # Only mark complete if the user hasn't cancelled while the crew was running
        if not JOBS[job_id].get("cancel_requested"):
            JOBS[job_id]["status"] = "complete"

    except Exception as exc:
        if not JOBS[job_id].get("cancel_requested"):
            JOBS[job_id]["status"] = "failed"
            JOBS[job_id]["error"] = str(exc)
