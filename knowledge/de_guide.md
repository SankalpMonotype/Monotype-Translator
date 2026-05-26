# German Translation Guide — Monotype

Quick-reference patterns for German translation. Vocabulary tables are in glossary.md.
Register: formal "Sie".

---

## Critical Vocabulary

| English | Correct German | NEVER use |
|---------|----------------|-----------|
| Font(s) | `Font(s)` (English loanword) | Schrift(en) |
| Font management (label) | `Fontverwaltung` | Schriftenverwaltung, Schriftverwaltung |
| Activate fonts | `Fonts aktivieren` | Schriften aktivieren |
| font licensing | `Font-Lizenzen` | Schriftlizenzen |
| Upload & manage fonts | `Fonts hochladen und verwalten` | Schriften hochladen |
| Label | `Label` (English loanword) | Bezeichnung, Beschriftung, Etikett |
| Service | `Service` (English loanword) | Dienst |
| Administration (UI section heading) | `Administration` (English/German loanword) | Verwaltung |
| Permanent | `Dauerhaft` | permanent |
| Temporary | `Temporär` | — |
| Auto | Keep as `Auto` | Automatisch |
| Sync and Downloads | `Synchronisierung und Downloads` | Sync & Downloads |
| quarterly (adjective) | `vierteljährlich` | quartalsweise |
| Monospaced | `Monospaced` (English loanword) | Monospace, Monodistanzschrift |
| Try X (command) | `Versuchen Sie X` | Probieren Sie |
| Empty state illustration | `Leerer Status` | Leere-Zustand-Abbildung |
| Informed for production | `Zur Produktion vorgemerkt` | — |
| Access Key / Copy Access Key | `Zugriffsschlüssel` / `Zugriffsschlüssel kopieren` | Zugangsschlüssel |
| Give us a moment... | `Einen Moment bitte...` | — |
| AI Search (sentence subject/object) | `die KI-Suche` (declined) | AI Search |
| AI Search (standalone label/button) | `AI Search` | (keep as-is) |
| AI (general UI text) | `KI` | AI |
| Font Philosopher says... | `Font Philosopher sagt...` | (keep "Font Philosopher" in English) |
| assets (UI noun — files, fonts, resources) | `Ressourcen` | Aktiva, Vermögenswerte |
| Create Assets (label) | `Ressourcen erstellen` | Aktiva erstellen |
| with anyone in the company | `mit allen im Unternehmen` | mit jedem in der Firma |
| company-wide sharing | `unternehmensweite Freigabe` | unternehmensweites Teilen |
| allow company-wide sharing (button) | `Unternehmensweite Freigabe zulassen` | Erlauben Sie unternehmensweites Teilen |
| with own teams only | `nur mit eigenen Teams` | nur mit meinen Teams |

---

## Font vs Schrift — When Each Applies

**DEFAULT: always `Font` / `Fonts` — this includes all compound words.**

| English | Correct | NEVER |
|---------|---------|-------|
| Activate fonts | `Fonts aktivieren` | Schriften aktivieren |
| Deactivate fonts | `Fonts deaktivieren` | Schriften deaktivieren |
| Font management | `Fontverwaltung` | Schriftenverwaltung |
| font licensing | `Font-Lizenzen` | Schriftlizenzen |
| Upload & manage fonts | `Fonts hochladen und verwalten` | Schriften hochladen |
| Manage how fonts can be used | `Verwalten Sie, wie Fonts genutzt werden` | wie Schriften genutzt werden |
| third-party fonts | `Fonts von Drittanbietern` | Schriften von Drittanbietern |
| production fonts | `Produktions-Fonts` | Produktionsschriften |

- **Schrift** / **Schriftarten**: EXCEPTION ONLY — use `Schriftarten` in specific marketing phrasing:
  - "Modern sans-serif fonts for campaigns" → `Moderne serifenlose Schriftarten für Kampagnen`
- **"Ähnliche Schriften anzeigen"**: EXCEPTION for "Get similar fonts" specifically.
- NO other exceptions — do NOT use `Schriften` in any standard UI string.

---

## Dialog Patterns — FOUR DISTINCT FORMS

Apply based on English string type:

### (1) "You are about to X" notification
→ `Sie sind dabei, X zu [infinitive].`
- e.g. `Sie sind dabei, {{user.count}} Benutzer zu deaktivieren.`
- NEVER use Möchten Sie for this pattern.

### (2) Short dialog title "Deactivate X users?" (3-6 word label, no full sentence)
→ `[obj] [infinitive]?`
- e.g. `{{user.count}} Benutzer deaktivieren?`
- Do NOT expand to Möchten Sie form.

### (3) Confirmation question in body text or standalone "Are you sure?"
→ `Möchten Sie [obj] wirklich [verb]en?`
- e.g. `Möchten Sie diesen Benutzer wirklich löschen?`
- NEVER `Sind Sie sicher, dass Sie...`
- With "Once deactivated/activated" prefix: consequence FIRST, question SECOND.
  - e.g. `Nach der Deaktivierung können diese Benutzer nicht mehr auf das System zugreifen. Möchten Sie wirklich alle {{user.count}} Benutzer deaktivieren?`

### (4) Affirmation button "Yes, deactivate X users."
→ `Ja, [obj] [INFINITIVE].` — object first, verb LAST.
- e.g. `Ja, {{user.count}} Benutzer deaktivieren.`
- NEVER `Ja, deaktivieren Sie {{user.count}} Benutzer.`

---

## "[X] will appear here for you to take action"

→ passive construction: `werden die [X] hier angezeigt, sodass Sie entsprechende Maßnahmen ergreifen können`

---

## "Ask me anything..."

→ `Fragen Sie mich alles...` — NEVER `Frag mich alles` (du form)

---

## KI-Suche Declension

| Case | Form |
|------|------|
| Nominative | `Die KI-Suche` |
| Accusative | `die KI-Suche` |
| Genitive / Dative | `der KI-Suche` |

- e.g. "Die KI-Suche liefert intelligente Empfehlungen..."
- e.g. "da die KI-Suche Fehler machen kann."

---

## Try X vs Probieren

"Try X" (command) → ALWAYS `Versuchen Sie X` — NEVER `Probieren Sie`

| English | Correct |
|---------|---------|
| Try out AI mode | `Versuchen Sie den KI-Modus` |
| Try our AI mode | `Versuchen Sie unseren KI-Modus` |

---

## Quarterly

MUST use `vierteljährlich` — NEVER `quartalsweise`.
- "Review your quarterly usage" → `Überprüfen Sie Ihre vierteljährliche Nutzung`

---

## Production Status Terms

| English | German |
|---------|--------|
| Informed for production | `Zur Produktion vorgemerkt` |
| [N] style(s) are informed to be marked for production | `[N] Stile wurden zur Produktion vorgemerkt.` |

---

## UI State Messages — Loading and Error Patterns

### Loading progress
"Loading X…" → **passive progressive**: `X werden geladen…`

| English | Correct | NEVER |
|---------|---------|-------|
| Loading permissions… | `Berechtigungen werden geladen…` | `Lade Berechtigungen ...` |
| Loading fonts… | `Fonts werden geladen…` | `Lade Fonts …` |

### Failed to load
"Failed to load X." → `X konnte(n) nicht geladen werden.`

| English | Correct | NEVER |
|---------|---------|-------|
| Failed to load permissions. | `Berechtigungen konnten nicht geladen werden.` | `Fehler beim Laden der Berechtigungen.` |
| Failed to load fonts. | `Fonts konnten nicht geladen werden.` | `Fehler beim Laden der Fonts.` |

---

## Button / Action Label Style

Short standalone action labels (no subject pronoun, ≤ 6 words): use **infinitive** without `Sie`.

| English | Correct | NEVER |
|---------|---------|-------|
| Allow company-wide sharing | `Unternehmensweite Freigabe zulassen` | `Erlauben Sie unternehmensweite Freigabe` |
| Open add team action | `Aktion „Team hinzufügen" öffnen` | `Fügen Sie die Teamaktion hinzu` |
| Generate report | `Bericht generieren` | `Bericht erstellen` |

For sentence-level instructions addressing the user, continue using `Sie` form.

---

## Untranslatable Terms

- Monotype, MyFonts, Fonts.com, Monotype AI, Mosaic, SkyFonts — always English
- "Made with ♡", "by Monotype.", "Powered by Monotype" — copy verbatim
