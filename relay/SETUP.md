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
- この中継は、プレイヤー1回の「始め」と「終わり」で各1回、トークンをもらうだけ。1日10万回には遠い。

**Azure Speech（East US）**
- 無料プラン（F0）：音声→文字の標準リアルタイムが月5時間まで無料。出典：https://azure.microsoft.com/en-us/pricing/details/speech/
- 発音評価の料金は、基本は音声→文字と同じ扱い（出典：Microsoft Learn「Use pronunciation assessment」https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment）。抑揚（prosody）などの上乗せ機能は別料金なので、このゲームでは**使わない**（確認ページも使っていない）。
- 計算：宣言文70語は約35〜42秒（011）。始めと終わりの2回で約80秒。5時間＝18,000秒 ÷ 80秒 ＝ **月に約225人ぶん**。
- 従量課金（S0）に切り替えた場合の目安は音声1時間あたり約$1（出典：Microsoft Q&A https://learn.microsoft.com/en-us/answers/questions/5608069/ ：公式の料金表の数字そのものではない）。この目安だと1人あたり約0.02ドル。**この金額は公式表で未確認。**

**未確認（キングの画面で確認してください）**
- 作成済みの Azure リソースが F0（無料）か S0（従量）か。ポータルのリソースの「Pricing tier」で見られる。F0 なら上限で止まるだけで請求は出ない。S0 なら、Azure の「Cost Management」で予算アラートを付けておく。
- 公式の料金ページ本体は、この作業環境から開けず、検索結果の抜粋とMicrosoft Learnの記述で確認した。
