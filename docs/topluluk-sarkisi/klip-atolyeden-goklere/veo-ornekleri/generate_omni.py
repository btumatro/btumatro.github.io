#!/usr/bin/env python3
"""Gerçek MATRO fotoğraflarından Gemini Omni ile kısa klip planları üretir."""
import argparse
import base64
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
MODEL = 'gemini-omni-1.1-flash'
SCENES = {
    'prusa-sinematik': {
        'image': '../ana-kareler/prusa-sinematik.png',
        'prompt': 'Animate this exact professional workshop documentary still as one continuous eight-second shot. The red PRUSA underwater vehicle remains stationary on the table. Camera makes only a slow 20-centimetre lateral slide at the same height; soft window light shifts very slightly across the existing shell. Preserve the exact red vented body, front grille, cream ducted thrusters and their current positions and count. Do not rotate propellers or add anything. No water, bubbles, lights, people, text, redesign, cuts, dialogue or music.'
    },
    'ashina-sinematik': {
        'image': '../ana-kareler/ashina-sinematik.png',
        'prompt': 'Animate this exact professional workshop documentary still as one continuous eight-second shot. The camera makes only a slow 20-centimetre forward move at bench height. The existing unfinished electronics assembly, tall capacitors, exposed wires, tools and cutting mat remain completely still and physically identical throughout. Gentle natural window light and soft background depth, with no sparks, glowing electronics, autonomous assembly, extra tools, people, text, cuts, dialogue or music.'
    },
    'matris-sinematik': {
        'image': '../ana-kareler/matris-sinematik.png',
        'prompt': 'Animate this exact professional documentary still as one continuous eight-second film shot. Two separate real quadcopters remain grounded in their exact positions. Camera makes only a restrained 20-centimetre lateral dolly at grass height, with delicate natural grass movement and stable late-afternoon shadows. Preserve both aircraft frame geometry, exact rotor and arm count, antennas, legs, colors and distance throughout. No flight, no new hardware, no morphing or melting, no people, no text, no cuts, no dialogue or music.'
    },
    'lodos-sinematik': {
        'image': '../ana-kareler/lodos-sinematik.png',
        'prompt': 'Animate this exact professional documentary still as one continuous eight-second shot. The current grey LODOS boat and its existing trolley stay entirely stationary on the pier. Camera performs only a very slow 20-centimetre push from the same three-quarter front angle; sea surface moves gently and clouds drift almost imperceptibly. Preserve every visible aspect of the existing hull, raised cabin, Turkish flag, red LODOS letters, side pontoon, trolley, red wheel and their proportions. No extra parts, no redesign, no launching, no people, no text overlays, no cuts, no dialogue or music.'
    },
    'zemheri-sinematik': {
        'image': '../ana-kareler/zemheri-sinematik.png',
        'prompt': 'Animate this exact professional night documentary still as one continuous eight-second shot. Camera makes a very slow low 20-centimetre lateral move along the wooden pier. The existing team members make only small natural hand and posture movements while the real work light reflects softly on the water. Preserve the pier, four people, white-and-red cylindrical test object, practical light, shore and city lights. No launch, no spectacle, no extra faces or equipment, no visual effects, no text, no cuts, no dialogue or music.'
    },
    'ashina-atolye': {
        'image': 'referanslar/ashina-atolye-ilk-kare.jpg',
        'prompt': 'An eight-second single continuous documentary close shot of this exact electronics workbench photograph. A restrained 30-centimetre camera push-in toward the existing electronics assembly. No person enters. The wires, capacitors, boards, taped components, yellow base, cutting mat, pliers and surrounding workbench stay in their exact locations and shapes; nothing assembles itself or moves independently. Soft practical workshop light with restrained warm highlights and natural material texture, cinematic but unmistakably real. Keep the background cabinets and papers stable. No new tools, no spinning blades, no sparks, no captions, no new readable text, no cuts, no dialogue or music.'
    },
    'zemheri-gece': {
        'image': 'referanslar/zemheri-ilk-kare.jpg',
        'prompt': 'An eight-second single unbroken documentary shot from this exact night pier photograph. The people continue their existing careful preparation with only tiny natural movements; the person at the water edge keeps the same posture and does not enter the water. The practical work light softly shimmers on the dark water and the distant city lights flicker gently. Camera makes a slow, stable 30-centimetre lateral move along the pier at the same eye level. Preserve the exact people count, pier boards, cables, equipment, shoreline and light positions. Natural night exposure, detailed shadows, restrained cinematic contrast, no fantasy effects. Do not invent a rocket launch, new people, signs, text, dramatic gestures or cuts. No dialogue or music.'
    },
    'matris-saha': {
        'image': 'referanslar/matris-ilk-kare.jpg',
        'prompt': 'An eight-second single continuous documentary shot of the two actual quadcopters in this exact reference photograph, resting in the same positions on the grass. The camera makes a very slow low lateral track from left to right, giving subtle depth between the nearer and farther aircraft. The aircraft stay grounded; no takeoff. Only tiny natural grass motion in the breeze. Preserve exactly two separate aircraft, their existing rotor and arm counts, landing legs, exposed electronics, colors, proportions, background fence and field markings. Physically plausible late afternoon light, gentle shallow depth of field, restrained cinematic color, real field texture. No extra drones, no morphing parts, no new signage or text, no cuts, no dialogue or music.'
    },
    'lodos-kiyi': {
        'image': 'referanslar/lodos-ilk-kare.jpg',
        'prompt': 'An eight-second single unbroken documentary shot based on this exact team photograph at the waterfront. The current grey LODOS unmanned boat remains stationary on its trolley at the same place. The camera makes a subtle smooth push toward the boat while the people keep relaxed natural poses with only tiny real-life movements. Preserve the exact raised opaque grey cabin, Turkish flag on top, grey hull, red LODOS lettering, red wheel, trolley, team clothing, human identities and number of people. Real waterfront daylight, slightly restrained cinematic contrast and natural skin tones. The boat must not enter the water or turn into a different model. No added controls, windows, antennas, hulls, faces, hands, signs, text or cuts. No dialogue or music.'
    },
    'ashina-flight-concept': {
        'image': '../assets/konsept-ashina-atolye.png',
        'prompt': 'Animate this already-created cinematic concept frame as one restrained eight-second shot. Keep the exact single fixed-wing ASHINA aircraft, all wings, motors, propellers, landing gear and proportions completely unchanged and stationary in the workshop. Only the camera performs a slow low dolly from left to right, revealing a little more depth in the existing hangar; practical window light stays steady. Preserve the image as a cinematic visualization, not archival footage. No takeoff, no spinning propellers, no extra aircraft, no added parts, no people, no text, no logos, no sparks, no cuts, no dialogue or music.'
    },
    'ashina-kalkis-concept': {
        'image': '../assets/konsept-ashina-kalkis.png',
        'prompt': 'Animate this already-created cinematic concept frame as a single eight-second AI visualization of the exact fixed-wing ASHINA aircraft shown. The aircraft makes a short, believable low takeoff from the same runway and climbs only slightly; use a gentle low tracking camera that follows from behind-left. Keep its wing outline, fuselage, visible motors, propellers, landing gear and markings exactly consistent with the reference. No dramatic banking, no extra aircraft, no new hardware, no morphing, no extra rotors, no text, no logos, no crowd, no cuts, dialogue or music. This is a concept visualization, not documentary footage.'
    },
    'lodos-seyir-concept': {
        'image': '../assets/konsept-lodos-seyir.png',
        'prompt': 'Animate this already-created cinematic concept frame as one restrained eight-second documentary visualization. The same current grey LODOS boat proceeds slowly in the direction already shown, leaving only a small natural wake. Camera tracks parallel at water height with a very gentle lateral move. Preserve the existing raised opaque cabin, Turkish flag, grey angular hull, side pontoons, red LODOS lettering and all visible proportions exactly. Keep the current shoreline, sea and light direction. No redesign, extra hardware, windows, boats, people, signs, text, splash spectacle, cuts, dialogue or music.'
    },
    'matris-ucus-concept': {
        'image': '../assets/konsept-matris-suru-ucus.png',
        'prompt': 'Animate this already-created cinematic concept frame as one continuous eight-second shot. The exact two separate MATRİS quadcopters hold their present low hover and spacing over the test field. Camera makes a slow lateral tracking move at low height; grass and shadows move naturally. Preserve each aircraft frame, rotor count, arm count, landing gear, exposed electronics, color and relative position. This is an AI visualization, not race footage. No third drone, no new hardware, no morphing, no camera orbit, no text or logos, no cuts, no dialogue or music.'
    },
    'prusa-sualti-concept': {
        'image': '../assets/konsept-prusa-sualti.png',
        'prompt': 'Animate this already-created cinematic underwater concept as one unbroken eight-second shot. The single red PRUSA ROV remains the same size, shape and orientation while gliding forward very slowly through the clear test pool; camera tracks alongside at the same depth. Preserve the rounded red vented shell, front grille and exact visible cream ducted thrusters and positions. Natural sun caustics drift softly across the pool, restrained documentary color, no dramatic bubbles or particles. Do not add arms, thrusters, lights, cables, people, text or logos; no redesign, cuts, dialogue or music. Clearly a cinematic visualization, not archival test footage.'
    },
    'gece-iskele-concept': {
        'image': '../assets/konsept-gece-iskele.png',
        'prompt': 'Animate this already-created cinematic night-test visualization as a single continuous eight-second observational shot. Keep the same small group, work light, pier, equipment and skyline in their exact positions; people stay mostly still and natural. Camera makes a slow push-in along the real wooden boards toward the testing area. Only subtle water reflections and distant lights shimmer; preserve deep night exposure, practical lighting and natural shadows. No launch, no added people or equipment, no exaggerated movement, no neon, no text, no logos, no cuts, no dialogue or music.'
    },
    'ashina-vakum-concept': {
        'image': '../assets/konsept-ashina-vakum-islem.png',
        'prompt': 'Animate this polished cinematic ASHINA workshop still as one calm eight-second documentary shot. Slow macro-to-medium slider move across the existing vacuum bagging work, maintaining the exact aircraft part, tools, gloved hands and bench layout. Only restrained hand movement as the existing material is checked; no new tools, no new people, no invented aircraft parts, no sparks, no readable text, no logos, no cuts, dialogue or music.'
    },
    'prusa-workshop-concept': {
        'image': '../assets/konsept-prusa-atolye.png',
        'prompt': 'Animate this polished cinematic PRUSA workshop still as one continuous eight-second shot. The exact red underwater vehicle stays fixed on the workbench; camera makes a slow low lateral dolly past its nose, revealing the existing cream ducted thrusters and workshop depth. Preserve exact vehicle shape and all visible component counts. Soft practical light, subtle parallax only; no propeller movement, water, bubbles, new parts, text, logos, cuts, dialogue or music.'
    },
    'lodos-sahil-concept': {
        'image': '../assets/konsept-lodos-guncel-sahil.png',
        'prompt': 'Animate this polished cinematic LODOS coastal still as a restrained eight-second image-to-video shot. The exact grey unmanned surface vessel stays in the shown position, moving forward only very slowly on calm water; a small natural wake forms behind it. Low waterline camera tracks parallel with a gentle dolly. Preserve hull, cabin, pontoons, flag, lettering and proportions exactly. No new hardware, vessels, people, text, dramatic spray, cuts, dialogue or music.'
    },
    'matris-field-concept': {
        'image': '../assets/konsept-matris-saha.png',
        'prompt': 'Animate this polished cinematic MATRİS field still as one eight-second shot. Both exact quadcopters remain grounded in their original positions. The camera makes a slow low push-in between foreground grass and the nearer aircraft; only grass tips and natural light shift gently. Preserve exactly two aircraft and every visible rotor, arm, landing leg and electronic detail. No takeoff, new drone, invented parts, text, logos, cuts, dialogue or music.'
    },
}

def find_video(payload):
    out = []
    def walk(node):
        if isinstance(node, dict):
            if node.get('type') == 'video' and isinstance(node.get('data'), str):
                out.append(base64.b64decode(node['data']))
            for key, val in node.items():
                if key != 'data': walk(val)
        elif isinstance(node, list):
            for val in node: walk(val)
    walk(payload)
    if not out: raise RuntimeError('Gemini yanıtında video bulunmadı.')
    return out[-1]

p = argparse.ArgumentParser()
p.add_argument('scene', choices=SCENES)
a = p.parse_args()
key = os.getenv('GEMINI_API_KEY')
if not key: raise SystemExit('GEMINI_API_KEY eksik.')
scene = SCENES[a.scene]
ref = ROOT / scene['image']
mime = 'image/png' if ref.suffix.lower() == '.png' else 'image/jpeg'
body = {
    'model': MODEL,
    'input': [
        {'type': 'image', 'data': base64.b64encode(ref.read_bytes()).decode(), 'mime_type': mime},
        {'type': 'text', 'text': scene['prompt']},
    ],
    'response_format': {'type': 'video', 'aspect_ratio': '16:9'},
    'generation_config': {'video_config': {'task': 'image_to_video'}},
}
request = urllib.request.Request(
    'https://generativelanguage.googleapis.com/v1beta/interactions',
    data=json.dumps(body).encode(),
    headers={'Content-Type': 'application/json', 'x-goog-api-key': key, 'Api-Revision': '2026-05-20'},
    method='POST',
)
try:
    with urllib.request.urlopen(request, timeout=480) as response:
        result = json.loads(response.read())
except urllib.error.HTTPError as error:
    raise SystemExit(f'Gemini HTTP {error.code}; yanıt gövdesi gizlendi.') from None
video = find_video(result)
out = ROOT / 'videolar' / f'{a.scene}-omni.mp4'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(video)
metadata = {'model': MODEL, 'scene': a.scene, 'reference': scene['image'], 'prompt': scene['prompt'], 'interaction_id': result.get('id')}
(ROOT / 'videolar' / f'{a.scene}-omni.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
print(f'Üretildi: {out} ({len(video):,} bayt)')
