"""İstem kaydı olmayan ekip görsellerinin yanına <ad>.istem.json yazar (var olanı ezmez).
Kaynaklar: agy çağrı kaydı, betik kaynakları, sürüm notları. Repo kökünden çalıştır."""
import ast, glob, json, os

T = 'docs/ekip/yz/talimatlar/'
MODEL = 'gemini-3-pro-image'
yazilan = 0

def yaz(gorsel, kayit):
    global yazilan
    hedef = os.path.splitext(gorsel)[0] + '.istem.json'
    if os.path.exists(hedef):
        return
    kayit = {"model": MODEL, **kayit}
    json.dump(kayit, open(hedef, 'w'), ensure_ascii=False, indent=1)
    yazilan += 1

def sabitler(betik):
    """betikteki uzun metin sabitleri: istemler bunlardan kurulur"""
    agac = ast.parse(open(betik).read())
    return [n.value for n in ast.walk(agac) if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 40]

# agy çağrı kaydı: kişi + görev -> son başarılı istem
agy = {}
for l in open(T + 'agy/gemini_calls.jsonl'):
    e = json.loads(l)
    adim = str(e.get('step') or e.get('task'))
    istem = e.get('prompt') or e.get('request')
    if e.get('success', True):
        agy.setdefault((e.get('slug'), adim), []).append({"zaman": e.get('ts'), "istem": istem, "referanslar": e.get('refs')})

def agy_kayit(slug, anahtar):
    eslesen = {a: v for (s, a), v in agy.items() if s == slug and anahtar in a}
    return eslesen

for klasor, anahtar, betik in [('docs/ekip/yz/codex/gri-fon', 'grifon', 'codex_uret.py, iyilestir.py, uret_gri_fon_yeni.py'),
                               ('docs/ekip/yz/codex/kadraj', 'kadraj', 'uret_26_kadraj_poisson.py, uret_ek9_8kadraj.py, fix_ek10_2kadraj.py'),
                               ('docs/ekip/yz/agy/stil-ornekleri', 'stil', 'uret_ek10_stil_ve_sheet.py, fix_ek10_13_stiller.py')]:
    for g in sorted(glob.glob(klasor + '/*.jpg')):
        ad = os.path.basename(g)[:-4]
        slug = ad[2:] if klasor.endswith('stil-ornekleri') else ad
        cagrilar = agy_kayit(slug, anahtar)
        betikler = [T + 'agy/' + b.strip() for b in betik.split(',')]
        istemsiz = not any(c['istem'] for v in cagrilar.values() for c in v)
        yaz(g, {"uretici": "agy (Antigravity CLI)", "gorev_notu": "docs/ekip/yz/CODEX-GOREV.md",
                "betik": betikler, "cagrilar": cagrilar or None,
                "istem_sabitleri": {b: sabitler(b) for b in betikler} if istemsiz else None,
                "not": "agy çağrı kaydındaki istemler ve referanslar" if not istemsiz else
                       "agy bu görevde istem metnini kaydetmemiş (yalnız referanslar); istem betikteki sabitlerden kuruluyor"})

for g in sorted(glob.glob('docs/ekip/yz/agy/karakter-sheet/*.jpg')):
    yaz(g, {"uretici": "agy", "betik": [T + 'agy/uret_ek10_stil_ve_sheet.py'],
            "istem_sabitleri": sabitler(T + 'agy/uret_ek10_stil_ve_sheet.py'),
            "not": "agy'nin önbelleğinden geri alındı; istem betikteki sabitlerden kuruluyor"})

# Claude, ilk stil turu
for g in sorted(glob.glob('docs/ekip/yz/claude/stil-ornekleri/tur1/*.jpg')):
    yaz(g, {"uretici": "Claude", "betik": 'docs/ekip/yz/claude/stil_uret.py', "istem_sabitleri": sabitler('docs/ekip/yz/claude/stil_uret.py'),
            "not": "1. tur. 'ilk-' önekliler kişi tarifinde yaş belirtilmeden; diğerleri yaş sayısı kaldırılmış sürümle üretildi. Betik son sürümdür."})

# Claude, elenenler
SURUM = {'tur2': 'kır sakal tarifi düzeltildi, kıyafet stüdyo portresine bağlandı; Bilgehan referans sayfası yoktu',
         'tur3': 'Bilgehan referans sayfası eklendi, stil örneği 6',
         'tur4': 'stil örneği 2 ve "başka kişiler" uyarısı; kontrolde elendi'}
for g in sorted(glob.glob('docs/ekip/yz/claude/elenen/**/*.jpg', recursive=True)):
    tur = g.split('/')[-2]
    yaz(g, {"uretici": "Claude", "betik": 'docs/ekip/yz/claude/referans_uret.py',
            "surum": SURUM.get(tur, 'ilk sürüm: Bilgehan tarifinde "biraz kır sakal", stil örneği en çok 6'),
            "not": "elendi; tam istem saklanmadı, güncel betikten yukarıdaki farkla kurulur"})

# Claude, önceki oturum: stilize ve karikatür
ONCEKI = [('docs/ekip/stilize/portre/*.jpg', ['portre.py', 'portre2.py', 'duzelt.py']),
          ('docs/ekip/stilize/*.png', ['ekip_gorsel.py', 'toplu.py']),
          ('docs/ekip/karikatur/*.jpg', ['karikatur.py'])]
for desen, betikler in ONCEKI:
    for g in sorted(glob.glob(desen)):
        yaz(g, {"uretici": "Claude (önceki oturum)", "betik": [T + 'claude-onceki/' + b for b in betikler],
                "istem_sabitleri": {b: sabitler(T + 'claude-onceki/' + b) for b in betikler},
                "not": "çağrı başına istem saklanmadı; istemler bu betiklerdeki sabitlerden kuruluyor"})

print(yazilan, 'istem kaydı yazıldı')
