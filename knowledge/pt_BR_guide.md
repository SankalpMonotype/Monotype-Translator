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
| workspace | `área de trabalho` | (already natural in pt-BR) |
| Monotype Library (product name) | `Biblioteca da Monotype` | Biblioteca Monotype |
| AI (general UI text) | `IA` | AI |
| AI Search (sentence subject/object) | `A função AI Search` | A busca por IA |
| AI Search (standalone button/label) | `AI Search` | (keep as-is) |

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
| Search (find fonts verb) | `Busque fontes` (not Pesquise) |
| Sync and Downloads (section heading) | `Sincronização e Downloads` (capital D, singular Sincronização) |
| I prefer this response | `Eu prefiro essa resposta` (essa not esta) |
| Auto | Keep as `Auto` — NEVER translate to Automático |
| Give us a moment... | `Aguarde um momento...` |
| quarterly (adjective) | `trimestral` |

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

## Untranslatable Terms

- Monotype, MyFonts, Fonts.com, Monotype AI, Mosaic, SkyFonts — always English
- "Made with ♡", "by Monotype.", "Powered by Monotype" — copy verbatim
