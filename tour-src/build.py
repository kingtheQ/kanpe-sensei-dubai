# -*- coding: utf-8 -*-
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import ipa, data, song_data, pa_data, camp_data
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'dubai', 'index.html'), encoding='utf-8').read()

# ---------- DLG ----------
missing = []
def wd(en, jp):
    p = ipa.phrase(en)
    if p is None:
        missing.append(en); p = '/' + en + '/'
    return [en, p, jp]
def bgfor(x):
    if x['id'].startswith('nbo_java'): return 'javaK'
    if x['id'].startswith('nbo_art'): return 'artK'
    if x['id'].startswith('nbo_eikaiwa'): return 'eikaiK'
    return x['bg']
def repo(v):   # 会話のあとの一言 (n, jp[, 話す人])
    r = {'n': v[0], 'jp': v[1]}
    if len(v) > 2: r['who'] = v[2]
    return r
dl = {}
for x in data.D:
    lines = []
    for p in x['pairs']:
        if isinstance(p, dict):   # 窓口の台本（window_data.py）: 分かれ目・相手の言い分け・長いカンペ
            nl = {'n': p['n'], 'jp': p['njp']}
            if 'by' in p: nl['by'] = dict((k, {'n': v[0], 'jp': v[1]}) for k, v in p['by'].items())
            if 'route' in p: nl['route'] = p['route']
            yl = {'y': p.get('y', ''), 'jp': p.get('yjp', '')}
            if 'opts' in p: yl['opts'] = [dict((k2, v2) if k2 != 'rep' else (k2, repo(v2)) for k2, v2 in o.items()) for o in p['opts']]
            if 'cueBy' in p: yl['cueBy'] = dict((k, {'y': v[0], 'jp': v[1]}) for k, v in p['cueBy'].items())
            if 'diag' in p: yl['diag'] = p['diag']
            if 'fork' in p: yl['fork'] = p['fork']   # 分かれ目(タスク053): 選ぶまでの時間を測る語
            if 'cards' in p: yl['cards'] = 1   # 日本語の単語カードで選ぶ分かれ目(タスク061)
            if 'rep' in p: yl['rep'] = {'n': p['rep'][0], 'jp': p['rep'][1]}
            lines.append(nl); lines.append(yl)
        else:
            (n, njp, y, yjp) = p
            lines.append({'n': n, 'jp': njp}); lines.append({'y': y, 'jp': yjp})
    dl[x['id']] = {'who': x['who'], 'story': 1, 'bg': bgfor(x), 'sp': x['sp'], 'hero': 'blue', 'lulu': 'plain', 'nogold': 1,
                   'inter': x.get('inter', []), 'intro': x['intro'], 'lines': lines, 'words': [wd(a, b) for a, b in x['words']]}
    if x.get('win'): dl[x['id']]['win'] = 1; dl[x['id']]['auto'] = x.get('auto', 1)
    if x.get('ev'):   # 割りこみ・ひとこと場面(タスク014)。自動で始まり、単語バトルに入らず、終わると元の流れにもどる
        dl[x['id']]['ev'] = 1; dl[x['id']]['auto'] = 1
        for k in ('lvis', 'nohelp', 'fx', 'pre'):   # pre='own': 食事の場面の始まりに、自分の声の放送を流す(タスク048)
            if x.get(k) is not None: dl[x['id']][k] = x[k]
    elif x.get('lvis') is not None or x.get('nohelp'):   # ふつうの5往復でも、ルルがいない始まり(タスク023 doh_city_t3)
        for k in ('lvis', 'nohelp'):
            if x.get(k) is not None: dl[x['id']][k] = x[k]
    if x.get('kind'): dl[x['id']]['kind'] = x['kind']
    if x.get('reveal'): dl[x['id']]['reveal'] = 1   # タスク085-E: Word Battle を挟まず Meaning!(日本語訳つき答え合わせ)だけ出す(賢者・チケット窓口の5場面)
    if x.get('conv'): dl[x['id']]['conv'] = 1   # 会話に溶かした場面(タスク053): Word Battle と Meaning! を出さない
    if x.get('freetalk'): dl[x['id']]['freetalk'] = 1   # タスク073: 台本パートのあとに、先生が5分の自由会話に誘う(freetalk.js)
    if x.get('camp78'): dl[x['id']]['camp78'] = x['camp78']   # 合宿デモ(タスク078): カード・単語・短文・ルルの台詞(camp_data.py)
    if x.get('flow2'): dl[x['id']]['flow2'] = 1   # 新しい会話の流れ(タスク061): おてほんボタンなし・自動おてほん・発音の数値なし・日本語カード・支払いの演出
    if x.get('keep'): dl[x['id']]['keep'] = x['keep']   # 秘密イベントの下地(タスク043): この場面を遊び終えたらルルが拾い物をする(画面には出さない)
# ---------- 持ち越し(005案B): 相手のセリフの差しかえ。種の場面(save.seen)を遊んでいたときだけ返る ----------
import event_data, window_data, doha_data
for (sc, ti, seed, nn, njp, yy, yjp) in event_data.VARIANTS + doha_data.VARIANTS:
    ln = dl[sc]['lines'][2 * ti]
    assert 'n' in ln, (sc, ti)
    v = {'s': seed, 'n': nn, 'jp': njp}
    if yy: v['y'] = window_data.star(yy); v['yjp'] = yjp
    ln.setdefault('vr', []).append(v)
J = lambda o: json.dumps(o, ensure_ascii=False)

def place(id, name, snd, x, y, ico, tip, v, **kw):
    p = dict(id=id, name=name, snd=snd, x=x, y=y, ico=ico, tip=tip, v=v); p.update(kw); return p
SAGE = [
 place('sage', '達人賢者', 'sage', 30, 28, '🧙', ['達人賢者', '旅のはじまりを聞く'], ['sage_1', 'sage_2', 'sage_3'],
       hub=True, hubBg='sage', hubHero='blue', hubEn='Welcome, travelers. What would you like to ask?',
       hubMsg='達人賢者の広間。', menu=[['Why go around the world?', 'sage_1'], ['Which ticket should we choose?', 'sage_2'], ['Tips for travel English', 'sage_3']]),
 place('ticket', 'チケットをえらぶ', 'tdesk', 70, 72, '🎫', ['航空券の窓口', '世界一周の窓口で相談して、券をえらぶ'], ['ticket_star', 'ticket_ow'],
       hubMap=1, win=1)]   # 窓口フロー(winStart)へ。券は おすすめのあと ▶ で えらぶ
ARR = [
 place('immig', '入国審査', 'info', 22, 16, '🛂', ['入国審査(Immigration)', 'eTA・目的・滞在日数・ホテル'], ['nbo_immig1', 'nbo_immig2']),
 place('bag', '手荷物受け取り', 'hall', 70, 36, '🧳', ['バゲージクレーム', 'スーツケース・レジ袋'], ['nbo_bag1', 'nbo_bag2']),
 place('sim', 'Safaricom SIM', 'info', 24, 58, '📱', ['Safaricom', 'SIMの登録とデータ'], ['nbo_sim1', 'nbo_sim2']),
 place('taxi', 'タクシー・Uber', 'hall', 70, 82, '🚕', ['タクシー乗り場とライドシェア', '市内へ・料金は架空'], ['nbo_taxi1', 'nbo_taxi2']),
# ホテルのロビー(タスク066: 通常版=スタッフの案内の3択 hub。ショータイムを選ぶとプールサイドの歌場面 nbo_song へ。049/060では歌場面そのものだった): 聴くだけの場面。v は空 = 到着の完了条件・場面の数・保存の記録(save.seen)に入らない(任意)。到着の場所を上から順に開く決まりで、タクシーのあとに開く
 place('hsong', 'ホテルのロビー', 'hotel', 24, 84, '🏨', ['Villa Rosa Kempinski', 'スタッフの案内で、ショータイムへ'], [],
       hub=True, hubBg='nlobby', hubHero='blue', hubEn=song_data.LOBBY_HUB['en'], hubMsg=song_data.LOBBY_HUB['msg'], menu=song_data.LOBBY_HUB['menu']),
# ホテルの部屋(タスク051): 到着の夜、部屋で休む場面。hsong と同じホテル。v は空 = 到着の完了条件・場面の数・保存の記録(save.seen)に入らない(任意・休憩)。hsong の次に開く(下の lockedPlace の補正)
 place('hroom', 'ホテルの部屋', 'hotel', 48, 88, '🛏️', ['Villa Rosa Kempinski', '部屋で休む'], [], rest='nbo_room')]
# ナイロビの滞在(観光。タスク058): サファリ・マサイマーケット。滞在3日の3日目(市場)・4日目(サファリ)。trip.js の ROWS / GROUPS で日に置く。タブは「滞在」。
# どちらも nbo_ の場面で conv=1(053の分かれ目の型)。空港の完了条件(PLACES_AIR)には入らない(世界マップのクリアの印は今までどおり空港の場所だけ)
STAY = [
 place('market', 'マサイマーケット', 'souk', 66, 60, '🧺', ['Maasai Market', '布・かご・お面。値段は架空'], ['nbo_market']),
 place('safari', 'サファリ', 'safari', 30, 28, '🦒', ['Nairobi National Park', 'ガイドと動物を見る'], ['nbo_safari'])]
# 英会話カフェ(タスク068・試作): ナイロビの小さな英会話カフェで、先生と短い予行練習。チェックモード(?check=1)からだけ入る(通常はタブも出ない)。
# TOUR_IDS・到着/空港の完了条件・旅の骨組み(trip.js)・セーブの進行には入れない。本編への組み込み位置はキングが後日決める
EIKAI = [
 place('eikai', '英会話カフェ', 'cafe', 50, 50, '☕', ['英会話カフェ', '先生と、ごあいさつと飲み物の注文'], ['nbo_eikaiwa1'])]
# 合宿(マッチョルル教室)デモ版(タスク078): チェックモード(?check=1)からだけ入る独立場面。TOUR_IDS・到着/空港の完了条件・旅の骨組み(trip.js)・セーブの進行には入れない。
# 入口の仕組み(失敗ポイントが尽きると強制的に発音教室へ=案B第4項)は未決定なので作らない
CAMP = [
 place('camp', '合宿(マッチョルル教室)', 'hall', 50, 50, '💪', ['合宿', 'マッチョルルの教室(デモ)'], ['camp_demo1'])]
AIR = [
 place('java', 'Java House', 'cafe', 22, 14, '☕', ['Java House', 'ラテとケーキ・値段は架空'], ['nbo_java1', 'nbo_java2']),
 place('art', 'Artcaffe', 'cafe', 70, 32, '🥐', ['Artcaffe', 'パンとジュース・値段は架空'], ['nbo_art1', 'nbo_art2']),
 place('lounge', 'Pride Lounge', 'ahlan', 24, 52, '🛋️', ['Pride Lounge', 'ラウンジの受付と、となりの人'], ['nbo_lounge1', 'nbo_lounge2']),
 place('duty', 'Duty Free', 'cafe', 70, 68, '🛍️', ['免税店', 'コーヒーと紅茶・値段は架空'], ['nbo_duty1', 'nbo_duty2'])]
NDEP = [
 place('qcheckin', 'Qatar Airways', 'info', 24, 18, '🎫', ['Qatar Airways チェックイン', '荷物の重さ・席・搭乗券'], ['nbo_checkin1', 'nbo_checkin2']),
 place('nsec', '保安検査', 'info', 70, 46, '🔍', ['保安検査', '荷物・上着・液体'], ['nbo_sec1', 'nbo_sec2']),
 place('gate', '搭乗ゲート', 'hall', 70, 76, '🚪', ['搭乗ゲート', '搭乗のアナウンス'], ['nbo_gate1', 'nbo_gate2']),
 place('qplane', '機内(Qatar Airways)', 'atop', 26, 76, '✈️', ['機内', '客室乗務員との会話。終わるとドーハへ飛ぶ'], ['nbo_plane1', 'nbo_plane2'])]
# 1日目 羽田から出発(タスク043)。券を買ったあと、ナイロビ到着の前。場面は上から順(seq=1)。tkv = 券ごとの場面(oneworld=Qatar Airways / Star Alliance=Turkish Airlines)。v は両方の券の場面を並べる(進み具合・鍵の数え用)
HDEP = [
 place('hcheckin', 'チェックイン', 'info', 22, 14, '🎫', ['羽田空港 チェックイン', '荷物を預けて、搭乗券をもらう'], ['hnd_checkin_ow', 'hnd_checkin_star'], seq=1,
       tkv={'ow': ['hnd_checkin_ow'], 'star': ['hnd_checkin_star']}),
 place('hsec', '保安検査', 'info', 72, 28, '🔍', ['保安検査', '荷物・上着・液体'], ['hnd_sec'], seq=1),
 place('hexit', '出国審査', 'info', 26, 46, '🛂', ['出国審査', 'パスポートと搭乗券'], ['hnd_exit'], seq=1),
 place('hgate', '出発ゲート', 'hall', 72, 62, '🚪', ['出発ゲート', '夜の静かなゲートで待つ'], ['hnd_gate_ow', 'hnd_gate_star'], seq=1,
       tkv={'ow': ['hnd_gate_ow'], 'star': ['hnd_gate_star']}),
 place('hboard', '搭乗', 'hall', 28, 78, '🛫', ['搭乗', '搭乗券を見せて、ブリッジへ'], ['hnd_board_ow', 'hnd_board_star'], seq=1,
       tkv={'ow': ['hnd_board_ow'], 'star': ['hnd_board_star']}),
 place('hplane', '機内(深夜便)', 'atop', 74, 90, '✈️', ['機内', '終わるとナイロビへ飛ぶ'], ['hnd_plane_ow', 'hnd_plane_star'], seq=1,
       tkv={'ow': ['hnd_plane_ow'], 'star': ['hnd_plane_star']})]
# 28日目の羽田に戻った場面(タスク059): 持ち主に落とし物を返す。keep.hnd1 のあるセーブだけに出る(trip.js の GCOND)。
# 場所は1つ(hreturn)。v は場面の記録(save.seen)に使うが、TOUR_IDS(「かいわ n / 全部」の数え)には入れない = 出ない人の分母を変えないため
HRET = [
 place('hreturn', '出発ゲート', 'hall', 50, 50, '🚪', ['羽田空港 出発ゲート', 'もどってきた羽田'], ['hnd_return'])]
TOUR_IDS = [i for p in HDEP + ARR + STAY + AIR + NDEP for i in p['v']]
DARR = [
 place('dimmig', '入国審査', 'info', 76, 18, '🛂', ['入国審査(Passport Control)', '滞在日数・次の航空券・ホテル'], ['doh_immig1', 'doh_immig2']),
 place('dbag', '手荷物受け取り', 'hall', 28, 38, '🧳', ['バゲージクレーム', 'ベルト・カート・そっくりなスーツケース'], ['doh_bag1', 'doh_bag2']),
 place('dsim', 'Ooredoo SIM', 'info', 74, 60, '📱', ['Ooredoo', '旅行者用SIM・値段は架空'], ['doh_sim1', 'doh_sim2']),
 place('dride', 'タクシー・Doha Metro', 'hall', 28, 82, '🚕', ['Karwaタクシーと Doha Metro', 'どちらで街へ行く？'], ['doh_taxi', 'doh_metro'],
       hub=True, hubMap=1, hubBg='dtaxi', hubHero='blue', hubEn='Would you like a taxi, or the metro?', hubMsg='タクシー乗り場と Doha Metro の案内。',
       menu=[['Karwa Taxi', 'doh_taxi'], ['Doha Metro', 'doh_metro']])]
# ドーハ後半(タスク023・018案A)。出発は「2つの広場＋列車」の八の字、市内は「湾の弧」。seq=1 は場面を上から順に出す
DDEP = [
 place('dcounter', 'カウンター・出国審査', 'info', 20, 14, '🎫', ['出発カウンターと出国審査', '荷物を預けて、出国へ'], ['doh_dep_checkin', 'doh_dep_passport'], seq=1),
 place('dsouth', '南の広場', 'hall', 72, 30, '🧸', ['南の広場', '大きなクマの前で'], ['doh_dep_bear']),
 place('dtrain', '空港の列車', 'info', 46, 52, '🚝', ['空港の中の列車', '南から北の広場へ'], ['doh_dep_train']),
 place('dnorth', '北の広場', 'ahlan', 24, 74, '🌳', ['北の広場', '木のある広場とラウンジの入口'], ['doh_dep_orchard', 'doh_dep_lounge']),
 place('dgate', 'ゲート・機内', 'atop', 74, 84, '✈️', ['ヘルシンキ行きのゲート', '機内の会話が終わると、ドーハを出発'], ['doh_dep_gate', 'doh_dep_plane'],
       hub=True, hubMap=1, hubBg='dgate', hubHero='blue', hubEn='The gate for Helsinki. Where would you like to go?', hubMsg='ヘルシンキ行きのゲート。',
       menu=[['Gate desk', 'doh_dep_gate'], ['Board the plane', 'doh_dep_plane']])]
DCITY = [
 place('calley', 'スークの路地', 'souk', 14, 84, '🏮', ['スーク・ワキーフの路地', '夜・道をきく・お茶'], ['doh_city_t2', 'doh_city_t1', 'doh_city_t3'], seq=1),
 place('chotel', 'ホテル', 'hotel', 26, 58, '🏨', ['ホテル(夜)', 'チェックインと夕食の相談'], ['doh_city_h1', 'doh_city_h2'], seq=1),
 place('csouq', 'スークの店', 'souk', 48, 40, '🧺', ['スーク・ワキーフの店', '香辛料・布・みやげ。値段は架空'], ['doh_city_s1', 'doh_city_s2', 'doh_city_s3']),
 place('crest', 'レストラン', 'cafe', 72, 26, '🍽️', ['スークの中のレストラン', '注文・となりの家族・会計'], ['doh_city_r1', 'doh_city_r2', 'doh_city_r3'], seq=1),
 place('cbreak', 'ホテルの朝', 'hotel', 84, 50, '☕', ['ホテル(朝)', '朝ごはんとチェックアウト'], ['doh_city_h3', 'doh_city_h4'], seq=1),
 place('ccorn', 'コルニーシュ', 'beach', 60, 72, '⛵', ['コルニーシュ(湾ぞいの遊歩道)', '写真・木の舟・学生。値段は架空'], ['doh_city_c1', 'doh_city_c2', 'doh_city_c3'])]
DOH_IDS = [i for p in DARR + DCITY + DDEP for i in p['v']]

# ロヴァニエミの到着まわり(タスク065): 5場所×2場面。場所は上から順に開く(trip.js の lockedPlace)。到着ロビーだけ実画(art.js の rvnlobby)。
# 場所の説明(tip)・名前は日本語(今までと同じ)。看板・店名・料金は確認できたものだけ(rvn_data.py の冒頭)。
RARR = [
 place('rimmig', '入国審査', 'info', 24, 14, '🛂', ['入国審査', '口数の少ない係官と、パスポート'], ['rvn_immig1', 'rvn_immig2']),
 place('rbag', '手荷物受け取り', 'hall', 72, 32, '🧳', ['バゲージクレーム', '雪の国の荷物とコート'], ['rvn_bag1', 'rvn_bag2']),
 place('rlobby', '到着ロビー', 'hall', 26, 50, '🌌', ['到着ロビー', '床に光の線・北極圏ライン'], ['rvn_lobby1', 'rvn_lobby2']),
 place('rwifi', '無料Wi-Fi', 'info', 72, 66, '📶', ['Rovaniemi Airport Free Wi-Fi', 'ネットにつなぐ'], ['rvn_wifi1', 'rvn_wifi2']),
 place('rbus', 'バス乗り場', 'hall', 28, 84, '🚌', ['バス乗り場', 'サンタクロース村へ・8番かAirport Express'], ['rvn_bus1', 'rvn_bus2'])]
# ロヴァニエミの滞在・夜・出発(タスク072)。座標は到着(RARR)と同じジグザグ(x=24〜28/72, y=14〜84)で、同じ画面の中では重ならない。並びは動線順。
# 村の広場・郵便局だけ実画(art.js の rvillage / rpostoffice)。ほかはコード描画(BGS)。村のカフェの場面は作らない。
RSTAY = [
 place('rvil', '村の広場', 'hall', 24, 14, '🎄', ['サンタクロース村の広場', '北極圏のラインをまたぐ'], ['rvn_village1', 'rvn_village2']),
 place('rpost', '郵便局', 'info', 72, 32, '✉️', ['サンタクロース村の郵便局', 'はがきと特別な消印'], ['rvn_post1', 'rvn_post2']),
 place('rsanta', 'サンタに会う', 'hotel', 26, 50, '🎅', ['サンタクロース・オフィス', '毎日会える・入場無料'], ['rvn_santa1', 'rvn_santa2']),
 place('rrein', 'トナカイ', 'beach', 72, 66, '🦌', ['トナカイにあいにいく', '雪の道とそり'], ['rvn_reindeer1', 'rvn_reindeer2']),
 place('rhotel', 'ホテルの夜', 'hotel', 28, 84, '🌌', ['ホテル(夜)', 'オーロラを待つ。出るとは限らない'], ['rvn_hotel1', 'rvn_hotel2'])]
RDEP = [
 place('rchk', 'チェックイン', 'hall', 24, 14, '🧳', ['チェックイン', '新しい広い出発ホール'], ['rvn_checkin1', 'rvn_checkin2']),
 place('rsec', '保安検査', 'info', 72, 32, '🛃', ['保安検査', 'トレイとコートとベルト'], ['rvn_sec1', 'rvn_sec2']),
 place('rshop', 'ギフトショップ', 'souk', 26, 50, '🎁', ['Napapiirin Lahja', '検査の前にも後にもある'], ['rvn_shop1', 'rvn_shop2']),
 place('rahk', 'Ahkio', 'cafe', 72, 66, '🍲', ['Ahkio Kitchen and Bar', '検査のあと・サーモンスープとトナカイバーガー'], ['rvn_ahkio1', 'rvn_ahkio2']),
 place('rgate', 'ゲート', 'hall', 28, 84, '🛫', ['出発ゲート', '雪の窓の前で'], ['rvn_gate1', 'rvn_gate2'])]
RVN_IDS = [i for p in RARR + RSTAY + RDEP for i in p['v']]

SPJS = r"""
SP.sage={pitch:.8,m:[[trav({}),P(4,{o:'#5a3a8a',p:'#3a2a5a',h:'#d9d4c6'})]]};
SP.desk_star={pitch:1.2,m:[[trav({hair:'long'}),P(1,{o:'#c8182a',p:'#2a2a33',h:'#241a14'})]]};
SP.desk_ow={pitch:.95,m:[[trav({hair:'cap'}),P(3,{o:'#5c0632',p:'#2a2a33',h:'#241a14'})]]};
SP.officer={pitch:.9,m:[[trav({hair:'cap'}),P(5,{o:'#2b3a5a',p:'#2b2b33',h:'#241a14'})]]};
SP.officer2={pitch:1.15,m:[[trav({hair:'long'}),P(4,{o:'#2b3a5a',p:'#2b2b33',h:'#241a14'})]]};
SP.bag_staff={pitch:1,m:[[trav({}),P(5,{o:'#f2b705',p:'#2a2a33',h:'#241a14'})]]};
/* 荷物受け取りの旅行者(タスク046)。見た目は d_metrop(リュックの旅行者)と同じ系統。声は pitch 1.0(成人・中性的。係員 bag_staff2=1.1・雨もりの旅行者 ev_wet=.95・ルル=1.35と被らない) */
SP.traveler={pitch:1,m:[[trav({}),P(2,{o:'#3a5a8a',p:'#2a2a33',h:'#14141a',pack:1})]]};
/* ナイロビの滞在(タスク058): サファリのガイド(声 pitch .9)とマサイマーケットの店の人(pitch 1.05)。絵は素材(t-safari-front / t-maasai-front)、ここはコードのドット絵(絵が読めないときの保険と声の高さ) */
SP.safari_guide={pitch:.9,m:[[trav({hair:'cap'}),P(5,{o:'#8a6a3a',p:'#4a3a2a',h:'#241a14'})]]};
SP.market_vendor={pitch:1.05,m:[[trav({hair:'long'}),P(1,{o:'#c8182a',p:'#2a2a33',h:'#241a14'})]]};
SP.bag_staff2={pitch:1.1,m:[[trav({hair:'long'}),P(4,{o:'#f2b705',p:'#2a2a33',h:'#241a14'})]]};
SP.sim_staff={pitch:1.1,m:[[trav({hair:'long'}),P(4,{o:'#43b02a',p:'#2a2a33',h:'#241a14'})]]};
SP.sim_staff2={pitch:.95,m:[[trav({}),P(5,{o:'#43b02a',p:'#2a2a33',h:'#241a14'})]]};
SP.taxi_staff={pitch:.9,m:[[trav({hair:'cap'}),P(5,{o:'#e8d8a8',p:'#3a3a48',h:'#241a14'})]]};
SP.driver={pitch:.95,m:[[trav({hair:'cap'}),P(4,{o:'#2f7a4a',p:'#2a2a33',h:'#241a14'})]]};
SP.cafe_staff={pitch:1.15,m:[[trav({hair:'long'}),P(4,{o:'#7a3b1e',p:'#2a2a33',h:'#241a14'})]]};
SP.cafe_staff2={pitch:.9,m:[[trav({hair:'curly'}),P(2,{o:'#2d8f8a',p:'#6a5a4a',h:'#6a5a3a',pack:1})]]};
/* 英会話カフェの先生=ピンクアフロのおじさん(タスク079)。声は pitch .6(旧 1.1)。ほかの全キャラ(最低は r_santa .72・次が賢者 .8)より低く、ルル 1.35・キングと聞き分けられる。台本パート(068)も自由会話(073)も、この値を S.pitch で読むので両方に効く */
SP.eikai_teacher={pitch:.6,m:[[trav({hair:'curly'}),P(4,{o:'#e8a21c',p:'#1f8a8a',h:'#d63a8a'})]]};
SP.cafe_staff3={pitch:1.2,m:[[trav({hair:'long'}),P(5,{o:'#2f4b7a',p:'#2a2a33',h:'#241a14'})]]};
SP.cafe_staff4={pitch:1,m:[[trav({}),P(4,{o:'#2f4b7a',p:'#2a2a33',h:'#241a14'})]]};
SP.lounge_staff={pitch:1.2,m:[[trav({hair:'long'}),P(4,{o:'#3a2a5a',p:'#2a2a33',h:'#241a14'})]]};
SP.lounge_guest={pitch:1,m:[[trav({hair:'curly'}),P(1,{o:'#d06a2a',p:'#44464f',h:'#8a6a3a'})]]};
SP.duty_staff={pitch:1.1,m:[[trav({}),P(5,{o:'#143fb0',p:'#2a2a33',h:'#241a14'})]]};
SP.duty_staff2={pitch:1.2,m:[[trav({hair:'long'}),P(4,{o:'#143fb0',p:'#2a2a33',h:'#241a14'})]]};
SP.gate_agent={pitch:1.15,m:[[trav({hair:'long'}),P(4,{o:'#1f6aa8',p:'#2a2a33',h:'#241a14'})]]};
SP.gate_agent2={pitch:.9,m:[[trav({hair:'cap'}),P(5,{o:'#1f6aa8',p:'#2a2a33',h:'#241a14'})]]};
SP.qr_checkin={pitch:1.2,m:[[trav({hair:'long'}),P(4,{o:'#5c0632',p:'#2a2a33',h:'#241a14'})]]};
SP.qr_checkin2={pitch:.95,m:[[trav({}),P(5,{o:'#5c0632',p:'#2a2a33',h:'#241a14'})]]};
SP.sec_n1={pitch:.85,m:[[trav({hair:'cap'}),P(5,{o:'#1b2a55',p:'#14141a',h:'#241a14'})]]};
SP.sec_n2={pitch:1.1,m:[[trav({hair:'long'}),P(4,{o:'#1b2a55',p:'#14141a',h:'#241a14'})]]};
SP.tk_checkin={pitch:1.15,m:[[trav({hair:'long'}),P(4,{o:'#c8102e',p:'#2a2a33',h:'#241a14'})]]};
SP.tk_crew={pitch:1.2,m:[[trav({hair:'long'}),P(2,{o:'#c8102e',p:'#c8102e',h:'#241a14'})]]};
SP.qr_crew={pitch:1.2,m:[[trav({hair:'long'}),P(2,{o:'#5c0632',p:'#5c0632',h:'#241a14'})]]};
SP.qr_crew2={pitch:1,m:[[trav({}),P(1,{o:'#5c0632',p:'#3a3a48',h:'#3b2a1f'})]]};
/* 割りこみ・顔なじみの相手(タスク014)。相手は係員だけに寄せない(005 配役D)。ev_ribbon は doh の d_traveler と同じ見た目(同じ旅行者) */
SP.ev_runner={pitch:1.1,m:[[trav({hair:'curly'}),P(2,{o:'#c0504a',p:'#44464f',h:'#241a14'})]]};
SP.ev_wet={pitch:.95,m:[[trav({}),P(4,{o:'#3a8f7a',p:'#2a2a33',h:'#14141a'})]]};
SP.ev_trav3={pitch:1.05,m:[[trav({hair:'long'}),P(3,{o:'#d9a441',p:'#2a2a33',h:'#241a14'})]]};
SP.ev_ribbon={pitch:.95,m:[[trav({}),P(4,{o:'#2d8f8a',p:'#44464f',h:'#14141a',pack:1})]]};
SP.ev_phone={ghost:1,pitch:1.1,m:[[trav({hair:'long'}),P(4,{o:'#5c0632',p:'#2a2a33',h:'#241a14'})]]};
"""
BGJS = r"""
BGS.sage=function(){grad(0,98,'#10143a','#2a2f6a',14);for(var i=0;i<26;i++){var sx=(i*47)%320,sy=(i*29)%60;if((Math.floor(t*2)+i)%5)R('#ffe9a8',sx,sy,2,2);else R('#fff',sx,sy,1,1)}
 R('#5a4a7a',40,20,18,78);R('#7a6a9a',36,18,26,4);R('#5a4a7a',262,20,18,78);R('#7a6a9a',258,18,26,4);
 R('#2a2448',0,98,VW,52);for(var x=0;x<VW;x+=32)R('#3a3460',x,98,1,52);
 R('#c9a03a',130,108,60,4);R('#ffd36a',140,106,40,2);R('#ffd36a',158,100,4,10)};
BGS.tdesk=function(){airWall('#eef0f4');floorAir('#d8dce6','#c4c8d4');signBox(90,8,140,'ROUND THE WORLD','#143fb0');
 R('#d9d4c6',60,58,200,40);R('#9a947f',60,58,200,3);R('#14141a',150,44,22,14);R('#2a6a9a',152,46,18,10);
 R('#c9a03a',20,112,280,2)};
BGS.javaK=function(){airWall('#e8dcc4');floorAir('#d8cdb0','#c4b898');signBox(90,8,140,'JAVA HOUSE','#6a3b1e');
 R('#7a5a30',30,62,260,36);R('#9a7a50',30,62,260,3);for(var i=0;i<6;i++){R('#fff',44+i*40,50,14,12);R('#3b2a1f',46+i*40,52,10,6)}
 R('#2a1a14',220,20,70,32);R('#c98a2a',226,26,24,6);R('#6a3b1e',256,26,24,6)};
BGS.eikaiK=function(){airWall('#e8dcc4');floorAir('#c98a5a','#b07646');signBox(70,8,180,'ENGLISH CAFE','#2f5a3a');
 R('#2a3a34',80,24,160,40);R('#8a6a3a',80,64,160,3);R('#7a5a30',110,88,100,10);R('#9a7a50',110,88,100,3)};
BGS.campK=function(){airWall('#243050');floorAir('#3a4a78','#2f3e68')};   /* 合宿(078): 紺の手順描画。082から背景は背景画(camp.png。artIdFor の campK→camp)。これは背景画が出せないとき(読み込み失敗・服の設定が通常でないとき)の保険だけ。使うのは camp_demo1 だけ */
BGS.artK=function(){airWall('#f1ede2');floorAir('#e0d8c4','#cfc6ae');signBox(90,8,140,'ARTCAFFE','#2f4b7a');
 R('#cfd6e4',30,62,260,36);R('#8aa0b8',30,62,260,3);for(var i=0;i<5;i++){R('#d9a441',44+i*48,48,26,14);R('#a87a2a',44+i*48,58,26,4)}
 R('#e8d8b8',230,20,60,26)};
BGS.lounge=function(){airWall('#3a2a4a');floorAir('#5a4a6a','#4a3a5a');signBox(90,8,140,'PRIDE LOUNGE','#c9a03a','#2a1a3a');
 R('#8a5a9a',30,66,90,32);R('#aa7aba',30,60,90,8);R('#8a5a9a',200,66,90,32);R('#aa7aba',200,60,90,8);
 R('#2a1a3a',140,76,40,22);R('#ffd36a',152,70,16,6)};
BGS.sim=function(){airWall('#f1ede2');floorAir('#e0d8c4','#cfc6ae');signBox(40,10,110,'SAFARICOM','#43b02a');
 R('#2b5a2a',40,34,160,52);T('SIM',120,52,16,'#fff');
 R('#d6d0be',30,84,250,14);R('#9a947f',30,84,250,2);for(var i=0;i<6;i++){R('#14141a',40+i*38,72,8,12);R('#5a8ad8',41+i*38,73,6,8)}};
BGS.taxi=function(){grad(0,70,'#7cc4ee','#dff2fa',10);R('#cfd6e4',0,40,VW,28);for(var i=0;i<9;i++)R('#8aa0b8',i*36+4,44,28,20);
 R('#5a5a66',0,86,VW,64);R('#8a8a94',0,86,VW,3);R('#f2c200',0,126,VW,2);
 R('#143fb0',20,6,70,17);T('TAXI',55,14.5,11,'#fff');R('#2f7a4a',108,6,120,17);T('RIDE SHARE ▶',168,14.5,9,'#fff');
 for(var k=0;k<2;k++){var x=130+k*90;R(k?'#f4f4ee':'#e8d8a8',x,70,70,18);R('#d6c48c',x+10,60,46,12);R('#7ac0f0',x+14,62,16,9);R('#7ac0f0',x+34,62,16,9);R('#14141a',x+8,86,12,8);R('#14141a',x+50,86,12,8)}};
BGS.duty=function(){R('#1b2a55',0,0,VW,98);R('#c9a03a',0,0,VW,4);R('#143fb0',60,6,200,21);R('#ffd36a',60,6,200,1);T('DUTY FREE',160,16.5,12,'#ffd36a');
 for(var s=0;s<3;s++){var y=34+s*20;R('#c9a03a',10,y+14,300,3);var cl=['#c98a2a','#8a1a2a','#2d8f8a','#f4f0e6','#7a3b8a','#3a5a2a'];for(var i=0;i<24;i++){var h=8+((i*7+s)%3)*3;R(cl[(i+s)%6],14+i*12,y+14-h,8,h)}}
 R('#efe6d0',0,98,VW,52);for(var x=0;x<VW;x+=32)R('#d0c6aa',x,98,1,52)};
BGS.gate=function(){airWall('#d8dde8');R('#8fd0f0',20,12,230,62);R('#cdeaf7',20,50,230,24);R('#6a6a76',20,74,230,6);
 var px=((t*10)%330)-40;R('#f6f6f2',px,54,70,12);R('#7ac0f0',px+10,56,48,3);R('#aab3c8',18,10,4,72);R('#aab3c8',248,10,4,72);R('#aab3c8',134,10,3,72);
 R('#05070f',262,16,50,34);T('GATE',287,26,9,'#ffd36a');T(Math.floor(t*1.2)%2?'BOARDING':'ON TIME',287,40,7,'#3ad36a');
 floorAir('#c4c8d4','#aeb2c0');R('#4a5a8a',266,68,46,10);R('#3a4a7a',266,78,46,6)};
"""
SPD = r"""
SP.d_officer={pitch:.85,m:[[trav({hair:'cap'}),P(3,{o:'#3a4a3a',p:'#2b2b33',h:'#14141a'})]]};
SP.d_officer2={pitch:1.1,m:[[trav({hair:'long'}),P(3,{o:'#3a4a3a',p:'#2b2b33',h:'#14141a'})]]};
SP.d_bag={pitch:1,m:[[trav({}),P(2,{o:'#8a1538',p:'#2a2a33',h:'#241a14'})]]};
SP.d_traveler={pitch:.95,m:[[trav({}),P(4,{o:'#2d8f8a',p:'#44464f',h:'#14141a',pack:1})]]};
SP.d_sim={pitch:1.15,m:[[trav({hair:'long'}),P(2,{o:'#e2231a',p:'#2a2a33',h:'#241a14'})]]};
SP.d_sim2={pitch:1.05,m:[[trav({hair:'long'}),P(5,{o:'#5a7a4a',p:'#44464f',h:'#241a14'})]]};
SP.d_taxi={pitch:.9,m:[[trav({hair:'cap'}),P(4,{o:'#2aa6a6',p:'#2a2a33',h:'#241a14'})]]};
SP.d_metrop={pitch:.95,m:[[trav({}),P(2,{o:'#3a5a8a',p:'#2a2a33',h:'#14141a',pack:1})]]};
SP.d_metro={pitch:1.1,m:[[trav({hair:'long'}),P(1,{o:'#c8182a',p:'#2a2a33',h:'#241a14'})]]};
/* ドーハ後半(タスク023)。服装・肌の色・髪型をばらけさせる。白い上下＋白い帽子は、地元の人の服装(悪役にしない) */
SP.d_ck={pitch:1.15,m:[[trav({hair:'long'}),P(3,{o:'#8a1538',p:'#2a2a33',h:'#241a14'})]]};
SP.d_exit={pitch:.9,m:[[trav({hair:'cap'}),P(4,{o:'#3a4a3a',p:'#2b2b33',h:'#14141a',c:'#3a4a3a'})]]};
SP.d_photo={pitch:1.2,m:[[trav({hair:'curly'}),P(5,{o:'#e8b23a',p:'#3a5a8a',h:'#14141a',pack:1})]]};
SP.d_trainp={pitch:.95,m:[[trav({}),P(2,{o:'#4a6a9a',p:'#2a2a33',h:'#8a6a3a'})]]};
SP.d_bench={pitch:1.05,m:[[trav({hair:'long'}),P(1,{o:'#9a5ab0',p:'#44464f',h:'#c9a060'})]]};
SP.lounge_guest={pitch:1,m:[[trav({hair:'curly'}),P(1,{o:'#d06a2a',p:'#44464f',h:'#8a6a3a'})]]};
SP.d_gate={pitch:1.1,m:[[trav({hair:'long'}),P(3,{o:'#8a1538',p:'#2a2a33',h:'#14141a'})]]};
SP.d_seat={pitch:.9,m:[[trav({}),P(2,{o:'#5a7a5a',p:'#3a3a48',h:'#d9d4c6'})]]};
SP.c_man={pitch:.85,m:[[trav({hair:'cap'}),P(4,{o:'#f4f2ea',p:'#f4f2ea',h:'#14141a',c:'#f4f2ea'})]]};
SP.c_tea={pitch:.95,m:[[trav({}),P(5,{o:'#c98a2a',p:'#3a3a48',h:'#14141a'})]]};
SP.c_young={pitch:1.05,m:[[trav({hair:'cap'}),P(3,{o:'#f4f2ea',p:'#f4f2ea',h:'#14141a',c:'#e8e4d8'})]]};
SP.c_front={pitch:1.15,m:[[trav({hair:'long'}),P(2,{o:'#2a3a5a',p:'#2a2a33',h:'#3b2a1f'})]]};
SP.c_guest={pitch:1,m:[[trav({hair:'curly'}),P(4,{o:'#2d8f5a',p:'#44464f',h:'#14141a'})]]};
SP.c_spice={pitch:.9,m:[[trav({}),P(4,{o:'#a8572a',p:'#3a3a48',h:'#14141a'})]]};
SP.c_cloth={pitch:1.2,m:[[trav({hair:'long'}),P(3,{o:'#2a2a33',p:'#2a2a33',h:'#14141a'})]]};
SP.c_souv={pitch:1,m:[[trav({hair:'cap'}),P(5,{o:'#3a6a8a',p:'#2a2a33',h:'#14141a',c:'#c8402a'})]]};
SP.c_waiter={pitch:1.05,m:[[trav({}),P(3,{o:'#f4f0e6',p:'#14141a',h:'#241a14'})]]};
SP.c_family={pitch:1.1,m:[[trav({hair:'long'}),P(2,{o:'#c0504a',p:'#44464f',h:'#241a14'})]]};
SP.c_waiter2={pitch:.9,m:[[trav({hair:'cap'}),P(4,{o:'#f4f0e6',p:'#14141a',h:'#241a14',c:'#14141a'})]]};
SP.c_break={pitch:1.15,m:[[trav({hair:'long'}),P(1,{o:'#6a8ac0',p:'#d9d4c6',h:'#7a5a3a'})]]};
SP.c_front2={pitch:.95,m:[[trav({}),P(3,{o:'#2a3a5a',p:'#2a2a33',h:'#241a14'})]]};
SP.c_walker={pitch:1.1,m:[[trav({hair:'curly'}),P(2,{o:'#e86a8a',p:'#2a2a33',h:'#241a14',shorts:1})]]};
SP.c_boat={pitch:.85,m:[[trav({hair:'cap'}),P(5,{o:'#f4f2ea',p:'#f4f2ea',h:'#14141a',c:'#f4f2ea'})]]};
SP.c_student={pitch:1.1,m:[[trav({}),P(3,{o:'#3a8f7a',p:'#2a2a33',h:'#14141a',pack:1})]]};
SP.ev_tourist={pitch:1.05,m:[[trav({hair:'long'}),P(1,{o:'#d9a441',p:'#3a5a8a',h:'#c9a060',pack:1})]]};
"""
BGD = r"""
/* ハマド国際空港: 砂色の壁・木の波形の天井・えんじ色(カタールの色)の案内 */
function hiaRoof(){R('#c9a878',0,0,VW,7);for(var x=0;x<VW;x+=16){R('#a8845a',x,7,8,2);R('#b89468',x+8,5,8,2)}}
BGS.dimmig=function(){airWall('#efe6d2');hiaRoof();floorAir('#e2d6bc','#cfc2a4');signBox(30,12,128,'PASSPORT CONTROL','#8a1538');
 for(var i=0;i<3;i++){var x=22+i*100;R('#d9d0bc',x,38,80,50);R('#9fb6c8',x+2,40,76,34);R('#6a5a4a',x,74,80,24);R('#c9a03a',x,74,80,2);R(Math.floor(t*2+i)%2?'#3ad36a':'#2a8a4a',x+34,32,10,4)}
 R('#8a1538',0,124,VW,2)};
BGS.dbag=function(){airWall('#efe6d2');hiaRoof();floorAir('#e2d6bc','#cfc2a4');signBox(30,12,128,'BAGGAGE CLAIM','#8a1538');
 R('#05070f',132,36,60,24);T('BELT 8',162,44,8,'#ffd36a');T('NAIROBI',162,54,6.5,'#fff');
 R('#2a2a33',0,76,VW,22);R('#4a4a56',0,76,VW,3);var cl=['#2f5bb0','#2d8f8a','#2f5bb0','#7a3b8a','#d9a441'];
 for(var i=0;i<5;i++){var x=((t*22+i*72)%390)-30;R(cl[i],x,64,26,14);R('#3a3a46',x+10,60,6,4);if(i===2)R('#c8182a',x+11,58,4,3)}
 R('#a0a0aa',0,96,VW,3)};
BGS.dsim=function(){airWall('#efe6d2');hiaRoof();floorAir('#e2d6bc','#cfc2a4');
 R('#e2231a',30,12,170,22);R('#fff',30,12,170,1);T('OOREDOO',115,23.5,13,'#fff');
 R('#f6f2e8',30,34,170,52);T('VISITOR SIM',115,52,10,'#e2231a');T('7 DAYS',115,68,8,'#5a5a66');
 R('#d6d0be',40,84,240,14);R('#9a947f',40,84,240,2);for(var i=0;i<6;i++){R('#14141a',52+i*38,72,8,12);R('#e2231a',53+i*38,73,6,8)}};
var _dn={v:false,at:-1e9};function dohNight(){if(t-_dn.at>30){_dn.at=t;try{var h=+new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Qatar',hour:'2-digit',hourCycle:'h23'}).format(new Date());_dn.v=h>=18||h<5}catch(e){_dn.v=false}}return _dn.v}
BGS.dtaxi=function(){var n=dohNight();grad(0,70,n?'#141a3a':'#7cc4ee',n?'#2a3466':'#dff2fa',10);
 R('#d9cfb8',0,36,VW,34);for(var i=0;i<9;i++)R(n?'#ffd98a':'#9fb6c8',i*36+6,42,24,20);R('#c9a878',0,30,VW,6);
 R('#5a5a66',0,86,VW,64);R('#8a8a94',0,86,VW,3);R('#f2c200',0,126,VW,2);
 R('#8a1538',20,6,70,17);T('TAXI',55,14.5,11,'#fff');R('#2aa6a6',108,6,90,17);T('KARWA',153,14.5,10,'#fff');
 for(var k=0;k<2;k++){var x=120+k*96;R('#2aa6a6',x,70,72,18);R('#238a8a',x+10,60,48,12);R('#bfe8f0',x+14,62,17,9);R('#bfe8f0',x+35,62,17,9);R('#14141a',x+8,86,12,8);R('#14141a',x+52,86,12,8);R('#ffd36a',x+28,56,16,4)}};
BGS.dmetro=function(){airWall('#e8e4da');hiaRoof();floorAir('#d8d2c2','#c4bca8');signBox(30,12,140,'DOHA METRO','#8a1538');
 R('#c8182a',0,34,VW,3);T('RED LINE',200,44,7,'#c8182a');
 R('#f4f2ec',20,50,150,40);R('#c8182a',20,84,150,4);for(var i=0;i<3;i++){R('#2b3a5a',30+i*46,56,34,18)}R('#14141a',20,90,150,4);
 for(i=0;i<3;i++){var gx=196+i*38;R('#8a8a94',gx,62,8,36);R('#8a8a94',gx+22,62,8,36);R(Math.floor(t*2+i)%2?'#3ad36a':'#2a8a4a',gx+11,70,8,10)}};
/* 市内の地図(湾の弧)と、出発の地図(2つの広場＋列車) */
function dohCityBg(g,cw,ch){var cx=cw*.56,cy=ch*1.02,rx=cw*.46,ry=ch*.36;
 for(var y=0;y<ch;y++){var dy=(y-cy)/ry;if(dy*dy>=1)continue;var hw=rx*Math.sqrt(1-dy*dy);g.fillStyle='#f0e2bc';g.fillRect(Math.round(cx-hw-3),y,Math.round(hw*2+6),1);g.fillStyle=(y%6<1)?'#a8dcef':'#86c8e4';g.fillRect(Math.round(cx-hw),y,Math.round(hw*2),1)}
 g.fillStyle='#c9a26a';for(var i=0;i<5;i++){g.fillRect(Math.round(cw*.06+i*5),Math.round(ch*.7),3,3);g.fillRect(Math.round(cw*.2+i*5),Math.round(ch*.32),3,3)}
 g.fillStyle='#8a5a2a';g.fillRect(Math.round(cx-6),Math.round(ch*.86),8,2);g.fillRect(Math.round(cx+10),Math.round(ch*.92),8,2)}
function dohDepBg(g,cw,ch){function plaza(px,py,col){var X=cw*px/100,Y=ch*py/100,r=Math.min(cw,ch)*.16;for(var y=-r;y<r;y++){var hw=Math.sqrt(r*r-y*y);g.fillStyle=col;g.fillRect(Math.round(X-hw),Math.round(Y+y),Math.round(hw*2),1)}}
 plaza(72,30,'#f4e8c4');plaza(24,74,'#dcecc8');
 g.fillStyle='#3a8a4a';for(var i=0;i<6;i++)g.fillRect(Math.round(cw*(.16+(i%3)*.06)),Math.round(ch*(.68+Math.floor(i/3)*.08)),3,3);
 var a=[cw*.72,ch*.30],b=[cw*.24,ch*.74];g.fillStyle='#c9a0a8';for(var k=4;k<=36;k+=2){var x=a[0]+(b[0]-a[0])*k/40,y=a[1]+(b[1]-a[1])*k/40;g.fillRect(Math.round(x)-1,Math.round(y),3,1)}}
/* ---- ドーハ後半(タスク023): 出発 ---- */
BGS.dcheck=function(){airWall('#efe6d2');hiaRoof();floorAir('#e2d6bc','#cfc2a4');signBox(30,12,110,'DEPARTURES','#8a1538');
 for(var i=0;i<3;i++){var x=14+i*102;R('#8a1538',x,38,90,10);T('CHECK-IN',x+45,43.5,7,'#fff');R('#d9d4c6',x,62,90,36);R('#9a947f',x,62,90,3);R('#14141a',x+34,50,20,12);R('#2a6a9a',x+36,52,16,8);R('#6a6a76',x+62,90,24,8)}
 for(i=0;i<8;i++){R('#c9a03a',14+i*40,112,2,12);R('#8a1538',14+i*40,114,38,1)}};
BGS.dsouth=function(){airWall('#efe6d2');R('#c9a878',0,0,VW,4);for(var x=0;x<VW;x+=20){R('#a8845a',x,4,2,30);R('#e4d4b4',x+2,34,16,2)}
 R('#9fd0ea',40,10,240,30);for(x=40;x<280;x+=30)R('#c9a878',x,10,2,30);floorAir('#e2d6bc','#cfc2a4');signBox(200,44,104,'SOUTH PLAZA','#8a1538');
 for(var i=0;i<7;i++){var px=((t*14+i*52)%380)-30;R(['#2f5bb0','#c0504a','#3a8f7a','#d9a441','#7a3b8a','#f4f2ea','#4a4a56'][i],px,80,8,16);R('#c99a6a',px+1,74,6,6)}};
BGS.dtrain=function(){airWall('#e8e4da');hiaRoof();R('#c8d6e4',0,30,VW,50);R('#8a1538',0,30,VW,3);
 var tx=(Math.sin(t*.6)*.5+.5)*140-20;R('#f4f2ec',tx,40,190,38);R('#8a1538',tx,72,190,4);for(var i=0;i<5;i++)R('#2b3a5a',tx+10+i*36,46,26,16);
 R('#6a6a76',0,80,VW,4);floorAir('#d8d2c2','#c4bca8');signBox(30,10,120,'TRAIN','#8a1538');T('NORTH ▶',176,18.5,8,'#8a1538')};
BGS.dorch=function(){airWall('#eef0e6');R('#c9a878',0,0,VW,4);R('#bfe4f2',0,4,VW,36);for(var x=0;x<VW;x+=24)R('#a8845a',x,4,2,36);floorAir('#e2d6bc','#cfc2a4');
 for(var i=0;i<6;i++){var x2=14+i*54;R('#7a5a3a',x2+10,52,6,46);R('#3a8a4a',x2,34,28,20);R('#4aa05a',x2+4,28,20,10);R('#2a6a3a',x2+2,50,24,4)}
 for(i=0;i<3;i++){R('#8a6a4a',40+i*100,104,60,6);R('#6a4a2a',44+i*100,110,4,8);R('#6a4a2a',92+i*100,110,4,8)}};
BGS.dlng=function(){airWall('#e2d6c4');hiaRoof();floorAir('#d8ccb0','#c4b898');
 R('#5a4a3a',30,24,110,74);R('#3a2a1e',36,30,98,68);T('LOUNGE ▶',85,62,8,'#c9a03a');R('#8a1538',180,24,110,74);R('#a8204a',186,30,98,68);T('?',235,60,18,'#f4d8a0');
 R('#3a8a4a',150,60,20,38);R('#4aa05a',146,50,28,14)};
BGS.dgate=function(){airWall('#e6e0d2');hiaRoof();R('#8fd0f0',84,12,230,62);R('#cdeaf7',84,50,230,24);R('#c9a878',84,74,230,6);
 var px=((t*10)%330)-40;if(px>70){R('#f6f6f2',px,54,70,12);R('#8a1538',px+60,46,10,10);R('#7ac0f0',px+10,56,48,3)}R('#c9a878',82,10,4,72);
 R('#05070f',14,16,60,34);T('HELSINKI',44,26,7.5,'#ffd36a');T(Math.floor(t*1.2)%2?'BOARDING':'CHANGED',44,40,7,'#3ad36a');
 floorAir('#d8d2c2','#c4bca8');R('#8a1538',266,68,46,10);R('#6a1030',266,78,46,6)};
BGS.dcabin=function(){R('#e6e2dc',0,0,VW,98);R('#bcb6ae',0,0,VW,22);R('#d0cac2',0,18,VW,5);for(var i=0;i<4;i++)R('#9a948c',10+i*76,24,60,4);
 R('#4a4a5a',0,98,VW,52);R('#3a3a4a',100,98,120,52);R('#5a5a6a',104,98,3,52);R('#5a5a6a',213,98,3,52);
 R('#05070f',250,42,40,30);R('#7ac0f0',253,45,34,24);var cx=((t*20)%80)-10;R('#f4f2ec',253+cx%40,52,18,6);
 for(i=0;i<3;i++){var x=14+i*34;R('#3a4a6a',x,60,28,38);R('#4a5a7a',x+3,56,22,10);R('#2a3a5a',x,92,28,6)}};
/* ---- ドーハ後半(タスク023): 市内。外の場面は現地の時刻で昼夜が変わる(dohNight) ---- */
function dohSky(n){grad(0,60,n?'#141a3a':'#7cc4ee',n?'#2a3466':'#dff2fa',10)}
function souqWall(n){var w=n?'#8a6a48':'#d9b888',w2=n?'#6a5034':'#b8986a';R(w,0,20,VW,80);for(var x=0;x<VW;x+=40){R(w2,x+30,20,4,80);R(n?'#3a2a1e':'#7a5a3a',x+8,8,16,12)}
 for(x=0;x<VW;x+=40){R(w2,x+6,60,20,38);R(n?'#ffd36a':'#5a4030',x+10,64,12,14)}}
BGS.calley=function(){var n=dohNight();dohSky(n);souqWall(n);
 for(var i=0;i<6;i++){var lx=20+i*54;R('#3a2a1e',lx+4,30,1,8);R(n?'#ffb84a':'#c98a2a',lx,38,10,10);R(n?'#ffe08a':'#e8b860',lx+2,40,6,6)}
 R(n?'#5a4634':'#c9a878',0,100,VW,50);for(var x=0;x<VW;x+=24)R(n?'#4a3826':'#b8986a',x,100,1,50);
 R('#7a5a3a',230,76,60,22);R('#c9a03a',230,74,60,3);R('#f4f2ea',244,66,8,8);R('#f4f2ea',262,66,8,8);if(Math.floor(t*2)%2)R('#e4e4e4',246,58,4,6)};
BGS.chotel=function(){var n=dohNight();R('#e8dcc4',0,0,VW,98);R('#c9a878',0,0,VW,6);R(n?'#2a3466':'#9fd0ea',220,14,80,50);R('#c9a878',258,14,4,50);
 R('#8a6a4a',30,62,150,36);R('#a8845a',30,60,150,4);T('RECEPTION',105,48,8,'#8a6a4a');R('#d9a441',60,20,90,18);R('#fff3d0',66,24,78,10);
 floorAir('#d8c8a8','#c4b494');R('#8a1538',200,96,110,14)};
BGS.csouq=function(){var n=dohNight();dohSky(n);souqWall(n);var cl=['#c98a2a','#a8572a','#d9a441','#7a3b1e','#e8c060','#8a1a2a'];
 for(var i=0;i<12;i++){var x=10+i*26;R(cl[i%6],x,78,20,10);R(cl[(i+2)%6],x+3,72,14,8)}
 for(i=0;i<9;i++){R(['#c8402a','#2d8f8a','#e8b23a','#7a3b8a','#3a6a8a'][i%5],180+i*14,30,10,30)}
 R(n?'#5a4634':'#c9a878',0,100,VW,50)};
BGS.crest=function(){var n=dohNight();dohSky(n);souqWall(n);R(n?'#5a4634':'#c9a878',0,98,VW,52);
 for(var i=0;i<3;i++){var x=30+i*96;R('#f4f0e6',x,92,70,6);R('#8a6a4a',x+6,98,4,22);R('#8a6a4a',x+60,98,4,22);R('#c98a2a',x+20,86,12,6);R('#d9d4c6',x+40,86,10,6)}
 for(i=0;i<5;i++){R(n?'#ffd36a':'#d9a441',40+i*60,14,2,6)}};
BGS.cbreak=function(){R('#f4ecd8',0,0,VW,98);R('#c9a878',0,0,VW,6);R('#9fd0ea',30,14,120,50);R('#dff2fa',30,40,120,24);R('#c9a878',88,14,4,50);
 R('#c9a878',180,60,120,8);for(var i=0;i<4;i++){R('#f4f2ea',188+i*28,48,16,12);R(['#d9a441','#c0504a','#7a3b1e','#3a8f4a'][i],190+i*28,50,12,6)}
 floorAir('#e2d6bc','#cfc2a4');R('#8a6a4a',40,104,90,6);R('#f4f2ea',60,98,12,6);R('#5a3a2a',64,96,4,3)};
BGS.ccorn=function(){var n=dohNight();dohSky(n);
 for(var i=0;i<9;i++){var h=18+((i*37)%30),x=150+i*18;R(n?'#2a3a5a':'#9aaac0',x,58-h,14,h);if(n)for(var y=58-h+4;y<56;y+=6)R('#ffd98a',x+4,y,2,2)}
 R(n?'#1a3a5a':'#4aa0c8',0,58,VW,30);for(i=0;i<8;i++){var wx=((t*8+i*44)%340)-10;R(n?'#3a5a7a':'#8ad0ea',wx,62+(i%3)*8,14,1)}
 for(i=0;i<2;i++){var bx=30+i*70+Math.sin(t+i)*3;R('#8a5a2a',bx,70,40,8);R('#6a4020',bx+4,78,32,3);R('#5a3a1e',bx+18,48,2,22);R('#f4ead0',bx+8,50,10,16)}
 R(n?'#6a6a7a':'#e2d6bc',0,88,VW,62);R(n?'#8a8a9a':'#f4ead0',0,88,VW,3);for(var x=0;x<VW;x+=30)R(n?'#5a5a6a':'#cfc2a4',x,88,1,62)};
"""
BGN = r"""
/* ナイロビの滞在(タスク58): 新しい絵(art.js の nsafari / nmarket)が読めないときと、アルバムの写真に使う、今までのドット絵 */
BGS.safariK=function(){grad(0,60,'#86b9e2','#d6e6ee',10);R('#8a9ab0',60,34,8,26);R('#8a9ab0',72,38,6,22);R('#8a9ab0',84,30,8,30);R('#8a9ab0',96,40,6,20);R('#8a9ab0',110,36,8,24);
 R('#d6b66a',0,60,VW,90);R('#c8a85a',0,84,VW,2);R('#b07a50',0,120,VW,14);
 for(var i=0;i<5;i++){var x=24+i*62;R('#6a4a2a',x+6,70,2,8);R('#4a7a3a',x,66,14,4)}
 R('#e8e0c8',150,78,14,10);R('#4a4a52',152,80,2,8);R('#4a4a52',160,80,2,8);R('#d9a050',200,70,3,18);R('#d9a050',194,70,16,3);R('#9a8a7a',250,86,18,9)};
BGS.marketK=function(){grad(0,60,'#a7cdee','#d6e6f2',10);R('#7e8aa0',40,20,14,30);R('#7e8aa0',200,14,16,36);R('#6a788e',250,22,12,28);
 R('#6a6a68',0,60,VW,90);R('#c8782a',34,40,70,8);R('#8a5a3a',36,60,66,22);R('#143fb0',110,36,100,8);R('#c8182a',116,36,16,8);R('#c8182a',150,36,16,8);R('#8a5a3a',112,62,96,24);
 R('#c8182a',140,48,22,16);R('#c8182a',222,38,70,8);R('#f2c200',230,38,12,8);R('#6a4a2a',224,48,66,30);
 R('#2a5aa0',22,100,80,30);R('#d7b26a',120,98,90,32);R('#9a2a2a',226,100,70,30)};
/* 羽田の出発(タスク043)。出発ゲートは 新しい絵(art.js の hgate)。絵が読めなかったときだけ、今までの ゲートの ドット絵に戻る */
BGS.immigH=function(){BGS.immig()};
BGS.hgateOW=function(){BGS.gate()};
BGS.hgateST=function(){BGS.gate()};
BGS.checkinT=function(){airWall('#eef0f4');floorAir('#d8dce6','#c4c8d4');
 for(var i=0;i<3;i++){var x=14+i*102;R('#c8102e',x,13,90,18);T('TURKISH AIRLINES',x+45,22,7.5,'#fff');R('#d9d4c6',x,62,90,36);R('#9a947f',x,62,90,3);R('#14141a',x+34,50,20,12);R('#2a6a9a',x+36,52,16,8);R('#6a6a76',x+62,90,24,8)}
 for(i=0;i<8;i++){R('#c9a03a',14+i*40,112,2,12);R('#c8102e',14+i*40,114,38,1)}};
BGS.cabinT=function(){R('#e6e2e2',0,0,VW,98);R('#b8b0b0',0,0,VW,22);R('#cfc6c6',0,18,VW,5);
 for(var i=0;i<4;i++){R('#9a9090',10+i*76,24,60,4)}
 R('#5a4448',0,98,VW,52);R('#4a3438',100,98,120,52);R('#6a5458',104,98,3,52);R('#6a5458',213,98,3,52);
 R('#05070f',250,42,40,30);R('#1b2a55',253,45,34,24);var cx=((t*20)%80)-10;R('#c8d0e8',253+cx%40,52,18,6);R('#c8d0e8',262+(cx*1.5)%30,58,14,5);
 for(i=0;i<3;i++){var x=14+i*34;R('#c8102e',x,60,28,38);R('#e0304a',x+3,56,22,10);R('#9a0a20',x,92,28,6)}
 R('#c8102e',70,7,120,17);T('TURKISH AIRLINES',130,16,8,'#fff')};
BGS.checkinQ=function(){airWall('#eef0f4');floorAir('#d8dce6','#c4c8d4');
 for(var i=0;i<3;i++){var x=14+i*102;R('#5c0632',x,13,90,18);T('QATAR AIRWAYS',x+45,22,8,'#fff');R('#d9d4c6',x,62,90,36);R('#9a947f',x,62,90,3);R('#14141a',x+34,50,20,12);R('#2a6a9a',x+36,52,16,8);R('#6a6a76',x+62,90,24,8)}
 for(i=0;i<8;i++){R('#c9a03a',14+i*40,112,2,12);R('#5c0632',14+i*40,114,38,1)}
 sp2r(trav({}),P(4,{o:'#2d8f8a',p:'#44464f',h:'#14141a',pack:1}),270,94,2,14);R('#2f5bb0',254,108,14,12);R('#1e3d80',254,108,14,2);R('#c8182a',259,105,3,4)};
BGS.cabinQ=function(){R('#e4dfe2',0,0,VW,98);R('#b8aeb6',0,0,VW,22);R('#cfc6cc',0,18,VW,5);
 for(var i=0;i<4;i++){R('#9a8e98',10+i*76,24,60,4)}
 R('#6a4a5a',0,98,VW,52);R('#5a3a4a',100,98,120,52);R('#7a5a6a',104,98,3,52);R('#7a5a6a',213,98,3,52);
 R('#05070f',250,42,40,30);R('#1b2a55',253,45,34,24);var cx=((t*20)%80)-10;R('#c8d0e8',253+cx%40,52,18,6);R('#c8d0e8',262+(cx*1.5)%30,58,14,5);
 for(i=0;i<3;i++){var x=14+i*34;R('#5c0632',x,60,28,38);R('#7a1a48',x+3,56,22,10);R('#44042a',x,92,28,6)}
 R('#5c0632',70,7,120,17);T('QATAR AIRWAYS',130,16,9,'#fff')};
"""
WORLDJS = r"""
/* 世界マップの「いま いる 空港」を合わせる(クリアは変えない) */
function worldAt(k){try{var w=JSON.parse(localStorage.getItem('kanpe-world-v1')||'null');if(!w||typeof w!=='object')w={v:1,at:'haneda',seen:{haneda:1},cleared:{haneda:1}};w.seen=w.seen&&typeof w.seen==='object'?w.seen:{};w.cleared=w.cleared&&typeof w.cleared==='object'?w.cleared:{};if(w.at!==k)w.from=w.at;w.at=k;w.seen[k]=1;localStorage.setItem('kanpe-world-v1',JSON.stringify(w))}catch(e){}}
"""
MAIN = r"""
/* ===== 世界一周編: ナイロビ(賢者・券えらび・到着・空港・出発) ===== */
var TOURDLG=%(dlg)s;
for(var _k in TOURDLG)DLG[_k]=TOURDLG[_k];
%(sp)s
%(bg)s
%(world)s
%(voice)s
%(diag)s
%(ev)s
%(win)s
var PLACES_SAGE=%(sage)s,PLACES_HDEP=%(hdep)s,PLACES_HRET=%(hret)s,PLACES_NARR=%(arr)s,PLACES_NSTAY=%(stay)s,PLACES_NAIR=%(air)s,PLACES_NDEP=%(dep)s,PLACES_EIKAI=%(eikai)s,PLACES_CAMP=%(camp)s;
PLACES_AIR=PLACES_NAIR;
PLACES_SAGE.concat(PLACES_HDEP,PLACES_HRET,PLACES_NARR,PLACES_NSTAY,PLACES_NAIR,PLACES_NDEP,PLACES_EIKAI,PLACES_CAMP).forEach(function(p){PBY[p.id]=p});
var TOUR_IDS=%(ids)s;
function hdepOn(){try{return !!save.ticket&&TRIP.departPending()}catch(e){return false}}
function hretOn(){try{return !!save.ticket&&TRIP.retToday()}catch(e){return false}}   /* 28日目の羽田(059): 落とし物を返す日をあそぶ時 */   /* 1日目の羽田の出発をあそぶ時(券を買った・まだ羽田) */
MODES={sage:{p:PLACES_SAGE,b:'🧙 賢者',h:'達人賢者の広間<small>世界一周のはじまり</small>',snd:'sage'},
 hdep:{p:PLACES_HDEP,b:'🛫 羽田',h:'羽田から出発<small>チェックインから機内まで・深夜便</small>',snd:'nbo'},
 hret:{p:PLACES_HRET,b:'🛬 羽田',h:'羽田に帰ってきた<small>おかえりなさい</small>',snd:'nbo'},
 arr:{p:PLACES_NARR,b:'🛬 到着',h:'ナイロビに到着<small>ジョモ・ケニヤッタ国際空港</small>',snd:'nbo'},
 stay:{p:PLACES_NSTAY,b:'🦒 滞在',h:'ナイロビの滞在<small>マサイマーケットとサファリ</small>',snd:'safari'},
 air:{p:PLACES_NAIR,b:'✈ 空港',h:'ナイロビの空港<small>出発までの時間</small>',snd:'nbo'},
 dep:{p:PLACES_NDEP,b:'🛫 出発',h:'ナイロビから出発<small>チェックインから機内まで</small>',snd:'nbo'},
 eikai:{p:PLACES_EIKAI,b:'☕ 英会話',h:'英会話カフェ<small>ナイロビの小さなカフェ</small>',snd:'cafe'},   /* 068: チェックモードだけ(タブは通常は隠す) */
 camp:{p:PLACES_CAMP,b:'💪 合宿',h:'合宿<small>マッチョルルの教室(デモ)</small>',snd:'hall'}};   /* 078: チェックモードだけ(タブは通常は隠す) */
"""
MAIN_DOH = r"""
/* ===== 世界一周編: ドーハ(到着・街・出発。タスク023 で街と出発を追加) ===== */
var TOURDLG=%(dlg)s;
for(var _k in TOURDLG)DLG[_k]=TOURDLG[_k];
%(sp)s
%(bg)s
%(world)s
%(voice)s
%(ev)s
var PLACES_DARR=%(arr)s,PLACES_DCITY=%(city)s,PLACES_DDEP=%(dep)s;
PLACES_AIR=PLACES_DDEP;   /* 世界マップのクリアの印: 出発の場所を全部(各1つ以上)あそんだら */
PLACES_DARR.concat(PLACES_DCITY,PLACES_DDEP).forEach(function(p){PBY[p.id]=p});
var TOUR_IDS=%(ids)s;
MODES={arr:{p:PLACES_DARR,b:'🛬 到着',h:'ドーハに到着<small>ハマド国際空港</small>',snd:'doh'},
 city:{p:PLACES_DCITY,b:'🏙 市内',h:'ドーハの街<small>スーク・ワキーフとコルニーシュ・1泊</small>',snd:'dohc'},
 dep:{p:PLACES_DDEP,b:'🛫 出発',h:'ドーハから出発<small>カウンターからヘルシンキ行きの機内まで</small>',snd:'doh'}};
worldAt('doha');
"""

# ---------- ロヴァニエミ(タスク065)の話者・背景・ページの枠 ----------
# 話者: 口数の少ない北の人たち。厚いコート・帽子の色ちがい(服装だけで悪役にしない)。声の高さは ナイロビ・ドーハの係員と かぶらないようにずらす
SPR = r"""
SP.r_officer={pitch:.88,m:[[trav({hair:'cap'}),P(5,{o:'#2b3a5a',p:'#2b2b33',h:'#241a14'})]]};
SP.r_officer2={pitch:1.12,m:[[trav({hair:'long'}),P(4,{o:'#2b3a5a',p:'#2b2b33',h:'#c9a45a'})]]};
SP.r_bag={pitch:.97,m:[[trav({}),P(5,{o:'#e0a21a',p:'#2a2a33',h:'#3b2a1f'})]]};
SP.r_skier={pitch:1.02,m:[[trav({hair:'cap'}),P(2,{o:'#c0392b',p:'#2a3350',h:'#c9a45a',pack:1})]]};
SP.r_greeter={pitch:1.18,m:[[trav({hair:'long'}),P(4,{o:'#2d6a6a',p:'#2a2a33',h:'#241a14'})]]};
SP.r_local={pitch:.82,m:[[trav({hair:'cap'}),P(3,{o:'#4a5a3a',p:'#3a3a48',h:'#d9d4c6'})]]};
SP.r_info={pitch:1.08,m:[[trav({hair:'long'}),P(4,{o:'#1f5a8a',p:'#2a2a33',h:'#a07a4a'})]]};
SP.r_wifi={pitch:.93,m:[[trav({}),P(1,{o:'#7a3b8a',p:'#44464f',h:'#14141a',pack:1})]]};
SP.r_stop={pitch:1.05,m:[[trav({hair:'curly'}),P(3,{o:'#d06a2a',p:'#2a2a33',h:'#5a3a24'})]]};
SP.r_driver={pitch:.9,m:[[trav({hair:'cap'}),P(5,{o:'#1b2a55',p:'#14141a',h:'#241a14'})]]};
SP.r_vguide={pitch:1.1,m:[[trav({hair:'long'}),P(4,{o:'#a02a2a',p:'#2a2a33',h:'#c9a45a'})]]};
SP.r_vwoman={pitch:1.14,m:[[trav({hair:'curly'}),P(3,{o:'#2a5a8a',p:'#3a3a48',h:'#5a3a24'})]]};
SP.r_postclerk={pitch:.92,m:[[trav({hair:'cap'}),P(2,{o:'#c8182a',p:'#2a2a33',h:'#d9d4c6'})]]};
SP.r_poststand={pitch:1.0,m:[[trav({}),P(1,{o:'#5a6a3a',p:'#44464f',h:'#241a14'})]]};
SP.r_santa={pitch:.72,m:[[trav({hair:'cap'}),P(4,{o:'#c0182a',p:'#8a1020',h:'#f2f0ea'})]]};
SP.r_herder={pitch:.88,m:[[trav({hair:'cap'}),P(3,{o:'#2a5a8a',p:'#7a2a2a',h:'#3b2a1f'})]]};
SP.r_family={pitch:1.06,m:[[trav({hair:'long'}),P(2,{o:'#d06a2a',p:'#2a3350',h:'#a07a4a',pack:1})]]};
SP.r_hfront={pitch:1.08,m:[[trav({hair:'long'}),P(5,{o:'#2b3a5a',p:'#2b2b33',h:'#241a14'})]]};
SP.r_nguest={pitch:.96,m:[[trav({}),P(1,{o:'#7a3b8a',p:'#44464f',h:'#5a3a24'})]]};
SP.r_ck1={pitch:1.12,m:[[trav({hair:'long'}),P(5,{o:'#1b3a6a',p:'#2a2a33',h:'#c9a45a'})]]};
SP.r_ck2={pitch:.9,m:[[trav({hair:'cap'}),P(5,{o:'#1b3a6a',p:'#2a2a33',h:'#241a14'})]]};
SP.r_sec1={pitch:.95,m:[[trav({hair:'cap'}),P(4,{o:'#3a4a5a',p:'#2b2b33',h:'#5a3a24'})]]};
SP.r_sec2={pitch:1.1,m:[[trav({hair:'long'}),P(2,{o:'#3a4a5a',p:'#2b2b33',h:'#a07a4a'})]]};
SP.r_shop1={pitch:1.16,m:[[trav({hair:'curly'}),P(1,{o:'#2d6a6a',p:'#2a2a33',h:'#5a3a24'})]]};
SP.r_shop2={pitch:.9,m:[[trav({}),P(3,{o:'#7a4a2a',p:'#2a2a33',h:'#d9d4c6'})]]};
SP.r_waiter1={pitch:.98,m:[[trav({hair:'cap'}),P(4,{o:'#e8e4d8',p:'#2a2a33',h:'#241a14'})]]};
SP.r_diner={pitch:.86,m:[[trav({}),P(2,{o:'#4a5a3a',p:'#3a3a48',h:'#c9a45a',pack:1})]]};
SP.r_gate1={pitch:1.05,m:[[trav({hair:'long'}),P(5,{o:'#1b3a6a',p:'#2a2a33',h:'#241a14'})]]};
SP.r_gate2={pitch:.93,m:[[trav({hair:'cap'}),P(5,{o:'#1b3a6a',p:'#2a2a33',h:'#5a3a24'})]]};
"""
# 背景: 夜の群青・雪の青白・灯りの橙。オーロラの緑は 到着ロビーの実画(art.js の rvnlobby)にだけ出る。
# 看板の文言は確認済みのものだけ(ロビー: ROVANIEMI / Arrivals / Welcome to Rovaniemi Airport、Wi-Fi名、バスの 8 と AIRPORT EXPRESS)。それ以外の文字は置かない。
BGR = r"""
function rSnow(y0,h){for(var i=0;i<28;i++){var x=(i*37+Math.floor(t*(3+i%4)))%VW,y=y0+((i*23+Math.floor(t*(9+i%3*4)))%h);R(i%5?'#e8f0fa':'#fff',x,y,1,1)}}
function rRoof(){R('#4a3626',0,0,VW,8);R('#33241a',0,8,VW,2);for(var x=10;x<VW;x+=46)R('#ffd98a',x,4,5,2)}
function rFloor(){R('#8a867e',0,98,VW,52);for(var x=0;x<VW;x+=32)R('#76726a',x,98,1,52);for(var y=112;y<150;y+=14)R('#76726a',0,y,VW,1)}
BGS.rimmig=function(){R('#cdd3de',0,10,VW,88);rRoof();rFloor();
 for(var i=0;i<3;i++){var x=22+i*100;R('#d9dde6',x,40,80,48);R('#8fb0c8',x+2,42,76,32);R('#5a4a3a',x,74,80,24);R('#c9a03a',x,74,80,2);R(Math.floor(t*2+i)%2?'#3ad36a':'#2a8a4a',x+34,34,10,4)}
 R('#2f4a7a',0,124,VW,2);R('#2f4a7a',0,136,VW,1)};
BGS.rbag=function(){R('#c7cfda',0,10,VW,88);rRoof();rFloor();
 R('#1c2a44',20,24,86,34);R('#3a4a6a',20,24,86,2);R('#e8f0fa',34,34,58,2);R('#e8f0fa',34,42,40,2);R('#e8f0fa',34,50,50,2);
 R('#2a2a33',0,76,VW,22);R('#4a4a56',0,76,VW,3);var cl=['#2f5bb0','#c0392b','#2f5bb0','#2d8f8a','#d9a441'];
 for(var i=0;i<5;i++){var x=((t*22+i*72)%390)-30;R(cl[i],x,64,26,14);R('#3a3a46',x+10,60,6,4);if(i===0||i===2){R('#f2c200',x+11,58,4,3)}}
 R('#a0a0aa',0,96,VW,3);R('#e8eef6',200,100,28,10);R('#b7c5d8',200,108,28,3)};
BGS.rlobby=function(){R('#0b1a3a',0,10,VW,50);for(var i=0;i<18;i++)R('#e8f0fa',(i*53)%VW,12+(i*29)%40,1,1);
 R('#1d6a5a',20,24,280,8);R('#2f8a6a',60,30,200,5);R('#3a3a7a',20,20,280,4);R('#cdd8e8',0,52,VW,10);rRoof();
 for(var x=30;x<VW;x+=40){R('#1a3a3a',x,44,6,12);R('#1a3a3a',x+1,40,4,6);R('#eaf2fa',x+1,40,4,1)}
 R('#6a4a2a',0,62,VW,8);T('ROVANIEMI',200,66,6,'#f4e8c8');R('#143a30',22,64,50,6);T('Arrivals',50,67,5,'#fff');
 rFloor();for(var k=0;k<5;k++)R(k%2?'#d7ecf2':'#b8d4dc',112+k*12,100+k*10,4,10);R('#e8f0fa',96,98,8,52);
 R('#143a30',226,84,56,34);R('#9a2a2a',226,84,56,4);T('Welcome to',254,95,4.5,'#fff');T('Rovaniemi',254,103,5.5,'#fff');T('Airport',254,111,5.5,'#fff')};
BGS.rwifi=function(){R('#d2d8e2',0,10,VW,88);rRoof();rFloor();
 R('#143a5a',60,22,200,40);R('#e8f0fa',60,22,200,2);T('Rovaniemi Airport',160,34,8,'#fff');T('Free Wi-Fi',160,48,11,'#ffd36a');
 for(var a=0;a<3;a++){R('#ffd36a',150+a*4-8,70-a*6,16-a*8+8,2)}
 R('#e8e4d8',30,72,60,26);R('#9a947f',30,72,60,3);R('#14141a',52,62,16,10);R('#2a6a9a',54,64,12,6);
 R('#8a6a3a',230,84,60,8);R('#8a6a3a',236,92,4,8);R('#8a6a3a',280,92,4,8)};
BGS.rbus=function(){grad(0,70,'#06122e','#1a3358',10);for(var i=0;i<22;i++)R('#e8f0fa',(i*47)%VW,(i*31)%56,1,1);
 R('#2a4a6a',0,56,VW,14);for(var x=6;x<VW;x+=22){R('#17343a',x,48,6,14);R('#17343a',x+1,43,4,6);R('#eaf2fa',x+1,43,4,1)}
 R('#d8e4f2',0,70,VW,80);R('#c3d2e6',0,92,VW,2);R('#9ab0cc',0,118,VW,1);
 R('#3a4a5a',20,36,4,50);R('#e8f0fa',8,26,28,20);R('#143a5a',10,28,24,16);T('8',22,37,16,'#ffd36a');
 R('#f2c200',120,52,150,34);R('#1b2a55',120,74,150,12);R('#9fd0f0',130,58,22,12);R('#9fd0f0',158,58,22,12);R('#9fd0f0',186,58,22,12);R('#9fd0f0',214,58,22,12);
 T('AIRPORT EXPRESS',195,80,6.5,'#fff');R('#14141a',140,84,14,10);R('#14141a',236,84,14,10);R('#ffe9a8',264,66,6,6);
 R('#ffe9a8',20,86,2,2);rSnow(0,98)};
/* ---- 072: 滞在・夜・出発(コード描画。広場と郵便局の実画が読めないときの代わりも兼ねる)。文字は確認済みの名前だけ ---- */
function rOut(){grad(0,64,'#9fb8d8','#dfe9f4',10);R('#e8f0fa',0,64,VW,86);R('#d3deee',0,92,VW,1);R('#c3d2e6',0,118,VW,1)}
function rPine(x,y,h){R('#4a3626',x+2,y+h-4,2,4);for(var i=0;i<3;i++){var w=6+i*3;R('#1d4a3a',x+3-w/2,y+i*(h-6)/3,w,(h-6)/3+2);R('#eaf2fa',x+3-w/2,y+i*(h-6)/3,w,1)}}
function rLog(x,y,w,h,rc){R('#7a4a2a',x,y,w,h);for(var i=2;i<h;i+=4)R('#5e3820',x,y+i,w,1);R(rc||'#eaf2fa',x-1,y-3,w+2,4)}
BGS.rvil=function(){rOut();rPine(8,34,34);rPine(30,40,28);rPine(292,32,36);rPine(272,42,26);
 R('#9a2a2a',60,46,40,22);R('#eaf2fa',58,43,44,4);R('#ffd98a',70,54,6,6);R('#ffd98a',84,54,6,6);
 R('#b8a58a',124,16,22,56);R('#8a7a5a',124,16,22,3);R('#c0392b',120,10,30,8);R('#eaf2fa',120,8,30,3);R('#ffd98a',130,30,5,6);
 rLog(168,48,70,26);R('#ffd98a',180,56,6,6);R('#ffd98a',200,56,6,6);R('#2a1a10',218,58,8,16);
 R('#d8a53a',0,96,VW,3);R('#7a3b8a',0,120,VW,3);R('#e8f0fa',0,124,VW,26);R('#4a8ad0',0,108,VW,2);rSnow(0,98)};
BGS.rpost=function(){R('#6a4a2a',0,0,VW,98);for(var y=6;y<98;y+=8)R('#53381e',0,y,VW,1);R('#4a3626',0,0,VW,8);
 R('#33241a',150,22,70,50);R('#c9a03a',150,22,70,2);R('#ffd98a',160,34,20,24);R('#ffd36a',166,40,8,14);R('#e0561a',168,44,4,10);
 R('#8a6a3a',20,52,70,5);R('#8a6a3a',26,57,4,40);R('#8a6a3a',80,57,4,40);R('#e8e4d8',34,46,22,6);
 R('#2a1a10',270,30,34,40);R('#c0392b',270,30,34,4);R('#e8e4d8',278,40,18,12);
 R('#8a867e',0,98,VW,52);for(var x=0;x<VW;x+=24)R('#76726a',x,98,1,52);R('#f2c200',292,100,16,22);R('#c9a000',292,112,16,2);rSnow(0,0)};
BGS.rsanta=function(){R('#5a3a24',0,0,VW,98);for(var y=6;y<98;y+=8)R('#46301c',0,y,VW,1);R('#3a2616',0,0,VW,8);
 R('#143a30',120,18,80,40);R('#c9a03a',120,18,80,2);R('#c9a03a',120,56,80,2);for(var i=0;i<5;i++){R('#c0392b',130+i*14,30+(i%2)*4,6,6);R('#1d6a3a',134+i*14,28,3,3)}
 R('#2a1a10',10,24,26,50);R('#8a1020',14,28,18,40);R('#ffd36a',20,44,6,6);
 R('#7a4a2a',236,50,60,48);R('#9a6a3a',236,50,60,4);R('#c0392b',250,34,22,16);R('#eaf2fa',250,32,22,4);
 R('#8a6a3a',0,98,VW,52);for(var x=0;x<VW;x+=28)R('#76582c',x,98,1,52);R('#8a1020',100,112,120,30);R('#c9a03a',100,112,120,2)};
BGS.rrein=function(){rOut();rPine(14,28,40);rPine(40,36,30);rPine(284,30,40);rPine(262,38,30);
 R('#7a4a2a',96,60,6,38);R('#7a4a2a',124,60,6,38);R('#7a4a2a',152,60,6,38);R('#7a4a2a',96,64,110,3);R('#7a4a2a',96,76,110,3);R('#7a4a2a',200,60,6,38);
 R('#e8f0fa',0,96,VW,54);R('#d3deee',0,92,VW,1);R('#c3d2e6',0,118,VW,1);R('#c3d2e6',0,132,VW,1);
 /* トナカイ(静止のドット絵。素材がないため動かない。柵の向こう、ふたりと話し相手のあいだ) */
 var rx=128;R('#8a6a4a',rx,66,26,14);R('#eaf2fa',rx+2,64,22,3);R('#a98a66',rx+4,70,18,5);R('#6e5238',rx+3,80,3,14);R('#6e5238',rx+9,80,3,14);R('#6e5238',rx+17,80,3,14);R('#6e5238',rx+23,80,3,14);
 R('#8a6a4a',rx+24,58,7,12);R('#8a6a4a',rx+28,58,8,7);R('#14141a',rx+33,60,2,2);R('#c0392b',rx+35,63,2,2);
 R('#d9d4c6',rx+26,48,2,10);R('#d9d4c6',rx+22,48,5,2);R('#d9d4c6',rx+30,46,2,12);R('#d9d4c6',rx+30,46,6,2);R('#d9d4c6',rx+34,50,2,6);
 rSnow(0,98)};
BGS.rhotel=function(){R('#0b1a3a',0,0,VW,98);for(var i=0;i<30;i++)R('#e8f0fa',(i*43)%VW,2+(i*17)%52,1,1);R(Math.floor(t*2)%2?'#f4f8ff':'#cdd8ea',(t*3)%VW,10,1,1);
 R('#d8e4f2',0,60,VW,38);R('#9ab0cc',0,60,VW,2);for(var x=0;x<VW;x+=40){R('#17343a',x+6,48,6,14);R('#17343a',x+7,43,4,6)}
 R('#4a3626',0,0,VW,6);R('#33241a',0,6,VW,2);R('#2a1a10',2,10,8,88);R('#2a1a10',VW-10,10,8,88);R('#2a1a10',2,10,VW-4,3);R('#2a1a10',2,95,VW-4,3);R('#2a1a10',VW/2-1,10,3,88);
 R('#6a4a2a',0,98,VW,52);for(var x=0;x<VW;x+=24)R('#53381e',x,98,1,52);R('#8a1020',90,114,140,26);R('#c9a03a',90,114,140,2);
 R('#ffd98a',20,76,2,2);R('#ffd98a',290,76,2,2)};
function rHall(){R('#d2d8e2',0,0,VW,98);R('#c9d2e0',0,0,VW,5);R('#4a3626',0,5,VW,4);for(var x=10;x<VW;x+=46)R('#ffd98a',x,6,5,2);rFloor()}
BGS.rchk=function(){rHall();R('#8a867e',0,98,VW,52);
 for(var i=0;i<3;i++){var x=14+i*100;R('#e8e4d8',x,56,72,28);R('#9a947f',x,56,72,3);R('#143a5a',x+10,32,52,18);R('#6a8ab0',x+14,36,44,2);R('#6a8ab0',x+14,42,30,2);R('#2a2a33',x,84,72,14)}
 R('#2a2a33',0,98,VW,4);R('#4a4a56',0,102,VW,2)};
BGS.rsec=function(){rHall();
 R('#3a4a5a',20,50,90,40);R('#2a3a4a',20,50,90,4);R('#14141a',40,64,50,22);R('#9fd0f0',44,68,42,10);
 R('#8a8a96',130,70,170,5);for(var i=0;i<6;i++)R('#c9d2e0',140+i*26,64,20,6);R('#14141a',130,76,170,4);
 R('#5a7a9a',250,24,48,26);R('#cdd8e8',252,26,44,22);R('#2a6a4a',262,34,24,8)};
BGS.rshop=function(){rHall();
 R('#143a30',10,20,300,14);T('Napapiirin Lahja',160,27,9,'#ffd36a');
 R('#8a6a3a',10,50,60,6);R('#8a6a3a',14,56,4,42);R('#8a6a3a',62,56,4,42);R('#c0392b',18,40,8,10);R('#e8e4d8',32,42,8,8);R('#2f5bb0',46,40,8,10);R('#d9a441',58,43,8,7);
 R('#8a6a3a',250,50,60,6);R('#8a6a3a',254,56,4,42);R('#8a6a3a',302,56,4,42);R('#7a4a2a',258,38,10,12);R('#c0392b',274,42,8,8);R('#e8e4d8',288,40,8,10);
 R('#e8e4d8',104,64,8,34);R('#cdd8e8',104,64,8,3)};
BGS.rahk=function(){rHall();R('#143a30',90,16,140,14);T('Ahkio',160,23,9,'#ffd36a');
 R('#7a4a2a',20,48,70,50);R('#9a6a3a',20,48,70,4);R('#e8e4d8',30,38,12,10);R('#d9a441',54,40,10,8);R('#c0392b',72,38,10,10);
 for(var i=0;i<3;i++){var x=116+i*58;R('#8a6a3a',x,70,36,4);R('#6a4a2a',x+4,74,4,24);R('#6a4a2a',x+28,74,4,24);R('#e8e4d8',x+10,64,8,6);R('#d9a441',x+20,66,6,4)}
 R('#5a7a9a',240,26,60,34);R('#cdd8e8',242,28,56,30)};
BGS.rgate=function(){airWall('#d6dce8');R('#4a3626',0,5,VW,4);R('#8fb0d8',60,16,240,58);R('#dfe9f4',60,52,240,22);R('#c3d2e6',60,64,240,2);R('#3a4a5a',58,14,244,3);R('#3a4a5a',58,72,244,3);
 for(var x=0;x<VW;x+=60)R('#3a4a5a',60+x,14,3,60);for(var i=0;i<18;i++)R('#fff',60+(i*47)%240,16+((i*29+Math.floor(t*6))%52),1,1);
 R('#17343a',200,44,8,14);R('#17343a',201,38,6,8);R('#17343a',232,46,8,14);R('#17343a',233,40,6,8);
 floorAir('#9a96a4','#86828e');for(var k=0;k<3;k++){R('#5a6a8a',12+k*34,86,22,6);R('#5a6a8a',12+k*34,92,3,6);R('#5a6a8a',31+k*34,92,3,6)}};
"""
MAIN_RVN = r"""
/* ===== 世界一周編: ロヴァニエミ(到着まわり。タスク065) ===== */
var TOURDLG=%(dlg)s;
for(var _k in TOURDLG)DLG[_k]=TOURDLG[_k];
%(sp)s
%(bg)s
%(world)s
%(voice)s
%(ev)s
var PLACES_RARR=%(arr)s,PLACES_RSTAY=%(stay)s,PLACES_RDEP=%(dep)s;
PLACES_AIR=PLACES_RARR;   /* 世界マップのクリアの印: 到着の場所を全部(各1つ以上)あそんだら(072でも変えない。滞在・出発の印は今後の検討) */
PLACES_RARR.concat(PLACES_RSTAY,PLACES_RDEP).forEach(function(p){PBY[p.id]=p});
var TOUR_IDS=%(ids)s;
MODES={arr:{p:PLACES_RARR,b:'🛬 到着',h:'ロヴァニエミに到着<small>ロヴァニエミ空港</small>',snd:'rvn'},
 stay:{p:PLACES_RSTAY,b:'🎅 滞在',h:'ロヴァニエミの滞在<small>サンタクロース村とホテルの夜</small>',snd:'rvn'},
 dep:{p:PLACES_RDEP,b:'🛫 出発',h:'ロヴァニエミから出発<small>チェックインからゲートまで</small>',snd:'rvn'}};
worldAt('rovaniemi');
"""

# ---------- 窓口の地図(線を引く): 多角形から 92x16 の陸地ビットマップを作る ----------
def wmap_rows():
    polys = [
     [(-168,66),(-160,70),(-141,70),(-125,70),(-95,72),(-82,69),(-62,60),(-56,52),(-66,45),(-70,42),(-76,35),(-81,30),(-80,25),(-84,30),(-90,30),(-97,26),(-97,20),(-90,21),(-87,21),(-83,10),(-78,8),(-80,8),(-86,12),(-92,15),(-105,20),(-110,24),(-114,31),(-117,32),(-124,40),(-124,48),(-135,58),(-150,60),(-165,60)],
     [(-55,60),(-45,60),(-20,70),(-20,80),(-60,82),(-72,78),(-55,66)],
     [(-80,8),(-72,12),(-62,10),(-50,0),(-35,-6),(-39,-15),(-48,-26),(-58,-35),(-65,-42),(-68,-52),(-72,-54),(-75,-48),(-73,-38),(-71,-28),(-70,-18),(-77,-12),(-81,-5),(-80,2)],
     [(-10,36),(-9,43),(-1,46),(-4,48),(8,54),(10,58),(5,62),(15,69),(30,71),(45,68),(60,70),(80,73),(110,77),(140,72),(170,70),(180,67),(165,60),(155,58),(140,52),(135,43),(128,35),(122,40),(121,30),(110,20),(106,10),(100,2),(98,10),(95,16),(90,22),(80,15),(77,8),(72,20),(67,25),(57,25),(52,27),(57,22),(52,15),(43,12),(35,28),(34,31),(27,37),(36,36),(30,36),(26,40),(23,36),(20,40),(13,38),(8,44),(3,43),(-2,37)],
     [(-17,21),(-10,30),(-6,36),(10,37),(20,32),(32,31),(35,28),(43,12),(51,12),(40,-2),(40,-15),(35,-25),(27,-34),(18,-34),(12,-18),(9,-1),(9,4),(-8,4),(-17,14)],
     [(114,-22),(122,-18),(130,-12),(137,-12),(142,-11),(146,-19),(153,-26),(150,-37),(141,-38),(130,-32),(115,-34)],
     [(130,31),(135,34),(140,36),(142,40),(141,45),(145,44),(142,38),(139,34),(131,33)],
     [(-5,50),(2,51),(0,58),(-6,58)],
    ]
    def inside(x, y, poly):
        c = False; n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
        return c
    rows = []
    for r in range(16):
        lat = 75 - (r + .5) * 130 / 16
        row = ''
        for c in range(92):
            lon = -180 + (c + .5) * 360 / 92
            row += '#' if any(inside(lon, lat, pg) for pg in polys) else '.'
        rows.append(row)
    return rows
WINJS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'window.js'), encoding='utf-8').read().replace('/*WMAP*/[]', json.dumps(wmap_rows()))
WINCSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'window.css'), encoding='utf-8').read()
HERE = os.path.dirname(os.path.abspath(__file__))
def _rd(n): return open(os.path.join(HERE, n), encoding='utf-8').read()
TRIPJS = None  # trip.js は _rd のあとで読む
def relay_url():
    # 中継のURLはここ1か所(tour-src/relay-url.txt)。空なら Azure は使わない。環境変数 KANPE_RELAY_URL はヘッドレス確認用
    u = os.environ.get('KANPE_RELAY_URL')
    if u is None:
        u = ''
        for ln in _rd('relay-url.txt').splitlines():
            ln = ln.strip()
            if ln and not ln.startswith('#'): u = ln; break
    u = u.strip().rstrip('/')
    if u and not re.match(r'^https://[A-Za-z0-9._:-]+(/[A-Za-z0-9._~/-]*)?$', u): raise SystemExit('relay-url が https の URL ではありません: ' + u)
    return u
VOICEJS = _rd('voice.js').replace("/*RELAY_URL*/''", json.dumps(relay_url()))
VOICECSS = _rd('voice.css')
DIAGJS = _rd('diag.js')
SPW = "SP.desk_rtw={pitch:1.05,m:[[trav({hair:'long'}),P(2,{o:'#143fb0',p:'#2a2a33',h:'#241a14'})]]};\n"

def rep(s, a, b, cnt=1):
    n = s.count(a)
    if n != cnt: raise SystemExit('PATCH MISS (%d!=%d): %s' % (n, cnt, a[:60]))
    return s.replace(a, b)
SNOTE_OLD = '<p class="snote">音声は 保存も 送信も しません。発音の きろくは この端末の中だけに のこります。</p>'
SNOTE_NEW = ('<p class="snote">声は、ゲームでは 保存しません。マイクの声は ブラウザの音声認識が 文字にします(Chrome は Google、Safari は Apple の サーバーに 声が おくられます)。'
             '「こえを おくる」を ONに した ときだけ、旅の はじめと おわりの 宣言の 声が、発音を しらべる ために Microsoft Azure に おくられます。発音の きろくは この端末の中だけに のこります。</p>')

# 機内アナウンスで読んだ声(タスク048)は、その便のあいだだけ端末の中に置く。「保存しません」の一文を、その事実に合わせる(ナイロビ tour/ だけ。画面に「録音」などの言葉は出さない)
SNOTE_TOUR = SNOTE_NEW.replace('声は、ゲームでは 保存しません。', '声は、ゲームでは 保存しません(機内アナウンスで 読んだ声だけは、その便の あいだ、この端末の中に 置きます。外には 送らず、便が おわると 消えます)。')
assert SNOTE_TOUR != SNOTE_NEW
def trip_patches(o, page):
    """タスク030: 旅の骨組み(DAY・券の束・記録)を、場面のあと・場所の鍵・タブの鍵につなぐ"""
    tj = _rd('trip.js')
    o = rep(o, "function storeSave(){", tj + "\nTRIP.setPage('" + page + "');TRIP.hooks.say=function(t){try{setMsgInstant(t,'LULU')}catch(e){}};TRIP.hooks.at=function(){try{return G.at}catch(e){return null}};TRIP.hooks.sparta=function(){try{if(G.view==='map')startCamp()}catch(e){}};TRIP.hooks.ui=function(){try{var b=document.getElementById('boothBtn');if(b)b.hidden=TRIP.restToday()}catch(e){}};TRIP.hooks.mode=function(k){try{if((k==='stay'||k==='hret')&&typeof MODES!=='undefined'&&MODES.stay&&MODE!==k)setMode(k)}catch(e){}};   /* 058: 滞在の日(市場・サファリ)の朝の1枚を開いたら、「滞在」タブへ移る。ほかの日は今までどおり(タブは自分で選ぶ) */\nfunction storeSave(){")
    # 場面の昼夜は 旅の中の現地時刻(タスク032 / 020-3)。nightNow(音)と dohNight(ドーハの外の絵)の「いまの時」を TRIP.hourNow に通す。旅の外は本当の時計のまま
    o, n = re.subn(r"var h=\+new Intl\.DateTimeFormat\('en-GB',\{timeZone:'([A-Za-z/_]+)',hour:'2-digit',hourCycle:'h23'\}\)\.format\(new Date\(\)\);",
                   lambda m: "var h=TRIP.hourNow('" + m.group(1) + "');", o)
    if n != 1: raise SystemExit('PATCH MISS (hourNow %s: %d)' % (page, n))
    # 場面が終わったあと: 券・お金・夜の1枚(続きは コールバックで)
    o = rep(o, "storeSave();worldSync();\n if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}",
            "storeSave();worldSync();\n (window.__CHK?function(a,c){c()}:TRIP.afterScene)(S,function(){if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}")
    # 場所の鍵・タブの鍵
    o = rep(o, "function lockedPlace(id){if(MODE!=='arr'&&MODE!=='dep')return false;",
            "function lockedPlace(id){if(window.__CHK)return false;if(TRIP.lockedPlace(id))return true;if(MODE!=='arr'&&MODE!=='dep')return false;")
    o = rep(o, "b.dataset.m=k;b.addEventListener('click',function(){",
            "b.dataset.m=k;b.addEventListener('click',function(){if(G.view==='map'&&MODE!==k&&!window.__CHK&&TRIP.lockedMode(k)){try{Snd.jingle('buzz')}catch(e){}return}")
    # 休養日は 強化合宿の入口(マップのボタン・合宿の開始)を出さない(タスク032 / 020-7)。単語バトルは場面の中にあり、休養日は場所が全部閉じるので入口がない
    o = rep(o, "function refreshBoothBtn(){var n=boothCount();$m('boothBtn').textContent=",
            "function refreshBoothBtn(){var n=boothCount();$m('boothBtn').hidden=TRIP.restToday();$m('boothBtn').textContent=")
    o = rep(o, "function startCamp(){\n var fromMap=", "function startCamp(){\n if(TRIP.restToday())return;\n var fromMap=")
    # スパルタ時間(タスク032 / 020-8): 強化合宿(マップから入るもの)を終えたら、スパルタの日はその日が終わる。ふつうの日は何も起きない
    o = rep(o, "location.href='../guam/#w=1';return}showMap();return}\n G.camp={scene:G.scene,ti:G.ti,sp:speaker,lt:luTalk};G.sid++;clearTimers();G.view='scene';$m('sceneView').hidden=false;Snd.go(G.snd||null);campDone()}",
            "location.href='../guam/#w=1';return}showMap();if(!P.sample)TRIP.spartaDone(function(){});return}\n G.camp={scene:G.scene,ti:G.ti,sp:speaker,lt:luTalk};G.sid++;clearTimers();G.view='scene';$m('sceneView').hidden=false;Snd.go(G.snd||null);campDone()}")
    return o

def sub(pref): return dict((k, v) for k, v in dl.items() if k.startswith(pref))
KBASE = "K.fountain=K.hall;K.safari=K.ahlan;K.marina=K.s34;K.beach=K.costa;"
REC = "b.appendChild(s4);\n $m('setView').hidden=false;"
def record(label, memo=False):
    mm = ("var mq=memoLoad();if(mq.length)s5.appendChild(el('div','tt','つぎの たびの メモ：'+mq.join(', ')));" if memo else '')
    return ("b.appendChild(s4);voiceSetSection(b);\n var s5=sSec('ルルの カバンの きろくちょう');s5.appendChild(el('div','tt','えらんだ チケット：'+(save.ticket==='star'?'Star Alliance':save.ticket==='ow'?'oneworld':'まだ えらんでいない')));"
            "if(save.keep&&save.keep.hnd1)s5.appendChild(el('div','tt',(save.seen&&save.seen.hnd_return>0?'かえした':'ひろった')+' もの：ちいさな わすれもの'));var dn=0;TOUR_IDS.forEach(function(k){if(save.seen[k]>0)dn++});s5.appendChild(el('div','tt','" + label + "の かいわ：'+dn+' / '+TOUR_IDS.length));" + mm + "b.appendChild(s5);\n $m('setView').hidden=false;")
# ---- 場面の部品(ナイロビ・ドーハ共通) ----
# 分かれ目(opts)・相手の言い分け(by)・持ち越しの差しかえ(vr)・あとの一言(rep)・自動で始まる場面(auto)・単語バトルに入らない場面(win/ev)
SHARED = [
 ("if(n.n&&L[i+1]&&L[i+1].y){T.push({npc:n.n,npcJp:n.jp,cue:L[i+1].y,cueJp:L[i+1].jp});i+=2}",
  "if(n.n&&L[i+1]&&L[i+1].y!==undefined){var Y=L[i+1];T.push({npc:n.n,npcJp:n.jp,cue:Y.y,cueJp:Y.jp,by:n.by,vr:n.vr,cueBy:Y.cueBy,opts:Y.opts,diag:Y.diag,rep:Y.rep,route:n.route,fork:Y.fork,cards:Y.cards,dw:n.dw});i+=2}"),
 (" clearPanel();G.phase='npc';var S=G.scene,T=S.turns[G.ti];\n if(T.ctx)applyCtx(T.ctx);",
  " clearPanel();G.phase='npc';var S=G.scene,T=S.turns[G.ti];\n"
  " if(T.vr&&!T.vd){T.vd=1;for(var vi=0;vi<T.vr.length;vi++){var vv=T.vr[vi];if(window.__CHK||save.seen[vv.s]>0){T.npc=vv.n;T.npcJp=vv.jp;if(vv.y){T.cue=vv.y;T.cueJp=vv.yjp}break}}}\n"
  " var bv=T.by&&S.pick&&T.by[S.pick];if(bv){T.npc=bv.n;T.npcJp=bv.jp}var cv=T.cueBy&&S.pick&&T.cueBy[S.pick];if(cv){T.cue=cv.y;T.cueJp=cv.jp}\n"
  " if(T.route!=null){S.rf=S.rn||0;S.rn=T.route;S.rt=t}\n"
  " if(T.dw&&!T.dts)T.dts=Date.now();\n"
  " if(T.ctx)applyCtx(T.ctx);"),
 ("var T=G.scene.turns[G.ti],toks=parseCue(T.cue);clearInterval(G.typeTimer);msgText.textContent=npcHide()?'':T.npc;",
  "var T=G.scene.turns[G.ti];if(T.opts&&!T.pk){(T.cards?cardsOpts:T.fork?forkOpts:((G.scene.d.ev||typeof winOpts!=='function')?evOpts:winOpts))(T);return}var toks=parseCue(T.cue);clearInterval(G.typeTimer);msgText.textContent=npcHide()?'':T.npc;"),
 ("function advance(){\n",
  "function advance(){\n if(!G.camp){var D0=G.scene.turns[G.ti];if(D0&&D0.rep&&!D0.repd){D0.repd=1;G.phase='rep';npcMsg(D0.rep.n,D0.rep.who||whoNow());spSay=true;(paRep(G.scene,D0.rep)?paSay:say)(D0.rep.n,.95,G.scene.pitch,gd(function(){spSay=false;later(450,advance)}));return}\n"
  " if(D0&&D0.pay&&!D0.payd){D0.payd=1;payStart(D0.pay,advance);return}}\n"),
 ("G.phase='pass';G.tries=0;var th=", "G.phase='pass';G.tries=0;dreamPass();var th="),
 ("G.tries++;\n if(G.tries>=3){if(G.camp){G.phase='assist'", "G.tries++;\n if(dreamGiveUp())return;\n if(G.tries>=3){if(G.camp){G.phase='assist'"),
 ("setMsgInstant('Clear!  ぜんぶ いえた！',whoNow());later(2000,startWords)",
  "var W0=G.scene.d&&(G.scene.d.win||G.scene.d.ev||G.scene.d.conv);setMsgInstant(G.scene.d.dream?'Good night.':W0?'Clear!':'Clear!  ぜんぶ いえた！',whoNow());later(W0?1300:2000,G.scene.d.reveal?startReveal:W0?(typeof FT!=='undefined'&&G.scene.d.freetalk?FT.end:finishScene):startWords)"),
 ("if(!G.scene||G.phase==='idle'||G.phase==='words'||G.phase==='reveal'||G.phase==='inter'||G.phase==='hub')return;",
  "if(!G.scene||G.phase==='idle'||G.phase==='words'||G.phase==='reveal'||G.phase==='inter'||G.phase==='hub'||G.phase==='sample'||G.phase==='pay')return;"),
 # 英会話カフェの5分自由会話(タスク073): 自由会話の最中に ✕ を押したら、先生が「バイバイ」に返してから出る(それ以外は今までどおり、すぐ出る)
 ("$m('exitBtn').addEventListener('click',function(){showMap()});", "$m('exitBtn').addEventListener('click',function(){if(typeof FT!=='undefined'&&FT.exit())return;showMap()});"),
 # 新しい会話の流れ(タスク061): この場面(d.flow2)だけ、おてほんボタンを置かず、発音の数値・判定の文字を出さない。他の場面は今のまま
 ("row.appendChild(demo);\n demo.addEventListener('click',", "if(!f2()||blind)row.appendChild(demo);\n demo.addEventListener('click',"),
 ("stat.className='stat ok';stat.textContent=(res.okN===res.n?'Nice!  ':'')+(hideNum()?'':cnt);onPass();return}\n  stat.className='stat ng';stat.textContent=hideNum()?'':cnt+'  7割未満';onFail()}",
  "stat.className='stat ok';stat.textContent=f2()?'':(res.okN===res.n?'Nice!  ':'')+(hideNum()?'':cnt);onPass();return}\n  stat.className='stat ng';stat.textContent=f2()?'':hideNum()?'':cnt+'  7割未満';onFail()}"),
 ("stat.textContent='Too short';onFail()", "stat.textContent=f2()?'':'Too short';onFail()"),
 ("stat.textContent='Too long';onFail()", "stat.textContent=f2()?'':'Too long';onFail()"),
 ("stat.className='stat ok';stat.textContent='Nice!';onPass()}}", "stat.className='stat ok';stat.textContent=f2()?'':'Nice!';onPass()}}"),
 ("drawFront();if(A0&&A0.fg)A0.fg(p0,S0)}", "drawFront();payFg();if(A0&&A0.fg)A0.fg(p0,S0)}"),
 (" setMsgInstant(S.d.intro||S.pl.tip[0],'');$m('tapHint').textContent='';\n var b=el('button','btn go','GO！');",
  " setMsgInstant(S.d.intro||S.pl.tip[0],'');$m('tapHint').textContent='';\n if(S.d.auto){if(S.d.fx)evFx(S.d.fx);later(700,function(){playInter(-1,npcTurn)});return}\n var b=el('button','btn go','GO！');"),
]

EVJS = r"""
/* ===== 割りこみ・持ち越し・顔なじみ(タスク014 / 005案 A+B+F) =====
   save.ev = {fired:{枠:1}, streak, last}。「飽きのサイン」は未決定(決定005-3)。いまの仮の定義は EVC.sameN だけ。 */
var EVSLOTS=EVSLOTS_JSON;
var EVC={sameN:2};   /* 未決定: 同じ型の場面が何回つづいたら「飽き」とみなすか(仮に2) */
var EVQ=(location.search.match(/[?&]ev=(\\w+)/)||[])[1]||'';
function evS(){var e=save.ev;if(!e||typeof e!=='object')e=save.ev={};if(!e.fired||typeof e.fired!=='object')e.fired={};if(typeof e.streak!=='number')e.streak=0;if(typeof e.last!=='string')e.last='';return e}
function evFx(k){try{Snd.fx('ding')}catch(e){}}
function evNote(S){
 if(!S||!S.d||S.d.win||TRIP.restToday())return;var e=evS(),k=S.d.kind||'std';
 if(k==='ev'||k==='short'){e.streak=0;e.last=k}
 else if(k===e.last)e.streak++;else{e.last=k;e.streak=1}
 storeSave()}
function evBored(){if(TRIP.restToday())return false;return EVQ==='all'||evS().streak>=EVC.sameN}
function evGate(at,key,cont){
 if(EVQ==='off'||TRIP.restToday())return false;var e=evS();
 for(var i=0;i<EVSLOTS.length;i++){var x=EVSLOTS[i];
  if(x.at!==at||x.key!==key||e.fired[x.id]||!DLG[x.vid])continue;
  if(x.need&&!(save.seen[x.need]>0))continue;
  if(x.sign&&!evBored())continue;
  e.fired[x.id]=1;e.streak=0;e.last='ev';storeSave();
  var pl=PBY[key]||(G.scene&&G.scene.pl)||PBY[Object.keys(PBY)[0]];
  G.evCont=cont;startVid(pl,x.vid,'ev');return true}
 return false}
function evFinish(S){
 save.seen[S.vid]=(save.seen[S.vid]||0)+1;storeSave();
 var c=G.evCont;G.evCont=null;if(c)c();else showMap()}
function evOpts(T){
 G.phase='opts';clearPanel();clearInterval(G.typeTimer);msgText.textContent=npcHide()?'':T.npc;var S=G.scene,sid=G.sid;
 var box=el('div','dqbox'),bs=[];
 T.opts.forEach(function(o){var b=el('button','dq');b.type='button';b.appendChild(el('span','cur','▶'));b.appendChild(el('span','',cueText(o.y)));
  b.addEventListener('click',function(){evPick(T,o)});box.appendChild(b);bs.push(b)});
 panel.appendChild(box);
 function sel(i){bs.forEach(function(b,j){b.classList.toggle('sel',j===i)})}
 bs.forEach(function(b,i){['focus','pointerenter','pointerdown'].forEach(function(ev){b.addEventListener(ev,function(){sel(i)})})});
 sel(0);
 (function rd(i){if(G.sid!==sid||G.phase!=='opts'||i>=T.opts.length)return;sel(i);say(cueText(T.opts[i].y),.9,1,gd(function(){later(300,function(){if(G.phase==='opts')rd(i+1)})}))})(0)}
function evPick(T,o){
 if(G.phase!=='opts')return;stopSay();var S=G.scene;
 S.pick=o.k;T.pk=o.k;T.cue=o.y;T.cueJp=o.jp;if(o.rep)T.rep=o.rep;
 showCue()}
/* ===== 放送の読み上げ(タスク034): 機内アナウンス・空港の放送を、英語の声で流す =====
   対象: 場面の fx が 'pa' の相手の台詞 と、あとの一言(rep)のうち話す人が Announcement / Captain のもの。ふつうの会話は今までどおり say()。
   音の設定(kd_snd)がオフなら声は出さず、文だけ出して進む。声が使えない環境でも止まらない(say と同じ保険の時計)。
   マイクのダッキング(__ambDuck)には触らない: 放送のあいだ環境音はそのまま、声のほうが大きい。 */
var paEl=null;
function paMark(on){
 try{if(!paEl){paEl=el('span','pa','🔊');paEl.setAttribute('aria-hidden','true')}
  var w=$m('msg');if(on){if(paEl.parentNode!==w)w.appendChild(paEl)}else if(paEl.parentNode)paEl.parentNode.removeChild(paEl)}catch(e){}}
function paOn(){try{return localStorage.getItem('kd_snd')!=='off'}catch(e){return true}}
var PAT={nbo_gate2:[0]};   /* ふつうの5往復の中の放送の行(場面の番号→何番目の台詞か)。部屋全体への呼びかけ(キングの決定 2026-11-18) */
function paTurn(S,T){if(!S||!S.d||!T||T.by)return false;if(S.d.ev&&S.d.fx==='pa')return true;
 var a=PAT[S.vid],i=S.turns?S.turns.indexOf(T):-1;return !!(a&&i>=0&&a.indexOf(i)>=0)}
function paRep(S,r){return !!(S&&S.d&&S.d.ev&&r&&(r.who==='Announcement'||r.who==='Captain'))}
function paSay(text,rate,pitch,done){
 var my=++sayTok,fired=false;function fin(){paMark(0);if(fired||my!==sayTok)return;fired=true;if(done)done()}
 var ok=paOn()&&('speechSynthesis' in window)&&typeof SpeechSynthesisUtterance!=='undefined';
 if(!ok){setTimeout(fin,Math.min(text.length*26+900,4200));return}
 try{speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang='en-US';u.rate=(rate||.95)*.92*PREF.rate;u.pitch=pitch||1;u.volume=PREF.voice/100;
  u.onstart=function(){if(my===sayTok)paMark(1)};u.onend=fin;u.onerror=fin;speechSynthesis.speak(u)}catch(e){}
 setTimeout(fin,text.length*85+2200)}
"""
import conv_data
EVJS += _rd('conv.js').replace('DREAMBANK_JSON', json.dumps(dict((k, [v[0], v[1], window_data.star(v[2]), v[3]]) for k, v in conv_data.DREAM.items()), ensure_ascii=False)).replace('DREAMFB_JSON', json.dumps(conv_data.FALLBACK, ensure_ascii=False))
EVJS += _rd('cards.js')   # 新しい会話の流れ(タスク061): 日本語カード・見本の音声先出し・自動おてほん・支払いの演出
EVJS += _rd('freetalk.js')   # 英会話カフェの5分自由会話(タスク073): 誘い・聞き取り・中継 /chat・締め。使うのは場面データに freetalk=1 がある場面だけ
EVJS = EVJS.replace("||[])[1]||'';", "||[])[1]||(window.__CHK?'off':'');", 1).replace('EVSLOTS_JSON', json.dumps(event_data.SLOTS + doha_data.SLOTS, ensure_ascii=False)).replace('\\\\w', '\\w')

def ev_patches(o):
    o = rep(o, KBASE, KBASE + "K.dream={bpm:function(){return 64},amb:function(){loopNoise(400,.6,.015,.08,.01,'lowpass')},"
        "st:function(s,t,e){var N=[72,76,79,84,79,76,74,71];if(s%4===0)pluck(hz(N[(s>>2)%8]),t,e*3,.07);if(s%16===0)tone(hz(48),t,e*16,'sine',.05,.5)}};")
    o = rep(o, "if(s0&&s0.gold)save.gold=1;", "if(s0&&s0.gold)save.gold=1;if(s0&&s0.ev&&typeof s0.ev==='object')save.ev=s0.ev;"
        "if(s0&&s0.keep&&typeof s0.keep==='object'){var kp={};Object.keys(s0.keep).forEach(function(k){if(/^[a-z0-9_]{1,16}$/.test(k)&&s0.keep[k])kp[k]=1});save.keep=kp}")
    o = rep(o, "sign:d.sign,tv:d.tv};", "sign:d.sign,tv:d.tv,lvis:d.lvis};")
    o = rep(o, "OUT.gold=ctx.gold?1:0;OUT.hvis=1;OUT.lvis=1;", "OUT.gold=ctx.gold?1:0;OUT.hvis=1;OUT.lvis=ctx.lvis===0?0:1;")
    o = rep(o, "function finishScene(){\n var S=G.scene;",
            "function finishScene(){\n var S=G.scene;if(S.d&&S.d.ev){evFinish(S);return}"
            "if(!S.evd){S.evd=1;evNote(S);if(evGate('after',S.pl.id,function(){G.scene=S;finishScene()}))return}")
    # ---- 放送の読み上げ(タスク034) ----
    o = rep(o, " say(T.npc,.95,S.pitch,gd(function(){spSay=false;if(G.phase==='npc')later(250,showCue)}))}",
            " (paTurn(S,T)?paSay:say)(T.npc,.95,S.pitch,gd(function(){spSay=false;if(G.phase==='npc')later(250,showCue)}))}")
    o = rep(o, "if(T){spSay=true;say(T.npc,.95,G.scene.pitch,gd(function(){spSay=false}))}",
            "if(T){spSay=true;(paTurn(G.scene,T)?paSay:say)(T.npc,.95,G.scene.pitch,gd(function(){spSay=false}))}")
    o = rep(o, "function stopSay(){sayTok++;try{speechSynthesis.cancel()}catch(e){}}", "function stopSay(){sayTok++;paMark(0);try{speechSynthesis.cancel()}catch(e){}}")
    o = rep(o, ".win .tag{position:absolute;", ".win .pa{position:absolute;top:-12px;right:12px;border-radius:4px;padding:0 8px;font-size:12px;font-weight:800;border:2px solid var(--line);background:var(--win);animation:paBlink 1s steps(2) infinite}@keyframes paBlink{50%{opacity:.35}}\n.win .tag{position:absolute;")
    o = rep(o, "function enterPlace(id){var pl=PBY[id];", "function enterPlace(id){var pl=PBY[id];if(evGate('enter',id,function(){enterPlace(id)}))return;")
    o = rep(o, "function startVid(pl,vid,from){\n", "function startVid(pl,vid,from){\n if(from!=='ev'&&evGate('vid',vid,function(){startVid(pl,vid,from)}))return;\n")
    return o

def common(o, tz):
    o = rep(o, "timeZone:'Asia/Dubai'", "timeZone:'%s'" % tz)
    o = rep(o, "SAVEKEY='kanpe-dubai-save-v2'", "SAVEKEY='kanpe-tour-save-v1'")
    o = rep(o, "if(s0&&s0.gold)save.gold=1;", "if(s0&&s0.gold)save.gold=1;if(s0&&(s0.ticket==='star'||s0.ticket==='ow'))save.ticket=s0.ticket;")
    # ---- 場面の絵は枠なし・フルブリード(タスク028): 画面の横と上にぴったり。会話欄とカンペは下のまま ----
    o = rep(o, '<canvas id="scene" width="320" height="150" aria-label="場面"></canvas>',
            '<canvas id="scene" width="320" height="150" aria-label="場面"></canvas>\n      <canvas id="sceneA" width="1536" height="960" aria-hidden="true" hidden></canvas>')
    o = rep(o, "#scene{display:block;width:100%;aspect-ratio:320/150;image-rendering:pixelated;border:3px solid var(--line);border-radius:6px;background:#222}", FULLBLEED_CSS)
    # ---- 場面の環境音の口(対応表は art.js)。ミュート・マイク中の停止は今ある音の設定に合わせる ----
    o = rep(o, " function go(kind){want=kind||null;if(!AC)return;", " function go(kind){want=kind||null;if(window.__ambGo)window.__ambGo(want);if(!AC)return;")
    o = rep(o, "  if(!AC)return;clearTimeout(duckT);", "  if(window.__ambDuck)window.__ambDuck(flag);if(!AC)return;clearTimeout(duckT);")
    o = rep(o, "try{localStorage.setItem('kd_snd',v?'on':'off')}catch(e){}if(v){", "try{localStorage.setItem('kd_snd',v?'on':'off')}catch(e){}if(window.__ambSync)setTimeout(window.__ambSync,0);if(v){")
    o = rep(o, " var S=G.scene;\n if(d.story){S.turns.forEach(", " var S=G.scene;if(window.__ambScene)window.__ambScene(G.snd,d.bg);\n if(d.story){S.turns.forEach(")
    # ---- 新しい絵の場面を描く(art.js)。新しい絵でなければ今までの描き方 ----
    o = rep(o, "  if(A0&&A0.tick)A0.tick(p0,S0);\n  if(A0&&A0.bg)A0.bg(p0,S0);else",
            "  if(A0&&A0.tick)A0.tick(p0,S0);\n  if(typeof ARTframe==='function'&&ARTframe(S0,A0,dt)){requestAnimationFrame(frame);return}\n  if(A0&&A0.bg)A0.bg(p0,S0);else")
    return o
FULLBLEED_CSS = (
 ".stage{margin:calc(-8px - env(safe-area-inset-top,0px)) calc(-1*max(16px,env(safe-area-inset-right,0px))) 0 calc(-1*max(16px,env(safe-area-inset-left,0px)))}\n"
 "@media (min-width:512px){.stage{margin-left:0;margin-right:0}}\n"
 "#scene,#sceneA{display:block;width:100%;border:0;border-radius:0;background:#222}\n"
 "#scene{aspect-ratio:320/150;image-rendering:pixelated}#sceneA{aspect-ratio:1536/960}\n"
 "#sceneView .stage #exitBtn,#sceneView .stage #tip,#sceneView .stage .setbtn{top:calc(6px + env(safe-area-inset-top,0px))}")
def song_js():
    sc = dict(song_data.SONG_SCENE); sc['listen'] = 1; sc['lobby'] = song_data.LOBBY_HUB['lines']
    rm = dict(song_data.ROOM_SCENE); rm['rest'] = 1   # ホテルの部屋(タスク051)
    pool = dict(song_data.POOL_SCENE); bar = dict(song_data.BAR_SCENE)   # タスク077: プール(実在)・バー(枠組みのみ。有効化は BAR_READY の1か所)
    sc['barReady'] = 1 if song_data.BAR_READY else 0
    return _rd('song.js').replace('/*SONGDATA*/null', J(sc)).replace('/*ROOMDATA*/null', J(rm)).replace('/*POOLDATA*/null', J(pool)).replace('/*BARDATA*/null', J(bar))
def pa_js():   # CAアナウンス・イベント(タスク048): ナイロビ(tour/)だけ。声は端末の中だけ(外へ送るコードなし)
    return _rd('pa.js').replace('/*PADATA*/null', J(dict((k, {'chunks': pa_data.chunks(k), 'text': pa_data.text(k)}) for k in pa_data.VARIANTS)))
def chant_js(base): return _rd('chant.js').replace('/*CHANTBASE*/', base)   # タイトルのチャント(タスク050): world/(開始・ループ)と tour/(続きから)に同じものを入れる
def art_js(base, sel): return _rd('art.js').replace("/*ARTBASE*/", base).replace("/*ARTSEL*/", sel)

# ---------- ナイロビ(tour/index.html) ----------
dn = dict(sub('sage_')); dn.update(sub('ticket_')); dn.update(sub('win_')); dn.update(sub('nbo_')); dn.update(sub('hnd_')); dn.update(sub('camp_'))
main = MAIN % dict(dlg=J(dn), sp=SPJS + SPW, bg=BGJS + BGN, world=WORLDJS, voice=VOICEJS, diag=DIAGJS, ev=EVJS, win=WINJS, sage=J(SAGE), arr=J(ARR), stay=J(STAY), air=J(AIR), dep=J(NDEP), hdep=J(HDEP), hret=J(HRET), eikai=J(EIKAI), camp=J(CAMP), ids=J(TOUR_IDS))
main += _rd('check.js').replace('__OTHER_HREF__', 'doha/?check=1').replace('__OTHER_LABEL__', 'ドーハ')
main += art_js('assets/art/', "function artIdFor(S){var g=S&&S.d&&S.d.bg,h=S&&S.hub&&S.ctx&&S.ctx.bg,v=String(S&&S.vid||''),k=/2$/.test(v)?'2':'1';if(/^nbo_/.test(v)){if(g==='checkinQ')return'ncheckin'+k;if(g==='security')return'nsec'+k;if(g==='duty')return'nduty'+k;if(g==='lounge')return'nlounge'+k;if(g==='gate')return'ngate'+k;if(g==='cabinQ')return'cabinQ';if(g==='javaK')return'javaK';if(g==='artK')return'artK'}if(/^hnd_/.test(v)){if(g==='checkinT')return'hcheckin_st';if(g==='checkinQ')return'hcheckin_ow';if(g==='security')return'hsec';if(g==='immigH')return'hexit';if(/^hnd_plane_/.test(v)){if(g==='cabinQ')return'hcabin_ow';if(g==='cabinT')return'hcabin_st'}}if(/^doh_/.test(v)&&g==='dimmig')return v==='doh_immig2'?'dimmig2':'dimmig';if(/^hnd_ev_ca_/.test(v))return 'cabinseat';if(/^hnd_ev_meal_/.test(v))return 'cabinmeal';if(g==='eikaiK')return'eikai';if(g==='campK')return'camp';return g==='npool'?'npool':g==='npoolq'?'npoolq':g==='nbar'?'nbar':(h==='nlobby'||g==='nlobby')?'nlobby':g==='nsong'?'nsong':g==='safariK'?'nsafari':g==='marketK'?'nmarket':g==='nroom'?'nroom':g==='sim'?'simshop':(g==='sage'||h==='sage')?'sage':((g==='tdesk'||g==='rtmap')?'ticket':(g==='taxi'?'nairobi':(g==='immig'?'immig':(g==='baggage'?'bagclaim':(g==='hgateOW'?'hgate_ow':(g==='hgateST'?'hgate_st':null))))))}")   # 羽田の出発(タスク067): vid が hnd_ のとき bg checkinQ→hcheckin_ow・security→hsec・immigH→hexit、機内の会話(hnd_plane_)は cabinQ→hcabin_ow・cabinT→hcabin_st(hnd_ev_ca_/hnd_ev_meal_ の cabinseat・cabinmeal は従来どおり)。本編側だけ。# ナイロビ出発まわり(タスク054: bg が checkinQ/security/duty/lounge/gate で vid が nbo_ のとき。羽田・ドーハの同名の bg は対象外。末尾の 2 で2つ目の配置)・羽田の出発ゲート(タスク043。券で絵が出し分け)・賢者の広間(sage_1〜3の会話・賢者のメニュー)・チケット売り場(窓口の全場面 ticket_*・win_*。bg が tdesk か rtmap。タスク041)・ナイロビ到着(タクシー乗り場)・入国審査・手荷物受け取り(bg が baggage。ナイロビだけ。タスク045)
main += _rd('camp.js').replace('/*CAMPDATA*/null', J(camp_data.payload()))   # タスク078: 合宿デモ(ナイロビ tour/ だけ)
main += chant_js('assets/song/') + song_js() + pa_js()   # 宣言文ソング(タスク049): テーマ(ホテルのロビーの歌手イベント)。チャントはタイトルの曲(タスク050)で再生は chant.js だけ。ナイロビ(tour/)だけ
o = ev_patches(common(src, 'Africa/Nairobi'))
o = rep(o, "(S.d.inter||[]).forEach(function(n){if(n.set&&n.set.gold)save.gold=1});storeSave();worldSync();",
        "(S.d.inter||[]).forEach(function(n){if(n.set&&n.set.gold)save.gold=1});if(S.d.keep&&/^[a-z0-9_]{1,16}$/.test(S.d.keep)){if(!save.keep||typeof save.keep!=='object')save.keep={};save.keep[S.d.keep]=1}storeSave();worldSync();")
# ---- 窓口フロー(タスク012)のためのエンジン側の追加。ナイロビ(tour)だけに入れる。ドバイ・ドーハは変えない ----
o = rep(o, "if(s0&&(s0.ticket==='star'||s0.ticket==='ow'))save.ticket=s0.ticket;",
        "if(s0&&(s0.ticket==='star'||s0.ticket==='ow'))save.ticket=s0.ticket;if(s0&&s0.win&&typeof s0.win==='object')save.win=s0.win;")
# 数字: 100万円台(1,074,300)と「5th」を言葉に直す(これまでは999まで)
o = rep(o, " if(n<1000)return [ONES[Math.floor(n/100)],'hundred'].concat(n%100?numWords(n%100):[]);return null}",
        " if(n<1000)return [ONES[Math.floor(n/100)],'hundred'].concat(n%100?numWords(n%100):[]);\n"
        " if(n<1e6)return numWords(Math.floor(n/1000)).concat(['thousand'],n%1000?numWords(n%1000):[]);\n"
        " if(n<1e9)return numWords(Math.floor(n/1e6)).concat(['million'],n%1e6?numWords(n%1e6):[]);return null}")
o = rep(o, "  if(/^[0-9]+$/.test(p)){var nw=numWords(parseInt(p,10));",
        "  var om=/^([0-9]+)(st|nd|rd|th)$/.exec(p);if(om&&ORD[+om[1]]){out=out.concat(ORD[+om[1]].split(' '));return}\n"
        "  if(/^[0-9]+$/.test(p)){var nw=numWords(parseInt(p,10));")
for _a, _b in SHARED: o = rep(o, _a, _b)   # 場面の部品(窓口・割りこみ・持ち越しで共有。ドーハ版にも同じものを入れる)
o = rep(o, "card=el('div','cue'+(blind?' blind':''));", "card=el('div','cue'+(blind?' blind':'')+(T.diag?' diag':''));")
o = rep(o, " if(!G.camp)addHelp(T)}", " if(!G.camp&&!T.diag&&!G.scene.d.nohelp)addHelp(T)}")
o = rep(o, " G.mute=null;var card=spans.length?spans[0].parentNode:null;",
        " G.mute=null;var card=spans.length?spans[0].parentNode:null;\n if(T.diag&&!PREF.silent&&card){var AZ=(T.diag==='decl'||T.diag==='decl_end'||T.diag==='readback')&&voiceAzureOn();if(AZ||SR){(AZ?setupDiagAz:setupDiag)(act,stat,toks,spans,T,card);return}}")
# 長いカンペは、ブザーも合格音もなく、いつも先へ進む
o = rep(o, "function onFail(){\n Snd.jingle('buzz');", "function onFail(){\n var Td=G.scene&&G.scene.turns[G.ti];if(Td&&Td.diag){diagDone();return}\n Snd.jingle('buzz');")
o = rep(o, "function onPass(){\n Snd.jingle('pass');", "function onPass(){\n var Td=G.scene&&G.scene.turns[G.ti];if(Td&&Td.diag){diagDone();return}\n Snd.jingle('pass');")
o = rep(o, "function finishScene(){\n var S=G.scene;",
        "function finishScene(){\n var S=G.scene;if(S.d&&S.d.win){save.seen[S.vid]=(save.seen[S.vid]||0)+1;storeSave();winAfter(S);return}")
o = rep(o, "function startScene(){\n clearPanel();var S=G.scene;", "function startScene(){\n clearPanel();var S=G.scene;if(S.d.hook==='consent'){consentScene(S);return}")
o = rep(o, "if(evGate('enter',id,function(){enterPlace(id)}))return;if(pl.hub){enterHub(pl);return}",
        "if(evGate('enter',id,function(){enterPlace(id)}))return;if(pl.win&&!save.ticket){winStart();return}if(pl.hub){enterHub(pl);return}")
o = rep(o, ".cue .heard.live{color:#8a7b55}", ".cue .heard.live{color:#8a7b55}\n" + WINCSS + VOICECSS)
o = rep(o, '<title>カンペ先生 ドバイ編</title>', '<title>空港えいご物語 世界一周編 ナイロビ</title>')
o = rep(o, SNOTE_OLD, SNOTE_NEW)
o = rep(o, "worldMark('dubai')", "worldMark('nairobi')")
o = rep(o, "function runStory(vid){startVid(G.scene.pl,vid,'hub')}",
        "function runStory(vid){if(vid==='ticket_star'||vid==='ticket_ow'){save.ticket=vid==='ticket_star'?'star':'ow';storeSave()}startVid(G.scene.pl,vid,'hub')}")
# 場面のあと: 窓口→到着 / 搭乗ゲート→出発(機内の前) / 機内→世界マップの飛ぶ画面→ドーハ
o = rep(o, "if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}showMap()}",
        "if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}"
        "if(S.pl.id==='qplane'){worldAt('nairobi');Snd.go(null);location.href=window.__CHK?'doha/?check=1':'../world/?fly=doha';return}"
        "if(S.pl.id==='hplane'){worldAt('haneda');Snd.go(null);location.href=window.__CHK?'./?check=1':'../world/?fly=nairobi';return}"
        "if(S.pl.id==='ticket'&&save.ticket){setMode('hdep');showMap();return}showMap();"
        "}")
o = rep(o, KBASE, KBASE + "K.sage=K.hall;K.tdesk=K.info;"
        "K.nbo={bpm:function(){return 84},amb:function(){loopNoise(500,.7,.02,.1,.01,'lowpass')},"
        "st:function(s,t,e){var KN=[64,67,69,72,69,67,64,62];if(s%2===0)pluck(hz(KN[(s>>1)%8]),t,e*2.2,ngt?.08:.12);"
        "if(s%8===4)pluck(hz(KN[0]-12),t,e*3,.09);if(s%16===0)tone(hz(40),t,e*16,'sine',.07,.5)}};")
o = rep(o, "if(G.view==='map'&&MODE!==k)setMode(k)",
        "if(G.view==='map'&&MODE!==k){if(k!=='sage'&&!save.ticket&&!window.__CHK){setMode('sage');G.at='ticket';placeWalkers('ticket',true);return}setMode(k)}")
o = rep(o, REC, record('ナイロビ', True))
o = trip_patches(o, 'tour')
o = rep(o, "if(MODE!=='arr'&&MODE!=='dep')return false;", "if(MODE!=='arr'&&MODE!=='dep'&&MODE!=='hdep')return false;")   # 羽田の出発も、上から順に開く
o = rep(o, "setMode('hdep');showMap();return}showMap();", "setMode('hdep');showMap();return}showMap();})")
o = rep(o, "function refreshMap(){\n", "/* 券ごとに場面が分かれる場所は、いまの券の場面だけを数える */\nfunction vv(p){return (p.tkv&&p.tkv[save.ticket])||p.v}\nfunction refreshMap(){\n")
o = rep(o, "TOTALV=PLACES.reduce(function(a,p){return a+p.v.length},0)", "TOTALV=PLACES.reduce(function(a,p){return a+vv(p).length},0)", 2)
o = rep(o, "p.v.forEach(function(){dd.appendChild(el('i'))})", "vv(p).forEach(function(){dd.appendChild(el('i'))})")
o = rep(o, "p.v.forEach(function(v,i){var on=(save.seen[v]||0)>0;dots[i].classList.toggle('on',on);if(on)c0++});n.classList.toggle('done',c0===p.v.length)",
        "var vs=vv(p);vs.forEach(function(v,i){var on=(save.seen[v]||0)>0;if(dots[i])dots[i].classList.toggle('on',on);if(on)c0++});n.classList.toggle('done',c0===vs.length)")
o = rep(o, "PLACES.forEach(function(p){p.v.forEach(function(v){if(save.seen[v])d++})});for(var i=0;i<TOTALV", "PLACES.forEach(function(p){vv(p).forEach(function(v){if(save.seen[v])d++})});for(var i=0;i<TOTALV")
o = rep(o, "function pickV(pl){\n var ids=pl.v,min=1e9;", "function pickV(pl){\n var ids=(pl.tkv&&pl.tkv[save.ticket])||pl.v,min=1e9;")
# 羽田の出発のタブ: 券を買って、まだ羽田にいるあいだだけ出す。最初の画面も、そのあいだは羽田の出発
# 券を買ったあとは 賢者のタブを出さない(賢者と窓口は 出発前の場面)
o = rep(o, "b.classList.toggle('on',b.dataset.m===MODE)});", "b.classList.toggle('on',b.dataset.m===MODE);if(b.dataset.m==='sage')b.hidden=!!save.ticket&&!window.__CHK;if(b.dataset.m==='hdep')b.hidden=!hdepOn()&&!window.__CHK;if(b.dataset.m==='hret')b.hidden=!hretOn()&&!window.__CHK;if(b.dataset.m==='eikai')b.hidden=!window.__CHK;if(b.dataset.m==='camp')b.hidden=!window.__CHK});")
o = rep(o, "dep:['#e9e2f2','#d9d0e8','#8a7ac0']}[MODE]", "dep:['#e9e2f2','#d9d0e8','#8a7ac0'],sage:['#e4dff2','#d3cbe8','#8a7ac0'],hdep:['#dfe6f2','#cdd7ea','#8a98c0'],hret:['#dfe6f2','#cdd7ea','#8a98c0'],stay:['#efe4c4','#e2d3a6','#c9a05a'],eikai:['#efe4c4','#e2d3a6','#c9a05a'],camp:['#efe4c4','#e2d3a6','#c9a05a']}[MODE]")   # 058: 滞在タブの地図の色(明るい砂色。暗くしない)
o = rep(o, "g.fillStyle='#143fb0';g.fillRect(0,0,5,ch);g.fillRect(cw-5,0,5,ch)", "g.fillStyle='#2f7a4a';g.fillRect(0,0,5,ch);g.fillRect(cw-5,0,5,ch)")
# タスク055: 賢者モードのマップだけ実画の背景(sage-map-bg-v1.png 960×1536)。要素いっぱいに引き伸ばす(100%×100%。cover は使わない=ノード位置とカームゾーンがずれるため)。他モードの描画は変えない。読めないときは今までの描画
o = rep(o, "function drawMapBg(){\n var cv2=", "function sageMapBg(cv){var im=window.__SMI;if(!im){im=window.__SMI=new Image();im.onerror=function(){im.bad=1};im.onload=function(){if(G.view==='map'&&MODE==='sage')drawMapBg()};im.src=ARTBASE+'sage-map-bg-v1.png'}if(im.bad||!im.complete||!im.naturalWidth)return false;cv.style.background=\"url('\"+ARTBASE+\"sage-map-bg-v1.png') 0 0/100% 100% no-repeat\";return true}\nfunction drawMapBg(){\n var cv2=")
o = rep(o, "cv2.width=cw;cv2.height=ch;var g=cv2.getContext('2d');\n", "cv2.width=cw;cv2.height=ch;var g=cv2.getContext('2d');\n if(MODE==='sage'&&sageMapBg(cv2))return;cv2.style.background='';\n")
# タスク055: ノードの余白。カード=内側に8px(アイコンが枠に触れない)、札=縦に余白(下を厚め)
o = rep(o, ".node{position:absolute;width:66px;height:66px;margin:-33px 0 0 -33px;padding:0;", ".node{position:absolute;width:66px;height:66px;margin:-33px 0 0 -33px;padding:8px;")
o = rep(o, "border:2px solid var(--brown);border-radius:6px;padding:0 6px}", "border:2px solid var(--brown);border-radius:6px;padding:4px 10px 6px;line-height:14px}")
o = rep(o, "#map.dense .node .nm{top:51px;font-size:10px;padding:0 4px}", "#map.dense .node .nm{top:51px;font-size:10px;padding:3px 8px 5px;line-height:13px}")
# 札が縦に伸びた分、進捗ドットを札の下(5px あけて)へ。札は行の高さを固定(14px/dense 13px)して、フォントで高さが変わらないようにする
o = rep(o, ".node .dots{position:absolute;bottom:-14px;", ".node .dots{position:absolute;top:103px;")
o = rep(o, "#map.dense .node .dots{bottom:-12px}", "#map.dense .node .dots{top:81px}")
o_pre = o   # 終わりの場面の土台(エンジンの部品はナイロビと同じ)
# ---- 宣言文ソング(タスク049): ナイロビ(tour/)だけ。終わりの場面・ドーハには入れない ----
# 場所に入る: ホテルのロビー(listen)は「聴くだけ」の場面へ(出来事の割りこみ・発音の流れは通らない)
o = rep(o, "function runStory(vid){", "function runStory(vid){if(window.__lobbyPick&&window.__lobbyPick(vid))return;")   # タスク066: ロビーの案内の3択(ショータイム・プール・Balcony Bar)
o = rep(o, "function enterPlace(id){var pl=PBY[id];if(evGate(", "function enterPlace(id){var pl=PBY[id];if(pl.listen){songListen(pl);return}if(pl.rest){roomRest(pl);return}if(evGate(")
# 場所を上から順に開く決まり: 場面の数が空の場所(ホテルのロビー・ホテルの部屋。任意)は「遊んだか」の数に入れず、飛ばして次の場所を開く(タスク051)
o = rep(o, "if(!PLACES[k].v.some(function(v){return save.seen[v]>0}))return true}return false}", "if(PLACES[k].v.length&&!PLACES[k].v.some(function(v){return save.seen[v]>0}))return true}return false}")
# オープニングのチャント: 賢者の広間の最初の会話の「GO！」(最初の操作)を押したあとに鳴らす
o = rep(o, "b.addEventListener('click',function(){if(S.d.story)playInter(-1,npcTurn);else npcTurn()})}", "b.addEventListener('click',function(){if(window.__songGo)window.__songGo(S);if(S.d.story)playInter(-1,npcTurn);else npcTurn()})}")
# 場面が変わったら、曲を鳴らしてよい場面にいるかを確かめる(離れたらすぐ止める)
o = rep(o, "function clearTimers(){G.timers.forEach(clearTimeout);G.timers=[];clearInterval(G.typeTimer)}", "function clearTimers(){G.timers.forEach(clearTimeout);G.timers=[];clearInterval(G.typeTimer);if(window.__songWatch)setTimeout(window.__songWatch,0)}")
# 場面の数が空の場所(ホテルのロビー)に「済」の印を出さない
o = rep(o, "n.classList.toggle('done',c0===vs.length)", "n.classList.toggle('done',vs.length>0&&c0===vs.length)")
# 記録(kanpe-tour-save-v1)がない初回だけ: マップでなく 賢者の広間に入り、賢者の最初の会話(sage_1)を開く(タスク022)
o = rep(o, "function storeSave(){", "var TOUR_FRESH=(function(){try{return localStorage.getItem(SAVEKEY)===null}catch(e){return false}})();\nfunction storeSave(){")
# ---- CAアナウンス・イベント(タスク048): ナイロビ(tour/)だけ ----
# 設定の注意書き(声の扱い)と、マイク画面のカンペの見た目。終わりの場面(o_pre のあと)には入れない
o = rep(o, SNOTE_NEW, SNOTE_TOUR)
o = rep(o, ".cue .heard.live{color:#8a7b55}", ".cue .heard.live{color:#8a7b55}\n" + _rd('pa.css') + _rd('cards.css') + _rd('freetalk.css') + _rd('camp.css'))
# ---- 合宿デモ(タスク078): camp_demo1(d.camp78)の時だけ効く差しこみ。ほかの場面は今のまま ----
o = rep(o, "function startScene(){\n clearPanel();var S=G.scene;if(S.d.hook==='consent'){consentScene(S);return}", "function startScene(){\n clearPanel();var S=G.scene;if(S.d.camp78){gsReady();return}if(S.d.hook==='consent'){consentScene(S);return}")
o = rep(o, "function advance(){\n", "function advance(){\n if(G.scene&&G.scene.d&&G.scene.d.camp78){gsAfter();return}\n")
o = rep(o, "function onPass(){\n var Td=G.scene&&G.scene.turns[G.ti];if(Td&&Td.diag){diagDone();return}\n", "function onPass(){\n if(G.scene&&G.scene.d&&G.scene.d.camp78){gsRecDrop();Snd.jingle('pass');G.phase='pass';G.tries=0;later(450,advance);return}\n var Td=G.scene&&G.scene.turns[G.ti];if(Td&&Td.diag){diagDone();return}\n")
o = rep(o, "function onFail(){\n", "function onFail(){\n if(G.scene&&G.scene.d&&G.scene.d.camp78){gsFail();return}\n")   # 083: 合宿の失敗は専用の流れ(自分の声→お手本→言い直し)
o = rep(o, "try{Snd.duck(1);r.start();listening=true;", "try{Snd.duck(1);if(G.scene&&G.scene.d&&G.scene.d.camp78)gsRecOn();r.start();listening=true;")   # 083: 聞き取りと同時に、自分の声を端末のメモリにだけ録る
o = rep(o, "function npcHide(){if(!(PREF.mode>=1)||G.camp||!G.scene)return false;", "function npcHide(){if(!(PREF.mode>=1)||G.camp||!G.scene||(G.scene.d&&G.scene.d.camp78))return false;")
o = rep(o, "function cueBlind(T){return PREF.mode===2&&!G.camp&&", "function cueBlind(T){return PREF.mode===2&&!G.camp&&!(G.scene&&G.scene.d&&G.scene.d.camp78)&&")
o = rep(o, "function showMap(){\n G.view='map';", "function showMap(){\n if(typeof gsOff==='function')gsOff();\n G.view='map';")
# 羽田の機内の会話が終わったとき、ほかの出来事より先に差しこむ(最初の長距離便で1回)
o = rep(o, "if(evGate('after',S.pl.id,function(){G.scene=S;finishScene()}))return}",
        "if(window.PA&&PA.gate(S,function(){G.scene=S;finishScene()}))return;if(evGate('after',S.pl.id,function(){G.scene=S;finishScene()}))return}")
# 食事の場面(pre='own')は、最初の台詞の前に チャイム→自分の声の放送 を流す
o = rep(o, "later(700,function(){playInter(-1,npcTurn)});return}", "var go0=function(){playInter(-1,npcTurn)};if(S.d.pre==='own'&&window.PA)PA.pre(S,go0);else later(700,go0);return}")
# 機内のチャイム(自作の3音。搭乗案内と同じ音)
o = rep(o, "else if(k==='sparkle'){tone(1568", "else if(k==='pachime'){chime(t0,.08)}else if(k==='sparkle'){tone(1568")
# 便が終わる(ナイロビへ・ドーハへ飛ぶ)とき、声を消す
o = rep(o, "if(S.pl.id==='qplane'){worldAt('nairobi');", "if(S.pl.id==='qplane'){if(window.PA)PA.discard();worldAt('nairobi');")
o = rep(o, "if(S.pl.id==='hplane'){worldAt('haneda');", "if(S.pl.id==='hplane'){if(window.PA)PA.discard();worldAt('haneda');")
o = rep(o, "setMode('arr');\nvar phoQ", main + "\nsetMode(save.ticket?(hdepOn()?'hdep':(hretOn()?'hret':'arr')):'sage');\n"
        "if(/[?&]pho=/.test(location.search)||window.__CHK){}else {CHANT.resume(TOUR_FRESH&&!save.ticket);TRIP.enter(function(){if(TOUR_FRESH&&!save.ticket){enterHub(PBY.sage);runStory('sage_1')}},'tour')}\nvar phoQ")
o = rep(o, '<head>', '<head><script>' + _rd('check_shim.js') + '</script>')   # タスク056: ?check=1 のときだけ効く(専用の記録)
os.makedirs(os.path.join(ROOT, 'tour'), exist_ok=True)
open(os.path.join(ROOT, 'tour', 'index.html'), 'w', encoding='utf-8').write(o)
print('nairobi built', len(o), 'bytes; dialogues', len(dn), 'words', sum(len(v['words']) for v in dn.values()))

# ---------- ドーハ(tour/doha/index.html) ----------
dd = sub('doh_')
# ドーハの外の絵の昼夜(dohNight)も 旅の中の現地時刻(タスク032 / 020-3)
BGD_T = rep(BGD, "var h=+new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Qatar',hour:'2-digit',hourCycle:'h23'}).format(new Date());", "var h=TRIP.hourNow('Asia/Qatar');")
main = MAIN_DOH % dict(dlg=J(dd), sp=SPD, bg=BGD_T, world=WORLDJS, voice=VOICEJS, ev=EVJS, arr=J(DARR), city=J(DCITY), dep=J(DDEP), ids=J(DOH_IDS))
main += _rd('check.js').replace('__OTHER_HREF__', '../?check=1').replace('__OTHER_LABEL__', 'ナイロビ')
main += art_js('../assets/art/', "function artIdFor(S){var g=S&&S.d&&S.d.bg,v=String(S&&S.vid||'');if(/^doh_/.test(v)&&g==='dimmig')return v==='doh_immig2'?'dimmig2':'dimmig';if(v==='doh_city_h1')return'hotel';if(v==='doh_city_c1'||v==='doh_city_c2'||v==='doh_city_c3'||v==='doh_ev_j_ask')return'dcorn';if(/^doh_city_t[123]$/.test(v)||v==='doh_ev_h_prayer')return'dalley';if(/^doh_city_s[123]$/.test(v))return'dsouq';return null}")   # ホテルのフロント / 入国審査・出国審査の実画(タスク064。bg が dimmig で vid が doh_ のとき) / コルニーシュ(タスク070) / スークの路地(夜。t1〜t3と割りこみ「祈り」。タスク071) / スークの広場(昼。店の3場面を店先の広場の絵で統一。タスク071)
o = ev_patches(common(src, 'Asia/Qatar'))
for _a, _b in SHARED: o = rep(o, _a, _b)
o = rep(o, " if(!G.camp)addHelp(T)}", " if(!G.camp&&!G.scene.d.nohelp)addHelp(T)}")
o = rep(o, '<title>カンペ先生 ドバイ編</title>', '<title>空港えいご物語 世界一周編 ドーハ</title>')
o = rep(o, SNOTE_OLD, SNOTE_NEW)
o = rep(o, ".cue .heard.live{color:#8a7b55}", ".cue .heard.live{color:#8a7b55}\n" + VOICECSS)
o = rep(o, "'../world/?map=1'", "'../../world/?map=1'", 2)
o = rep(o, "worldMark('dubai')", "worldMark('doha')")   # タスク023: 出発の場所を全部あそんだら印(PLACES_AIR=PLACES_DDEP)
# 地図: 市内は湾の弧、出発は2つの広場＋列車。地図のあとの音楽はモードの曲(ドーハの曲)
o = rep(o, "if(cty){g.fillStyle='#e8f0f4';g.fillRect(0,ch-8,cw,8);g.fillStyle='#9ad0e4';g.fillRect(0,ch-6,cw,6);return}",
        "if(cty){dohCityBg(g,cw,ch);return}if(MODE==='dep')dohDepBg(g,cw,ch);")
o = rep(o, "Snd.go(MODE==='city'?'city':'map')", "Snd.go(MODES[MODE].snd)")
# seq=1 の場所は、場面を上から順に出す(物語の順番: 道をきく→お茶→ルルがいない など)
o = rep(o, "function pickV(pl){\n var ids=pl.v,min=1e9;ids.forEach(function(i){min=Math.min(min,save.seen[i]||0)});\n",
        "function pickV(pl){\n var ids=pl.v,min=1e9;ids.forEach(function(i){min=Math.min(min,save.seen[i]||0)});\n"
        " if(pl.seq){for(var q=0;q<ids.length;q++)if((save.seen[ids[q]]||0)===min)return ids[q]}\n")
# 場面のあと: 乗り場(タクシー・メトロ)→市内のタブ / 機内→クリアの印をつけて世界マップへ
o = rep(o, "if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}showMap()}",
        "if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}"
        "if(S.vid==='doh_dep_plane'){worldMark('doha');Snd.go(null);location.href=window.__CHK?'./?check=1':'../../world/?map=1';return}"
        "showMap();if(S.pl.id==='dride')setMode('city')}")
o = rep(o, KBASE, KBASE +
        "K.doh={bpm:function(){return 66},amb:function(){loopNoise(320,.6,.015,.08,.008,'lowpass')},"
        "st:function(s,t,e){var KD=[62,63,65,67,69,67,65,63];if(s%4===0)pluck(hz(KD[(s>>2)%8]),t,e*3.4,ngt?.07:.1);"
        "if(s%16===8)pluck(hz(KD[0]-12),t,e*5,.08);if(s%32===0)tone(hz(38),t,e*30,'sine',.06,.6)}};"
        # 市内の曲(タスク023): ヒジャーズ調の、ゆっくりした つま弾き。背景音は静かに、高い音は使わない
        "K.dohc={bpm:function(){return ngt?60:72},amb:function(){loopNoise(260,.5,.012,.07,.006,'lowpass')},"
        "st:function(s,t,e){var KC=[62,63,66,67,69,67,66,63];if(s%4===0)pluck(hz(KC[(s>>2)%8]-12),t,e*3.6,ngt?.08:.1);"
        "if(s%8===6)pluck(hz(KC[((s>>3)+2)%8]-12),t,e*2,.05);if(s%16===0)tone(hz(43),t,e*14,'sine',.06,.5)}};")
o = rep(o, REC, record('ドーハの'))
o = trip_patches(o, 'doha')
o = rep(o, "showMap();if(S.pl.id==='dride')setMode('city')}", "showMap();if(S.pl.id==='dride')setMode('city')})}")
o = rep(o, "g.fillStyle='#143fb0';g.fillRect(0,0,5,ch);g.fillRect(cw-5,0,5,ch)", "g.fillStyle='#8a1538';g.fillRect(0,0,5,ch);g.fillRect(cw-5,0,5,ch)")
o = rep(o, "setMode('arr');\nvar phoQ", main + "\nsetMode('arr');if(!/[?&]pho=/.test(location.search)&&!window.__CHK)TRIP.enter(function(){},'doha');\nvar phoQ")
o = rep(o, '<head>', '<head><script>' + _rd('check_shim.js') + '</script>')   # タスク056
os.makedirs(os.path.join(ROOT, 'tour', 'doha'), exist_ok=True)
open(os.path.join(ROOT, 'tour', 'doha', 'index.html'), 'w', encoding='utf-8').write(o)
print('doha built', len(o), 'bytes; dialogues', len(dd), 'words', sum(len(v['words']) for v in dd.values()))
print('missing IPA:', missing)

# ---------- ロヴァニエミ(tour/rovaniemi/index.html。タスク065) ----------
dr = sub('rvn_')
main = MAIN_RVN % dict(dlg=J(dr), sp=SPR, bg=BGR, world=WORLDJS, voice=VOICEJS, ev=EVJS, arr=J(RARR), stay=J(RSTAY), dep=J(RDEP), ids=J(RVN_IDS))
main += _rd('check.js').replace('__OTHER_HREF__', '../doha/?check=1').replace('__OTHER_LABEL__', 'ドーハ')
main += art_js('../assets/art/', "function artIdFor(S){var v=String(S&&S.vid||'');return /^rvn_lobby[12]$/.test(v)?'rvnlobby':/^rvn_village[12]$/.test(v)?'rvillage':/^rvn_post[12]$/.test(v)?'rpostoffice':null}")   # 実画: 到着ロビー(rovaniemi-arrivals-v1.png＋オーロラ strip)・村の広場(072。オーロラ・煙・きらめき)・郵便局(072。暖炉の炎)。ほかはコード描画
o = ev_patches(common(src, 'Europe/Helsinki'))
for _a, _b in SHARED: o = rep(o, _a, _b)
o = rep(o, " if(!G.camp)addHelp(T)}", " if(!G.camp&&!G.scene.d.nohelp)addHelp(T)}")
o = rep(o, '<title>カンペ先生 ドバイ編</title>', '<title>空港えいご物語 世界一周編 ロヴァニエミ</title>')
o = rep(o, SNOTE_OLD, SNOTE_NEW)
o = rep(o, ".cue .heard.live{color:#8a7b55}", ".cue .heard.live{color:#8a7b55}\n" + VOICECSS)
o = rep(o, "'../world/?map=1'", "'../../world/?map=1'", 2)
o = rep(o, "worldMark('dubai')", "worldMark('rovaniemi')")   # 到着の場所を全部あそんだら印(PLACES_AIR=PLACES_RARR)
o = rep(o, "dep:['#e9e2f2','#d9d0e8','#8a7ac0']}[MODE]", "dep:['#e9e2f2','#d9d0e8','#8a7ac0'],stay:['#e4eef6','#d3e0ee','#8aa8c8']}[MODE]")   # 滞在タブの地図の色(072。到着・出発は既存の色)
o = rep(o, "Snd.go(MODE==='city'?'city':'map')", "Snd.go(MODES[MODE].snd)")
o = rep(o, "if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}showMap()}",
        "if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}showMap();/*RVN_END*/}")
# 音: 基本は静か(低い風だけ)。やわらかい弦(カンテレ風)を、ときどき1音。シャカシャカした高い音は使わない
o = rep(o, KBASE, KBASE +
        "K.rvn={bpm:function(){return 54},amb:function(){loopNoise(220,.5,.010,.06,.005,'lowpass')},"
        "st:function(s,t,e){var KR=[60,62,65,67,69,67,65,62];if(s%8===0)pluck(hz(KR[(s>>3)%8]),t,e*4,ngt?.05:.07);"
        "if(s%32===0)tone(hz(36),t,e*28,'sine',.05,.6)}};")
o = rep(o, REC, record('ロヴァニエミの'))
o = trip_patches(o, 'rovaniemi')
o = rep(o, "showMap();/*RVN_END*/}", "showMap()})}")
o = rep(o, "g.fillStyle='#143fb0';g.fillRect(0,0,5,ch);g.fillRect(cw-5,0,5,ch)", "g.fillStyle='#2a5a8a';g.fillRect(0,0,5,ch);g.fillRect(cw-5,0,5,ch)")
o = rep(o, "setMode('arr');\nvar phoQ", main + "\nsetMode('arr');if(!/[?&]pho=/.test(location.search)&&!window.__CHK)TRIP.enter(function(){},'rovaniemi');\nvar phoQ")
o = rep(o, '<head>', '<head><script>' + _rd('check_shim.js') + '</script>')   # タスク056
os.makedirs(os.path.join(ROOT, 'tour', 'rovaniemi'), exist_ok=True)
open(os.path.join(ROOT, 'tour', 'rovaniemi', 'index.html'), 'w', encoding='utf-8').write(o)
print('rovaniemi built', len(o), 'bytes; dialogues', len(dr), 'words', sum(len(v['words']) for v in dr.values()))
print('missing IPA (all):', missing)

# ---------- 終わりの場面(tour/ending/index.html): 旅の一か月後のリビングで、アルバムの白いページを埋める ----------
import window_data
ENDJS = _rd('ending.js').replace("/*DECL*/''", json.dumps(window_data.DECL))
ENDCSS = _rd('ending.css')
e = o_pre
e = rep(e, '<title>空港えいご物語 世界一周編 ナイロビ</title>', '<title>空港えいご物語 世界一周編 アルバム</title>')
e = rep(e, "'../world/?map=1'", "'../../world/?map=1'", 2)
e = rep(e, "worldMark('nairobi')", "void 0")
e = rep(e, "K.sage=K.hall;", "K.sage=K.hall;K.home=K.hall;")
e = rep(e, "else if(k==='poof')whoosh(t0,.5,.07,400,3000);", "else if(k==='poof')whoosh(t0,.5,.07,400,3000);else if(k==='page'){noise(t0,.09,.12,1800,'highpass');noise(t0+.08,.06,.08,2600,'highpass')}")
e = rep(e, ".cue .heard.live{color:#8a7b55}", ".cue .heard.live{color:#8a7b55}\n" + ENDCSS)
e = rep(e, "'ナイロビの かいわ：'", "'アルバムの かいわ：'")
e = rep(e, "setMode('arr');\nvar phoQ", "\n" + VOICEJS + "\n" + DIAGJS + "\n" + EVJS + "\n" + ENDJS + "\nMODES={arr:{p:[],b:'',h:'',snd:'home'}};MODE='arr';PLACES=[];\nendingStart();\nvar phoQ")
os.makedirs(os.path.join(ROOT, 'tour', 'ending'), exist_ok=True)
open(os.path.join(ROOT, 'tour', 'ending', 'index.html'), 'w', encoding='utf-8').write(e)
print('ending built', len(e), 'bytes')

# ---------- 世界マップ(world/index.html は手書き。trip.js だけ マーカーの間に入れる) ----------
_w = open(os.path.join(ROOT, 'world', 'index.html'), encoding='utf-8').read()
_i, _j = _w.index('/*TRIPJS-BEGIN*/'), _w.index('/*TRIPJS-END*/')
_w = _w[:_i] + '/*TRIPJS-BEGIN*/' + _rd('trip.js') + _w[_j:]
open(os.path.join(ROOT, 'world', 'index.html'), 'w', encoding='utf-8').write(_w)
_w = open(os.path.join(ROOT, 'world', 'index.html'), encoding='utf-8').read()
_i, _j = _w.index('/*CHANTJS-BEGIN*/'), _w.index('/*CHANTJS-END*/')
_w = _w[:_i] + '/*CHANTJS-BEGIN*/' + chant_js('../tour/assets/song/') + _w[_j:]
open(os.path.join(ROOT, 'world', 'index.html'), 'w', encoding='utf-8').write(_w)
print('world trip.js + chant.js injected')
