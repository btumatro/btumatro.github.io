"""Yöneticiler için referans sayfaları ve stil örnekleri. Repo kökünden çalıştır.
python3 referans_uret.py sayfa   -> her kişi için gerçekçi + a stili 3x3 kimlik paftası
python3 referans_uret.py stil    -> yeni kişiler için 6 stil portre"""
import base64, glob, io, json, os, sys, urllib.request, concurrent.futures as cf
from PIL import Image, ImageOps

KEY = os.environ['GEMINI_API_KEY']
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent"
E = 'docs/ekip/'
A = '/Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/'
PK = '/Users/wildgenie/Downloads/Podcast_Bolum2_Produksiyon_Paketi/source/publication/avatar/'
OUT = E + 'yz/claude/'

GENC = "a young university student; keep exactly the age seen in the photos, do NOT make them look older"
KISI = {
 'mehmet-onur-genc': "Mehmet Onur, the academic advisor: dark wavy hair, full dark beard, warm smile, dark suit and tie. Keep exactly the age seen in the photos; do NOT make him look older",
 'bilgehan-zeki-ozaytac': "Bilgehan (Zeki): bald head, short fully DARK beard (no grey hair at all), dark rectangular glasses in most casual photos. Keep exactly the age seen in the photos; do NOT make him look older",
 'muhammed-ataman': "Muhammed, a young man under 30: thick dark wavy hair swept back, full dark beard. Do NOT make him look older",
 'irmak-karaagac': "Irmak, " + GENC + ": she wears a hijab, friendly smile",
 'omer-cihan-demir': "Ömer, " + GENC + ": short dark hair with a quiff, slim face, slightly heavy relaxed eyelids, SHORT SPARSE light beard and moustache (not thick, not full), calm soft expression",
 'gulsiye-begum-gumus': "Gülsiye, " + GENC + ": she wears a patterned grey hijab, often glasses resting on her head",
 'feyza-karabicak': "Feyza, " + GENC + ": she wears a dark brown hijab and round thin glasses",
}
# listede tarifi olmayanlar: yalnız ad + yaş kuralı; görünüş fotoğraflardan okunur
for _k in json.load(open('src/data/ekibimiz.json'))['people']:
    _s = os.path.basename(_k['photo'])[:-4]
    KISI.setdefault(_s, _k['name'].split()[0] + ", " + GENC)
# benzemeyen çıktılardan sonra eklenen düzeltmeler (26 Ekim 2026)
EK = {
 'duygu-solak': "long DARK BROWN wavy hair (not blonde, not light)",
 'esma-demirkiyik': "calm front-facing studio pose, hands not in frame",
 'melisa-aydirek': "long DARK BROWN straight hair exactly as dark as in the photos (not light, not blonde)",
 'eslem-kilic': "long dark brown hair with lighter ends only as in the photos (overall dark, not light), black cat-eye glasses",
 'muhammed-efe-coskunpinar': "light fair skin, fuller rounded lower face and soft jaw, CLEAN-SHAVEN (no beard, no stubble), thick dark hair swept back with a loose strand falling on the forehead, calm closed-mouth slight smile, black t-shirt",
}
for _s, _e in EK.items():
    KISI[_s] += ": " + _e
# grup fotoğraflarında kim kim
GRUP = {
 'irmak-karaagac-bilgehan': {'bilgehan-zeki-ozaytac': 'the bald man with glasses on the LEFT', 'irmak-karaagac': 'the young woman in the brown hijab on the RIGHT'},
 'luna-omer-bilgehan': {'bilgehan-zeki-ozaytac': 'the bald man', 'omer-cihan-demir': 'the young bearded man in a black t-shirt'},
 'irmak-karaagac-muhammed-ataman': {'irmak-karaagac': 'the young woman in the hijab at the lectern', 'muhammed-ataman': 'the bearded man standing on the right'},
 'muhammed-ataman-grup': {'muhammed-ataman': 'the bearded man in black on the far LEFT'},
}
# kullanıcının kendi onaylı avatar çizimleri (kimlik + stil için)
OZEL = {'bilgehan-zeki-ozaytac': [E + 'orijinal/bilgehan-zeki-ozaytac-referans-sayfasi.png', PK + 'zeki_avatar_1024.jpg', A + 'morph_07_yakin_plan_mimik.jpg']}

def kayit_parcalari(parts):
    # görseller yerine dosya yolu, metinler aynen
    return [x.get('_yol') or x.get('text') for x in parts]

def img(p, m=1024):
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB'); im.thumbnail((m, m))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=88)
    return {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}, "_yol": os.path.relpath(p)}

def fotolar(slug):
    L = []
    for p in sorted(glob.glob(E + 'orijinal/*.jpg')):
        ad = os.path.basename(p)[:-4]
        grup = next((g for g in GRUP if ad.startswith(g)), None)
        if grup and slug in GRUP[grup]:
            L.append((p, 'group photo; this person is ' + GRUP[grup][slug] + '; ignore everyone else'))
        elif not grup and ad.startswith(slug) and 'referans-sayfasi' not in ad:
            L.append((p, 'photo of this person'))
    for p, n in [(E + f'alternatif/{slug}.jpg', 'another photo'), (E + f'yz/codex/kadraj/{slug}.jpg', 'wider crop of a real photo'), (E + f'yz/codex/gri-fon/{slug}.jpg', 'studio portrait of this person (generated; real photos win if they differ)')]:
        if os.path.exists(p): L.append((p, n))
    return L

def ilk_tur(slug):
    p = [{"text": f"These are ALL real photos of one person: {KISI[slug]}. Study the face from every photo: face shape, eyes, eyebrows, nose, mouth, beard, hairline, skin tone, real age. Reply only 'OK'."}]
    for f, n in fotolar(slug):
        p += [{"text": n + ':'}, img(f)]
    for f in OZEL.get(slug, []):
        p += [{"text": ("THE MAIN APPROVED REFERENCE SHEET of this person (follow this face, age, beard colour and build most closely):" if "referans-sayfasi" in f else "approved illustrated avatar of this same person:")}, img(f, 1536)]
    return p

def gemini_kayit(istem, cikti, kod, hata, oran):
    # gemini-atolyesi/gemini-kayit biçimi; gapi yerine REST kullanıldığı için elle yazılır
    d = os.environ.get('GAPI_KAYIT_DIZINI', os.path.expanduser('~/gemini-kayit'))
    os.makedirs(d, exist_ok=True)
    import datetime
    z = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    out = {"path": cikti, "size_bytes": os.path.getsize(cikti)} if kod == 0 else {}
    with open(f'{d}/{z[:10]}.jsonl', 'a') as fh:
        fh.write(json.dumps({"zaman": z, "komut": "gemini-rest-python", "argumanlar": ["generateContent", "-m", URL.split('/models/')[1].split(':')[0], "--aspect-ratio", oran, "--cok-turlu"],
                             "cikis_kodu": kod, "stdout": out, "stderr": hata, "istem": istem, "kaynak": os.path.relpath(__file__)}, ensure_ascii=False) + '\n')

def cagir(slug, p2, oran, cikti):
    p1 = ilk_tur(slug)
    temiz = lambda ps: [{k: v for k, v in x.items() if k != '_yol'} for x in ps]
    g = {"contents": [{"role": "user", "parts": temiz(p1)}, {"role": "model", "parts": [{"text": "OK"}]}, {"role": "user", "parts": temiz(p2)}],
         "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": oran}}}
    # yeniden üretilebilsin: istem metinleri ve referans dosyaları çıktının yanına
    os.makedirs(os.path.dirname(cikti), exist_ok=True)
    with open(cikti[:-4] + '.istem.json', 'w') as kf:
        json.dump({"model": URL.split('/models/')[1].split(':')[0], "oran": oran,
                   "tur1": kayit_parcalari(p1), "tur2": kayit_parcalari(p2)}, kf, ensure_ascii=False, indent=1)
    hata = ''
    for _ in range(3):
        try:
            r = urllib.request.Request(URL, data=json.dumps(g).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
            j = json.load(urllib.request.urlopen(r, timeout=300))
            for q in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in q:
                    os.makedirs(os.path.dirname(cikti), exist_ok=True)
                    Image.open(io.BytesIO(base64.b64decode(q["inlineData"]["data"]))).convert('RGB').save(cikti, quality=90)
                    gemini_kayit({"tur1": kayit_parcalari(p1), "model_yaniti": "OK", "tur2": kayit_parcalari(p2)}, cikti, 0, '', oran)
                    return os.path.basename(cikti) + ' tamam'
            hata = 'görsel yok'
        except Exception as e:
            hata = str(e)[:120]
    gemini_kayit({"tur1": kayit_parcalari(p1), "model_yaniti": "OK", "tur2": kayit_parcalari(p2)}, cikti, 1, hata, oran)
    return os.path.basename(cikti) + ' HATA ' + hata

# pafta-taslak-sozlugu "Kimlik paftası (karakter)" düzeni
# kullanıcının kendi gerçekçi referans sayfasının düzeni (26 Ekim'de sohbette paylaştı)
SAYFA = ("Create a character reference sheet of THIS exact person on a light grey seamless studio background, landscape 3:2, thin white gutters, no text. "
         "TOP ROW, six head-and-shoulders panels: front view; three-quarter view; side profile; serious look with head slightly down; warm smile; big surprised laugh. "
         "BOTTOM ROW, four full-body standing panels: front; side profile; back view; relaxed three-quarter pose with one hand in pocket. "
         "Same person, same real age, same outfit (take the outfit from the studio portrait; add simple trousers and shoes that suit it) and the same accessories in every panel.")
STILLER = {
 'gercek': "Photorealistic studio photography, soft even light, true skin texture, exactly like the real photos.",
 'a': "Render it in Zeki's reels scene illustration style: graphic-novel look, thin dark ink outlines, painterly soft shading, warm lamp key light with cool navy fill.",
}
STIL6 = {
 'a': "Zeki's reels scene style: graphic-novel illustration, thin dark ink outlines, painterly soft shading, cinematic warm desk-lamp key light with cool navy fill, dark navy-grey background.",
 'b': "flat 2D cartoon character style: clean dark outlines, flat colours with one soft shadow tone, plain warm grey-beige background.",
 'c': "soft 3D animated feature film character style, gentle subsurface skin, soft studio light, plain grey background.",
 'd': "flat vector illustration, clean geometric shapes, limited palette, plain light background.",
 'e': "loose watercolour portrait on textured paper, soft washes, light pencil lines.",
 'f': "comic book style, bold black ink outlines, halftone shading, strong colours.",
}

def stil_ornekleri(h):
    L = sorted(glob.glob(OUT + f'stil-ornekleri/{h}-*.jpg')) + sorted(glob.glob(OUT + f'stil-ornekleri/tur1/{h}-*.jpg'))
    return L[:6]

def sayfa(slug, h):
    p2 = [{"text": SAYFA + " " + STILLER[h]}]
    if h == 'a':
        p2 = [{"text": "Style references (copy ONLY the drawing style, never these people):"}, img(A + 'morph_07_yakin_plan_mimik.jpg'), img(A + '01_sahne_zeki_ve_ani_masada_00_00.jpg')] \
             + [{"text": "Earlier approved drawings of team members in this style:"}] + [img(x, 768) for x in stil_ornekleri('a')] + p2
    return cagir(slug, p2, '3:2', OUT + f'referans-sayfasi/{h}-{slug}.jpg')

def portre(slug, h):
    # shortcut: en çok 2 stil örneği; fazlası kimliği karıştırıp başka kişiyi çizdirdi (Bilgehan yerine Irmak)
    ornek = [x for x in stil_ornekleri(h) if slug not in x][:2]
    p2 = [{"text": "STYLE ONLY: drawings of OTHER, DIFFERENT people. Copy only their rendering; never draw these people:"}] + [img(x, 512) for x in ornek]
    if h == 'a':
        p2 += [{"text": "Style references (copy ONLY the drawing style):"}, img(A + 'morph_07_yakin_plan_mimik.jpg')]
    if h == 'b':
        p2 += [{"text": "Style reference (copy ONLY the drawing style):"}, img(A + 'KARAKTER_KIMLIK_PAFTASI_v1.jpg')]
    p2.append({"text": f"Now draw a head-and-shoulders portrait of the person from the REAL PHOTOS in the first message ({KISI[slug].split(':')[0]}), not anyone from the style images. Keep every accessory from the photos (glasses, hijab, beard). Draw in {STIL6[h]}"})
    p2.append({"text": f"Portrait of THIS person in {STIL6[h]} Instantly recognisable: same face, beard/hair, hijab or glasses as in the photos. "
               "Do NOT make them look older, no wrinkles, no extra weight, no beautifying, no big eyes. Same outfit as in the studio portrait. Centred, square 1:1. No text."})
    return cagir(slug, p2, '1:1', OUT + f'stil-ornekleri/{h}-{slug}.jpg')

if __name__ == '__main__':
    mod = sys.argv[1]
    if mod == 'sayfa':
        isler = [(sayfa, s, h) for s in KISI for h in STILLER]
    else:
        yeni = [s for s in KISI if s not in ('muhammed-ataman', 'irmak-karaagac')]
        isler = [(portre, s, h) for s in yeni for h in STIL6]
    with cf.ThreadPoolExecutor(4) as ex:
        for r in ex.map(lambda a: a[0](a[1], a[2]), isler):
            print(r, flush=True)
