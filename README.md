# 空港えいご物語

空港を舞台にした英会話のリハーサルゲーム(試作・私用)。

## 声について

- このゲームは、声を保存しません。ただし1つだけ例外があります：最初の長距離フライトで機内アナウンスを読んだ声だけは、その便のあいだ、この端末の中（ブラウザの IndexedDB `kanpe-pa-rec-v1`）に置き、食事の場面で流します。外には一切送りません（Azure の経路とは別で、通信するコードがありません）。食事の場面が終わるか、便が終わると消えます。マイクが使えない・許可しない・「こえをださない」のときは、静かに飛ばします。
- マイクの声は、ブラウザの音声認識で文字にします。ブラウザの種類によって、Google（Chrome）や Apple（Safari）のサーバーに声が送られます。
- プレイヤーが「送ってOK」を選んだときだけ、旅の始めの宣言・窓口での券の読み返し・旅の終わりの宣言の3つの場面（言い直したときの声も含む）で、声が、発音を調べるために Microsoft Azure に送られます。送らなくても、最後まで同じ物語を遊べます。選びは、設定でいつでも変えられます。
- 同意の画面（ゲーム内）は短い文にしてあります。くわしい内容は、ここに書きます：
  - 送るのは、旅のはじめの宣言・窓口での券の読み上げ・旅のおわりの宣言の3つの場面だけです。言い直したときの声も送ります。ほかの場面の声は Azure には送りません（ほかの場面では、ブラウザの音声認識が声を文字にします。Chrome なら Google、Safari なら Apple のサービスです）。
  - ゲームは声を保存しません。Microsoft は、リアルタイムの音声→文字では音声をサーバーのメモリ上で処理し、保存しないと説明しています（Microsoft Learn「Data and Privacy for Speech to text」）。
  - 結果は、この端末の中だけに残ります。送らなくても、ゲームは最後まで同じように遊べます。いつでも、設定で変えられます。
- Azure に送るときの合鍵は、Cloudflare の中継が渡します。声は中継を通りません。
- 発音の記録は、各自のブラウザ（localStorage）にだけ残り、ゲームの運営側には集まりません。設定の「声の記録を消す」で、始めと終わりの比べの記録を消せます。

## ページのならび

- `/` : オープニング(`world/`)へ自動で移る。
- `world/` : オープニングと世界マップ。羽田から、グアム・ナイロビ(世界一周編)へ飛ぶ。
- `guam/` : グアム編(時計版)。20空港の現地時刻と日本時間を時計に表示する。天気は Open-Meteo(個人情報なし)から取得し、取れないときは月ごとの平均で表示する。
- `dubai/` : ドバイ編(以前はトップにあった)。世界一周編の元になる本体。
- `tour/` : 世界一周編 賢者・窓口・ナイロビ(到着・空港・出発)。機内の会話を終えると、世界マップの飛ぶ画面をはさんでドーハへ。
- `tour/doha/` : 世界一周編 ドーハ(到着)。
- `tour/rovaniemi/` : 世界一周編 ロヴァニエミ(到着)。
- `tour/honolulu/` : 世界一周編 ホノルル(到着4・街3・出発3の10場面。到着は国内線で入国審査なし・出発はシドニー行き)。`tour/frankfurt/` の次(ニューヨーク100との接続は未)。
- `tour/frankfurt/` : 世界一周編 フランクフルト(鉄道の到着・街・出発の10場面。入国審査なし)。`tour/athens/` の次。
- `tour/sydney/` : 世界一周編 シドニー(到着4=SmartGate・ゲートと窓口・検疫・空港の駅／街3／出発3の10場面)。出発案内板の中身は別素材(`tour/assets/art/sydney-board-sin-strip.png`、作り方 `tour-src/art/prep_sydney102.py`)。探知犬は別素材で後から足す。ホノルル(101)の次。
- `tour/rome/` : 世界一周編 ローマ(到着4・街3・出発3の10場面。入国審査なし、出発は鉄道)。発車標の中身は背景に描かず別素材(`tour/assets/art/rome-departure-board-strip.png`、`python3 -I tour-src/art/prep_rome_board.py` で生成)を重ねる。点検: `tour/rome/?check=1`、テスト: `tour-src/tests/test_rome094.py`。

## 実機の点検用「チェックモード」

`tour/` と `tour/doha/` のURLに `?check=1` を付けた時だけ動く(付けなければ従来どおり)。全場所がロックなしで開き、左端の「CHECK」から場面一覧を開いて、どの場面も直接始められる(券は Star / oneworld を一覧で切りかえ、前の場面・券・お金は満たした扱い。割りこみは自動では入らず、一覧から始める)。進行は専用キー `chk1:…` にだけ入り、通常のセーブ(`kanpe-…`)は読みも書きも消しもしない。旅の骨組み(DAY・お金・場所の鍵)は動かさない。対象はナイロビ・ドーハ(`tour/ending/` は対象外)。実装は `tour-src/check_shim.js`(記録の向きかえ)と `tour-src/check.js`(一覧)、build.py の `window.__CHK` の分岐。確認は `python3 tour-src/tests/test_check056.py`。

## 世界一周編の作り方

`tour-src/data.py` に会話、`tour-src/build.py` に場所・人物・背景・音を書き、`python3 tour-src/build.py` で `dubai/index.html` から `tour/index.html` と `tour/doha/index.html` を作る(`pip install cmudict` が必要)。
旅の骨組み(DAY・券の束・日ごとの記録 `kanpe-trip-v1`・精算とアルバム)は `tour-src/trip.js` 1か所。ビルドが tour/・tour/doha/・tour/ending/ と、`world/index.html` の `/*TRIPJS-BEGIN*/…/*TRIPJS-END*/` の間に入れる。どの日にどの場面を載せるかは `trip.js` の `ROWS`(30日の表)と `GROUPS`(場面のまとまり)。確認は `tour-src/tests/test_trip030*.py`。

## 発音記号について

強化合宿の発音記号は、CMU Pronouncing Dictionary(米国英語の公開辞書)から、このゲームの会話に出る単語分を作って埋め込んでいます。

## 開発の記録・ルール（AIも人も最初に読む）

`CLAUDE.md`（入口）、`docs/rules.md`（ルール）、`docs/handover.md`（引き継ぎ）、`docs/world-tour-design.md`（世界一周編の設計図）、`docs/materials/`（イベント素材集）、`docs/sources.md`（参考URL）。
