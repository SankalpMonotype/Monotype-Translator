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
| webkit | `kit web` | webkit (do NOT keep as English) |
| offline (kit web / web project state = not serving fonts) | `invisible` | fuera de línea |
| online (kit web / web project state = serving fonts) | `visible` | en línea |
| offline (network connectivity context) | `sin conexión` | fuera de línea |
| online (network connectivity context) | `con conexión` | en línea |
| Take webkit offline | `Hacer kit web invisible` | Tomar webkit fuera de línea |
| Take webkit online | `Hacer kit web visible` | Tomar webkit en línea |
| Take webkits offline | `Hacer kits web invisibles` | — |
| Yes, take offline (confirmation button) | `Sí, hacer invisible` | Sí, tomar fuera de línea |
| unpublish (web project) | `ocultar` | despublicar, anular publicación |
| Are you sure you want to unpublish this web project? | `¿Seguro que quieres ocultar este proyecto web?` | — |
| (All Web projects will be unpublished) | `(Se ocultarán todos los proyectos web)` | — |
| Live (standalone status label — published & active) | `En producción` | en vivo, activo |
| live (adjective in warning sentences about active webkits) | `activos` | en vivo |
| live and published work | `trabajos activos y publicados` | — |
| invite list | `lista de invitaciones` | lista de invitados |
| kerning (typography term) | `kerning` — keep as English | espaciado (NEVER use for kerning) |
| expiry date | `fecha de caducidad` | fecha de vencimiento |
| expire / expires | `caducar / caduca` | vencer (only acceptable in billing/contract text) |
| expired (adjective) | `caducado/a` | vencido/a |
| expiry (noun) | `caducidad` | vencimiento |
| set expiry date | `configurar fecha de caducidad` | — |
| pin (verb) | `anclar` | fijar, clavar |
| unpin (verb) | `desanclar` | desfijar |
| pinned (adjective) | `anclado/a` | fijado/a |
| Pin to top | `Anclar arriba` | — |
| archive (verb) | `archivar` | — |
| archived (adjective) | `archivado/a` | — |
| unarchive | `desarchivar` | — |
| Inform for production | `Informar de uso en producción` | — |
| production intent | `intención de uso en producción` | — |
| Share intent for X styles | `Compartir intención de uso de los X estilos` | — |
| Something went wrong | `Ha ocurrido un error` | Algo ha salido mal |
| Something went wrong. Please try again. | `Ha ocurrido un error. Inténtalo de nuevo.` | — |
| Ask me anything… | `Pregúntame lo que quieras…` | Pregúntame cualquier cosa |
| Anchor font (font pairing UI) | `Fuente destacada` | — |

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

## "Unable to X" / "Cannot X" System Error Messages

System-level inability (the system cannot perform the action) uses **No es posible X** — NEVER "No se puede X".

| English | Correct es-ES | NEVER |
|---------|---------------|-------|
| Unable to delete user | `No es posible eliminar el usuario` | `No se puede eliminar el usuario` |
| Unable to deactivate user | `No es posible desactivar el usuario` | `No se puede desactivar al usuario` |

---

## Error Messages — "We couldn't" vs "Failed to"

Two distinct patterns; do not mix them:

| English pattern | es-ES pattern | Example |
|-----------------|---------------|---------|
| `We couldn't [action]` — system tried on behalf of user | `No hemos podido [action]` (first-person plural) | `We couldn't delete '{{name}}'.` → `No hemos podido eliminar «{{name}}».` |
| `Failed to [action]` — system-level failure, no agent | `No se ha podido [action]` (impersonal reflexive) | `Failed to export data.` → `No se han podido exportar los datos.` |

- `We couldn't update sharing.` → `No hemos podido actualizar el uso compartido.`
- `We couldn't find any font pairs.` → `No hemos podido encontrar ningún par para esta fuente.`

---

## Font Lifecycle — "Leaving" Strings (es-ES)

In es-ES, "leaving" (a font being retired from the library) is expressed as the font "leaving us" — a human-warmth metaphor:

| English | Correct es-ES | NEVER |
|---------|---------------|-------|
| Leaving soon | `Nos dejan` | Se van pronto |
| Leaving soon fonts | `Fuentes que nos dejan` | Fuentes que se van |
| Leaving soon in {{count}} | `Nos dejan en {{count}}` | — |
| Leaving soon — {{count}} days | `Nos deja — en {{count}} días` | — |
| Leaving in | `Nos deja en` | — |
| Leaving earliest | `Próxima retirada` | Salida más próxima |
| Sort by Leaving earliest | `Ordenar por Próxima retirada` | — |

---

## Quotation Marks in es-ES

Use **«»** (guillemets, no inner space) for all quoted text in es-ES — NEVER straight quotes or "double quotes":
- `No results found for "{{query}}"` → `No se han encontrado resultados para «{{query}}»`
- `Are you sure to untag {{name}}?` → `¿Seguro que quieres quitar la etiqueta de «{{name}}»?`
- `We couldn't delete '{{name}}'.` → `No hemos podido eliminar «{{name}}».`

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
| No results found | `No se han encontrado resultados` |
| No results found for "{{query}}" | `No se han encontrado resultados para «{{query}}»` |
| Something went wrong! Please try again. | `Ha ocurrido un error. Inténtalo de nuevo.` |
| Activate & Deactivate Fonts | `Activar y desactivar fuentes` |
| Mark for production | `Marcar como de producción` |
| Unmark from production | `Desmarcar como de producción` |
| Mark / Unmark fonts for production | `Marcar/desmarcar fuentes como de producción` |
| Inform for production | `Informar de uso en producción` |
| Share production use intent for {familyName} | `Compartir intención de uso en producción de {familyName}` |
| Allow downloading | `Permitir descargas` |
| Allow importing fonts | `Permitir importar fuentes` |
| Allow self hosting webkit downloads | `Permitir descargas autoalojadas de kits web` |
| Already Added | `Ya añadido` |
| AI Search can make mistakes, check important info. | `La función AI Search puede cometer errores, comprueba la información importante.` |
| You can pin up to 5 assets, please unpin one to add another. | `Puedes anclar hasta 5 recursos. Desancla uno para añadir otro.` |
| Invite already sent. Please retry in one hour. | `Ya se ha enviado la invitación. Inténtalo de nuevo en una hora.` |
| Are you sure you want to revoke this invite? | `¿Seguro que quieres revocar esta invitación?` |
| Accept invitation | `Aceptar invitación` |
| Decline invitation | `Rechazar invitación` |

---

## Untranslatable Terms

- Monotype, MyFonts, Fonts.com, Monotype AI, Mosaic, SkyFonts — always English
- "Made with ♡", "by Monotype.", "Powered by Monotype" — copy verbatim
- **Third-party product names** — keep in English exactly as written:
  - `Adobe Fonts` → NEVER `Fuentes de Adobe`
  - `Google Fonts` → NEVER `Fuentes de Google`
  - Other third-party named products follow the same rule; the name is not a description.

---

## Creative / Marketing / Delight Copy

Strings that are playful, punchy, or use wordplay (loading messages, empty states, slogans) must be **idiomatically adapted** — NEVER translated word-for-word.

Rules:
- If the string is in the Translation Memory (TM), use the TM version verbatim.
- If the string is NOT in the TM, aim for the same tone and punch as the English original. Reorder or rephrase freely; the goal is a Spanish native speaker feeling the same delight, not decoding a literal translation.
- `kerning` stays as `kerning` even in creative copy — do NOT replace with `espaciado`.
- Typography jargon that is industry-standard in Spanish design contexts (`kerning`, `glifo`, `serif`) should remain as-is; these are not "translated", they are standard terms.

| English (example) | Correct es-ES | NEVER |
|-------------------|---------------|-------|
| You are looking "font-astic" today. | `Hoy tienes un aspecto «fuentástico».` | `Hoy te ves "font-ástico".` (literal) |
| Designers are 90% coffee, 10% kerning. | `Diseñadores: 90 % café, 10 % kerning.` | `Los diseñadores son 90% café, 10% espaciado.` |
| Fixing kerning that only designers complain about. | `Corrigiendo ese kerning que solo los diseñadores detectarían.` | `Corrigiendo el espaciado del que solo se quejan los diseñadores.` |
| Designers will notice. Trust us. | `Los diseñadores se darán cuenta. Créenos.` | `Los diseñadores notarán. Confía en nosotros.` |
