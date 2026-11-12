# -*- coding: utf-8 -*-
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import ipa, data
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

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
    return x['bg']
dl = {}
for x in data.D:
    lines = []
    for (n, njp, y, yjp) in x['pairs']:
        lines.append({'n': n, 'jp': njp}); lines.append({'y': y, 'jp': yjp})
    dl[x['id']] = {'who': x['who'], 'story': 1, 'bg': bgfor(x), 'sp': x['sp'], 'hero': 'blue', 'lulu': 'plain', 'nogold': 1,
                   'inter': [], 'intro': x['intro'], 'lines': lines, 'words': [wd(a, b) for a, b in x['words']]}
J = lambda o: json.dumps(o, ensure_ascii=False)

def place(id, name, snd, x, y, ico, tip, v, **kw):
    p = dict(id=id, name=name, snd=snd, x=x, y=y, ico=ico, tip=tip, v=v); p.update(kw); return p
SAGE = [
 place('sage', '達人賢者', 'sage', 30, 28, '🧙', ['達人賢者', '旅のはじまりを聞く'], ['sage_1', 'sage_2', 'sage_3'],
       hub=True, hubBg='sage', hubHero='blue', hubEn='Welcome, travelers. What would you like to ask?',
       hubMsg='達人賢者の広間。', menu=[['Why go around the world?', 'sage_1'], ['Which ticket should we choose?', 'sage_2'], ['Tips for travel English', 'sage_3']]),
 place('ticket', 'チケットをえらぶ', 'tdesk', 70, 72, '🎫', ['航空券の窓口', 'Star Alliance か oneworld をえらぶ'], ['ticket_star', 'ticket_ow'],
       hub=True, hubMap=1, hubBg='tdesk', hubHero='blue', hubEn='Which ticket will you take?', hubMsg='航空券の窓口。',
       menu=[['Star Alliance', 'ticket_star'], ['oneworld', 'ticket_ow']])]
ARR = [
 place('immig', '入国審査', 'info', 22, 16, '🛂', ['入国審査(Immigration)', 'eTA・目的・滞在日数・ホテル'], ['nbo_immig1', 'nbo_immig2']),
 place('bag', '手荷物受け取り', 'hall', 70, 36, '🧳', ['バゲージクレーム', 'スーツケース・レジ袋'], ['nbo_bag1', 'nbo_bag2']),
 place('sim', 'Safaricom SIM', 'info', 24, 58, '📱', ['Safaricom', 'SIMの登録とデータ'], ['nbo_sim1', 'nbo_sim2']),
 place('taxi', 'タクシー・Uber', 'hall', 70, 82, '🚕', ['タクシー乗り場とライドシェア', '市内へ・料金は架空'], ['nbo_taxi1', 'nbo_taxi2'])]
AIR = [
 place('java', 'Java House', 'cafe', 22, 14, '☕', ['Java House', 'ラテとケーキ・値段は架空'], ['nbo_java1', 'nbo_java2']),
 place('art', 'Artcaffe', 'cafe', 70, 32, '🥐', ['Artcaffe', 'パンとジュース・値段は架空'], ['nbo_art1', 'nbo_art2']),
 place('lounge', 'Pride Lounge', 'ahlan', 24, 52, '🛋️', ['Pride Lounge', 'ラウンジの受付と、となりの人'], ['nbo_lounge1', 'nbo_lounge2']),
 place('duty', 'Duty Free', 'cafe', 70, 68, '🛍️', ['免税店', 'コーヒーと紅茶・値段は架空'], ['nbo_duty1', 'nbo_duty2']),
 place('gate', '搭乗ゲート', 'hall', 26, 86, '🚪', ['搭乗ゲート', '搭乗のアナウンス'], ['nbo_gate1', 'nbo_gate2'])]
TOUR_IDS = [i for p in ARR + AIR for i in p['v']]

SPJS = r"""
SP.sage={pitch:.8,m:[[trav({}),P(4,{o:'#5a3a8a',p:'#3a2a5a',h:'#d9d4c6'})]]};
SP.desk_star={pitch:1.2,m:[[trav({hair:'long'}),P(1,{o:'#c8182a',p:'#2a2a33',h:'#241a14'})]]};
SP.desk_ow={pitch:1.1,m:[[trav({hair:'cap'}),P(3,{o:'#5c0632',p:'#2a2a33',h:'#241a14'})]]};
SP.officer={pitch:.9,m:[[trav({hair:'cap'}),P(5,{o:'#2b3a5a',p:'#2b2b33',h:'#241a14'})]]};
SP.officer2={pitch:1.15,m:[[trav({hair:'long'}),P(4,{o:'#2b3a5a',p:'#2b2b33',h:'#241a14'})]]};
SP.bag_staff={pitch:1,m:[[trav({}),P(5,{o:'#f2b705',p:'#2a2a33',h:'#241a14'})]]};
SP.bag_staff2={pitch:1.1,m:[[trav({hair:'long'}),P(4,{o:'#f2b705',p:'#2a2a33',h:'#241a14'})]]};
SP.sim_staff={pitch:1.1,m:[[trav({hair:'long'}),P(4,{o:'#43b02a',p:'#2a2a33',h:'#241a14'})]]};
SP.sim_staff2={pitch:.95,m:[[trav({}),P(5,{o:'#43b02a',p:'#2a2a33',h:'#241a14'})]]};
SP.taxi_staff={pitch:.9,m:[[trav({hair:'cap'}),P(5,{o:'#e8d8a8',p:'#3a3a48',h:'#241a14'})]]};
SP.driver={pitch:.95,m:[[trav({hair:'cap'}),P(4,{o:'#2f7a4a',p:'#2a2a33',h:'#241a14'})]]};
SP.cafe_staff={pitch:1.15,m:[[trav({hair:'long'}),P(4,{o:'#7a3b1e',p:'#2a2a33',h:'#241a14'})]]};
SP.cafe_staff2={pitch:.9,m:[[trav({hair:'curly'}),P(2,{o:'#2d8f8a',p:'#6a5a4a',h:'#6a5a3a',pack:1})]]};
SP.cafe_staff3={pitch:1.2,m:[[trav({hair:'long'}),P(5,{o:'#2f4b7a',p:'#2a2a33',h:'#241a14'})]]};
SP.cafe_staff4={pitch:1,m:[[trav({}),P(4,{o:'#2f4b7a',p:'#2a2a33',h:'#241a14'})]]};
SP.lounge_staff={pitch:1.2,m:[[trav({hair:'long'}),P(4,{o:'#3a2a5a',p:'#2a2a33',h:'#241a14'})]]};
SP.lounge_guest={pitch:1,m:[[trav({hair:'curly'}),P(1,{o:'#d06a2a',p:'#44464f',h:'#8a6a3a'})]]};
SP.duty_staff={pitch:1.1,m:[[trav({}),P(5,{o:'#143fb0',p:'#2a2a33',h:'#241a14'})]]};
SP.duty_staff2={pitch:1.2,m:[[trav({hair:'long'}),P(4,{o:'#143fb0',p:'#2a2a33',h:'#241a14'})]]};
SP.gate_agent={pitch:1.15,m:[[trav({hair:'long'}),P(4,{o:'#1f6aa8',p:'#2a2a33',h:'#241a14'})]]};
SP.gate_agent2={pitch:.9,m:[[trav({hair:'cap'}),P(5,{o:'#1f6aa8',p:'#2a2a33',h:'#241a14'})]]};
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
MAIN = r"""
/* ===== 世界一周編: ナイロビ(賢者・券えらび・到着・空港) ===== */
var TOURDLG=%(dlg)s;
for(var _k in TOURDLG)DLG[_k]=TOURDLG[_k];
%(sp)s
%(bg)s
var PLACES_SAGE=%(sage)s,PLACES_NARR=%(arr)s,PLACES_NAIR=%(air)s;
PLACES_AIR=PLACES_NAIR;
PLACES_SAGE.concat(PLACES_NARR,PLACES_NAIR).forEach(function(p){PBY[p.id]=p});
var TOUR_IDS=%(ids)s;
MODES={sage:{p:PLACES_SAGE,b:'🧙 賢者',h:'達人賢者の広間<small>世界一周のはじまり</small>',snd:'sage'},
 arr:{p:PLACES_NARR,b:'🛬 到着',h:'ナイロビに到着<small>ジョモ・ケニヤッタ国際空港</small>',snd:'nbo'},
 air:{p:PLACES_NAIR,b:'✈ 空港',h:'ナイロビの空港<small>出発までの時間</small>',snd:'nbo'}};
"""
main = MAIN % dict(dlg=J(dl), sp=SPJS, bg=BGJS, sage=J(SAGE), arr=J(ARR), air=J(AIR), ids=J(TOUR_IDS))

def rep(s, a, b, cnt=1):
    n = s.count(a)
    if n != cnt: raise SystemExit('PATCH MISS (%d!=%d): %s' % (n, cnt, a[:60]))
    return s.replace(a, b)
o = src
o = rep(o, '<title>カンペ先生 ドバイ編</title>', '<title>空港えいご物語 世界一周編 ナイロビ</title>')
o = rep(o, "timeZone:'Asia/Dubai'", "timeZone:'Africa/Nairobi'")
o = rep(o, "SAVEKEY='kanpe-dubai-save-v2'", "SAVEKEY='kanpe-tour-save-v1'")
o = rep(o, "if(s0&&s0.gold)save.gold=1;", "if(s0&&s0.gold)save.gold=1;if(s0&&(s0.ticket==='star'||s0.ticket==='ow'))save.ticket=s0.ticket;")
o = rep(o, "worldMark('dubai')", "worldMark('nairobi')")
o = o.replace("'world/?map=1'", "'../world/?map=1'")
o = rep(o, "function runStory(vid){startVid(G.scene.pl,vid,'hub')}",
        "function runStory(vid){if(vid==='ticket_star'||vid==='ticket_ow'){save.ticket=vid==='ticket_star'?'star':'ow';storeSave()}startVid(G.scene.pl,vid,'hub')}")
o = rep(o, "if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}showMap()}",
        "if(S.from==='hub'&&!S.pl.hubMap){enterHub(S.pl);return}showMap();if(S.pl.id==='ticket'&&save.ticket)setMode('arr')}")
o = rep(o, "K.fountain=K.hall;K.safari=K.ahlan;K.marina=K.s34;K.beach=K.costa;",
        "K.fountain=K.hall;K.safari=K.ahlan;K.marina=K.s34;K.beach=K.costa;"
        "K.sage=K.hall;K.tdesk=K.info;"
        "K.nbo={bpm:function(){return 84},amb:function(){loopNoise(500,.7,.02,.1,.01,'lowpass')},"
        "st:function(s,t,e){var KN=[64,67,69,72,69,67,64,62];if(s%2===0)pluck(hz(KN[(s>>1)%8]),t,e*2.2,ngt?.08:.12);"
        "if(s%8===4)pluck(hz(KN[0]-12),t,e*3,.09);if(s%16===0)tone(hz(40),t,e*16,'sine',.07,.5)}};")
o = rep(o, "if(G.view==='map'&&MODE!==k)setMode(k)",
        "if(G.view==='map'&&MODE!==k){if(k!=='sage'&&!save.ticket){setMode('sage');G.at='ticket';placeWalkers('ticket',true);return}setMode(k)}")
o = rep(o, "b.appendChild(s4);\n $m('setView').hidden=false;",
        "b.appendChild(s4);\n var s5=sSec('ルルの カバンの きろくちょう');s5.appendChild(el('div','tt','えらんだ チケット：'+(save.ticket==='star'?'Star Alliance':save.ticket==='ow'?'oneworld':'まだ えらんでいない')));"
        "var dn=0;TOUR_IDS.forEach(function(k){if(save.seen[k]>0)dn++});s5.appendChild(el('div','tt','ナイロビの かいわ：'+dn+' / '+TOUR_IDS.length));b.appendChild(s5);\n $m('setView').hidden=false;")
o = rep(o, "dep:['#e9e2f2','#d9d0e8','#8a7ac0']}[MODE]", "dep:['#e9e2f2','#d9d0e8','#8a7ac0'],sage:['#e4dff2','#d3cbe8','#8a7ac0']}[MODE]")
o = rep(o, "g.fillStyle='#143fb0';g.fillRect(0,0,5,ch);g.fillRect(cw-5,0,5,ch)", "g.fillStyle='#2f7a4a';g.fillRect(0,0,5,ch);g.fillRect(cw-5,0,5,ch)")
o = rep(o, "setMode('arr');\nvar phoQ", main + "\nsetMode(save.ticket?'arr':'sage');\nvar phoQ")
os.makedirs(os.path.join(ROOT, 'tour'), exist_ok=True)
open(os.path.join(ROOT, 'tour', 'index.html'), 'w', encoding='utf-8').write(o)
print('built', len(o), 'bytes; dialogues', len(dl), 'words', sum(len(v['words']) for v in dl.values()), 'missing IPA:', missing)
