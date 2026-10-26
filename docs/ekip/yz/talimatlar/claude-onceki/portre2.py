import base64, json, os, io, sys, urllib.request, concurrent.futures as cf
from PIL import Image, ImageOps
KEY=os.environ['GEMINI_API_KEY']; O='docs/ekip/orijinal/'
STIL=("Style: soft editorial watercolor and colored pencil illustration, visible paper texture, gentle warm light. "
"Framing: head and shoulders bust, head about 40 percent of the image height, generous space above the head, centered, cropped at mid-chest. "
"Background: plain warm cream paper with a very light watercolor wash. No text, no logos, no frame. Square image. "
"Faithful likeness is the top priority: keep face shape, eyes, nose, lips, eyebrows, skin tone, age, hair or headscarf, glasses and beard exactly; do not beautify or slim.")
IS={
"muhammed-ataman":(["muhammed-ataman-yuz-1.jpg","muhammed-ataman-yuz-2.jpg","muhammed-ataman-yuz-3.jpg"],
 "All three references are the same man, mid 30s: wavy dark brown hair swept back with some volume, full dark beard and moustache neatly trimmed, warm brown eyes, slight friendly smile, rounded cheeks. Keep his real proportions and age. Black zip-up fleece jacket. "),
"omer-cihan-demir":(["omer-cihan-demir-yakin.jpg","omer-cihan-demir-luna-2.jpg","omer-cihan-demir-luna-1.jpg","omer-cihan-demir-luna-3.jpg"],
 "All four references are close-ups of the same man, around 30 years old. Copy his exact facial structure: long narrow face with a strong jaw, short thick dark hair cut short on the sides with a little volume on top, thick straight dark eyebrows, slightly hooded deep-set eyes, long straight prominent nose, full dark beard trimmed close on the cheeks, dark moustache. He is NOT a generic young model: keep his real proportions and age. Natural friendly smile showing teeth, black t-shirt. "),
"irmak-karaagac":(["irmak-karaagac-bilgehan-1.jpg","irmak-karaagac-bilgehan-2.jpg"],
 "Draw a portrait of the young woman wearing the brown headscarf (not the bald man with glasses): same headscarf color and wrapping, same olive-brown jacket, gentle smile. "),
"bilgehan-zeki-ozaytac":(["bilgehan-zeki-ozaytac.jpg","luna-omer-bilgehan-2.jpg","irmak-karaagac-bilgehan-1.jpg"],
 "All references show the same bald man with a short dark beard and moustache: in the group photos he is the bald man wearing blue rectangular glasses (not the other people). Draw a portrait of him only, wearing his blue rectangular glasses, short greying dark beard, calm friendly smile, dark brown t-shirt. "),
}
def b64(p):
    im=ImageOps.exif_transpose(Image.open(O+p)).convert('RGB'); im.thumbnail((1600,1600)); b=io.BytesIO(); im.save(b,'JPEG',quality=90); return base64.b64encode(b.getvalue()).decode()
def uret(slug):
    refs,ek=IS[slug]
    parts=[{"inlineData":{"mimeType":"image/jpeg","data":b64(r)}} for r in refs]+[{"text":"Create a portrait illustration from these reference photos. "+ek+STIL}]
    g={"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1"}}}
    hata=''
    for _ in range(3):
        try:
            r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(g).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
            j=json.load(urllib.request.urlopen(r,timeout=300))
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert('RGB').resize((800,800),Image.LANCZOS).save(f'docs/ekip/stilize/portre/{slug}.jpg',quality=88); return slug+' tamam'
            hata='görsel yok'
        except Exception as e: hata=str(e)[:150]
    return slug+' HATA '+hata
with cf.ThreadPoolExecutor(3) as ex:
    for s in ex.map(uret, sys.argv[1].split(',') if len(sys.argv)>1 else IS): print(s)
