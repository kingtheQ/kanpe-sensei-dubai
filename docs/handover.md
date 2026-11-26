# 引き継ぎまとめ（2026-11-16 時点）

別のAI・別のチャットがこのリポジトリを読んで続きを作るための記録です。**先に `CLAUDE.md` と `docs/rules.md` を読んでください。決定の正本は `docs/pm/DECISIONS.md`（資料と食い違うときはこちらを優先し、PMに確認）。**

## いまの状態
- 公開物：グアム編・ドバイ編・世界一周編（賢者・窓口・ナイロビ・ドーハ到着）・オープニングと世界マップ。ページ構成は `README.md` を参照。
- 世界一周編は `tour-src/data.py`（会話）と `tour-src/build.py`（場所・人物・背景・音）から `python3 tour-src/build.py` で生成する（`pip install cmudict` が必要）。
- 最新のコード変更：c833e47「おてほんの間は聞くのを止める(ドバイ本体・グアム)、券を買ったあとは賢者タブを出さない」（11/14）。そのあとは文書のコミット（最新は 5878034「007 ゲームルール全体の監査」、11/16）。この文書を更新した回で、docs の合わせ直し・006 段0（a〜d）・台本の食いちがい修正が入った。
- PM試行（11/15〜）：PM＝おちゃ、設計案づくり＝Fable、コード＝クロ。決定は `docs/pm/DECISIONS.md`、運用は `docs/pm/README.md`。
- 成果物（すべて**設計案であり決定ではない**。`docs/pm/deliverables/`）：003 冒頭（賢者＋窓口）、004 発音の弱点の把握、005 「飽きてきた」対策（台本の棚卸しつき）、006 強化合宿の設計レビュー（追補：筋トレの前提）、007 ゲームルール全体の監査（食いちがい22件）。

## 今回（11/11〜11/14）決まったこと
詳細は `docs/rules.md` の第9章。要点：
- 世界一周編の名前は KING & LULU WORLD JOURNEY。空港が主役、空港50％・観光ほか50％、約30日、5000語、何度でも遊べる（券＝ルールセットの入れ替え）。
- 広告のキャッチは「100万円の世界一周航空券、まずゲームで買ってみた。」。
- 始まり：賢者（心構え・後悔しない助言）＋チケット窓口（希望を聞いて券をすすめ、買う流れで決まりを学ぶ）。聞き取りは12種類の「旅のしかた」を係員の質問にする。
- 51空港を最終的に全部作る。リサーチは2周目（リスボン・アテネ）でしめ、組み立てに入る。
- 組み立ては1周目→2周目。まず「A 流れを1周つなぐ」（トップ→世界マップ⇄世界一周編→ナイロビ出発・機内→次の空港の到着）。ナイロビの次は仮にドーハ。世界マップからの入口は「羽田の搭乗ゲートで西の？？の国を選ぶ」（新しいボタンは足さない）。
- 到着・出発は順番に開く／国クリア後は世界マップへ戻す／券購入後のナイロビに賢者を出さない／会話で「東京へ行く」と言わせない。
- グアム編をドバイ編に合わせる（設定・文字色・自動で聞き始める・強化合宿）。世界マップ上の「いまの ばしょ」枠は枠なし・薄い黄色・黒文字。

## 11/15〜11/16 に決まったこと（`docs/pm/DECISIONS.md`）
- 日本語はなるべく使わない。「復習」の言葉・画面は入れない（くり返しは物語の必然の中で）。
- 文字を打つ入力なし／NPCに近づいてタップなし（イベントはプレイヤーの方に来る）。
- 既存の英語アプリの型（並べ替え、英単語→日本語3択、聞き取り→選択肢のくり返し）は流用しない。Word Battle の3択は廃止の方向で、タイマーは選別装置。
- 単語5,000語（最初の2,809語は NGSL）。場面は空港5割・市内5割。
- 到着は「国旗＋国の色＋ふざけた一言＋現地の挨拶」の1枚画面。スタンプは自作。
- 発音の合格ラインは今のまま（7割）。冒頭の診断は「まとまった文」を物語の中で話させる。
- 発音は「筋トレ」（口の筋肉を動かせば覚える）。目的は勉強から脱して楽しく旅すること（11/16）。
- 相棒ルルは「英語が得意なロボット」（キングの前提。ゲームの中の言葉にはまだ出していない）。

## 今回（11/16）コードでやったこと
- 強化合宿（006 段0 a〜d）：合宿で言えたものを記録に戻して「言えなかった」から外す／続けて同じ音・単語を出さない／マップから入っても言えた文を消す／Word Battle の間違い・時間切れの記録（出口は未作成）。
- 世界一周編の台本の食いちがい：スーツケースを青・黄タグに統一（ドーハ側を直した）、ナイロビのラウンジ会話を出発前の内容に、搭乗ゲートを「出発」タブのチェックイン・保安検査のあとへ、nbo_java2 の話者を「となりのお客さん」に。

## 今回（11/17）タスク016でやったこと
- 声の同意の1枚・設定・Azure接続（`tour-src/voice.js`、長いカンペの読み取りは `diag.js`）、記録 `kanpe-voice-v1`、終わりの場面 `tour/ending/`（`tour-src/ending.js`）。詳細と対応表は `docs/pm/deliverables/016-ending-impl-report-v1.md`
- 中継 URL は `tour-src/relay-url.txt` の1か所（空なら Azure 無効・同意の1枚も出ない）。確認は `python3 tour-src/tests/test_routes.py`
- 未確認：マイクと Azure 実通信（実機）。決めた区切り（色 80/60、良くなった5点）と4数字の式は仮

## 今回（11/18）タスク030でやったこと（旅の骨組み）
- `tour-src/trip.js`（新規）：DAY（朝の1枚を開いた回数）・券の束（つづり）・日ごとの記録 `kanpe-trip-v1`・夜の1枚・精算とアルバムの1日1ページ。ビルドが tour/・tour/doha/・tour/ending/ に入れ、world/index.html は `/*TRIPJS-BEGIN*/…/*TRIPJS-END*/` の間に入れる（手書きの world はこの間だけ生成）。
- 世界マップ：「クリア n / 20」をやめ、旅の中は「区間 n / 13」、旅の外は「スタンプ n」。未実装の行き先（次の区間だけ）は「もうすぐ」で出し、入れない。
- 既存場面の割り当て（oneworld：1窓口／2ナイロビ到着4／6ナイロビ空港4+出発4+ドーハ到着4／7ドーハ市内5+ホテルの朝1／9ドーハ出発5。スター：1窓口／3ナイロビ到着4／6ナイロビ空港4）。表は `trip.js` の `ROWS` と `GROUPS`。
- 確認：`python3 tour-src/tests/test_trip030.py`（はじめから→券→つづり→ナイロビ）、`test_trip030_ending.py`（精算・アルバム）、`test_trip030_doha.py`（日の鍵）。報告は `docs/pm/deliverables/030-journey-structure-impl-report-v1.md`。
- 決まったこと（DECISIONS.md「旅の骨組み」に記録済み）：020-1〜12 すべて／スターはナイロビで止まるまま（アディスアベバは後で作る）／未実装の日は飛ばす／夜の1枚は自動／搭乗券にちぎった実日付を出す／ホテルの朝は7日目／タクシー・メトロの値段は目安のまま。
- まだ実装していないこと：場面の現地時刻の切り替え、休養日に単語バトル・合宿の入口を隠す、スパルタ時間（休養の翌日の★）、何もない日の写真（素の瞬間の絵）、29日目の読み上げ5項目のうち 手数料・別切符 と 選んだ重さ（3項目までは入っている）。表の9日目「空港12本」と既存8本の差も未確認。
- 守ること：画面に「復習」「テスト」「測定」を出さない／連続記録を使わない／写真・声・個人情報は記録に入れない（写真は場面の名前だけ）。

## 今回（11/18）タスク035でやったこと（冒頭の発音の結果を、鍛える音に反映）
- `trainSounds()`（`dubai/index.html`、build で `tour/` へ）：`kanpe-pron-v1` から音ごとの弱さ＝(X+0.5)/(N+2)を毎回計算（新しい保存キーなし）。「弱い音」は2つ以上の違う単語・2つ以上の場面で失敗した音だけ。上位3つが「鍛える音」。合宿の記録（camp）は出た回数に入り（言えるほど弱さが下がる）、場面の数には入れない。何も聞こえなかった回（hd が空）は数えない。
- 反映：合宿（`pickLessons`）は鍛える音の中から選ぶ（直近の音は後ろ）。単語バトル（`startWords`）は、場面の語のうち鍛える音をふくむ語を最大2つ先に出す（語は増減しない）。記録が無い・少ないときは変更前と同じ。
- 確認：`OLDROOT=<変更前の作業コピー> python3 tour-src/tests/test_train035.py`（集計・式・上位3つ・src の印・壊れた記録・変更前との同一性）。画面には何も足していない。
- 未実装：場面の語を、鍛える音の語へ言い分けで差し替える（設計004 4-1 規則1）。単語バトルは場面の語が固定なので、いまは出す順だけ。

## 今回（11/18）タスク033でやったこと（つづりの点滅）
- 原因：世界マップ（world/）の `.star`（きらめきの点：2px四方・明滅アニメ）と、Star Alliance 券のクラス名 `star` が衝突。券が高さ2pxに潰れ、文字が重なって点滅していた（oneworld 券は無事）。`.top`（世界マップの上の帯）も、ちぎる動きの `top` と衝突していた。
- 直し：券とちぎる動きのクラスを `tp-` 付きに変更（`tour-src/trip.js`）。数えの表示：上は `Landed 0 / 13`、券の角は `FLIGHT 1 / 13`。
- 確認：`python3 tour-src/tests/test_bundle033.py`（Android Chrome 相当の画面。実機は未確認）。
- ビルドには `pip install cmudict` が必要（なしだと発音記号が変わる）。

## 今回（11/18）タスク032でやったこと（決まったのに骨組みに入っていなかった5項目）
- ブランチ `task-032-trip-gaps`（1項目1コミット）。詳細と未確認は `docs/pm/deliverables/032-trip-gaps-report-v1.md`。
- 020-3 時刻：`TRIP.hourNow`（旅の途中の昼の間は、その場所の旅の中の時刻。それ以外は実時計）。表は `TRIP.HOUR`（物語上の時刻。実在の便ではない）。
- 020-7 休養日：単語バトル・合宿の入口なし、場所は全部閉じる、朝の1枚に NOTICE。飽きサインは数えない。
- 020-10 精算：手数料（`TRIP.addFee`）と別切符（95 USD・架空）の読み上げ。保存は `led` に入る（形式は変えていない）。
- 020-8 スパルタ時間：★の入口の枠（`TRIP.spartaDone` / `isSparta`）。中身は今の合宿。作り直しはタスク017。
- 020-9 写真：`TRIP.RAW`（face/sleep/snack）。`TRIP.setRaw` / `setRawImage` で差し替え。
- テスト：`tour-src/tests/test_{time,rest,settle,sparta,raw}032.py`（ヘッドレス。マイク・実機は未確認）。

## 今回（11/20）タスク045でやったこと（ナイロビの荷物受取）
- 手荷物受け取り（`nbo_bag1/2`、bg=baggage）が新しい背景＋荷物アニメで出る。荷物6個が楕円（中心(800,660)・356×56）を1周24秒、奥の荷物は島のうしろ（`tour-src/art.js` の `artBelt`、ART `bagclaim`）。素材の作り方は `tour-src/art/prep_baggage.py`（荷物の外の画素が素材と一致しなければ止まる）。雨もり出来事ではベルトが止まる。ドーハの手荷物は今のまま。
- 確認：`python3 tour-src/tests/test_bag045.py`（周期の実測24.0秒ほか）。報告と**会話文の下書き（PM確認待ち・未組み込み）**は `docs/pm/deliverables/045-baggage-report-v1.md`。
- 未確認：実機での見え方・滑らかさ。指示書 `pm-kit/tasks/045-…md` と `kanpe-assets-baggage-045.zip` はリポジトリに無く、依頼文と素材の zip の中身で実装した。

## 今回（11/20）タスク046でやったこと（荷物受取の会話文の本組み込み）
- PM決定の案A：`nbo_bag1` を、045の下書き（同じ便の旅行者と5往復・青+黄タグのスーツケースを見つけて取る）に**置き換え**。id は `nbo_bag1` のまま（trip.js・場所の並び・セーブのキーは無変更）。雨もりを遊んだあとは**1行目**が「雨でベルトが止まっていた」を受ける（`event_data.py` の VARIANTS）。
- 旅行者 `SP.traveler`：声 pitch=1.0、見た目は d_metrop 系。専用スーツケース（青+黄タグ）はスプライト2行目を差し替え（`tour-src/art/prep_hero_bag.py`）。台詞3のあいだ緑の板のとなりに来て、台詞5・`nbo_bag2` ではベルトから消える（`art.js` の `artHeroTh`）。
- 確認：`python3 tour-src/tests/test_bag046.py`。報告は `docs/pm/deliverables/046-baggage-dialogue-report-v1.md`。未確認：実機の見え方・音。

## 今回（11/21）タスク049でやったこと（宣言文ソング）
- オープニングのチャント版（`sage_1`、DAY 1 のあとの最初の GO！で1回・音量0.2）と、ナイロビのホテルロビーの歌手の「聴く」場面（`nbo_song`／場所 `hsong`、到着タブ・任意）を組み込んだ。キングの決定：完了条件に入れない・曲の途中でも離れられる。テーマ曲はこの場面だけ。詳細と数字は `docs/pm/deliverables/049-song-impl-report-v1.md`。
- 未確認：実機の音量・iPhone・マイクとの重なり。Suno曲の公開利用の権利はキングが確認。新しい参考URLなし。

## 今回（11/21）タスク048でやったこと（CAアナウンス・イベント）
- 最初の長距離便（羽田→ドーハ=oneworld／→イスタンブール=Star）の機内のあと、CAが放送を頼む → マイク画面（カンペを意味のまとまりで区切って表示。ボタン: おてほん／はなす→もういちど・これでOK）→ 食事の場面でチャイム→自分の声の放送→ルルの反応、の順。
- 声は端末内だけ（IndexedDB `kanpe-pa-rec-v1`。`kanpe-pron-v1` とは別）。通信するコードなし（`tour-src/pa.js`）。「これでOK」まで保存せず、食事の場面が終わる／便が終わると消す。6時間たった物・再生済みの物は起動時に捨てる。
- マイク不許可・MediaRecorderなし・こえをださないモードでは静かに飛ばす。1回きり（`save.ev.fired.pa1`）。`?ev=off` で無効。
- 変更点（PMに報告）: 放送文の到着時刻は「in the morning」（PM案は evening。ドーハ到着の現地時刻に合わせた）／おてほんボタンを追加／プライバシーの注意書きを旅編だけ書き換え（`SNOTE_TOUR`）／SDのCA絵は使わず資産として保管。
- 作った物: `tour-src/pa.js` `pa.css` `pa_data.py` `tests/test_pa048.py`、`art.js` に機内アップの背景2枚。実機（iPhone/Android）のマイク・録音形式・音量は未確認。

## 今回（11/22）タスク056でやったこと（実機点検用のチェックモード）
- `tour/`・`tour/doha/` に `?check=1` を付けた時だけ動く点検モード。全場所ロックなし／左端の「CHECK」で場面一覧（各場所の場面・割りこみ・窓口の各段）から直接開始／券は一覧で切りかえ・前の場面は満たした扱い／進行は専用キー `chk1:` で通常のセーブに触れない／旅の骨組み（TRIP）は動かさない。パラメータなしは従来どおり（生成物の差分はゲート付きの追加だけ）。
- 確認：`tour-src/tests/test_check056.py`（通常時の不変・全場面の直接開始・通常セーブの不変）。既存テストは通る（trip030・people047 は変更前の main でも同じく失敗＝今回の変更とは無関係）。未確認：実機の見え方・マイク。点検モードのまま 世界マップ(🌏)・強化合宿へ行くと、そのページは通常モードになる。対象外：`tour/ending/`。

## 今回（11/24）タスク070でやったこと（ドーハのコルニーシュの実画 ccorn）
- 対象は bg ccorn の4場面（doh_city_c1/c2/c3・doh_ev_j_ask、すべて doha 側）。ART `dcorn`（tour-src/art.js）：背景 doha-corniche-v1.png・wide・足もと y=884・ルル x=1060・キング x=1180・ふたりは右から歩いて入る(dir:-1)・スーツケースは左どなり(x=960)・相手は左の舗道(x=800)
- 結びは doha 側 artIdFor（build.py）だけ。doh_city_h1→'hotel' は据え置き。ナイロビ側 artIdFor は触っていない
- 別素材 strips：きらめき(0,372,4コマ,0.5秒)・ダウ舟(700,258,2コマ,0.8秒・その場で揺れる)。実画の表示中はドット描画(BGS.ccorn)のキャンバスが隠れるので舟は二重に出ない。実画が読めないときだけ BGS.ccorn に落ちる
- 台詞は変更なし。テスト: tour-src/tests/test_corniche070.py
- 参考: 同梱の指示書 070-doha-corniche-binding.md（正本は pm-kit/tasks/）

## 今回（11/22）タスク060でやったこと（ホテル歌場面のステージと観客）
- 歌場面（`nbo_song`）の背景を歌場面版（`nairobi-hotel-lobby-song-v1.png`、art 設定 `nsong`）に。歌手は台の上、観客5人は半円、ルル・キングは中央。入りは「観客の絵→つぎへ→ルルの一言（英語のみ）→GO！→歌」。歌・曲後の会話・ほかの場面は変更なし。通常のロビー（`nlobby`）は残してある。詳細・数字・プレビューとの違いは `docs/pm/deliverables/060-song-stage-report-v1.md`。

## 今回（11/24）タスク071でやったこと（ドーハ・スークの実画）
- bg `calley`（夜の路地）= `doh_city_t1/t2/t3` と割りこみ `doh_ev_h_prayer` に ART `dalley`、bg `csouq`（昼の広場）= `doh_city_s1/s2/s3`（店の3場面は「店先の広場」の絵で統一・PM判断）に ART `dsouq` を結んだ。結びは doha 側ビルドの `artIdFor`（build.py）だけ。`doh_city_h1`→'hotel' は不変。ナイロビ側 artIdFor は触っていない。
- 別素材: 路地=ランタン(step1)・吊り布(step0.8)とも全面(0,0)・1536×960、広場=屋台布 (0,452) 1536×176 step0.8・鳥 (0,36) 1536×120 step0.4（その場の羽ばたきのみ）。素材は `tour/assets/art/doha-souq-*`、配置の正本プレビューは `docs/materials/071/`。
- art.js に `nosuit` を追加（プレビューにスーツケースが無いので出さない。既存の場面は影響なし）。`doh_city_t3` のルル不在は既存の `lvis` の出し分けのまま。台詞・会話・セーブ形式は変えていない。
- テスト `test_souq071.py`（背景・2コマの動きを素材との画素一致で確認、?check=1 経由）。相手の人（既存のドット絵の顔）の位置は路地=x228（プレビューの人の位置）・広場=x980（プレビューに人がいないので仮）。広場の x980 はキング確認の余地あり。
- 実機の見え方は未確認。`test_doha023.py` は今回の変更の前から200秒で終わらない（最新main単体でも同じ）ため、今回の確認には使えていない。

## 今回（11/23）タスク059でやったこと（羽田の秘密イベントの回収場面）
- 28日目の羽田（oneworld）に `hnd_return` を追加。1日目に拾った落とし物（木のおもちゃの飛行機）を持ち主に返す。保存の `keep.hnd1` があるセーブだけに出る（`trip.js` の `GCOND`）。新しい保存キーなし。カバンの記録帳の1行が「ひろった」→「かえした」に変わる。
- 背景は既存の出発ゲート。会話は053の分かれ目の型（英語のみ・日本語訳なし）。テスト `test_hnd059.py`（25 OK）。詳細は `docs/pm/deliverables/059-haneda-return-report-v1.md`。
- 実機（マイク・音・見え方）は未確認。途中の日（10〜27日）はまだ作っていないため、28日目へ自然に進む通し遊びは未確認（テストは保存を直接つくって確認）。
- 参考にしたURL：なし。

## 今回（11/24）タスク064でやったこと（ドーハ入国審査の実画）
- bg が dimmig の3場面（doh_immig1 / doh_immig2 / doh_dep_passport）の背景を、コード描画から実画 `doha-immigration-v1.png` に差し替え。art id は dimmig（doh_immig2 だけ dimmig2＝話し相手が右の窓口）。artIdFor は本編側・ドーハ側の両方に結び、vid が doh_ のときだけ効く（ナイロビの immig・羽田の同名 bg は変わらない）。
- 係官は3窓口とも同じ絵（o-front-officer-blue）を ×0.93（表示51×127）、top=511・clip=600 で頭と肩だけ。表示灯は `doha-immigration-lights-strip.png`（2コマ・(0,300)・1秒ごと）。ガラス越しの薄い色（190,215,226 の22%）と、ロープの中の後ろ姿2人・ふたりの立ち位置は、同梱の正本プレビューに合わせた。
- 倍率つきの窓口（booths の `s`）とガラス（`glass`）は art.js に足した汎用の部品。ナイロビの immig は変わらない。テスト `test_doha064.py`（全OK）。
- 未確認：実機の見え方。ふたりの荷物はナイロビの入国審査と同じ簡易の絵（正本プレビューの青いスーツケースとは形が違う）。指示書 064-doha-immigration-binding.md は添付・リポジトリになかったため、README とキングの要点・正本プレビューを仕様にした。
- 参考にしたURL：なし。

## 今回（11/22）タスク058でやったこと（ナイロビ滞在の観光2場面）
- 「滞在」タブ（🦒）にサファリ `nbo_safari`・マサイマーケット `nbo_market` を追加。oneworld は3日目＝市場・4日目＝サファリ、スターは4日目に両方。053の分かれ目の会話・裏の計測・夢への持ち越し。テスト `test_stay058.py`（49 OK）。詳細は `docs/pm/deliverables/058-stay-safari-market-report-v1.md`。
- 実機（マイク・音・見え方）は未確認。`pages.yml` が `tour/assets/` を公開に入れていない件は未確認のまま報告のみ。
- 参考にしたURL：なし（素材は同梱パックのみ）。

## 今回（11/26）タスク090・091でやったこと（アテネ到着4＋街3＋出発3、マイク画像の差し替え）
- **マイク**：`MICBIG_IMG` を同梱の `tour/assets/art/mic-large-v1.png` に差し替え（`window.js`）。表示のタイミング(`.on`)と箱の大きさ(84×119)は変更なし。正方形の絵は `object-fit:contain`(下そろえ)で収めた(`window.css`)。画像が読めないときは従来のコード描画(`declMicPix`)に戻る。
- **アテネ10場面**（`tour-src/ath_data.py`、`data.py` の最後で `ath_data.add(D)`）。すべて新形式（flow2・conv・選択は場面に1回・カード式）。生成物は `tour/athens/index.html`（`build.py` の MAIN_ATH）。
  - 到着(4): ath_immig1・ath_immig2(EES：顔写真と指紋、スタンプなし)・ath_taxi1(客引き→定額)・ath_transit1(地下鉄の空港用切符。**金額は台詞に出さない**)。背景 athens-arrival-v1。
  - 街(3): ath_cafe1(タベルナ)・ath_shop1(おみやげ屋)・ath_hotel1(チェックインと朝食)。背景 athens-street-v1 / athens-hotel-v1。
  - 出発(3): ath_checkin1・ath_depimmig1(出発30分前の優先)・ath_gate1(時刻変更)。背景 athens-departure-v1。**時刻・搭乗口番号・値段は台詞に入れていない**。
  - 数字の例外は2つだけ：taxi の「forty euros」（PM指示の定額）と depimmig の「thirty minutes」（指示の場面設定）。
  - 場所：aimmig/ataxi/ametro・acafe/ashop/ahotel・acheck/adepimm/agate。ロヴァニエミ(072)の次の都市として世界マップ(`world/index.html` の AP/NEI)・旅の骨組みの GROUPS/PLACEGRP/MODEGRP/HOUR/THEME・IMPL(ATH)に追加。
  - チェックモード：`tour/athens/?check=1` から10場面すべて選べる。ロヴァニエミのチェック画面に「アテネへ」のリンクを追加(`check.js` の `/*CHKX*/`)。
  - 人物の絵はアテネ専用がなく、既存の仮の絵を流用している（客引き・運転手は話者ごとに `cx` で切り替え）。ホテル名・店名は出していない。
- **未決（PMへ）**：旅の骨組みの `LEGS`/`ROWS`（30日表）にアテネの便がまだない。旅モードから飛行機でアテネへ行く道はない（世界マップと点検モードから入る）。また `LEGS.star` は088の統一ルート（ロヴァニエミの次がアテネ）と食い違ったまま。既存テスト(13区間など)を壊さないため触っていない。決めてもらったら表を直す。
- **参考にしたURL**（2026-11-26確認、`docs/sources.md` にも記載）：https://www.aia.gr/en/traveller/international-travellers ／ https://www.mfa.gr/ireland/en/new-eu-digital-entryexit-system-takes-full-effect-on-the-10th-of-april-2026/ ／ https://www.mfa.gr/missionsabroad/en/ireland-en/news/greece-to-start-using-eu-digital-entryexit-system-on-12-october-2025.html
- **ルール**：既存場面の台詞・流れは変えていない。画面に「復習/テスト/測定」を出さない。未確認の数字は台詞に入れない。マイク・実機の見え方・実機の音は未確認。
- テスト：`tour-src/tests/test_athens090.py` を追加。既存テストのうち、057系(flow2の場面数にアテネを含めない)・072(MODEGRPの文字列)・065(NEIの文字列)を、アテネ追加に合わせて直した。

## 今回（11/26）タスク093でやったこと（アテネ背景 v1→v2 差し替え）
- 背景4枚を v2（実写真を下絵に描き直した版）に差し替えた：`athens-arrival-v2`（到着4場面）・`athens-street-v2`（街2場面＝cafe/shop）・`athens-hotel-v2`（ath_hotel1）・`athens-departure-v2`（出発3場面）。置き場所は v1 と同じ `tour/assets/art/`（v1 は削除せず残した）。台詞・流れ・場面の順番・チェックモードの出し方は変えていない。変更は `tour-src/art.js` の `ART.ath*` だけ（生成物の `tour/*/index.html` は build.py で作り直し）。
- **v2 は構図が変わったため、配置を直した**（1536×960 の座標）：
  - 到着(ath_immig1・2)：窓口が3→5つ(6〜10番)になり、中央(8番)は x=769 のまま。カウンター上面が y=648→585。入国審査官の切り位置 clip 648→585、top を 63px 上へ(immig1 522→459・immig2 512→449)、吹き出しの予備位置 y480→417。
  - 街 cafe：タベルナが右→左の戸口(x30〜240)になった。店員を (1112,800) → (150,775) へ。
  - 街 shop：左の家の戸口が無くなり、おみやげの壁が右(x1212〜)になった。おみやげ屋の人を (271,780) → (1140,915) へ。
  - ホテル：v2 は手前が一面のベッド(y745〜)で床がない。ルル・キング・フロントの人の足もとを y=900 → 752（ベッドの奥の縁）へ。x は変更なし。
  - 出発 checkin：受付が3カウンター→1本の長い受付になり、上面が y=612→595。係員を x768→775（看板「123」と「eTicket」の隙間）、top 490→473、clip 612→595、吹き出しの予備位置 (768,450)→(775,433)。
  - 到着のタクシー・地下鉄・出発の出国審査・搭乗口(athtaxi/athmetro/athdep)と、ルル(x700)・キング(x836)の足もと y=884 は、v2 でも重ならず床の上なので変更なし。
- MOVES/STOPS の札と区間番号の札は、窓口の「線を引く地図」(`artRoute`)だけで描かれ、アテネの10場面には出ない。マイク(`.declmic`)はステージ右下に固定の別部品で、v2 でも置き去りにならない（右下は受付・床・壁で、人物と重なるのは到着のタクシー運転手(x1250)の左はしだけ。v1 のときと同じ位置関係）。
- テスト：`test_athens090.py` を v2 に更新（背景の対応・1536×960・配置の値の確認を追加。65 OK）。`test_eikaiwa068.py`・`test_gasshuku078.py` は「既存の ART が変更前(HEAD)と同じ」を見るガードで、意図して変えたアテネの `ath*` を除外に追加した（過去の nroom・ticket と同じ扱い）。
- 変更前(HEAD)から落ちていて今回の変更と無関係のテスト：`test_people047`（PM同梱の `nbo-bag1-traveler-preview.png` が必要）・`test_departure054`（085 の cabinQ の期待値が古い）・`test_time032`（空の昼夜）・`test_trip030`。
- 実機の見え方・マイク・音は未確認。参考にしたURL：なし（素材は同梱パックのみ）。

### 台詞全文（アテネ10場面）
### ath_immig1
- 係員: Hello, hello! A Japanese passport? No automatic gate for you today. Come to the window, please!
  - ルル/キング: Hello. Thank you. Here I come.
- 係員: Hat off, sunglasses off, please! I need to see your face. And the passport, open at the photo page!
  - ルル/キング: Sorry. Here is my passport.
- 係員: Good, good. Why are you visiting Greece?
  - 選択: We are here for sightseeing. → 係員: Sightseeing! The best reason. We have a lot of old stones here, my friend!
  - 選択: We are traveling around the world. → 係員: Around the world! Wonderful. Greece is a very good stop!
- 係員: And how long will you stay in Athens?
  - ルル/キング: We will stay for a few days.
- 係員: Perfect! Enjoy the sun and the old stones. Welcome to Greece, my friends!
  - ルル/キング: Thank you very much!
### ath_immig2
- 係員: Next, please! This is the new system. First, look at the camera. Straight, my friend, straight!
  - ルル/キング: Like this? Okay.
- 係員: Good photo! Now your fingers. Put them on the glass, please. Flat, flat!
  - ルル/キング: Is this right?
- 係員: Perfect. The machine is happy! Do you know the new system? It is called EES.
  - 選択: No, I didn't know. What is it? → 係員: It keeps a digital record of your face and fingers when you come in. Easy!
  - 選択: Yes, I read about it. → 係員: Smart traveler! Then you know the rule.
- 係員: So, no stamp in your passport now. The computer keeps the record, not the paper.
  - ルル/キング: No stamp? That is a little sad.
- 係員: Ha! I know, I know. Many travelers say so. Maybe next time it will be faster. Welcome to Athens!
  - ルル/キング: Thank you. See you!
### ath_taxi1
- 係員: Taxi, taxi, my friend! Good price, good price! Come, come with me!
  - 選択: No, thank you. We will go to the taxi rank. → 係員: Okay, okay, no problem! Have a nice day!
  - 選択: No, thank you. We only take the official taxi. → 係員: Okay, okay. You are smart! Have a nice day!
- 係員: Welcome! This is the taxi rank, the real one. Where to, my friends?
  - ルル/キング: To the city center, please.
- 係員: No problem! Please get in. The luggage goes in the back.
  - ルル/キング: Thank you. It is a fixed price of forty euros to the center, right?
- 係員: Yes, yes, correct! Forty euros to the center, a fixed price. No surprise, my friend!
  - ルル/キング: Good. Thank you for telling us.
- 係員: Sit back and relax. Welcome to Athens!
  - ルル/キング: Thank you. Efharisto!
### ath_transit1
- 係員: Hello, hello! You look lost, my friends. Can I help you?
  - ルル/キング: Yes, please. We want to go to the city by metro.
- 係員: Great choice! Look at the machine. There are many tickets. Which one do you want?
  - 選択: Which one is the airport ticket? → 係員: This one! Many people choose the wrong one, so you are smart to ask!
  - 選択: I want the cheapest ticket. → 係員: No, no, no! The cheap city ticket does not go to the airport. You need the airport ticket!
- 係員: Press the button for the airport ticket here. Then pay, and take your ticket.
  - ルル/キング: This button? Okay. Can I pay by card?
- 係員: Yes, a card is fine. The machine will tell you what to do. Easy, easy!
  - ルル/キング: Thank you. Which way is the train to the city?
- 係員: Follow the signs for the metro! The train comes soon. Have a good trip, my friends!
  - ルル/キング: Thank you very much. Bye!
### ath_cafe1
- 係員: Yia sas, my friends! Come, come! You look hungry!
  - ルル/キング: Yes, we are. What do you recommend?
- 係員: Gyros! Everybody loves it. Meat, tomato, onion, and pita, all together. Here, or to go?
  - 選択: We'll eat here, please. → 係員: Wonderful! Fresh and hot, coming right up!
  - 選択: To take away, please. Could you wrap it? → 係員: Of course! I wrap it nicely, no problem!
- 係員: Anything else? Try the loukoumades! Little fried sweets with honey. Very good!
  - ルル/キング: Sounds nice. We will try the loukoumades too.
- 係員: Excellent choice! Everything is almost ready. Please wait just a little.
  - ルル/キング: Thank you. It smells so good.
- 係員: Enjoy, enjoy! Come back again, my friends!
  - ルル/キング: We will. Thank you!
### ath_shop1
- 係員: Welcome, welcome! Look, touch, smell! Everything is made with love!
  - ルル/キング: Thank you. We like your sandals. Can we try a pair?
- 係員: Of course! Leather sandals, very comfortable. Try this pair. How do they feel?
  - 選択: They fit well. This size is good. → 係員: Perfect! Greek feet, I think!
  - 選択: They are a little tight. Do you have a bigger size? → 係員: Of course! Wait, wait, I bring the bigger ones!
- 係員: Good, good. Now look here. Mastic soap, and natural cosmetics. Very Greek!
  - ルル/キング: They smell nice. What is mastic?
- 係員: Mastic comes from a tree on a Greek island. We use it in sweets, and in cosmetics. Very special!
  - ルル/キング: Interesting. How much are the sandals?
- 係員: The price is on the little tag, my friend. And for two pairs, I make you a better price. Okay?
  - ルル/キング: Okay. We will think about it. Thank you!
### ath_hotel1
- 係員: Good evening, and welcome to Athens! Do you have a reservation?
  - ルル/キング: Yes, we do. Here is my passport.
- 係員: Perfect! I make your check-in, one moment! Please sign here.
  - ルル/キング: Here you are. Thank you.
- 係員: Done! Your room has a beautiful view of the Acropolis. You will love it, I promise!
  - ルル/キング: Wonderful! What time is breakfast tomorrow?
- 係員: Breakfast is in the restaurant, early in the morning. Do you prefer the restaurant, or your room?
  - 選択: We'll have breakfast in the restaurant. → 係員: Good choice! Fresh bread, fresh fruit, and good coffee!
  - 選択: Could we have breakfast in our room? → 係員: Of course! Just tell me tonight, and I arrange everything.
- 係員: Enjoy your stay, my friends! If you need anything, call me!
  - ルル/キング: Thank you. Good night!
### ath_checkin1
- 係員: Hello! Passport and ticket, please. Let's go, let's go!
  - ルル/キング: Here you are.
- 係員: Thank you. You want to check this bag, yes? Put it on the belt, please.
  - ルル/キング: Yes. Just this one suitcase.
- 係員: Good! Now, window seat, or aisle seat?
  - 選択: A window seat, please. → 係員: Window! You will see the clouds!
  - 選択: An aisle seat, please. → 係員: Aisle! Easy to stand up and walk!
- 係員: Here is your boarding pass. Now listen to me, my friends: passport control takes time today. Please go early!
  - ルル/キング: Is the line long today?
- 係員: It can be very long! Don't take your time. Go now, go, go!
  - ルル/キング: I see. We will go right now. Thank you!
### ath_depimmig1
- 係員: Next, next! Passport and boarding pass, please!
  - ルル/キング: Here you are. Our flight leaves in thirty minutes.
- 係員: Thirty minutes? Oh my! The line is long today. What do you need?
  - 選択: Is there a priority lane, please? → 係員: A priority lane? Not always, my friend. But your flight is soon, so I help you. Come, come!
  - 選択: We are in a hurry. Can we go first, please? → 係員: I understand, I understand. Okay, okay, come with me, quickly!
- 係員: This way! Please stand here. Passport open at the photo page.
  - ルル/キング: Thank you so much.
- 係員: Camera, please. Then your fingers. Fast, fast! Good!
  - ルル/キング: Okay. Is that all?
- 係員: All done! Now walk fast, but don't fall! Go, go, go!
  - ルル/キング: Thank you! Goodbye!
### ath_gate1
- 係員: Attention, my friends! Your flight has a change. The time is different now!
  - ルル/キング: Oh no. What is the new time?
- 係員: The flight leaves later than before. Please look at the screen. The new time is there. Very clear!
  - ルル/キング: Thank you. And the gate? Is it the same?
- 係員: The gate changed too! Please check the board. Do you want me to show you?
  - 選択: Yes, please show us the way. → 係員: Of course! Come, I show you. Follow me!
  - 選択: No, thank you. We will check the screen. → 係員: Good, good! The board is right there. You are very quick!
- 係員: Don't worry. You have time. Sit, drink some water, relax!
  - ルル/キング: Thank you. We will wait here.
- 係員: I call everyone when we board. Please listen for the announcement!
  - ルル/キング: Okay. Thank you very much!

## 未決・考え中
- ナイロビ・ドーハまで遊んで「飽きてきた」。どの国も入国審査・手荷物受け取りなど同じ場面が続くため。対策案は 005。どうするかは未決定。
- 強化合宿の作り直しの方向は未決定（006）。006 の e（開けない「発音教室」画面と古い合宿の整理）はキングの判断待ちで、まだやっていない。
- Word Battle（英単語→日本語3択）と Meaning!（日本語で答え合わせ）の実物の置き換えは別依頼（置き換え先の設計が先に必要）。
- 未決定のまま触っていないもの：イベント発火確率、飽きサインの定義、先に作る券、5,000語の配り方、出発の月、29日目の中身。
- 設計図の「キングが決めること7つ」のうち、先に作る券（クロの案：oneworld）、5000語の配り方、出発の月、「はじめから」で消す範囲、券の選び直しの可否は、まだキングの返事が記録に残っていない（`docs/world-tour-design.md` 末尾）。
- 新しい画面の提案（日にち表示・記録帳のお金・アルバム・読む場面・聞く場面）を受けるか。
- 「できていない流れ」23件のうち、どこまで直したかの最新の再確認（設計図は 6090947 時点）。
- マイクの動作は実機でしか確認できない。実機で確認できるまで「未確認」。
- 湾岸の空域制限（2026年2月末〜）の最新状況。便・時刻・金額は作る直前に公式で再確認。

## 次の候補
1. 「できていない流れ」の①②③（トップをオープニングに／世界マップ⇄世界一周編の入口と戻り口／ナイロビの出発・機内・ドーハ到着までの接続）。
2. 窓口（聞き取り→おすすめ→購入）の新しい会話約10本と、新しい見た目2つ（▶で複数選択、係員が線を引く地図）。見た目は作る前に提案して確認を取る。
3. 「飽きてきた」への対策案を出す（同じ場面の繰り返しを、国・空港の規模ごとに変える）。キングの了承を取ってから。
4. 3周目15空港・4周目8空港の素材集め（作る順が近づいたら）。

## ファイルの案内
| ファイル | 中身 |
|---|---|
| `CLAUDE.md` / `AGENTS.md` | 最初に読む入口 |
| `docs/rules.md` | プロジェクト指示文＋キングの決定（守るルール） |
| `docs/world-tour-design.md` | 世界一周編 全体設計図 第2版の要点（ルート・30日・窓口・分岐・5000語・できていない流れ23件） |
| `docs/materials/event-materials.md` | イベント素材集（20空港・実在の出来事524件、行ける51空港の表、賢者のアドバイス81件、船旅との比べ） |
| `docs/sources.md` | 参考にしたURL |

## まだこのリポジトリに入っていないもの
- **ルール案の全文**（claude.ai 上のドキュメント「空港えいご物語 世界一周編 ルール案」、2026-11-11作成）。要点（運賃の決まり方・大陸のくくり・区間数・日付変更・乗り遅れ・手数料・旅の組み方・体験談から拾った教訓）は `docs/world-tour-design.md` に反映済みだが、全文のコピーはない。claude.ai の画面からMarkdownで書き出して `docs/` に置けば完全になる。
- **設計図の元アーティファクト**（見た目つきの版）。内容は `docs/world-tour-design.md` に書き起こしてある。
- 素材集の「機種・一時帰国・ラウンジ・会話の種・最後の点検」の各節は未作成（3周目の調査のときに足す予定）。
- シート「空港一覧」（素材の列）。素材集の件数表とは別に管理されていた。
- キング本人の好みや決定のうち、この計画に関係しないもの（このリポジトリは公開なので入れない）。

## 参考にしたURL
`docs/sources.md` を参照。

## 今回（11/21）タスク051でやったこと（ナイロビ到着まわりの新背景）
- SIM（art id `simshop`）・タクシー（`nairobi` の差し替え）に新しい背景。回転台とOPEN看板の strip アニメは汎用部品 `artStrips`（`art.js`。`strips:[{img,x,y,n,fw,fh,step}]`）。SIMとタクシーに旅行者2人ずつ。
- 新しい場所「ホテルの部屋」`hroom`（`nbo_room`。読み上げ＋表示だけ・v 空・完了条件に入らない）。tour だけ `lockedPlace` を「場面の数が空の場所は飛ばして次を開く」に補正。TV画面の矩形は `ART.nroom.tv` に記録（未使用）。
- 詳細・数値・未確認は `docs/pm/deliverables/051-nairobi-arrival-backgrounds-report-v1.md`。確認は `tour-src/tests/test_arrival051.py`。

## 今回（11/22）タスク061でやったこと（カフェ試作 nbo_java1 の新しい会話の流れ）
- この場面だけ（`d.flow2=1`）：店員が英語 → 日本語の単語カードで1回選ぶ（カード払い／現金／M-Pesa）→ 見本の英語が音声だけ → カンペ → 間違えたら自動おてほん→言い直し（おてほんボタンなし）→ 発音の数値なし（店員の反応で返す）→ 支払いの演出（払ってコーヒーとケーキが出る）。M-Pesa は「What is M-Pesa?」と聞いて、短い説明のあと支払い。
- 実装：`tour-src/cards.js`・`cards.css`（新規）、`data.py` の nbo_java1、`build.py` の SHARED。確認は `python3 tour-src/tests/test_flow061.py`（30項目）と `test_conv053.py`。報告と「クロが決めたこと」は `docs/pm/deliverables/061-cafe-flow-impl-report-v1.md`。
- 裏の反応時間→持ち越し→夢（053）は継続（shillings だけ。iced・slice の計測は選択がなくなったため外れた）。ルルの代行回数・ポイント・スパルタ教室は未決定のため入れていない（詰んだときは既存ヘルプ）。
- 未確認：実機のマイク・声・見え方。参考にしたURL：なし（新しい外部URLは使っていない）。

## 今回（11/24）タスク065でやったこと（ロヴァニエミ到着まわり）
- 新しい到着のまとまり `rvn_arr`（入国審査・手荷物・到着ロビー・無料Wi-Fi・バス乗り場 × 各2場面）と新ページ `tour/rovaniemi/`。台詞は `tour-src/rvn_data.py`、場所・背景・音は `build.py`、旅程は `trip.js`（10日目・両ルート）。到着ロビーだけ実画＋オーロラstrip（`art.js` の `rvnlobby`）。
- 詳細・数値・要確認（指示書が見当たらない／oneworldの入国審査／23時／Wi-Fi名が公式で未確認／バス8番の扱い／tour/assets未公開）は `docs/pm/deliverables/065-rovaniemi-arrival-report-v1.md`。確認は `tour-src/tests/test_arrival065.py`。

## 今回（11/24）タスク072でやったこと（ロヴァニエミ第2弾：滞在＋出発）
- 新しいまとまり `rvn_stay`（村の広場・郵便局・サンタ・トナカイ×各2）と `rvn_night`（ホテルのオーロラ待ち×2）と `rvn_dep`（チェックイン・保安・ギフトショップ Napapiirin Lahja・Ahkio・ゲート×各2）。両ルート11日目に滞在、oneworld12日目に夜、出発は oneworld13日目・Star12日目。`rvn_night` はStarの旅程に入らずチェックモードから入る。計20場面。台詞は `tour-src/rvn_stay_data.py`、場所・背景は `build.py`、旅程は `trip.js`。
- 実画は村の広場（`ART.rvillage`＝オーロラ・煙・きらめき）と郵便局（`ART.rpostoffice`＝炎）だけ。ほかはコード描画（実画は後続タスクで差し替え）。トナカイは静止のドット絵を背景のコード描画の中に描いた（別素材なし）。ホテルのオーロラ strip は出していない。
- 詳細・全文・数値・PMへの確認事項は `docs/pm/deliverables/072-rovaniemi-stay-departure-report-v1.md`。確認は `tour-src/tests/test_rovaniemi072.py`（194項目）。
- 未確認：実機のマイク・声・音・見え方。参考にしたURL：新しい外部URLなし。

## 今回（11/24）タスク066でやったこと（ロビーを通常版に・ショータイムはプールサイド）
- ホテルのロビー（`hsong`）は受付スタッフの案内の3択（ショータイム／プール／Balcony Bar。英文だけ）。ショータイムを選ぶと別場面のプールサイド（背景 `npool`）で歌う（歌手は高さ250）。ロビーの真ん中で歌う060の形は廃止（素材と `nsong` 設定は残置）。
- プールサイドの照明ストリップは、テーマ曲が鳴っているあいだは曲の再生位置の拍（`song_data.py` の `beats`）に合わせて点滅、鳴っていないときはゆっくり明滅。
- 指示書 066-lobby-showtime.md は届いていなかったため、案内の英文・「プール」「Balcony Bar」の動き（スタッフの一言→選択にもどる）・場面idは私が決めた。詳細・数字は `docs/pm/deliverables/066-lobby-showtime-report-v1.md`。実機（音・見え方）は未確認。
- 参考にしたURL：なし。

## 今回（11/24）タスク068でやったこと（ナイロビの英会話カフェ・予行練習の試作）
- 新場面 `nbo_eikaiwa1`（場所 `eikai`・art id `eikai`）。**チェックモード（`?check=1`）の一覧からだけ入る**。通常は「☕ 英会話」のタブも隠れ、`TOUR_IDS`・到着/空港の完了条件・旅の骨組み（`trip.js`）・セーブの進行に入らない。本編のどこに置くか（お試し券をもらう導入など）はキングが後日決める。`nbo_java` は無変更。
- 絵：背景 `nairobi-eikaiwa-cafe-v1.png`＋別素材3点（ランプ／窓の外の影／湯気。`strips`）。先生（キング制作）は素材の ×0.791（160×285・アフロ幅156px）、中心 x=800・底辺 y=706、**y=648 より下は描かない**（天板で下半身が隠れる）。キング（左）・ルル（右）は `hall-*-back` を 148×248／129×200 に拡大（足もと y=932・影なし）。先生の素材9点（ポーズ8＋宝箱アイコン）は `tour/assets/art/` に入れた（将来の場面用）。
- 実装：`tour-src/art.js`（ART `eikai`、`artSwayZ`＝大きさ指定の揺れ描き、`artNpcSrc`＝名前が `@` で始まる絵は art/ 直下から読む、strips の `over:1`＝人物より手前）、`build.py`（`EIKAI`・MODES `eikai`・`BGS.eikaiK`・`SP.eikai_teacher`）、`tour-src/eikaiwa_data.py`（会話。新規）。
- 会話：先生と5往復（挨拶→飲み物の注文→ミルクの確認→ひとこと雑談→おわり）。日本語の訳は台本にも画面にもない（`words=[]`・`conv=1`＝Word Battle と Meaning! は出ない）。実在の店名・メニュー名なし。自由会話AIなし。
- 確認：`EIKAI_PREVIEW=<teacher-cafe-preview.png> python3 tour-src/tests/test_eikaiwa068.py`（30項目）。報告は `docs/pm/deliverables/068-eikaiwa-cafe-report-v1.md`。`test_departure054.py` の出発まわりの絞り込みに `eikai` を足した。
- 未確認：実機のマイク・声・見え方。並び（キング左・ルル右）は同梱プレビューのとおりで、`docs/rules.md` の「ルルが左・キングが右」とは逆（PM確認待ち）。参考にしたURL：なし（新しい外部URLは使っていない）。

## 今回（11/25）タスク083でやったこと（合宿デモv2：体の高さをそろえる・カード1枚・言えなかったときの流れ・口パーツを出さない）
- ルルの大きさのばらつき: コマごとに体の高さ(頭のてっぺん→足の裏)が違った(素材でコマ1・2=340px、コマ3・4=334px)のが原因。コマごとの倍率を 340÷(foot_y−12) にして、画面での体の高さを全コマで同じにした(足もと・中心も同じ。0.66倍・左下固定は変えない)。
- 1回の合宿=カード1枚(camp_data.CARDS[0]=ill)。選ぶ画面なし。thr のデータは残してある。
- 短文を変更: ill=「Drills are good for my skills.」/ thr=「I can throw it through.」(カードの画像を同梱の新版に差し替え。短文の枠 SENT_BOX=(110,1480,860,300) は新カードの文字を測って決めた)。
- 短文は意味のまとまり(chunks)ごと: ill=「Drills are good / for my skills.」thr=「I can / throw it / through.」→最後に全文1回。
- 言えなかったとき(合宿だけ。build.py が onFail を差しかえ): 単語・全文=自分の声→お手本(自動・ふつうの速さ)→言い直し。3回続けて外れたらルルが代わりに言って先へ。まとまり=2回続けて外れたらお手本をもう一度流して次へ。言えたときは自分の声を流さない。ほかの場面は074のまま。
- 自分の声: camp.js の gsRec*/gsOwn*。端末のメモリだけ。1回鳴らしたら捨てる。通信・保存の命令なし。pa.js(IndexedDB保存)・voice.js(Azure)とは別系統。実機のマイク(音声認識と録音が同じマイクを同時に使えるか。特にiOS)は未確認。
- 口パーツの表示を外した(素材ファイルは残す)。
- テスト: tests/test_gasshuku078.py(58項目。偽のマイク・録音・通信監視つき)。
- 未決: 実機での録音の同時利用。

## 今回（11/25）タスク081＋082でやったこと（合宿デモの仕上げ。キングの実機感想への対応）
- 081 ルル：通常のルル代用をやめ、**マッチョルルのダンベル・アニメ**に。`tour-src/camp_data.py` の `LULU_FRAMES`（4コマ。ファイル名・画像の大きさ・足もと `foot_y`／`foot_x`）・`LULU_SEQ`（[0,1,2,1]＝1→2→3→2→1…）・`LULU_FRAME_SEC`（0.45）・`LULU_SCALE`（0.66）の1か所。足もとは素材から測った値で全コマそろえる（`test_gasshuku078.py` が同じ式で照合）。`camp.js` の `gsLuluGo` が時間だけでコマ送り（読み上げ中も続く・動きを減らす設定では1コマ目で止まる）。素材16枚は `tour/assets/art/camp/`（今回使うのは dumbbell だけ。exercise／rope／barbell は将来用）。
- 081 大きさ：ルル＝従来の表示の高さ×0.66（基準は従来の計算をそのまま残して出す）。カード＝ステージ幅の55%（`CARD_SHARE`。従来は約46%）。小さい画面（高さが足りない）はステージを画面の高さの58%まで伸ばして幅を確保。ハイライト枠は従来どおり % 指定でカードに追従。
- 081 口パーツ：ルルの頭の上に重ねる。ルルは左下に固定で、口の出入りで位置も大きさも変えない（旧「カラムの高さをルルと口で分け合う」計算は廃止）。口はルルが読む間だけ。
- 082 背景：`tour/assets/art/camp.png`（1536×960・ゴールドジム風・人なし）。`artIdFor`（`build.py`）に `campK→camp` を足し、`ART.camp`（`camp.js`）で既存の画像背景の仕組みに乗せた。紺の手順描画 `BGS.campK` は camp_demo1 だけが使っていたので、背景画が出せないとき（読み込み失敗・服の設定が通常でないとき）の保険として残した。
- 変えていない：合宿の流れ・カードの中身（v3）・失敗ルール（074）・口パーツの仕組み。新しい保存キーなし。
- 確認：`python3 tour-src/tests/test_gasshuku078.py`（49項目）。未確認：実機の見え方（ルルの大きさの好み・カードの文字の読みやすさ・背景の切り取り位置）、実機のマイク・声。参考にしたURL：なし（新しい外部URLは使っていない）。

## 今回（11/25）タスク078でやったこと（合宿＝マッチョルル教室のデモ版）
- 新場面 `camp_demo1`（場所 `camp`）。**チェックモード（`?check=1`）の一覧（「💪 合宿」）からだけ入る**。本編の進行・セーブ・完了の数えに入れず、新しい保存キーなし。入口の仕組み（案B第4項）は未決定のまま。
- 画面：大きなルル（左・078では通常のルルで代用。081でマッチョルルのアニメに置き換え済み＝下の081の節）＋カード（右・1080×1920を1枚ずつ・青い枠で今の単語）＋口パーツ（ルルの真下・読み上げ中だけ）＋今の単語（既存のカンペ表示）。
- 流れ：導入→全単語を1語ずつ2回ずつ→Repeat after me!→1語ずつ→短文（2回→Repeat→丸ごと）→2枚目→締め。発音判定・失敗ルール（074）は既存の `showCue`／`onFail`／`autoRescue` を流用。
- 実装：`tour-src/camp_data.py`（データ）・`camp.js`（進行）・`camp.css`、`build.py` に差しこみ。確認：`python3 tour-src/tests/test_gasshuku078.py`（42項目）。報告は `docs/pm/deliverables/078-gasshuku-demo-report-v1.md`。
- 未確認：実機のマイク・単語1語の判定の感触・声・見え方。同梱の `mouth-open` / `mouth-round` は実寸480×384（ファイル名は160x128）。

## 今回（11/24）タスク074でやったこと（タイトルの3モード・失敗ルール統一・オープニングの語り）
- モード：`PREF.mode`（`kd_prefs_v1` の数値キー。0＝カンペ／1＝耳学＆カンペ／2＝耳学）。出し分けは土台 `dubai/index.html` の `npcHide()`（相手の台詞の文字）・`cueBlind(T)`（自分のカンペ）・`npcMsg()`・`showCue()`（耳学で見本の自動再生）。`tour-src/build.py` の生成で tour／doha／rovaniemi／ending 全ページに入る。台本データは変更なし。
- 失敗ルール：`onFail()`→`failDemo()`（自動おてほん）→3回目 `autoRescue()`（ルルが代行・save.help は減らさない・noteWeak）。`luSayCue()` は手動ヘルプ `useHelp()` と共通。強化合宿（G.camp）だけ従来の assist。061 専用だった `f2Fail`（cards.js）は全場面共通の onFail に統合して削除。
- 数字のスコア（「3/5語 60%」など）は `hideNum()` で強化合宿以外は出さない。
- world：タイトルのコマンド窓にモード選択（`#mSel`）と「せつめいを きく」（`#cNarr`）。「はじめから」→語り（`playOpeningNarration`）→語り終えたら（または「すすむ」）tour/ へ。チャントは `CHANT.narr()` で語りのあいだ一時停止。
- 確認：`python3 tour-src/tests/test_modes074.py`。チェックモード（?check=1）の保存は専用の名前 `chk1:kd_prefs_v1` になる（タイトルで選んだモードはチェックモードへ引き継がない。チェックモードの設定から3モードを確認できる）。
- 未確認：実機の日本語読み上げの声質、実マイクでの3モードの流れ（耳学モードの「お手本→マイク」）。

## 今回（11/24）タスク076＋077でやったこと（プールサイドのショータイム格上げ／ロビーの3択を行き先につなぐ・コードのみ）
- 076：歌手は再生中 [sing1→正面→sing2→正面] を拍ごとに（正面は既存素材 `s-stand-front`・新規素材なし）。GO！のあと呼びかけ "Come on, everybody — sing with me!" を読み上げてから曲。歌詞は `song_data.py` の `SONG_SCENE['lyrics']`（21行・`[開始秒, 行]`）を曲の再生位置に連動して画面下に1行ずつ（英語のみ）。ステージ照明（光の円錐・足もとの光だまり・拍で脈打つキラキラ）は art.js の `artSpot`（`npool` の stage に `spot:1`）。**歌詞タイミングは初版近似・実機調整前提**（直すのは表の秒だけ）。
- 077：ロビーの「The swimming pool」は実在の場面 `nbo_pool1`（art `npoolq`・ルルとキングだけ・聞くだけ型・終わるとマップへ）。「The Balcony Bar」は枠組みのみ（`nbo_bar1`・art `nbar`＝PLACEHOLDER・台本 `BAR_SCENE`）で**背景素材待ち**。有効化は `song_data.py` の `BAR_READY = True` の1か所だけ（背景 nairobi-balcony-bar-v1.png・別ストリップ・座標確定のあと、後続の素材結びタスクで）。それまでは「スタッフの一言→メニューに戻る」。
- 確認：`tour-src/tests/test_showtime076.py`・`test_lobby077.py`・更新した `test_lobby066.py`。詳細は docs/pm/DECISIONS.md の 076・077。
- 未確認：実機の曲と歌詞の同期・照明の見え方・読み上げの聞こえ方・iPhone の自動再生。参考にしたURL：なし。

## 今回（11/25）タスク079でやったこと（英会話カフェ自由会話の実機フィードバック改善・コードのみ）
- 対象：`tour-src/freetalk.js`・`freetalk.css`、`relay/worker.js` の /chat、先生の声（`build.py` の `SP.eikai_teacher`）。台本パート（068）と他の場面は触っていない。
- 聞き取りは continuous＋final の蓄積＋自動再開。送るのは「最後の発話から約2.8秒の沈黙（`FT.silenceMs`）」か「🎤タップ＝言い終わり」だけ。聞き取り中は🎤が脈打ち、先生の考え中は吹き出しに「…」。
- /chat は `{reply, fix, via}`。fix（直した1文・はっきりした間違いのときだけ）があるときは、先生がお手本を読み→本人が言い直し（ゆるい一致・2回合わなければ先生がもう一度お手本を言って進む）→先生が短く受けて reply。fix なし／旧形式の応答は従来どおり。**カフェ（予行練習の場）に限った設計変更（キング決定 2026-11-25）**で、本編の「日常会話は止めない・採点しない」は変えていない。
- 先生プロンプトを強化（具体的な中身に触れる・毎回質問で終えない・同じ言い出しを繰り返さない・出力は `FIX:`／`REPLY:` の2行）。reask・nudge は各8種で、直近に使った文を避ける。
- 先生の声：pitch 1.1 → **0.6**（ほかの最低は r_santa 0.72・ルル 1.35）。
- **中継のデプロイはPM待ち**（`relay/worker.js` が変わった）。確認：`python3 tour-src/tests/test_eikaiwa073.py`（78項目）・`node relay/test/worker.test.mjs`（30項目）。報告：`docs/pm/deliverables/079-freetalk-improvements-report-v1.md`。
- 未確認：実機のマイク（continuous・自動再開・2.8秒の感触）・声の聞こえ方・実際のモデルが `FIX:`／`REPLY:` の形で返すか。

## タスク089（2026-11-26）窓口と宣言場面の分かりやすさ
- 内容と決定は `docs/pm/DECISIONS.md` の2026-11-26。窓口の流れ・マイク・地図の区間番号・再訪の飛ばし方は `tour-src/window.js`（WSTEP・declMic）、台本は `tour-src/window_data.py`（win_decl・win_c1・win_route・win_back）、地図の絵は `tour-src/art.js`（ticket の route）。
- 参考にしたURL：なし（スターアライアンスの決まりの数字は088で確認済みのものをそのまま使用。確認日2026-11-25）。
- PMに確認したいこと：win_c8・win_rec も1周目から外した（流れの図に無かったため）。マイクの素材（PM作成）が来たら `MICBIG_IMG` に入れる。実機のマイクの動きは未確認。

## タスク096（2026-11-26）チューリッヒ10場面（到着4・街3・出発3）
- 前提：到着も出発も鉄道（チューリッヒ中央駅）。到着はローマ発・ミラノ乗り換え。出発はフランクフルト行き直通ICE（乗り換えなし・約4時間。時刻表サイト2つの一致）。シェンゲン圏内なので入国審査の場面は無い。
- 場面：`tour-src/zur_data.py`（zur_arr1/locker1/tram1/info1・cafe1/shop1/hotel1・dep_board1/dep_ticket1/dep_train1）。新形式（flow2・選択は場面に1回・日本語カード）。台詞に数字・値段・時刻・ホーム番号・トラム番号・店名は出さない（例外：切符の窓口の four hours）。生成物は `tour/zurich/index.html`。
- 背景：`tour/assets/art/zurich-{arrival,street,hotel,departure}-v1.png`（PM制作・1536×960）。配置は `tour-src/art.js` の `ART.zur*`。
- 発車標の別素材：`zurich-board-fra-v1.png`（432×44。`tour-src/art/prep_096.py` で生成）を zur_dep_board1 の絵だけに still で重ねる（x=232,y=226）。行き先「Frankfurt (Main) Hbf」とホーム番号9のみ・発車時刻なし。**番号9は物語の中の架空**（背景の9番線の灰色の列車に合わせた。台詞には出さない）。
- つなぎ：旅の骨組み（`trip.js` の AIRP/IMPL/GROUPS/PLACEGRP/MODEGRP/HOUR/THEME）・世界マップ（AP に zurich）・チェックモード（アテネ⇄チューリッヒのリンク、タブは到着4・街3・出発3）。**ローマ(094)がmainに入っていないため `NEI` は `zurich:[]`**。094のマージ時に `rome:[…,'zurich']`・`zurich:['rome']` の2行と、ローマのチェックモードからのリンクを足してつなぐ。LEGS/ROWS（日ごとの表）にはアテネ同様まだ入れていない（PM確認待ち）。
- 確認：`python3 tour-src/tests/test_zurich096.py`。未確認：実機のマイク・声・見え方。店名・ホテル名は出していない（PM確認の点）。
- 参考にしたURL：時刻表（Omio・Trainline）の直通確認は zurich-prep.md（PM・確認日2026-11-26）。公式（SBB/DB）は未確認。
