# Japanese Translation Guide — Monotype

Quick-reference patterns for Japanese translation. Vocabulary tables are in glossary.md.
These are the behavioural rules the model most frequently gets wrong.

---

## Counter Words

| Context | Rule | Correct | Wrong |
|---------|------|---------|-------|
| {{count}} = quantity of items (fonts, projects, etc.) | Append 件 immediately after variable | `{{count}}件` | `{{count}}` |
| X of Y used | Use 件中 | `{{count}}件中{{count}}件が使用済み` | `{{count}}のうち{{count}}` |
| {{user.count}} = number of users | Append 人 with a space before it | `{{user.count}} 人のユーザー` | `{{user.count}}人のユーザー` |
| Count in parenthetical label | Full-width brackets, 件 inside | `（{{count}}件）` | `({{count}}件)` or `（{{count}} 件）` |

---

## Button Labels vs Full Sentences

**Standalone button labels and short action labels (1-5 words, no subject):**
- OMIT trailing する
- Use shortest natural form

| English | Correct | Wrong |
|---------|---------|-------|
| Activate all users | `すべてのユーザーを有効化` | `すべてのユーザーを有効化する` |
| Retain the fonts | `フォントを保持` | `フォントを保持する` |
| Notify admin | `管理者に通知` | `管理者に通知する` |
| Ignore conflict | `競合を無視` | `競合を無視する` |
| Turn off X | `Xをオフ` | `Xをオフにする` |
| Turn on X | `Xをオン` | `Xをオンにする` |
| View guidelines | `ガイドラインを表示` | `ガイドラインを見る` |
| Type to search | `入力して検索` | `検索するには入力してください` |

EXCEPTION — keep する when already established: "Set expiry date" → `有効期限を設定する`

---

## Active vs Passive Voice

Toast/success messages → **ACTIVE voice** (〜しました), NEVER passive (〜されました).

| English | Correct | Wrong |
|---------|---------|-------|
| Font activated. | `フォントをアクティベートしました。` | `フォントがアクティベートされました。` |
| {{styleName}} added to Favourites. | `{{styleName}}をお気に入りに追加しました。` | `{{styleName}}がお気に入りに追加されました。` |
| {{styleName}} removed from Favourites. | `{{styleName}}をお気に入りから削除しました。` | `{{styleName}}がお気に入りから削除されました。` |

---

## は vs が in Negative / Empty-State Sentences

Negative sentences and empty-state messages: use **は**, NEVER が.

| English | Correct | Wrong |
|---------|---------|-------|
| No inactive users available | `非アクティブユーザーはいません` | `非アクティブユーザーがいません` |
| You don't have any users currently | `現在、ユーザーはいません` | `現在、ユーザーがいません` |

---

## Empty States — "No X yet"

Prefix with **まだ**, placed BEFORE the noun phrase.

| English | Correct | Wrong |
|---------|---------|-------|
| No fonts approved yet | `まだ承認済みのフォントがありません` | `承認されたフォントはまだありません` |
| No users added yet | `まだユーザーが追加されていません` | `ユーザーはまだ追加されていません` |

Short "No X available" labels: use "Xはいません" — no 利用できる prefix.
e.g. "No inactive users available" → `非アクティブユーザーはいません` NOT `利用できる非アクティブユーザーがいません`

---

## Confirmation Dialog Patterns

| Pattern | Rule |
|---------|------|
| "Are you sure you want to X?" | Use てよろしいですか？ — NEVER てもよろしいですか？ |
| "You are about to X" | X+しようとしています — NEVER X+するところです |
| Short "Are you sure you want to proceed?" | 続行しますか？ — NOT 続行してよろしいですか？ |
| Confirmation body | Consequence FIRST, question SECOND |
| NEVER add | 本当に — use only よろしいですか？ |

---

## Font Activation — Critical Vocabulary Split

| Context | Japanese | NEVER use |
|---------|----------|-----------|
| User account deactivate | 無効化する | 無効にする |
| User account activate | 有効化する | 有効にする |
| Font activation | アクティベートする / アクティベートしました | 有効化する |
| "Fonts activated" | フォントをアクティベートしました | フォントが有効化されました |
| "Activated Fonts" (label) | アクティベートされたフォント | 有効化されたフォント |

---

## "Leaving" in Font-Lifecycle Context

"Leaving" / "leaves" = font being DISCONTINUED/RETIRED — NEVER "departing".

| English | Correct | Wrong |
|---------|---------|-------|
| Leaving in {{count}} days | `{{count}}日後に終了` | `{{count}}日後に出発します` |
| Leaving earliest | `終了日が早い順` | `早く出発する順` |
| font leaves the Monotype Library | `Monotypeライブラリから提供終了となった` | `ライブラリを離れる` |

---

## Sort / Filter Labels

| English | Correct | Wrong |
|---------|---------|-------|
| Filter by: | `フィルター：` | `次の条件でフィルタリング:` |
| Filter by glyphs | `グリフで絞り込み` | `グリフでフィルタリング` |
| Sort by X (sort criterion label) | just X + 順 | X + 順に並べ替え |
| Sort by Leaving earliest | `終了日が早い順` | `終了日が早い順に並べ替え` |

---

## Native Vocabulary over Katakana (Section/Heading Labels)

| English | Correct | Wrong |
|---------|---------|-------|
| Bulk action | `一括操作` | `バルクアクション` |
| Additional actions | `その他の操作` | `追加アクション` |
| Sort (section label) | `並べ替え` | `ソート` |
| Total results | `総件数` | `合計結果` |
| Table (list/grid view) | `一覧` | `テーブル` |
| Go forward / Next | `次へ` | `進む` |
| Pairs well with | `相性の良いペア` | `よく合う` |
| Process (technical) | `処理` | `プロセス` |
| Collaborator | `共同編集者` | `コラボレーター` |
| Full-access | `すべての権限` | `フルアクセス` |
| Only me (sharing scope) | `自分のみ` | `私だけ` |

---

## Updates vs Refresh

| Term | Japanese |
|------|----------|
| Updates (software version, section heading) | `アップデート` |
| Refresh (reload/reload data action) | `更新` |

NEVER use 更新 for software update news or changelogs.

---

## Destination Particle: に NOT へ

For "sync/add/copy/move to [place]": use **に** not へ.

- "Auto sync to list" → `リストに自動同期` (NOT リストへ自動同期)
- "Sync font to server" → `フォントをサーバーに同期` (NOT フォントをサーバーへ同期)

---

## Access in Permissions Context

"access" in permissions/roles context → **アクセス権** (NOT 権限 alone).

- "This access is inherited" → `このアクセス権は継承されている`
- "access cannot be removed" → `アクセス権を削除することはできない`

---

## Library Spelling

"Library" in UI/product context → **ライブラリ** — NEVER ライブラリー (no trailing ー).

- My Library → `マイライブラリ`
- Company Library → `社内ライブラリ`

---

## Try Again

ALWAYS: `もう一度お試しください` — NEVER 再度お試しください.

---

## Marketing / Tagline Copy

DO NOT translate word-for-word. Adapt for tone and punch.

| English | Correct | Wrong |
|---------|---------|-------|
| Making Helvetica proud. | `Helveticaも納得の仕上がりに` | `ヘルベチカを誇りに思います。` |
| Designers will notice. Trust us. | `気づく人には、ちゃんと伝わる` | literal |
| You are looking font-astic today. | `今日のあなた、font-astic。` | `今日は「フォント素晴らしい」です。` |

When English uses a pun or wordplay, keep the English word that carries the play.

---

## Placeholder Spacing

Strip inner spaces from `{{ name }}` → `{{name}}` (no spaces inside braces).

- `{{ name }} column` → `{{name}}列`

---

## Untranslatable Short Strings

- "Made with ♡", "by Monotype.", "Powered by Monotype" → copy verbatim, DO NOT translate
- "Monotype", "MyFonts", "Fonts.com", "Monotype AI", "Mosaic" → always English, NEVER モナタイプ
