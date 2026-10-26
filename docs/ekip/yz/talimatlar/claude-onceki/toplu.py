import base64, json, os, io, sys, urllib.request, concurrent.futures as cf
from PIL import Image
KEY=os.environ['GEMINI_API_KEY']; S=sys.argv[1]
def b64(p,m):
    im=Image.open(p).convert('RGB'); im.thumbnail((m,m)); b=io.BytesIO(); im.save(b,'JPEG',quality=88); return base64.b64encode(b.getvalue()).decode()
K=[("muhammed-ataman","man, wavy dark hair, full dark beard, black fleece jacket"),
("irmak-karaagac","woman, brown headscarf, olive jacket"),
("gulsiye-begum-gumus","woman, grey patterned headscarf, sunglasses on top of head, burgundy sweater"),
("omer-cihan-demir","man about 30, short thick dark hair, full trimmed beard, long narrow face, black t-shirt"),
("yusuf-sarsici","young man, white hard hat, neon yellow safety vest, thin moustache"),
("feyza-karabicak","woman, dark brown headscarf, round thin gold glasses, cream sweater"),
("nusret-bircan-keser","young man, voluminous dark quiff, short beard, green-white scarf, navy jacket"),
("rumeysa-akarsu","woman, mauve-brown patterned silk headscarf, rust brown dress"),
("zeynep-seher-yolasigmaz","woman, short dark hair with bangs, thick black glasses, navy t-shirt"),
("berat-eren-karakas","man, curly light brown hair, thin metal glasses, moustache, black sweatshirt"),
("zehra-bulut","woman, dark brown patterned headscarf, brown top, big smile"),
("aslihan-okumus","woman, blue-grey headscarf, beige trench coat, big smile"),
("melek-ozkeser","woman, long dark auburn hair, sunglasses on head, white crochet top"),
("emine-sultan-gunes","woman, navy satin headscarf, sparkly navy top"),
("melisa-aydirek","woman, long light brown hair, gold top, red lipstick"),
("eslem-kilic","woman, long wavy brown hair, black cat-eye glasses, light striped shirt"),
("esma-demirkiyik","woman, long dark hair, sunglasses on head, white tank top, gold bracelets"),
("muhammed-efe-coskunpinar","young man, dark wavy hair, black t-shirt, blue lanyard"),
("adem-baglan","man, short dark hair, goatee beard, black blazer, white shirt"),
("bilgehan-zeki-ozaytac","bald man, blue rectangular glasses, short greying beard, brown t-shirt")]
ad={s:i+1 for i,(s,_) in enumerate(K)}
parts=[]
for i,(s,t) in enumerate(K):
    yol=f'{S}/ref/{s}.jpg' if os.path.exists(f'{S}/ref/{s}.jpg') else f'public/media/ekip/{s}.jpg'
    parts+=[{"text":f"Person {i+1} ({t}), real photo:"},{"inlineData":{"mimeType":"image/jpeg","data":b64(yol,1024)}}]
parts+=[{"text":"Workshop reference photos (our real workshop: yellow steel columns and beams, dark grey walls, white workbenches and cabinets, blue tool pegboard). Ignore the people in these photos:"},
 {"inlineData":{"mimeType":"image/jpeg","data":b64(f'{S}/atolye/IMG_2245-dik.jpg',1024)}},
 {"text":"Our vehicles (match their shapes and colors, not this drawing style):"},{"inlineData":{"mimeType":"image/jpeg","data":b64('docs/ekip/stilize/araclar-bant.png',1280)}}]
def sira(ls): return ", ".join(f"person {ad[s]}" for s in ls)
ARKA=["yusuf-sarsici","berat-eren-karakas","nusret-bircan-keser","omer-cihan-demir","muhammed-ataman","bilgehan-zeki-ozaytac","adem-baglan"]
ORTA=["muhammed-efe-coskunpinar","rumeysa-akarsu","zehra-bulut","aslihan-okumus","feyza-karabicak","gulsiye-begum-gumus","esma-demirkiyik"]
ON=["zeynep-seher-yolasigmaz","eslem-kilic","irmak-karaagac","emine-sultan-gunes","melek-ozkeser","melisa-aydirek"]
METIN=("Create ONE group illustration. Copy the art style, composition, camera angle, lighting and the way people are posed and arranged from the STYLE REFERENCE image, but replace its people with the 20 real people above. The style reference shows fewer people; our picture must have MORE: exactly 20, in three rows of 7, 7 and 6. "
"It must contain EXACTLY 20 people, persons 1 to 20, each drawn with the same face, hair or headscarf, glasses, beard and clothing as their own reference, nobody added, nobody repeated, no background crowd. "
"Faces must match each person's real photo closely (face shape, eyes, nose, skin tone, age, hair or headscarf, glasses, beard), stylized only as much as the style requires. There are 8 men and 12 women; 7 of the women wear headscarves. "
f"Back row standing, left to right: {sira(ARKA)}. Middle row standing, left to right: {sira(ORTA)}. Front row seated on workshop stools, left to right: {sira(ON)}. "
"All faces clearly visible, friendly smiles, looking at the viewer. Setting: our real workshop from the photos, with the camouflage ground vehicle on the floor at one side and the purple underwater ROV and white underwater rocket on a workbench at the other side, drones on a shelf. "
"Before finishing, count the people: back row 7, middle row 7, front row 6, total 20; nobody hidden behind others, every face fully visible. Absolutely no text, no numbers, no names, no labels, no logos anywhere.")
def uret(a):
    oran,adx,stil=a
    sr=[{"text":"STYLE REFERENCE (art style and layout only, ignore its faces):"},{"inlineData":{"mimeType":"image/png","data":b64(f'docs/ekip/stilize/{stil}.png',1400)}}]
    g={"contents":[{"parts":parts+sr+[{"text":METIN}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":oran}}}
    hata=''
    for _ in range(3):
        try:
            r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(g).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
            j=json.load(urllib.request.urlopen(r,timeout=500))
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p: open(f'docs/ekip/stilize/{adx}.png','wb').write(base64.b64decode(p["inlineData"]["data"])); return adx+' tamam'
            hata='görsel yok'
        except urllib.error.HTTPError as e: hata=f"{e.code} {e.read()[:200]}"
        except Exception as e: hata=str(e)[:200]
    return adx+' HATA '+hata
with cf.ThreadPoolExecutor(3) as ex:
    for s in ex.map(uret,[("3:2","ekip-toplu-vektor","ekip-vektor"),("3:2","ekip-toplu-animasyon","ekip-animasyon"),("3:2","ekip-toplu-cizgi-roman","ekip-cizgi-roman")]): print(s)
