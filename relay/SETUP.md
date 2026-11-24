# 中継の設置手順（キング用）

目的：Azure のキーを、ゲームの外（Cloudflare の中）に隠したまま、ゲームに「10分だけ使える合鍵（トークン）」を渡す。
所要時間の目安：30分。費用：0円（根拠は末尾）。
**キーは、このリポジトリにも、チャットにも、どこにも貼らない。** 貼る場所は、手順3の Cloudflare の入力欄ただ1か所。

## 手順1：Cloudflare のアカウントを作る
1. https://dash.cloudflare.com/sign-up/workers-and-pages を開き、メールアドレスとパスワードで登録する（無料）。
2. 届いたメールの確認リンクを開く。

## 手順2：中継を作る
1. Cloudflare の画面で「Workers & Pages」を開く。
2. 「Create application」→「Create Worker」を選ぶ。名前は `kanpe-speech-relay` にして「Deploy」。
3. 作った Worker を開き「Edit code」を押す。
4. 最初から入っているコードを全部消し、このフォルダの `worker.js` の中身を全部貼り付ける。
5. 「Deploy」（または「Save and deploy」）を押す。

## 手順3：キーを登録する（いちばん大事）
1. その Worker の「Settings」を開き、変数を足す場所（「Variables and Secrets」または「Environment Variables」）を開く。
2. 次の3つを足す。
   | 名前 | 値 | 種類 |
   |---|---|---|
   | `AZURE_SPEECH_KEY` | Azure のキー（下の「キーの出し方」） | **Secret（暗号化）にする** |
   | `AZURE_SPEECH_REGION` | `eastus` | 普通の文字 |
   | `ALLOWED_ORIGINS` | `https://kingtheq.github.io` | 普通の文字 |
3. 保存して「Deploy」する。

キーの出し方：Azure のポータルで、作った Speech のリソースを開き、「Keys and Endpoint」にある KEY 1 をコピーする。
キーを間違えて人に見せたり貼ったりしたら、同じ画面で「Regenerate」（作り直し）をして、手順3をやり直す。

※画面の名前は Cloudflare の更新で変わることがあります。見つからないときは、画面の名前を教えてください。

## 手順4：中継のURLを控える
Worker の画面に出る `https://kanpe-speech-relay.○○.workers.dev` が中継のURL。次の手順で使う。
（このURLは公開されても構いません。キーは入っていません。）

## 手順5：動くか確かめる
確認ページは、このリポジトリを main に反映すると `https://kingtheq.github.io/kanpe-sensei-dubai/relay-check/` に出る（`relay/check.html`）。
1. そのページを、スマホかPCの Chrome で開く。
2. 「中継のURL」に手順4のURLを貼り、「① トークンをもらう」を押す。「成功：トークンを受け取りました」と出れば、中継は動いている。
3. 「② マイクで言って採点する」を押し、マイクを許可して、表示された英文を言う。
4. 「成功：発音評価が1回動きました」と、全体・正確さ・流暢さ・言い切り度・単語ごとの点が出れば完成。
5. 確認が終わったら、`.github/workflows/pages.yml` の `relay-check` の行を消せば、確認ページは非公開に戻せる（やってほしいときはクロに頼む）。

## 手順6：中継のURLをゲームに入れる（クロに伝える）
手順4のURL（`https://kanpe-speech-relay.○○.workers.dev`）を、クロに伝えてください。クロが `tour-src/relay-url.txt` の1行に入れて、ゲームを作り直します（キングの作業はありません）。
- URL が空のあいだ、ゲームは Azure を使いません（同意の画面も出ません）。ブラウザの音声認識だけで、いつもどおり遊べます。
- URL を入れたあと、ゲームは「旅の始めの宣言」の前に、声を送ってよいかを一度だけ聞きます。
- キーは、ゲームにも、リポジトリにも入りません（入るのは公開してよい URL だけ）。

うまくいかないとき：
- 「403」：手順3の `ALLOWED_ORIGINS` が `https://kingtheq.github.io` と一字一句同じか確かめる（最後に `/` を付けない）。
- 「503」：`AZURE_SPEECH_KEY` が登録されていない。手順3をやり直す。
- 「502」：キーかリージョンが違う。Azure のリソースが East US か確かめる。
- 「429」：短時間に押しすぎ。1分待つ。

## 費用（無料枠で収まる根拠）　確認日：2026-11-16
**Cloudflare Workers（無料プラン）**
- 1日10万リクエストまで、1回あたりCPU時間10ミリ秒まで。超えると止まる（請求はされない）。出典：https://developers.cloudflare.com/workers/platform/pricing/ と https://developers.cloudflare.com/workers/platform/limits/
- この中継は、プレイヤー1回の「始め」「窓口の読み返し」「終わり」で、トークンをもらうだけ（トークンは端末側で9〜10分使い回すので、実際の回数はもっと少ない）。1日10万回には遠い。

**Azure Speech（East US）**
- 無料プラン（F0）：音声→文字の標準リアルタイムが月5時間まで無料。出典：https://azure.microsoft.com/en-us/pricing/details/speech/
- 発音評価の料金は、基本は音声→文字と同じ扱い（出典：Microsoft Learn「Use pronunciation assessment」https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment）。抑揚（prosody）などの上乗せ機能は別料金なので、このゲームでは**使わない**（確認ページも使っていない）。
- 計算：宣言文70語は約35〜42秒（011）。始めと終わりの2回で約80秒。窓口の読み返し（58語。70語から比例させた目安で約29〜35秒。実測ではない）を足すと、1人あたり約110〜115秒。5時間＝18,000秒 ÷ 115秒 ＝ **月に約155人ぶん**（言い直しがあれば、その分減る）。
- 従量課金（S0）に切り替えた場合の目安は音声1時間あたり約$1（出典：Microsoft Q&A https://learn.microsoft.com/en-us/answers/questions/5608069/ ：公式の料金表の数字そのものではない）。この目安だと1人あたり約0.02ドル。**この金額は公式表で未確認。**

**未確認（キングの画面で確認してください）**
- 作成済みの Azure リソースが F0（無料）か S0（従量）か。ポータルのリソースの「Pricing tier」で見られる。F0 なら上限で止まるだけで請求は出ない。S0 なら、Azure の「Cost Management」で予算アラートを付けておく。
- 公式の料金ページ本体は、この作業環境から開けず、検索結果の抜粋とMicrosoft Learnの記述で確認した。

---

# 英会話カフェの自由会話（タスク073）：返事AIの設定　確認日：2026-11-24

ゲーム側は、先生の返事を同じ中継の `POST /chat` にお願いします。**キーはゲームにも、リポジトリにも入りません。**
`/chat` は、①Cloudflare の Workers AI（バインディング）→ ②外部API（Groq・用意したときだけ）の順に試します。どちらも未設定なら 503 を返し、ゲームは先生のやさしい結びの一言で場面を終えます（エラー画面は出ません）。**何も設定しなくても、ゲームは壊れません。**

## 手順A：中継を作り直して出し直す（必須）
`relay/worker.js` が新しくなったので、Cloudflare に出し直します（手順2と同じ「Worker のコードを貼って Deploy」。コードはクロが用意したものをそのまま貼る）。出し直しでも、既存のシークレット・変数は消えません。

## 手順B：Workers AI をつなぐ（①。キーは不要）
つなぎ方は2通りあります。
- **wrangler で出す場合（確認済みの書き方）**：`relay/wrangler.toml` に `[ai]` / `binding = "AI"` を足してあります（出典：https://developers.cloudflare.com/workers-ai/configuration/bindings/ ）。`wrangler deploy` で有効になります。
- **画面（ダッシュボード）で出している場合**：Worker の設定画面に AI のバインディングを足す場所があるはずですが、**この作業環境では画面の名前・場所を確認できていません（未確認）**。見つからないときは、Worker の設定画面のスクリーンショットを送ってください。画面を見て案内します。
- 変数名（バインディング名）は `AI` と、大文字2文字で入れる。

## 手順C：外部API（Groq）を予備につなぐ（②。①が使えないときだけ。やらなくてもよい）
1. Groq のサイトでアカウントを作り、APIキーを作る（画面の名前は変わることがあります。見つからないときは教えてください）。
2. Cloudflare の Worker の設定で、次を登録する。
   - 変数 `CHAT_API_URL` ＝ `https://api.groq.com/openai/v1/chat/completions`
   - 変数 `CHAT_MODEL` ＝ `llama-3.1-8b-instant`（未設定でもこれが使われる）
   - **シークレット** `CHAT_API_KEY` ＝ Groq のキー（手順3の Azure のキーと同じ「シークレット」で登録する。キーはこの入力欄にだけ貼る。チャットにもリポジトリにも貼らない）
3. Gemini の無料枠と OpenRouter の無料枠は、子ども向けアプリの規約・1日50回の上限のため、つながないことにしています（決定）。

## `CHAT_MODEL` の決まり
- 先頭が `@`（例 `@cf/google/gemma-4-26b-a4b-it`）→ Workers AI のモデル名として使う。未設定なら `@cf/google/gemma-4-26b-a4b-it`。
- `@` で始まらない（例 `llama-3.1-8b-instant`）→ 外部APIのモデル名として使う。
- **注意**：Workers AI の Llama 3.1 8B(fp8)・Llama 3.2 3B は、公式の一覧で廃止日が 2026-11-20 と書かれていた（確認日 2026-11-24。https://developers.cloudflare.com/workers-ai/models/ ）。古いモデル名を `CHAT_MODEL` に入れないでください。

## うまくいかないとき（`/chat`）
- 「503」：AIバインディングも外部APIも未設定。手順B（または C）をやる。ゲームは先生の結びの一言で終わる。
- 「502」：AI・外部APIのどちらも答えなかった（モデル名の廃止・キー違い・上限など）。Cloudflare の Worker の「ログ」で確認する。
- 「429」：同じ端末から1分に20回を超えた（`/token` の12回とは別に数える）。

## 費用（確認日：2026-11-24）
- Workers AI の無料枠は **1日 10,000 Neurons**（超えると止まる。請求はされない）。出典：https://developers.cloudflare.com/workers-ai/platform/pricing/
- **1往復あたりの Neurons は、実機で測っていない（未確認）。** 目安としての見込みは約7 Neurons／往復（先生の設定文＋直近12発言を送る見積り）だが、これは**測った数字ではない**。1人5分で最大30往復なので、1日に遊べる人数は最初に Cloudflare の「使用量」画面で実測してから判断してください。
- Groq の無料枠の上限は、**この作業環境では公式の数字を確認できていません（未確認）**。つなぐ前に Groq の画面で確認してください。
