import base64, json, os, sys, io, urllib.request, concurrent.futures as cf
from PIL import Image, ImageOps
KEY=os.environ['GEMINI_API_KEY']
PROMPT=("Create a portrait illustration of the exact person in the reference photo. Faithful likeness is the top priority: "
"keep their face shape, eye shape, nose, lips, eyebrows, skin tone, age, hair or headscarf (same color, pattern and wrapping), glasses frame shape and color, beard or moustache exactly as in the photo. "
"Do not beautify, slim, or change ethnicity. Same clothing colors as the photo. "
"Framing: head and shoulders, facing the viewer as in the photo, head centered horizontally, generous space above the head (about 15 percent of the height), shoulders reaching the bottom edge. "
"Style: soft editorial watercolor and colored pencil illustration, visible paper texture, gentle warm light. "
"Background: plain warm cream paper with a very light watercolor wash, nothing else. No text, no logos, no frame. Square image.")
EK=sys.argv[2] if len(sys.argv)>2 else ""
def uret(slug):
    im=ImageOps.exif_transpose(Image.open(f'docs/ekip/orijinal/{slug}.jpg')).convert('RGB'); im.thumbnail((1600,1600))
    b=io.BytesIO(); im.save(b,'JPEG',quality=90)
    g={"contents":[{"parts":[{"inlineData":{"mimeType":"image/jpeg","data":base64.b64encode(b.getvalue()).decode()}},{"text":PROMPT+EK}]}],
       "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1"}}}
    hata=''
    for _ in range(3):
        try:
            r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(g).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
            j=json.load(urllib.request.urlopen(r,timeout=300))
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert('RGB').resize((800,800),Image.LANCZOS).save(f'docs/ekip/stilize/portre/{slug}.jpg',quality=88)
                    return slug+' tamam'
            hata='görsel yok'
        except Exception as e: hata=str(e)[:150]
    return slug+' HATA '+hata
slugs=sys.argv[1].split(',')
with cf.ThreadPoolExecutor(6) as ex:
    for s in ex.map(uret,slugs): print(s)
