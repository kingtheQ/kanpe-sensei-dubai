import re
try:
    import cmudict
    _D = cmudict.dict()
except Exception:
    _D = {}
M = {'AA':'ɑː','AE':'æ','AH':'ə','AO':'ɔː','AW':'aʊ','AY':'aɪ','B':'b','CH':'tʃ','D':'d','DH':'ð','EH':'ɛ','ER':'ɚ','EY':'eɪ','F':'f','G':'ɡ','HH':'h','IH':'ɪ','IY':'iː','JH':'dʒ','K':'k','L':'l','M':'m','N':'n','NG':'ŋ','OW':'oʊ','OY':'ɔɪ','P':'p','R':'r','S':'s','SH':'ʃ','T':'t','TH':'θ','UH':'ʊ','UW':'uː','V':'v','W':'w','Y':'j','Z':'z','ZH':'ʒ'}
X={'safaricom':'ˈsæfɑːrikɑːm','mpesa':'ɛm ˈpeɪsə','kenya':'ˈkɛnjə','nairobi':'naɪˈroʊbi','eta':'iː tiː eɪ','java':'ˈdʒɑːvə','artcaffe':'ɑːrt kæˈfeɪ','uber':'ˈuːbɚ','bolt':'boʊlt','wifi':'ˈwaɪfaɪ','kikoy':'kɪˈkɔɪ','jkia':'dʒeɪ keɪ aɪ eɪ','kes':'keɪ ɛs','swahili':'swɑːˈhiːli','asante':'ɑːˈsɑːnteɪ','jambo':'ˈdʒɑːmboʊ','pesa':'ˈpeɪsə','mombasa':'mɑːmˈbɑːsə','sim':'sɪm','usd':'juː ɛs diː'}
def word(w):
    w = re.sub(r"[^a-z']", '', w.lower())
    if w in X: return X[w]
    if w not in _D: return None
    ph = _D[w][0]
    out = ''
    for p in ph:
        b = re.sub(r'\d', '', p); st = re.sub(r'\D', '', p)
        s = M.get(b, '')
        if b == 'AH' and st == '0': s = 'ə'
        elif b == 'AH': s = 'ʌ'
        V = ('AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW')
        if b in V and st in ('1','2'):
            m = 'ˈ' if st == '1' else 'ˌ'
            k = len(out)
            while k > 0 and out[k-1] not in 'ɑæəɔʊɛɚɪʌaeiouːˈˌ' and (len(out)-k) < 2: k -= 1
            out = out[:k] + m + out[k:]
        out += s
    return out
def phrase(t):
    parts = [word(x) for x in t.split()]
    if any(p is None for p in parts): return None
    return '/' + ' '.join(parts) + '/'
