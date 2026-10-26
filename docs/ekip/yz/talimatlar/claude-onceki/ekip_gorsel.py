import base64, json, os, sys, urllib.request, concurrent.futures as cf
KEY=os.environ['GEMINI_API_KEY']
REF=base64.b64encode(open(sys.argv[1],'rb').read()).decode()
ORTAK=("The reference image is a grid of 17 portrait photos of real members of a university robotics club. "
"Create ONE group picture where all 17 people appear together, each one clearly recognizable from their own reference portrait: "
"keep each person's face shape, skin tone, hair or headscarf style and color, glasses, and beard exactly. Exactly 17 people, no extra people, no duplicates. "
"Scene: a bright university robotics workshop, people standing and sitting in two or three rows, friendly confident expressions, "
"around them a small unmanned ground vehicle, a quadcopter drone, an underwater ROV and a robot arm on workbenches. "
"Everyone wears casual clothes in dark navy and black with small lime green accents. No text, no letters, no logos, no watermarks. Wide 16:9 composition. Style: ")
STIL={"vektor":"modern flat vector editorial illustration, clean geometric shapes, soft gradients, limited palette of deep navy, slate and lime green accents.",
"animasyon":"stylized 3D animated feature film look, soft global illumination, appealing slightly stylized proportions, warm cinematic lighting.",
"cizgi-roman":"graphic novel illustration, confident ink lines with muted watercolor washes, dynamic but readable composition."}
def uret(ad):
    govde={"contents":[{"parts":[{"inlineData":{"mimeType":"image/jpeg","data":REF}},{"text":ORTAK+STIL[ad]}]}],
           "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9"}}}
    for deneme in range(3):
        try:
            r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",
              data=json.dumps(govde).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
            j=json.load(urllib.request.urlopen(r,timeout=300))
            for p in j["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    open(f"docs/ekip/stilize/ekip-{ad}.png","wb").write(base64.b64decode(p["inlineData"]["data"])); return ad+" tamam"
            return ad+" görsel yok: "+str(j["candidates"][0].get("finishReason"))
        except Exception as e: hata=str(e)[:200]
    return ad+" hata: "+hata
with cf.ThreadPoolExecutor(3) as ex:
    for s in ex.map(uret, STIL): print(s)
