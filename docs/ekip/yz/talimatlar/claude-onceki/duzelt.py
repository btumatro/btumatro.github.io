import base64, json, os, io, sys, urllib.request, concurrent.futures as cf
from PIL import Image, ImageOps
sys.path.insert(0,os.path.dirname(__file__)); from kisiler import S
KEY=os.environ['GEMINI_API_KEY']; O='docs/ekip/orijinal/'; P='docs/ekip/stilize/portre/'
def b64(p,m=1280):
    im=ImageOps.exif_transpose(Image.open(p)).convert('RGB'); im.thumbnail((m,m)); b=io.BytesIO(); im.save(b,'JPEG',quality=90); return base64.b64encode(b.getvalue()).decode()
img=lambda p,m=1280: {"inlineData":{"mimeType":"image/jpeg","data":b64(p,m)}}
CAPA=[P+'zehra-bulut.jpg',P+'nusret-bircan-keser.jpg',P+'aslihan-okumus.jpg']
IS={
"omer-cihan-demir":([f'{S}/ref/omer-cihan-demir.jpg',O+'omer-cihan-demir-luna-2.jpg',O+'omer-cihan-demir-luna-3.jpg'],
 "He is a 21-year-old university student; draw him young (early twenties), not older. Long narrow face, prominent straight nose, thick straight eyebrows close to the eyes, deep-set eyes, short thick dark hair, full dark beard. Use a calm closed-mouth slight smile as in the close-up photo."),
"rumeysa-akarsu":([O+'rumeysa-akarsu.jpg'],
 "The face is too small and generic. Make the head much larger (about 40 percent of image height). Her face is round and soft with full cheeks, warm skin tone, almond eyes, gentle closed smile; patterned mauve-brown satin headscarf wrapped loosely as in the photo."),
"irmak-karaagac":([f'{S}/ref/irmak-karaagac.jpg',O+'irmak-karaagac-bilgehan-1.jpg',O+'irmak-karaagac-muhammed-ataman-kursu.jpg'],
 "The face is too small and generic. Make the head larger (about 40 percent of image height). Her face: long oval face, pale skin, thick dark straight eyebrows, light hazel eyes, straight nose, soft closed smile; plain brown headscarf; olive-brown jacket."),
"melisa-aydirek":([O+'melisa-aydirek.jpg'],
 "The portrait looks like a different woman. Her face is rounder with fuller cheeks, warm tan skin, large dark brown eyes, dark brown hair (not light), a playful slight side smile and red lipstick, head slightly tilted as in the photo."),
"bilgehan-zeki-ozaytac":([O+'bilgehan-zeki-ozaytac.jpg',f'{S}/ref/bilgehan-zeki-ozaytac.jpg',O+'luna-omer-bilgehan-2.jpg'],
 "The head is far too small and he looks too old. Make the head large (about 40 percent of image height) and draw him younger-looking, smooth skin, no deep wrinkles, beard mostly dark with only a little grey. Bald round head, blue rectangular glasses, short dark beard, moustache, calm friendly face; dark brown t-shirt. In group photos he is the bald man with glasses."),
}
def uret(slug):
    refs,not_=IS[slug]
    parts=[{"text":"We are making a consistent set of watercolor team portraits. These three finished portraits define the style, framing and paper background that every portrait must share:"}]+[img(c,768) for c in CAPA]
    parts+=[{"text":"Real reference photos of the person to draw (likeness must come from these):"}]+[img(r) for r in refs]
    parts+=[{"text":"Our current portrait of this person, which needs correction:"},img(P+slug+'.jpg',768)] if slug!='omer-cihan-demir' else []
    parts+=[{"text":"Redraw this person's portrait. Corrections: "+not_+" Keep the exact same style, paper background, head-and-shoulders framing with space above the head as the three style portraits. Faithful likeness first; do not beautify. No text. Square image."}]
    g={"contents":[{"role":"user","parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1"}}}
    hata=''
    for _ in range(3):
        try:
            r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(g).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
            j=json.load(urllib.request.urlopen(r,timeout=300))
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert('RGB').resize((800,800),Image.LANCZOS).save(f'{S}/yeni-{slug}.jpg',quality=88); return slug+' tamam'
            hata='görsel yok'
        except Exception as e: hata=str(e)[:150]
    return slug+' HATA '+hata
with cf.ThreadPoolExecutor(5) as ex:
    for s in ex.map(uret, sys.argv[1].split(',') if len(sys.argv)>1 else IS): print(s)
