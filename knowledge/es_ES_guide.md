# Spanish (es-ES / Castilian) Translation Guide — Monotype

Quick-reference patterns for es-ES translation. Vocabulary tables are in glossary.md.
Castilian Spanish — NEVER Latin American variants.

---

## Critical Vocabulary — Castilian Standard

| English | Correct es-ES | NEVER use |
|---------|---------------|-----------|
| workspace | `espacio de trabajo` | área de trabajo |
| seat (licensing unit) | `plaza` | licencia individual, asiento |
| Manage (UI action) | `Gestionar` | Administrar |
| entitlement | `derecho` | titularidad, privilegio |
| add-on (plan context) | `complemento` | extensión |
| bulk (mass action) | `masivo/a` or `de forma masiva` | — |
| Bulk import | `Importación masiva` | — |
| Add (action verb) | `Añadir` | Agregar (Latin American) |
| upload | `subir` | cargar (Latin American) |
| settings/ajustes | `ajustes` | configuración |
| membership | `pertenencia` | membresía (Latin American) |
| output (font production) | `producción` | salida |
| features (OpenType, UI) | `características` | funciones |
| specific / exact (qualifying noun) | `concreto/a` | específico/a |
| Common characters (UI label) | `Caracteres habituales` | caracteres comunes |
| Embed code (noun label) | `Código de incrustación` | Código incrustado |
| Retry (standalone button) | `Reintentar` | Inténtalo de nuevo |
| revoke invite (past action label) | `Invitación revocada` | revocar invitación |
| yet | `todavía` | aún |
| MyLibrary / library (product) | `Mi biblioteca` / `biblioteca` | — |
| Company Library | `biblioteca de empresa` | — |
| AI (general UI text) | `IA` | AI |
| AI Search (sentence subject/object) | `La función AI Search` | La búsqueda IA |
| AI Search (standalone label) | `AI Search` | (keep as-is) |
| Auto | Keep as `Auto` — NEVER translate to Automático | — |
| assets (UI noun — files, fonts, resources) | `recursos` | activos |
| Create Assets (label) | `Crear recursos` | Crear activos |
| self-hosting (web kit context) | `autoalojamiento` (one word, no hyphen) | auto-hospedaje, auto-alojamiento |
| Download web self-hosting kits | `Descargar kits web de autoalojamiento` | Descargar kits de auto-hospedaje web |
| Direct Production Marking | `Marcar directamente como de producción` | Marcado de producción directa |
| with own teams only | `solo con tus equipos` | solo con sus propios equipos |
| with anyone in the company | `con todos en la empresa` | — |

---

## tú Register (Tone)

Use **tú** throughout (informal, conversational). NEVER usted except strictly legal text.

| Form | Correct | Wrong |
|------|---------|-------|
| State verbs | estás, tienes, quieres | está, tiene, quiere |
| Possessives | tu, tus | su, sus |
| tú imperative | Busca, Activa, Prueba | Busque, Active, Pruebe |

---

## Button Labels — Infinitive vs tú Imperative

**Standalone button labels and "Sí, X" confirmation buttons → INFINITIVE:**

| English | Correct | Wrong |
|---------|---------|-------|
| Activate all users | `Activar todos los usuarios` | `Activa todos los usuarios` |
| Yes, deactivate X users. | `Sí, desactivar {{user.count}} usuarios.` | `Sí, desactiva {{user.count}} usuarios.` |
| Yes, delete and transfer | `Sí, eliminar y transferir` | `Sí, elimina y transfiere` |

**Sentence-level copy addressing the user → tú imperative:**
- "Check your settings" → `Revisa tus ajustes`

---

## Impersonal / Passive Constructions

System state, system requirement, error descriptions → **impersonal SE** — NEVER tú forms.

| English | Correct | Wrong |
|---------|---------|-------|
| No users found to export | `No se han encontrado usuarios que exportar` | No has encontrado usuarios |
| Failed to export data. Retry | `No se han podido exportar los datos. Reintentar` | No has podido exportar |

The tone setting does NOT change grammatical voice — only second-person address.

---

## Personal 'a'

Use only before singular definite human nouns:
- ✅ `desactivar a un usuario`, `desactivar a este usuario`, `Si desactivas a este usuario`
- ❌ NEVER before count variables: `desactivar {{user.count}} usuarios` (no 'a')
- ❌ NEVER before "todos": `Activar todos los usuarios` (no 'a')

---

## "You are about to X"

- ✅ `Estás a punto de X`
- ❌ NEVER `Está a punto de X`

---

## Confirmation Dialog Pattern — "Once deactivated/activated"

- ✅ `Si los desactivas, no podrán acceder al sistema. ¿Seguro que quieres desactivar los {{user.count}} usuarios?`
- ✅ `Si desactivas a este usuario, no podrá acceder al sistema.`
- ❌ NEVER "Una vez desactivados…" or "Una vez activados…"
- ❌ NEVER "¿Está seguro de X?"
- ✅ Confirmation question: `¿Seguro que quieres X?`

---

## Paired Actions

When two actions are paired (approve/reject, mark/unmark): join with **o** — NEVER a slash.

---

## "No X yet" Empty States

Use **todavía** — NEVER aún.
- ✅ `No hay fuentes aprobadas todavía`
- ❌ `No hay fuentes aprobadas aún`

---

## "[X] will appear here for you to take action"

→ `para que actúes como corresponda`
- e.g. `las fuentes aparecerán aquí para que actúes como corresponda.`

---

## Specific Pattern Examples

| English | Correct es-ES |
|---------|---------------|
| 5 seats | `5 plazas` |
| View reports & entitlements | `Ver informes y derechos` |
| Add an add-on | `Añadir un complemento` |
| Bulk import | `Importación masiva` |
| bulk action | `acción masiva` |
| Include OpenType features | `Incluir características de OpenType` |
| Enter specific characters | `Introducir caracteres concretos` |
| Select specific languages | `Selecciona los idiomas concretos que se admitirán` |
| At least one setting must be enabled before you can proceed. | `Se debe activar al menos un ajuste para poder continuar.` |
| Check your settings | `Revisa tus ajustes` |
| Download web self-hosting kits | `Descargar kits web de autoalojamiento` |
| Create Assets | `Crear recursos` |
| Direct Production Marking | `Marcar directamente como de producción` |

---

## Untranslatable Terms

- Monotype, MyFonts, Fonts.com, Monotype AI, Mosaic, SkyFonts — always English
- "Made with ♡", "by Monotype.", "Powered by Monotype" — copy verbatim
