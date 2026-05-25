# French Translation Guide — Monotype

Quick-reference patterns for French translation. Vocabulary tables are in glossary.md.
Register: formal "vous".

---

## Critical Vocabulary

| English | Correct French | NEVER use |
|---------|----------------|-----------|
| Auto | Keep as `Auto` | Automatique |
| Label (UI element) | `Étiquette` | Libellé |
| Get similar fonts | `Obtenir des polices similaires` | — |
| Verify / Check | `Vérifiez` | Consultez, Examinez |
| submit a report | `envoyez votre rapport` | soumettez |
| No X yet (empty state) | `Aucune X pour l'instant` | Aucune X pour le moment |
| Give us a moment... | `Donnez-nous un instant...` | — |
| Monospaced | `Monoespace` | Chasse fixe |
| tags | `tags` (keep as-is) | balises |
| View / Read (permission label) | `Consulter` | Voir, Lire |
| unmark (remove production marking) | `retirer le marquage` | Démarquer, démarrer |
| Do not X (negative action label) | `Ne pas X` (infinitive) | Ne partagez pas X (imperative) |
| quarterly (adjective) | `trimestriel / trimestrielle` | — |
| AI (general UI text) | `IA` | AI |
| AI Search (sentence subject/object) | `La recherche IA` | AI Search |
| AI Search (standalone label/button) | `AI Search` | (keep as-is) |
| total fonts activated | `Nombre total de polices activées` | — |
| Informed for production | `Prêt pour la production` | — |
| Font Philosopher says... | `Font Philosopher dit...` | (keep "Font Philosopher" in English) |

---

## Button Labels — INFINITIVE Form

Standalone action labels and "Oui, X" confirmation buttons use **INFINITIVE** — NEVER vous imperative.

| English | Correct | Wrong |
|---------|---------|-------|
| Activate all users | `Activer tous les utilisateurs` | `Activez tous les utilisateurs` |
| Revoke all invites | `Révoquer toutes les invitations` | `Révoquez toutes les invitations` |
| Yes, deactivate {{user.count}} users. | `Oui, désactiver {{user.count}} utilisateurs.` | `Oui, désactivez {{user.count}} utilisateurs.` |

Reserve vous imperative (Vérifiez, Choisissez) for **sentence-level instructions only**.

---

## Confirmation Dialog Body Pattern

Consequence FIRST, "Êtes-vous sûr" SECOND — NEVER reverse the order.
ALWAYS: `Êtes-vous sûr de vouloir [infinitive]...?` — NEVER `Voulez-vous vraiment`.

| Pattern | Example |
|---------|---------|
| Multiple users | `Une fois désactivés, ces utilisateurs ne pourront plus accéder au système. Êtes-vous sûr de vouloir désactiver tous les {{user.count}} utilisateurs ?` |
| Single user | `Une fois désactivé, cet utilisateur ne pourra plus accéder au système. Êtes-vous sûr de vouloir désactiver l'utilisateur ?` |

---

## Typography: Spaces Before Punctuation

Use **regular space (U+0020)** — NOT non-breaking space — before ?, !, :, ;.

(Post-processing strips non-breaking spaces automatically, but generate correct output.)

---

## Paired Actions

When two actions are paired (approve/reject, mark/unmark, add/remove): join with **ou** — NEVER a slash.

---

## "[X] will appear here for you to take action"

→ `pour que vous puissiez prendre les mesures nécessaires`
- e.g. `les polices apparaîtront ici pour que vous puissiez prendre les mesures nécessaires.`

---

## Sentence Structure

Preserve the syntactic structure of the English source — do NOT reorder constituents, nominalise verbs, or restructure clauses. Translate the words; keep the grammar shape.

---

## Production Status Terms

| English | French |
|---------|--------|
| Informed for production | `Prêt pour la production` |
| [N] style(s) are informed to be marked for production | `[N] style(s) sont marqués pour la production` |

---

## Empty States — "No X yet"

Use **pour l'instant** — NEVER pour le moment.

| English | Correct |
|---------|---------|
| No fonts approved yet | `Aucune police approuvée pour l'instant` |
| No fonts rejected yet | `Aucune police refusée pour l'instant` |

---

## Consulter vs Voir / Lire

For read/view access in permission or capability descriptions: ALWAYS `Consulter`.
"Voir" and "Lire" are too casual for permission descriptions.

---

## Untranslatable Terms

- Monotype, MyFonts, Fonts.com, Monotype AI, Mosaic, SkyFonts — always English
- "Made with ♡", "by Monotype.", "Powered by Monotype" — copy verbatim
