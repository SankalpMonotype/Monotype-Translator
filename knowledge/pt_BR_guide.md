# Brazilian Portuguese (pt-BR) Translation Guide — Monotype

Quick-reference patterns for pt-BR translation. Vocabulary tables are in glossary.md.
Focus: terminology the model frequently translates incorrectly.

---

## Critical Vocabulary — SaaS / UI Context

| English | Correct pt-BR | NEVER use |
|---------|---------------|-----------|
| role (user role) | `função` | papel |
| scan (document/risk analysis verb) | `analisar … em busca de` | escanear |
| membership (team context) | `membros` | filiação |
| entitlements (access context) | `permissões` | direitos |
| entitlements (licensing context) | `licenças` | direitos |
| seat (software licensing unit) | `licença individual` | assento, lugar |
| foundry (generic noun, not brand) | `fundidora` | fundição |
| Label (UI label element) | `Marcador` | Etiqueta, Rótulo |
| tag (noun — UI tags feature) | `tag` (English loanword, invariant) | etiqueta |
| tags (plural noun) | `tags` | etiquetas |
| to tag (verb — apply a tag) | `marcar com tag` | etiquetar |
| tagged (adjective — has a tag) | `marcado(a)(s)` or `marcado(a)(s) com tag` | etiquetado(a)(s) |
| to untag (verb — remove a tag) | `remover a tag de` / `remover tag` | desetiquetar, des-etiquetar |
| Untag (standalone button label) | `Remover tag` | Desetiquetar |
| workspace | `área de trabalho` | (already natural in pt-BR) |
| Monotype Library (product name) | `Biblioteca da Monotype` | Biblioteca Monotype |
| AI (general UI text) | `IA` | AI |
| AI Search (sentence subject/object) | `A função AI Search` | A busca por IA |
| AI Search (standalone button/label) | `AI Search` | (keep as-is) |
| assets (UI noun — files, fonts, resources) | `ativos` | recursos |
| Create Assets (label) | `Criar ativos` | Criar recursos |
| self-hosting (web kit context) | `self-hosting` (keep English, no translation) | auto-hospedagem, auto-gerenciamento |
| Download web self-hosting kits | `Baixar kits para self-hosting web` | Baixar kits de auto-hospedagem da web |
| with own teams only | `apenas com suas equipes` | somente com suas próprias equipes |
| with anyone in the company | `com todos na empresa` | — |
| embedding (web font delivery) | `incorporação` | incorporado |
| organization | `organização` | empresa (in org/account context) |
| user | `usuário` | utilizador (NEVER — European PT) |
| admin | `administrador` | — |

---

## Article Before "Monotype Fonts"

When "Monotype Fonts" is the subject or object of a sentence, ALWAYS use feminine article **a**:
- ✅ "Com **a** Monotype Fonts, é fácil…"
- ❌ "Com Monotype Fonts, é fácil…"

---

## Confirmation Dialog Body Pattern

Start with consequence, THEN ask:
- ✅ `Após a desativação, esses usuários não poderão acessar o sistema. Tem certeza de que deseja desativar todos os {{user.count}} usuários?`
- ✅ `Após a desativação, este usuário não poderá acessar o sistema. Tem certeza de que deseja desativar o usuário?`
- ❌ NEVER start with "Uma vez desativados/ativados…"

---

## "No X yet" Short Status Labels

Short labels omit "ainda":
- ✅ "No fonts rejected yet" → `Nenhuma fonte rejeitada`
- ❌ NOT `Nenhuma fonte rejeitada ainda`

---

## List Connectors

When the final item in a list is a longer action phrase, prefer **além de** over a plain comma:
- ✅ `Criar, renomear e excluir equipes, além de gerenciar os membros das equipes.`
- ❌ `Criar, renomear e excluir equipes, e gerenciar os membros das equipes.`

---

## Specific Term Rules

| English | Correct pt-BR |
|---------|---------------|
| Search (verb) | `pesquisar` | buscar |
| Sync and Downloads (section heading) | `Sincronização e Downloads` (capital D, singular Sincronização) |
| I prefer this response | `Eu prefiro essa resposta` (essa not esta) |
| Auto | Keep as `Auto` — NEVER translate to Automático |
| Give us a moment... | `Aguarde um momento...` |
| quarterly (adjective) | `trimestral` |

---

## Button Labels — INFINITIVE Form

Standalone action labels use **INFINITIVE** — NEVER imperative, matching the rule applied in French, German, and es-ES.

| English | Correct pt-BR | NEVER |
|---------|--------------|-------|
| Select specific languages | `Selecionar idiomas específicos` | `Selecione os idiomas específicos` |
| Enter specific characters | `Inserir caracteres específicos` | `Insira caracteres específicos` |
| Select the exact characters needed | `Selecionar os caracteres exatos necessários` | `Selecione os caracteres...` |
| Upload new | `Carregar novo` | `Fazer upload de novo` |

Reserve the imperative for sentence-level instructions addressing the user directly.

---

## "Unable to X" / "Cannot X" Error Messages

System-level inability messages use **Não foi possível X** — NEVER a literal calque of "Incapaz de".

| English | Correct pt-BR | NEVER |
|---------|--------------|-------|
| Unable to delete user | `Não foi possível excluir o usuário` | `Incapaz de excluir o usuário` |
| Unable to deactivate user | `Não foi possível desativar o usuário` | `Incapaz de desativar o usuário` |

---

## Register

- Use **você** throughout (not tu, not o senhor/a senhora)
- Brazilian Portuguese — NOT European Portuguese
- Informal conversational tone unless string is strictly legal/contractual

---

## Role Examples

| English | Correct |
|---------|---------|
| Manage users, teams & roles | `Gerenciar usuários, equipes e funções` |
| Select the permissions to assign to this role. | `Selecione as permissões a serem atribuídas a esta função.` |

## Scan Examples

| English | Correct |
|---------|---------|
| scan documents for risk | `analisar documentos em busca de riscos` |

## Membership Examples

| English | Correct |
|---------|---------|
| manage team membership | `gerenciar os membros das equipes` |

## Entitlement Examples

| English | Correct |
|---------|---------|
| View reports & entitlements | `Visualizar relatórios e permissões` (access context) |
| View reports & entitlements | `Visualizar relatórios e licenças` (licensing context) |

---

## Tags Feature — Full Pattern Reference

| English pattern | Correct pt-BR | NEVER |
|---|---|---|
| tag (noun) | `tag` | etiqueta |
| tags (noun plural) | `tags` | etiquetas |
| "Search tagged fonts" | `Pesquisar fontes marcadas` | fontes etiquetadas |
| "No fonts tagged to this tag" | `Nenhuma fonte marcada com esta tag` | marcada para esta etiqueta |
| "Could not load tagged fonts" | `Não foi possível carregar fontes marcadas` | fontes etiquetadas |
| "You can use tags to organize…" | `Você pode usar tags para organizar…` | usar etiquetas |
| "Use tags to organize…" | `Use tags para organizar…` | Use etiquetas |
| "You haven't created any tags yet." | `Você ainda não criou nenhuma tag.` | nenhuma etiqueta |
| "No unused tags available" | `Nenhuma tag não utilizada disponível` | Nenhuma etiqueta |
| "1 unused tag cleared successfully" | `1 tag não utilizada removida com sucesso` | etiqueta |
| "{{count}} unused tags cleared" | `{{count}} tags não utilizadas removidas com sucesso` | etiquetas |
| "Failed to clear unused tags." | `Falha ao remover tags não utilizadas.` | etiquetas |
| "Delete tags" | `Excluir tags` | Excluir etiquetas |
| "You are about to delete '[tagName]' tag." | `Você está prestes a excluir a tag "[tagName]".` | a etiqueta |
| untag (verb — to remove tags) | `remover a tag de` / `remover tag` | desetiquetar |
| "Are you sure to untag [X]?" | `Tem certeza de que deseja remover a tag de [X]?` | desassociar / desetiquetar |
| "You can always tag the fonts again later." | `Você poderá marcar as fontes novamente depois.` | etiquetar |

---

## Typography Terms — Critical Distinctions

These two terms are **counterintuitive** in pt-BR and frequently confused:

| English | Correct pt-BR | Why it looks wrong |
|---------|---------------|--------------------|
| **Legibility** (ease of reading individual characters) | `Leiturabilidade` | Looks like "readability" in English |
| **Readability** (ease of reading running text) | `Legibilidade` | Looks like "legibility" in English |

**Always use `leiturabilidade` for "legibility" and `legibilidade` for "readability".** The terms are not interchangeable.

Other confirmed typographic term translations (from Bianca Glossary):

| English | pt-BR |
|---------|-------|
| Typeface | `Família tipográfica` — NEVER "tipo de letra" or "fonte" for a typeface design |
| Font (individual file/weight) | `Fonte` |
| Glyph | `Glifo` |
| Kerning | `Kerning` — keep as English |
| Leading | `Entrelinha` |
| Tracking | `Entreletra` |
| Small caps | `Versalete` |
| Script (font style) | `Script ou Conectada` |
| Blackletter | `Letra gótica` |
| Stylistic Set | `Conjunto estilístico` |
| Optical size | `Tamanho óptico` |
| x-height | `Altura de X` |
| Body copy | `Corpo de texto` |
| Ascender | `Ascendente` |
| Descender | `Descendente` |

---

## EULA — Watch Out for European Portuguese

Bianca's reference glossary contains a European Portuguese mistranslation:
- ❌ `Contrato de licença do utilizador final` ("utilizador" = European PT)
- ✅ `EULA (Contrato de Licença de Usuário Final)` ("Usuário" = Brazilian PT)

Always use the Brazilian form with "Usuário".

---

## Untranslatable Terms

- Monotype, MyFonts, Fonts.com, Monotype AI, Mosaic, SkyFonts, Anyword — always English
- "Made with ♡", "by Monotype.", "Powered by Monotype" — copy verbatim
