# タスク062 実装報告：チェックモードにCAアナウンス(048)の入口（v1）

## 結論
`?check=1` のパネル「割りこみ・顔なじみ」の欄に、CAアナウンスを直接試せる入口を足した。通しは CA場面 → マイク → 機内食の場面で自分の声が再生されるところまで。専用テスト `tour-src/tests/test_check062.py`（oneworld・Star 各2回の通し）は NG 0件。実機（iPhone/Android）のマイクは未確認。

## 入口
- 「CAアナウンス 通し」: CA場面 → 引き受ける → マイク画面 → これでOK → 機内食の場面（チャイム→自分の声→ルルの反応）→ 地図へ。
- 「機内食の場面だけ」: 食事の場面から始める（その時点で声が残っていれば再生、なければ文だけ）。
- 行き先は券で決まる。パネル上の券ボタンで Star Alliance（Istanbul）／oneworld（Doha）を切りかえる。欄に今の行き先を表示する。
- 実装: `tour-src/pa.js` に `PA.chk()`（`window.__CHK` のときだけ動く）、`tour-src/check.js` にボタン。`PA.gate`（通常の出方）は無変更。

## 専用の記録の範囲
- 進行は `chk1:` のキー、声は IndexedDB `chk1:kanpe-pa-rec-v1`（`check_shim.js` が向ける。無変更）。
- 通常のセーブ（localStorage の見本）は変わらず、通常の録音DB `kanpe-pa-rec-v1` は点検で作られない。旅の骨組み（kanpe-trip-v1）は動かない。
- `fired.pa1/pa2` は見ず・書かないため、何度でも通しで試せる。

## 数字
- test_check062: NG 0件（通常の出方の確認・両券の通し×2回・専用の記録・ネットワーク送信0・禁止語なし）。
- 既存: test_pa048 NG 0件、test_check056 すべてOK。
- 生成物: tour/index.html と tour/doha/index.html のみ変更（doha は check.js 由来の9行。ドーハ側には入口は出ない）。ending・world は差分なし。

## 未確認
実機のマイク・音量・見え方。

## 最後の点検
お金／健康・診断／個人情報（声は端末内・専用の置き場のみ）／権利: 問題なし。
