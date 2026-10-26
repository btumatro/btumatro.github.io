import base64, json, os, io, sys, glob, urllib.request, concurrent.futures as cf
from PIL import Image, ImageFilter, ImageDraw
KEY=os.environ['GEMINI_API_KEY']; OUT='docs/ekip/yz/kadraj2/'; os.makedirs(OUT,exist_ok=True)
C=780; P=600; X=(C-P)//2; Y=150   # ust bosluk 150, yanlar 90, alt 30
def is_(s):
    out=OUT+s+'.jpg'
    if os.path.exists(out): return s+' var'
    src=Image.open(f'public/media/ekip/{s}.jpg').convert('RGB')
    can=Image.new('RGB',(C,C),(128,128,128)); can.paste(src,(X,Y))
    b=io.BytesIO(); can.save(b,'JPEG',quality=95)
    parts=[{"inlineData":{"mimeType":"image/jpeg","data":base64.b64encode(b.getvalue()).decode()}},
      {"text":"This photo is placed on a flat grey canvas. Outpaint: replace ONLY the flat grey border areas (top, left, right, bottom) by naturally extending the existing scene, background, hair, headscarf, shoulders and clothing so it looks like the original wider photo. Do not change anything inside the existing photo area; the person's face must stay pixel-identical. No new people, hands, objects or text. Return the full square image."}]
    g={"contents":[{"role":"user","parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1"}}}
    for _ in range(3):
        try:
            r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",data=json.dumps(g).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
            j=json.load(urllib.request.urlopen(r,timeout=300))
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    gen=Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert('RGB').resize((C,C),Image.LANCZOS)
                    import numpy as np
                    g_=np.asarray(gen,dtype=np.float32); s_=np.asarray(src,dtype=np.float32)
                    ring=np.ones((P,P),bool); ring[40:P-40,40:P-40]=False
                    d=s_[ring].mean(0)-g_[Y:Y+P,X:X+P][ring].mean(0)
                    gen=Image.fromarray(np.clip(g_+d,0,255).astype(np.uint8))
                    m=Image.new('L',(C,C),0); ImageDraw.Draw(m).rectangle((X+30,Y+30,X+P-31,Y+P-31),fill=255); m=m.filter(ImageFilter.GaussianBlur(18))
                    full=src.copy(); bg=gen.copy(); canv=Image.new('RGB',(C,C)); canv.paste(full,(X,Y))
                    bg.paste(canv,(0,0),m)
                    bg.resize((600,600),Image.LANCZOS).save(out,quality=88); return s+' tamam'
        except Exception as e: err=str(e)[:100]
    return s+' HATA'
SL=sys.argv[1].split(',') if len(sys.argv)>1 else sorted(os.path.basename(p)[:-4] for p in glob.glob('public/media/ekip/*.jpg'))
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(is_,SL): print(r,flush=True)
