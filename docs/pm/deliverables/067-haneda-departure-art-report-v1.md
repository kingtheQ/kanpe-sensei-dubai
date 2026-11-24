# タスク067 完了報告：羽田出発の残り5場面の実画（2026-11-24）

## 結果
- 5場面（hnd_checkin_ow / hnd_sec / hnd_exit / hnd_plane_ow / hnd_plane_star）に実画の背景を結んだ。別素材（ベルトの荷物・トレイ・表示灯・機内の明滅）が動く。
- 結びは本編側（tour/index.html）の artIdFor だけ。ドーハ側（tour/doha/）・ロヴァニエミ側の artIdFor は変えていない（ART の表は共通のため項目は入るが、場面には結ばれない）。
- 通常モードでも `?check=1` でも5場面とも実画が出る（test_haneda067.py の F）。

## 結び（artIdFor）
| 場面 | bg | 条件 | art |
|---|---|---|---|
| hnd_checkin_ow | checkinQ | vid が hnd_ | hcheckin_ow |
| hnd_sec | security | vid が hnd_ | hsec |
| hnd_exit | immigH | vid が hnd_ | hexit |
| hnd_plane_ow | cabinQ | vid が hnd_plane_ | hcabin_ow |
| hnd_plane_star | cabinT | vid が hnd_plane_ | hcabin_st |

機内は hnd_ev_ca_（048 の cabinseat）・hnd_ev_meal_（cabinmeal）が同じ bg を使うため、hnd_plane_ に絞った。ナイロビ（nbo_）の ncheckin/nsec・055 の hcheckin_st・羽田のゲートは変わらない。

## 測った数字（配置の正本プレビューとの画素差。動く別素材・「…」の場所は除く）
- hnd_checkin_ow 0.21% ／ hnd_sec 0.27% ／ hnd_exit 0.49% ／ hnd_plane_ow 2.03% ／ hnd_plane_star 2.04%（機内は乗務員の揺れ・影の形の差）
- 客室乗務員：高さ274、頭（お団子の天辺〜顎）106px（指定は105px。キングの頭100pxの1.0〜1.1倍の範囲）
- テスト：test_haneda067.py すべてOK（結び・描画・配置・大きさ・チェックモード）

## 正本（プレビュー）に合わせた判断
- 出国審査の係官：既存の o2-front-officer-blue（幅110）は、プレビューの係官（幅97）と大きさ・作りが違うため、プレビューから切り出した hexit-officer を使った。
- 青いスーツケース：既存の artSuit（四角い箱）とは別の絵なので、プレビューから切り出した hexit-suitcase を使った（art.js の suitImg。hexit だけが使う）。
- 切り出しは tour-src/art/prep_haneda067.py（元は tour-src/art/ref-haneda067/ に置いたプレビュー）。
- 乗務員は既存の ca-front（139×266）を高さ274にした ca-front-274（プレビューと画素を突き合わせ、同じ絵と確認）。

## PM に決めてほしいこと（出国審査の係官の大きさ）
- 指示書の数値（top≈482・clip=600）とプレビューは、頭と肩が大きく見える係官（幅97・窓から見える高さ118）。これは 064（ドーハ入国審査）の係官（×0.93・頭56px・top=511）の約2倍の頭の大きさで、「大人の頭はキングの頭の1.0〜1.1倍まで」の物差しからは外れる（この場面のキングの頭は約58px）。
- 今回は「数値が食い違うときはプレビューの見た目を優先」に従い、プレビューのまま実装した。064 と同じ大きさにしたい場合は、hexit の booths を 064 と同じ設定（o-front-officer-blue ×0.93・top=511）に差し替えるだけ（画面の流れ・会話は変わらない）。

## 入れていないもの・未確認
- 出国審査のプレビューの左に並ぶ旅行者（バックパッカー）は指定になく、合う素材もないので入れていない。
- 影：プレビューのルル・キングには影がないが、出国審査は既存の仕組み（影つき）のまま。
- 実機・マイクの見え方は未確認。

## テスト
- 追加：test_haneda067.py。更新：test_doha064.py（本編側の artIdFor で hnd_exit が hexit になる期待値）、test_departure054.py（羽田の checkinQ/security の期待値を新しい結びに、dep 設定の除外に新しい項目と 065 の rvnlobby を追加）。
- 既存テストは、実行したものすべて通過。通らないのは次の2つで、この変更とは関係がない：test_trip030.py（world/ ページを開く。変更前の main でも同じ場所で落ちる）／test_people047.py（外部の /home/claude/t047/ のプレビュー画像を読む）。

## 点検（最後）
お金・健康情報・診断と誤解される表現・個人情報・権利：新しく足した文字列に該当なし。素材はキングの素材パック。公開物にメールアドレス・通知先・鍵は入れていない。
