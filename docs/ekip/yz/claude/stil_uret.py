"""Her kişi için çok turlu Gemini sohbeti: ilk tur tüm kesilmemiş fotoğraflar, sonra stil.
Kullanım: python3 stil_uret.py [harf...]  (repo kökünden çalıştır)"""
import base64, io, json, os, sys, urllib.request, concurrent.futures as cf
from PIL import Image

KEY = os.environ['GEMINI_API_KEY']
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent"
E = 'docs/ekip/'
A = '/Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/'
AGY = E + 'yz/agy/stil-ornekleri/'
OUT = E + 'yz/claude/stil-ornekleri/'

KISI = {
 'adem-baglan': ("Adem, a young male university student: short black hair, trimmed black beard and moustache, dark eyes, slim face.",
   [('orijinal/adem-baglan-canva.jpg', 'ID-style photo, blue polo shirt'),
    ('orijinal/adem-baglan.jpg', 'full-body night photo, black blazer over white shirt'),
    ('alternatif/adem-baglan.jpg', 'closer crop of the night photo')]),
 'irmak-karaagac': ("Irmak, a young female university student who wears a hijab (headscarf), friendly smile, light skin, dark eyebrows.",
   [('orijinal/irmak-karaagac.jpg', 'outdoor photo at sunset, white cap over black hijab, MATRO navy t-shirt, blue lanyard'),
    ('alternatif/irmak-karaagac.jpg', 'close-up selfie, brown hijab'),
    ('orijinal/irmak-karaagac-bilgehan-1.jpg', 'selfie: Irmak is the young woman in the brown hijab on the RIGHT; ignore the bald man'),
    ('orijinal/irmak-karaagac-bilgehan-2.jpg', 'Irmak is the young woman in the brown hijab on the right'),
    ('orijinal/irmak-karaagac-muhammed-ataman-kursu.jpg', 'Irmak is the young woman in the brown hijab at the lectern; ignore the man')]),
 'muhammed-ataman': ("Muhammed, a young man (under 30): thick dark wavy hair swept back, full dark beard, warm brown eyes.",
   [('orijinal/muhammed-ataman.jpg', 'selfie in front of a historic building, white puffer jacket, grey striped scarf'),
    ('orijinal/muhammed-ataman-yuz-1.jpg', 'close-up face, black zip sweater'),
    ('orijinal/muhammed-ataman-yuz-2.jpg', 'close-up face, smiling'),
    ('orijinal/muhammed-ataman-yuz-3.jpg', 'face, profile-ish view'),
    ('orijinal/muhammed-ataman-grup-1.jpg', 'group photo: Muhammed is the bearded man in black on the far LEFT; ignore the others')]),
}

STIL = {
 'a': ("Zeki's reels scene style: graphic-novel illustration, thin dark ink outlines, painterly soft shading, cinematic warm desk-lamp key light with cool navy fill, dark navy-grey background.",
       [A+'morph_07_yakin_plan_mimik.jpg', A+'01_sahne_zeki_ve_ani_masada_00_00.jpg', A+'10_sahne_zeki_kisisel_itiraf_cene_elde_05_38.jpg']),
 'b': ("flat 2D cartoon character style: clean dark outlines, flat colours with one soft shadow tone, plain warm grey-beige background.",
       [A+'KARAKTER_KIMLIK_PAFTASI_v1.jpg']),
 'c': ("soft 3D animated feature film character style, gentle subsurface skin, soft studio light, plain grey background.", []),
 'd': ("flat vector illustration, clean geometric shapes, limited palette, plain light background.", []),
 'e': ("loose watercolour portrait on textured paper, soft washes, light pencil lines.", []),
 'f': ("comic book style, bold black ink outlines, halftone shading, strong colours.", []),
}

def img(p, m=1024):
    im = Image.open(p).convert('RGB'); im.thumbnail((m, m))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=88)
    return {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}}

def uret(slug, h):
    tarif, foto = KISI[slug]
    p1 = [{"text": f"These are ALL real photos of one person. {tarif} Study the face carefully from every photo: face shape, eyes, eyebrows, nose, mouth, beard, hairline, skin tone, age. Reply only 'OK'."}]
    for f, n in foto:
        p1 += [{"text": n + ':'}, img(E + f)]
    p1 += [{"text": "Studio portrait of the same person (for face reference):"}, img(E + f'yz/codex/gri-fon/{slug}.jpg')]
    stil, sref = STIL[h]
    p2 = [{"text": "Style references (copy ONLY the drawing style, never these people):"}] + [img(x) for x in sref]
    # stil tutarlılığı: bu stilde daha önce üretilmiş tüm çizimler (agy + bu turda diğer kişiler)
    ornek = [AGY + f'{h}-{k}.jpg' for k in KISI] + [OUT + f'tur1/{h}-{k}.jpg' for k in KISI] + [OUT + f'{h}-{k}.jpg' for k in KISI if k != slug]
    ornek = [x for x in ornek if os.path.exists(x)]
    if ornek:
        p2 += [{"text": "Earlier drawings in this exact style (team members, including this person). Match this rendering, line work, palette and lighting exactly; take identity only from the real photos above:"}] + [img(x, 768) for x in ornek]
    p2.append({"text": f"Now draw a head-and-shoulders portrait of THIS person in {stil} "
               "The person must stay instantly recognisable to friends: same face shape, features, beard/hair, hijab or glasses exactly as in the photos. "
               "Keep exactly the age seen in the photos; do NOT make them look older, do NOT make them older, no wrinkles, no extra weight, no beautifying, no big eyes. "
               "Front or slight three-quarter view, centred, square 1:1. No text, no letters."})
    g = {"contents": [{"role": "user", "parts": p1}, {"role": "model", "parts": [{"text": "OK"}]}, {"role": "user", "parts": p2}],
         "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}}
    hata = ''
    for _ in range(3):
        try:
            r = urllib.request.Request(URL, data=json.dumps(g).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
            j = json.load(urllib.request.urlopen(r, timeout=300))
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert('RGB').resize((1024, 1024), Image.LANCZOS).save(OUT + f'{h}-{slug}.jpg', quality=90)
                    return f'{h}-{slug} tamam'
            hata = 'görsel yok'
        except Exception as e:
            hata = str(e)[:120]
    return f'{h}-{slug} HATA {hata}'

os.makedirs(OUT, exist_ok=True)
harfler = sys.argv[1:] or list(STIL)
def stil_sirayla(h):
    # aynı stilde kişiler sırayla: sonraki kişi öncekinin çıktısını stil örneği olarak görür
    return [uret(s, h) for s in KISI]
with cf.ThreadPoolExecutor(3) as ex:
    for sonuc in ex.map(stil_sirayla, harfler):
        print('\n'.join(sonuc), flush=True)
