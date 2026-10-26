import base64, json, os, io, sys, glob, urllib.request, concurrent.futures as cf
from PIL import Image, ImageOps
KEY=os.environ.get('GEMINI_API_KEY'); O='docs/ekip/orijinal/'; OUT='docs/ekip/yz/'
ANA={'omer-cihan-demir':'omer-cihan-demir-canva','adem-baglan':'adem-baglan-canva','aslihan-okumus':'aslihan-okumus-canva',
'muhammed-efe-coskunpinar':'muhammed-efe-coskunpinar-canva','mehmet-onur-genc':'mehmet-onur-genc-kare'}
SLUGS=sorted(os.path.basename(p)[:-4] for p in glob.glob('public/media/ekip/*.jpg'))
def refs(s):
    ana=O+ANA.get(s,s)+'.jpg'
    if not os.path.exists(ana): ana=O+s+'-canva.jpg'
    diger=[p for p in sorted(glob.glob(O+s+'*.jpg')) if p!=ana and 'grup' not in p and 'bilgehan' not in p.replace(O+s,'') and 'kursu' not in p]
    # ayni fotografin kopyasini ele
    diger=[p for p in diger if not (p.endswith('-canva.jpg') and os.path.exists(O+s+'.jpg'))]
    EK={'omer-cihan-demir':[O+'omer-cihan-demir-yakin.jpg',O+'omer-cihan-demir.jpg'],'irmak-karaagac':['docs/ekip/alternatif/irmak-karaagac.jpg']}
    return ana, EK.get(s,diger[:3])
def b64(p,m=1536):
    im=ImageOps.exif_transpose(Image.open(p)).convert('RGB'); im.thumbnail((m,m)); b=io.BytesIO(); im.save(b,'JPEG',quality=92); return base64.b64encode(b.getvalue()).decode()
img=lambda p,m=1536: {"inlineData":{"mimeType":"image/jpeg","data":b64(p,m)}}
KADRAJ=("Recompose THIS SAME photograph as a clean square head-and-shoulders portrait: subject centred, eyes at about 40% from the top, comfortable headroom above the hair or headscarf, both shoulders visible. Zoom in so that the head (from chin to top of hair or headscarf) is about 40% of the image height; if the person is far away, crop in closer. "
 "Only extend or crop the background where needed so nothing is cut off. Keep the face, identity, expression, hair, headscarf, glasses, clothing, skin texture, lighting and background scene exactly as in the photo. "
 "Do not beautify, slim, smooth or change any facial feature. No added hands, objects or text. Photorealistic.")
VESIKA=("Make a standard ID-card / team-card portrait photograph of this same real person. Front-facing head and shoulders, centred, eyes at about 40% from the top, space above the head, "
 "plain pure white seamless studio background, soft even studio lighting, natural relaxed expression (a slight smile is fine). Keep the same hairstyle, headscarf if any, glasses if any, and the same clothing tidied up. "
 "The face must be the exact same person: do not beautify, slim, smooth skin, change eye or nose shape, or alter age. No hands, no text, no logos. Photorealistic camera photo, not an illustration.")
def cagir(parts):
    g={"contents":[{"role":"user","parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1"}}}
    hata=''
    for _ in range(3):
        try:
            r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(g).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
            j=json.load(urllib.request.urlopen(r,timeout=300))
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p: return Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert('RGB'),''
            hata='görsel yok'
        except Exception as e: hata=str(e)[:120]
    return None,hata
def is_(a):
    s,tur=a; ana,diger=refs(s); out=f'{OUT}{tur}/{s}.jpg'
    if os.path.exists(out): return f'{s} {tur} var'
    SIKI=os.environ.get('SIKI')=='1'
    if SIKI and tur=='kadraj':
        parts=[{"text":"Already cropped close-up of the person (keep this framing scale, only fix it):"},img('public/media/ekip/'+s+'.jpg'),{"text":"Full original photo, for context only:"},img(ana,1024)]
    else: parts=[{"text":"Main photo of the person:"},img(ana)]
    if diger: parts+=[{"text":"Other photos of the SAME person, only to help keep the likeness:"}]+[img(d,1024) for d in diger]
    parts+=[{"text":(KADRAJ if tur=='kadraj' else VESIKA)+(' The head must be large: about 45% of the image height; the person fills the frame from mid-chest up. Never show the full body.' if SIKI else '')}]
    im,h=cagir(parts)
    if im is None: return f'{s} {tur} HATA {h}'
    im.resize((1024,1024),Image.LANCZOS).save(out,quality=90); return f'{s} {tur} tamam ({len(diger)} ek ref)'
os.makedirs(OUT+'kadraj',exist_ok=True); os.makedirs(OUT+'vesikalik',exist_ok=True)
isler=[(s,t) for s in (sys.argv[1].split(',') if len(sys.argv)>1 else SLUGS) for t in ('kadraj','vesikalik')]
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(is_,isler): print(r,flush=True)
