#!/usr/bin/env python3
"""Gerçek araç referanslarından profesyonel sinematik ana kareler üretir."""
import argparse, base64, json, os, urllib.request, urllib.error
from pathlib import Path
HERE = Path(__file__).resolve().parent
MEDIA = HERE.parents[3] / 'public/media'
MODEL = 'gemini-3-pro-image'
SCENES = {
  'prusa': {
    'images': ['galeri-prusa-detay.jpg','galeri-prusa-teknofest.jpg'],
    'prompt': 'Create a single premium 16:9 cinematic documentary still of the ACTUAL red PRUSA unmanned underwater vehicle in the two provided event photographs. This is an improved professional product photograph at a real workshop display table, NOT underwater and NOT a redesign. Match its unique wide red vented upper shell, rounded honeycomb nose grille, cream-colored ducted side thrusters, frame arrangement and compact proportions exactly. Three-quarter low front angle at table height, 50 mm lens look, soft directional window light and restrained cool shadow with fine natural grain. Background workshop is softly out of focus. The vehicle rests physically on the table and casts a coherent contact shadow. Remove the event placard and surrounding people from the new composition, but preserve the actual vehicle. No extra propellers, fins, wires, lights, logos, text, people, water, bubbles or sci-fi glow. Photographic not CGI.'
  },
  'ashina': {
    'images': ['galeri-ashina-sunum-elektronik-masa.jpg','galeri-ashina-uretim.jpg'],
    'prompt': 'Make one premium 16:9 cinematic documentary photograph based on the supplied real ASHİNA workshop photographs. Primary subject is the exact unfinished electronics assembly on the yellow box from the FIRST image, with its existing green circuit board, tall black capacitors, heat-shrink wiring and surrounding tools. Keep all components plausible and physically attached in the same places. The SECOND image is context for the team aircraft development only; do not combine a plane with the electronics or add a plane to this shot. Camera at bench height with a 50 mm lens look, tight but breathable composition, gentle directional window light from camera left, practical workshop shadows, a hint of warmer background depth, natural surfaces and subtle film grain. Professional exposure and color grading, photographic not illustrated, no neon, no glowing circuits, no sparks, no people, no text, no duplicated components or tools.'
  },
  'matris': {
    'images': ['galeri-matris-sunum-saha-iki-iha.jpg','galeri-matris-test-ucus.jpg'],
    'prompt': 'Use the two provided photographs as the sole technical identity reference for the MATRİS team aircraft. Create one premium 16:9 cinematic documentary still, as if photographed professionally at the real outdoor test field. Exactly TWO distinct exposed-frame quadcopters rest on short field grass, one near camera left and one behind to the right, each retaining its own real rotor count, arms, landing legs, exposed electronics, antennas, colors and proportions from the reference photographs. Low camera at grass height, 50 mm lens look, restrained shallow depth of field, late-afternoon side light with coherent soft shadows, neutral real grass, slight atmospheric depth. Composition follows a subtle diagonal between the two machines and leaves breathable negative space above. Fine natural photographic grain, realistic imperfections, no glossy CGI, no neon, no lens flare. No people, no extra drones, no invented rotors or panels, no text, no logos, no captions. Prioritize technical fidelity over dramatic effect.'
  },
  'lodos': {
    'images': ['galeri-lodos-ekip-sahil.jpg','takim-lodos.jpg'],
    'prompt': 'Use BOTH supplied photographs to identify the current grey LODOS unmanned surface boat, not any older white version. Make a premium 16:9 cinematic documentary still of THIS EXACT grey boat alone, stationary on its EXISTING small launch trolley at a Bursa waterfront pier just before the test. Preserve the raised opaque grey cabin with the Turkish flag on top, the compact angular hull, side pontoon arrangement, current red LODOS lettering, the existing trolley structure and all visible hardware proportions. Do not redesign the hull, add windows, antenna, knobs, wings, extra boats, or change the lettering. No people in the new frame. Camera 35 mm at boat height, three-quarter front view that stays close to the reference geometry. Natural overcast late-afternoon light with a warm break near the horizon, restrained cool shadows, real concrete, real water, coherent contact shadows. Clean professional exposure and subtle film grain. Understated factual documentary photograph, not CGI, not a concept redesign. No title or graphical overlay.'
  },
  'zemheri': {
    'images': ['galeri-zemheri-gece-iskele-testi.jpg','galeri-zemheri-sunum-gece-su-testi.jpg'],
    'prompt': 'Create one professional 16:9 cinematic documentary still of the actual night water test in the supplied photographs. Preserve the same simple wooden pier, practical white work light at the water edge, dark water, distant city lights and restrained team activity. Photograph from a lower position near the pier boards with a 35 mm lens look, strong foreground wood texture leading toward the small working group. Faces are not foregrounded; workers are natural silhouettes and nobody has an exaggerated expression. Keep equipment and people physically plausible, no rocket launch, no fire, no new machinery. Deep navy night shadows, warm city lights, a single cool work light, detailed but natural exposure, subtle fine grain, no neon, no fantasy glow, no text, no logo, no invented event.'
  }
}
def image_data(payload):
  found=[]
  def walk(node):
    if isinstance(node,dict):
      if node.get('type')=='image' and isinstance(node.get('data'),str): found.append(base64.b64decode(node['data']))
      for k,v in node.items():
        if k!='data':walk(v)
    elif isinstance(node,list):
      for v in node:walk(v)
  walk(payload)
  if not found: raise RuntimeError('Gemini yanıtında görsel bulunamadı.')
  return found[-1]
p=argparse.ArgumentParser();p.add_argument('scene',choices=SCENES);a=p.parse_args()
key=os.getenv('GEMINI_API_KEY')
if not key:raise SystemExit('GEMINI_API_KEY eksik.')
s=SCENES[a.scene]
inputs=[{'type':'text','text':s['prompt']}]
for f in s['images']:
  inputs.append({'type':'image','data':base64.b64encode((MEDIA/f).read_bytes()).decode(),'mime_type':'image/jpeg'})
body={'model':MODEL,'input':inputs,'response_format':{'type':'image','aspect_ratio':'16:9','image_size':'2K'}}
req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/interactions',data=json.dumps(body).encode(),headers={'Content-Type':'application/json','x-goog-api-key':key},method='POST')
try:
  with urllib.request.urlopen(req,timeout=300) as response: result=json.loads(response.read())
except urllib.error.HTTPError as error: raise SystemExit(f'Gemini HTTP {error.code}; yanıt gövdesi gizlendi.') from None
out=HERE/f'{a.scene}-sinematik.png';out.write_bytes(image_data(result))
(HERE/f'{a.scene}-sinematik.json').write_text(json.dumps({'model':MODEL,'references':s['images'],'prompt':s['prompt'],'interaction_id':result.get('id')},ensure_ascii=False,indent=2))
print(f'Üretildi: {out} ({out.stat().st_size:,} bayt)')
