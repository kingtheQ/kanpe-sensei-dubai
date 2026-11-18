# -*- coding: utf-8 -*-
"""タスク024: 4つの数字(Azure の値そのもの)の確認。使い方: python3 tour-src/tests/test_numbers.py
ブラウザの中の vPron / voiceWhole / voiceBuildM を直接呼ぶ。期待値は
 (1) 公開されている Azure の結果の例(下の PUBLIC)と Microsoft Learn の式、(2) 手で計算した値。
リポジトリの tour/ は書き換えない(出力は /tmp)。"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_routes as T
from playwright.sync_api import sync_playwright

# 公開されている結果の例: (正確さ, 流れ, 言い切り度, 総合) 抑揚なし。出典は報告書に記載
PUBLIC = [(100, 96, 100, 97.6), (44, 80, 20, 36.8), (54, 100, 0, 30.8)]

HOOK = "window.__N={vPron:vPron,voiceWhole:voiceWhole,voiceBuildM:voiceBuildM,vShow:vShow};"

def main():
    os.makedirs(T.SHOTS, exist_ok=True)
    d = T.build('num', None)
    srv = T.serve(d); base = 'http://127.0.0.1:%d' % srv.server_address[1]
    fails = []; rows = []
    def check(name, got, want, tol=0.05):
        ok = (got == want) if not isinstance(want, (int, float)) or isinstance(want, bool) else (got is not None and abs(got - want) <= tol)
        rows.append((name, got, want, 'OK' if ok else 'NG'))
        if not ok: fails.append(name)
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = br.new_page()
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        def hook(route):
            r = route.fetch(); body = r.text()
            assert T.HOOK_N in body
            route.fulfill(response=r, body=body.replace(T.HOOK_N, HOOK + T.HOOK_N, 1))
        pg.route('**/tour/index.html', hook)
        pg.goto(base + '/tour/index.html'); pg.wait_for_timeout(600)
        # 1. PronScore の式(公開の例と一致するか)
        for a, f, c, p in PUBLIC:
            check('vPron(%s,%s,%s)' % (a, f, c), pg.evaluate("([a,f,c])=>__N.vPron(a,f,c)", [a, f, c]), p)
        # 2. 区切りが1つ: Azure の4つの値そのまま(PronScore も Azure の値)
        W = pg.evaluate("()=>__N.voiceWhole([[97.6,100,96,100,10,5e7]],[],10)")
        check('1区切り tot', W['tot'], 97.6); check('1区切り acc', W['acc'], 100); check('1区切り flu', W['flu'], 96); check('1区切り cmp', W['cmp'], 100)
        W = pg.evaluate("()=>__N.voiceWhole([[null,70,60,90,10,5e7]],[],10)")   # PronScore が無ければ式で
        check('1区切り PronScoreなし tot', W['tot'], 0.6*60 + 0.2*70 + 0.2*90)
        # 3. 区切りが2つ: 単語数で平均 / 長さで平均 / 紙の単語のうち 正確さ60以上の割合 / 式
        w = [['a', 90, 'None', []]] * 6 + [['b', 59, 'None', []], ['c', None, 'Omission', []], ['d', 60, 'None', []], ['e', 80, 'None', []]]   # 10語。60以上=6+1+1=8
        W = pg.evaluate("(w)=>__N.voiceWhole([[null,80,70,100,6,3e7],[null,60,90,100,4,1e7]],w,10)", w)
        acc = (80*6 + 60*4) / 10; flu = (70*3 + 90*1) / 4; cmp = 80.0
        check('2区切り acc', W['acc'], acc); check('2区切り flu', W['flu'], flu); check('2区切り cmp', W['cmp'], cmp)
        s = sorted([acc, flu, cmp]); check('2区切り tot', W['tot'], .6*s[0] + .2*s[1] + .2*s[2])
        # 4. voiceBuildM: 実際の形の結果(2区切り)から、記録の形と印を確認
        r = pg.evaluate("""()=>{
          var tg='We went to the sea'.split(' ');
          function wd(w,a){return {Word:w,Duration:3000000,PronunciationAssessment:{AccuracyScore:a,ErrorType:'None'},Phonemes:[{Phoneme:'x',PronunciationAssessment:{AccuracyScore:a}}]}}
          var segs=[{text:'we went to',pa:{AccuracyScore:90,FluencyScore:80,CompletenessScore:100,PronScore:90.0},words:[wd('we',95),wd('went',90),wd('to',85)]},
                    {text:'the sea',pa:{AccuracyScore:70,FluencyScore:60,CompletenessScore:100,PronScore:70.0},words:[wd('the',60),wd('sea',80)]},
                    {text:'ignored',pa:null,words:[]}];
          var res={words:tg.map(function(){return {ok:true}})};
          return __N.voiceBuildM(tg,segs,'we went to the sea',res)}""")
        check('M.nv', r.get('nv'), 2); check('M.src', r.get('src'), 'az'); check('M.nseg', r.get('nseg'), 2)
        check('M.acc', r['acc'], (90*3+70*2)/5); check('M.flu', r['flu'], 72.0)   # (80*9+60*6)/15
        check('M.cmp', r['cmp'], 100.0); check('M.az 区切りの値そのまま', r['az'], [[90.0,90.0,80.0,100.0,3,9000000],[70.0,70.0,60.0,100.0,2,6000000]])
        check('M に pa=null の区切りは入らない', len(r['az']), 2)
        # 5. 区切りに Azure の値が無い → sr
        r = pg.evaluate("""()=>{var tg=['we','went'];var segs=[{text:'we went',pa:null,words:[]}];
          return __N.voiceBuildM(tg,segs,'we went',{words:[{ok:true},{ok:true}]})}""")
        check('Azureの値なし → src', r['src'], 'sr'); check('Azureの値なし → nv なし', r.get('nv'), None); check('Azureの値なし → tot', r['tot'], None)
        check('vShow(72.4)', pg.evaluate("()=>__N.vShow(72.4)"), '72'); check('vShow(null)', pg.evaluate("()=>__N.vShow(null)"), '-')
        check('JSエラー', len(errs), 0)
        br.close()
    srv.shutdown()
    for r_ in rows: print('%-4s %-44s got=%s want=%s' % (r_[3], r_[0], json.dumps(r_[1], ensure_ascii=False), json.dumps(r_[2], ensure_ascii=False)))
    print('合計 %d 件 / NG %d 件' % (len(rows), len(fails)))
    sys.exit(1 if fails else 0)
main()
