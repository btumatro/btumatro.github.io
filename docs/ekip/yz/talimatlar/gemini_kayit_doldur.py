"""Geçmiş Gemini görsel çağrılarını gemini-kayit JSONL biçimine yazar (bir kez çalıştırılır).
Biçim: gemini-atolyesi/gemini-kayit skill'i; satırda zaman, komut, argumanlar, cikis_kodu, stdout, stderr.
Bu çağrılar gapi yerine Python REST ile yapıldığı için sonradan eklendi (sonradan_eklendi: true).
Kullanım: repo kökünden  python3 docs/ekip/yz/talimatlar/gemini_kayit_doldur.py"""
import datetime, glob, json, os

KAYIT = os.environ.get('GAPI_KAYIT_DIZINI', os.path.expanduser('~/gemini-kayit'))
T = 'docs/ekip/yz/talimatlar/'
MODEL = 'gemini-3-pro-image'
satirlar = []

def zaman(ts):
    return datetime.datetime.fromtimestamp(ts).astimezone().isoformat(timespec='seconds')

def ekle(z, kaynak, argumanlar, istem, cikti=None, kod=0, not_=''):
    out = {}
    if cikti and os.path.exists(cikti):
        out = {"path": cikti, "size_bytes": os.path.getsize(cikti)}
    elif cikti:
        out = {"path": cikti, "durum": "dosya artık yok (elendi ya da silindi)"}
    satirlar.append({"zaman": z, "komut": "gemini-rest-python", "argumanlar": argumanlar, "cikis_kodu": kod,
                     "stdout": out, "stderr": "", "istem": istem, "kaynak": kaynak,
                     "sonradan_eklendi": True, "not": not_})

# 1) Claude, bu oturum: her görselin yanındaki istem kaydı
for f in sorted(glob.glob('docs/ekip/yz/claude/**/*.istem.json', recursive=True)):
    k = json.load(open(f))
    g = f.replace('.istem.json', '.jpg')
    ekle(zaman(os.path.getmtime(g) if os.path.exists(g) else os.path.getmtime(f)), 'docs/ekip/yz/claude/referans_uret.py',
         ['generateContent', '-m', k.get('model', MODEL), '--aspect-ratio', k.get('oran', '1:1'), '--cok-turlu'],
         {"tur1": k['tur1'], "model_yaniti": "OK", "tur2": k['tur2']}, g, not_=k.get('not', ''))

# 1b) Claude, elenen çıktılar: tam istem saklanmadı, hangi betik sürümüyle üretildiği not edilir
SURUM = {'tur2': 'kır sakal tarifi düzeltildi, kıyafet stüdyo portresine bağlandı; Bilgehan referans sayfası yoktu',
         'tur3': 'Bilgehan referans sayfası eklendi, stil örneği 6',
         'tur4': 'stil örneği 2 ve "başka kişiler" uyarısı; kontrolde elendi'}
for g in sorted(glob.glob('docs/ekip/yz/claude/elenen/**/*.jpg', recursive=True)):
    tur = g.split('/')[-2]
    ekle(zaman(os.path.getmtime(g)), 'docs/ekip/yz/claude/referans_uret.py (o turdaki sürüm)',
         ['generateContent', '-m', MODEL, '--cok-turlu'], None, g,
         not_='elendi; tam istem saklanmadı. Sürüm: ' + SURUM.get(tur, 'ilk sürüm: Bilgehan tarifinde "biraz kır sakal", stil örneği en çok 6'))

# 2) agy: kendi çağrı kaydı (istem metni ve referans dosyaları var, görsel verisi yok)
for l in open(T + 'agy/gemini_calls.jsonl'):
    e = json.loads(l)
    istem = e.get('prompt') or e.get('request')
    adim = e.get('step') or e.get('task')
    z = e.get('ts') or zaman(os.path.getmtime(T + 'agy/gemini_calls.jsonl'))
    if istem is None:
        istem = 'bu satırda istem yok; görev adına (' + str(adim) + ') karşılık gelen agy betiğinde'
    ekle(z, 'agy (Antigravity CLI), docs/ekip/yz/talimatlar/agy/',
         ['generateContent', '-m', MODEL, '--kisi', str(e.get('slug')), '--adim', str(adim)],
         {"istem": istem, "referanslar": e.get('refs')}, None,
         kod=0 if e.get('success', True) else 1, not_='agy gemini_calls.jsonl satırından')

# 3) Claude, önceki oturum ve ilk stil turu: istem betiğin içinde; betik kaynağı tam olarak saklanır
for b in sorted(glob.glob(T + 'claude-onceki/*.py')) + ['docs/ekip/yz/claude/stil_uret.py']:
    ekle(zaman(os.path.getmtime(b)), b, ['generateContent', '-m', MODEL, '--betik', os.path.basename(b)],
         {"betik_kaynagi": open(b).read()}, None,
         not_='çağrı başına istem saklanmadı; istem metinleri bu betiğin içindeki sabitlerden oluşur')

os.makedirs(KAYIT, exist_ok=True)
gunler = {}
for s in satirlar:
    gunler.setdefault(s['zaman'][:10], []).append(s)
for gun, L in gunler.items():
    with open(f'{KAYIT}/{gun}.jsonl', 'a') as fh:
        for s in sorted(L, key=lambda x: x['zaman']):
            fh.write(json.dumps(s, ensure_ascii=False) + '\n')
    print(gun, len(L))
