"""
Translation gap analysis: Linguist A vs AI B
Prints all divergent pairs (similarity < 80) and pattern summaries per language.
"""

import sys
import pandas as pd
from rapidfuzz import fuzz

LINGUIST_A = "/Users/sankalpkhandelwal/Downloads/Linguist A.xlsx"
AI_B       = "/Users/sankalpkhandelwal/Downloads/AI B.xlsx"
THRESHOLD  = 80

# ── 1. Load files ──────────────────────────────────────────────────────────────
la = pd.read_excel(LINGUIST_A)
ab = pd.read_excel(AI_B)

print("=== Column names ===")
print("Linguist A:", la.columns.tolist())
print("AI B      :", ab.columns.tolist())
print()

# Normalise column names (strip whitespace)
la.columns = la.columns.str.strip()
ab.columns = ab.columns.str.strip()

# Language mapping: canonical name → (col in la, col in ab)
# Both files share these language columns but may differ in casing / spacing
def find_col(df, candidates):
    for c in df.columns:
        if c.strip().lower() in [x.lower() for x in candidates]:
            return c
    return None

languages = {
    "German":     (["German", "Deutsch"],           ["German", "Deutsch"]),
    "French":     (["French", "Français"],           ["French", "Français"]),
    "Spanish":    (["Spanish", "Español"],           ["Spanish", "Español"]),
    "Portuguese": (["Portuguese", "Português",
                    "pt-BR", "Portuguese (Brazil)"], ["Portuguese", "Português",
                                                      "pt-BR", "Portuguese (Brazil)"]),
    "Japanese":   (["Japanese", "日本語"],            ["Japanese", "日本語"]),
}

# ── 2. Align rows on English source ───────────────────────────────────────────
la_eng = find_col(la, ["English"])
ab_eng = find_col(ab, ["English"])

if la_eng is None or ab_eng is None:
    sys.exit("Could not locate English column in one of the files.")

# Merge on English (inner join keeps only rows present in both)
merged = pd.merge(
    la.rename(columns={la_eng: "English"}),
    ab.rename(columns={ab_eng: "English"}),
    on="English",
    how="inner",
    suffixes=("_LA", "_AB"),
)
print(f"Rows after inner-join on English: {len(merged)}\n")

# ── 3. Helper: normalise a cell value ─────────────────────────────────────────
def norm(v):
    if pd.isna(v):
        return ""
    return str(v).strip()

# ── 4. Per-language analysis ───────────────────────────────────────────────────
DIVIDER = "=" * 90

for lang, (la_cands, ab_cands) in languages.items():

    # Locate the right column in merged df (they got suffixed after merge)
    def find_merged(cands, suffix):
        for cand in cands:
            col = cand + suffix
            if col in merged.columns:
                return col
            # also try original (if column was unique across both files)
            if cand in merged.columns:
                return cand
        return None

    col_la = find_merged(la_cands, "_LA")
    col_ab = find_merged(ab_cands, "_AB")

    if col_la is None or col_ab is None:
        print(f"\n{'─'*60}")
        print(f"LANGUAGE: {lang}")
        print(f"  [!] Could not locate columns — skipping.")
        print(f"      Searched LA suffixed: {[c+'_LA' for c in la_cands]}")
        print(f"      Searched AB suffixed: {[c+'_AB' for c in ab_cands]}")
        print(f"      Available merged cols: {merged.columns.tolist()}")
        continue

    # Compute similarity scores
    rows = []
    for idx, row in merged.iterrows():
        en   = norm(row["English"])
        t_la = norm(row[col_la])
        t_ab = norm(row[col_ab])

        # Skip if both translations are empty
        if not t_la and not t_ab:
            continue

        score = fuzz.token_sort_ratio(t_la, t_ab)
        rows.append({
            "row":     idx + 2,          # Excel row (1-indexed header)
            "english": en,
            "la":      t_la,
            "ab":      t_ab,
            "score":   score,
        })

    df_lang = pd.DataFrame(rows)
    divergent = df_lang[df_lang["score"] < THRESHOLD].reset_index(drop=True)

    print(f"\n{DIVIDER}")
    print(f"LANGUAGE: {lang}  |  Total comparable rows: {len(df_lang)}  |  Divergent (< {THRESHOLD}): {len(divergent)}")
    print(DIVIDER)

    if divergent.empty:
        print("  No divergent pairs found.")
        continue

    # ── Print every divergent pair ────────────────────────────────────────────
    for _, r in divergent.iterrows():
        print(f"\n  Row {r['row']}  [score={r['score']}]")
        print(f"  EN : {r['english']}")
        print(f"  LA : {r['la']}")
        print(f"  AB : {r['ab']}")

    # ── Pattern analysis ──────────────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print(f"  PATTERN ANALYSIS — {lang} ({len(divergent)} divergent pairs)")
    print(f"{'─'*60}")

    # Bucket each pair heuristically
    word_choice      = []
    formality        = []
    completeness     = []
    structural       = []
    semantic         = []
    ui_terminology   = []
    other            = []

    # Helpers
    import re

    def token_set(s):
        return set(re.sub(r"[^\w\s]", "", s.lower()).split())

    def char_len_ratio(a, b):
        la, lb = len(a), len(b)
        if la == 0 and lb == 0:
            return 1.0
        return min(la, lb) / max(la, lb) if max(la, lb) > 0 else 1.0

    # Simple UI term detector (common button/menu words)
    UI_TERMS_EN = {
        "save", "cancel", "ok", "close", "open", "load", "search", "filter",
        "apply", "reset", "clear", "next", "back", "previous", "continue",
        "submit", "login", "logout", "sign in", "sign out", "upload", "download",
        "select", "deselect", "delete", "remove", "add", "create", "edit",
        "update", "view", "show", "hide", "more", "less", "expand", "collapse",
        "confirm", "skip", "done", "finish", "start", "stop", "pause", "play",
        "share", "copy", "paste", "cut", "undo", "redo", "export", "import",
        "settings", "preferences", "profile", "account", "home", "help",
        "activate", "deactivate", "enable", "disable",
    }

    # German formality markers
    DE_FORMAL = {"sie", "ihr", "ihnen", "ihres", "ihrem", "ihrer"}
    DE_INFORMAL = {"du", "dein", "deine", "deinen", "deines", "deinem", "dir", "dich"}

    # Spanish formality
    ES_FORMAL = {"usted", "ustedes", "su", "sus"}
    ES_INFORMAL = {"tú", "tu", "vos", "tus", "te", "ti"}

    for _, r in divergent.iterrows():
        la_t  = r["la"].lower()
        ab_t  = r["ab"].lower()
        en_t  = r["english"].lower()
        la_tk = token_set(r["la"])
        ab_tk = token_set(r["ab"])

        assigned = False

        # 1. Completeness: very different length
        lr = char_len_ratio(r["la"], r["ab"])
        if lr < 0.55:
            completeness.append(r)
            assigned = True

        # 2. Formality (language-specific)
        if lang == "German":
            la_formal = bool(la_tk & DE_FORMAL)
            ab_formal = bool(ab_tk & DE_FORMAL)
            la_inform = bool(la_tk & DE_INFORMAL)
            ab_inform = bool(ab_tk & DE_INFORMAL)
            if (la_formal and ab_inform) or (la_inform and ab_formal):
                formality.append(r); assigned = True

        if lang == "Spanish":
            la_formal = bool(la_tk & ES_FORMAL)
            ab_formal = bool(ab_tk & ES_FORMAL)
            la_inform = bool(la_tk & ES_INFORMAL)
            ab_inform = bool(ab_tk & ES_INFORMAL)
            if (la_formal and ab_inform) or (la_inform and ab_formal):
                formality.append(r); assigned = True

        # 3. UI terminology: English source is a short UI phrase & translations differ
        en_tokens = token_set(r["english"])
        if not assigned and en_tokens & UI_TERMS_EN and len(r["english"].split()) <= 5:
            ui_terminology.append(r); assigned = True

        # 4. Structural: same token set but score still low (punct/cap/order)
        if not assigned and la_tk == ab_tk:
            structural.append(r); assigned = True

        # 5. Semantic divergence: token overlap < 30% and score < 60
        if not assigned:
            common = la_tk & ab_tk
            union  = la_tk | ab_tk
            jaccard = len(common) / len(union) if union else 0
            if jaccard < 0.30 and r["score"] < 60:
                semantic.append(r); assigned = True

        # 6. Word choice: moderate overlap, similar length
        if not assigned and lr >= 0.55:
            word_choice.append(r); assigned = True

        if not assigned:
            other.append(r)

    def print_cat(name, items):
        if items:
            print(f"\n  [{name}]  ({len(items)} pairs)")
            for r in items:
                print(f"    Row {r['row']} [{r['score']}]  EN: {r['english'][:60]}")
                print(f"      LA: {r['la']}")
                print(f"      AB: {r['ab']}")

    print_cat("Word Choice / Vocabulary",   word_choice)
    print_cat("Formality / Register",       formality)
    print_cat("Completeness",               completeness)
    print_cat("Structural",                 structural)
    print_cat("Semantic Divergence",        semantic)
    print_cat("UI Terminology",             ui_terminology)
    print_cat("Other",                      other)

    # Quick summary counts
    print(f"\n  Summary counts:")
    print(f"    Word choice     : {len(word_choice)}")
    print(f"    Formality       : {len(formality)}")
    print(f"    Completeness    : {len(completeness)}")
    print(f"    Structural      : {len(structural)}")
    print(f"    Semantic        : {len(semantic)}")
    print(f"    UI terminology  : {len(ui_terminology)}")
    print(f"    Other           : {len(other)}")

print(f"\n{DIVIDER}")
print("Analysis complete.")
print(DIVIDER)
