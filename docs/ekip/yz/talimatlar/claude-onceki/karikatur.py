import base64, json, os, io, urllib.request, concurrent.futures as cf
from PIL import Image
KEY=os.environ['GEMINI_API_KEY']; P='docs/ekip/stilize/portre/'
def img(p,m=768):
    im=Image.open(p).convert('RGB'); im.thumbnail((m,m)); b=io.BytesIO(); im.save(b,'JPEG',quality=88); return {"inlineData":{"mimeType":"image/jpeg","data":base64.b64encode(b.getvalue()).decode()}}
REF=[{"text":"Character A, Irmak: young woman, plain brown headscarf, olive-brown jacket:"},img(P+'irmak-karaagac.jpg'),img('public/media/ekip/irmak-karaagac.jpg'),
     {"text":"Character B, Bilgehan: bald man, blue rectangular glasses, short dark beard, dark brown t-shirt:"},img(P+'bilgehan-zeki-ozaytac.jpg'),
     {"text":"Team group picture style reference (yellow steel workshop):"},img('docs/ekip/stilize/ekip-toplu-vektor.png',1024)]
STIL=("Style: funny editorial cartoon, clean bold ink outlines with soft watercolor fills, expressive exaggerated faces, warm colors, keep both characters clearly recognizable from the references. "
"Wholesome slapstick humor, nothing violent or scary. Absolutely no text, no letters, no speech bubbles, no captions. Square panel.")
SAHNE={
"1":"Panel: Character A stands in the workshop holding her phone, looking sheepish and pleading with puppy eyes, hands pressed together, asking for a favor; in the background on the wall hangs a framed team group illustration.",
"2":"Panel: Character B at a workbench rolls up his sleeves with an evil-genius grin, glasses glinting, lifting a comically giant pink pencil eraser like a hero holding a sword; the framed team group illustration is in front of him.",
"3":"Panel: Character B scrubs the framed team group illustration with the giant pink eraser, eraser crumbs flying; inside the picture Character A is half-erased (her lower half is faded to blank paper) and she stares out with the shocked wide-eyed face of a tiny startled monkey, hands to cheeks. The other people in the picture keep smiling.",
"4":"Panel: plot twist. Character B stares in disbelief, jaw dropped, eraser falling from his hand, because the framed team group illustration is now filled with MANY copies of Character A in every spot, all smiling and giving thumbs up; a small laptop on the bench glows proudly.",
}
def uret(k):
    g={"contents":[{"parts":REF+[{"text":SAHNE[k]+" "+STIL}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1"}}}
    hata=''
    for _ in range(3):
        try:
            r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(g).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
            j=json.load(urllib.request.urlopen(r,timeout=300))
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert('RGB').resize((1000,1000),Image.LANCZOS).save(f'docs/ekip/karikatur/kare-{k}.jpg',quality=90); return k+' tamam'
            hata='görsel yok'
        except Exception as e: hata=str(e)[:150]
    return k+' HATA '+hata
with cf.ThreadPoolExecutor(4) as ex:
    for s in ex.map(uret,SAHNE): print(s)
