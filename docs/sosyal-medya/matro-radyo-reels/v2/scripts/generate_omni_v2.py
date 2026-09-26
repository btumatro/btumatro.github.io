#!/usr/bin/env python3
"""Generate MATRO Reels v2 site and radio clips with Gemini Omni Flash."""

import argparse
import base64
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


HERE = Path(__file__).resolve().parents[1]
MODEL = "gemini-omni-1.1-flash"
SCENES = {
    "chibi": (
        HERE / "assets/images/chibi-radio-source.png",
        HERE / "assets/video/chibi-opening-omni-v2.mp4",
        "Animate this exact 9:16 chibi MATRO workshop illustration into one continuous 8-second opening shot. Preserve the same bald character, calm face and relaxed eye size, black glasses, black shirt, vintage radio, workbench, little robot, warm desk lamp and exact illustrated chibi style. Keep both glasses on his face, no exaggerated surprise, no wide-eyed expression, no face or body morphing, no new limbs, no extra fingers and no fused hands or objects. His right hand stays on the radio's single frequency knob already positioned at the far lower-right of the radio face below the horizontal frequency scale. Do not add any button, dial or object on top of his hand. Do not create another frequency knob; do not move or animate any other radio control. Let only that existing lower-right knob turn a few degrees, with a restrained dial glow; the character gives a tiny natural nod toward the radio and a subtle smile. Slow restrained camera push-in, no cuts. No speech, no lip movement, no generated words, captions, signs, logos, watermarks or gibberish. No generated music.",
    ),
    "site": (
        HERE / "assets/images/robotik-sahne-kaynagi-v2.png",
        HERE / "assets/video/site-robots-omni-v2.mp4",
        "Animate this exact vertical 9:16 MATRO robotics scene as one elegant 8-second cinematic shot. Preserve the three existing machines and their distinctive shapes exactly: the red four-rotor X-frame quadcopter in the sky; the black six-wheel box-chassis rover with its exposed sensor mast on the rocky track; the single-hull low gray unmanned surface boat on the water. Do not redesign them, change their number of rotors, wheels, hulls, or proportions, merge parts, add machines, or make any part melt or morph. Restrained motion only: slow camera push-in, the drone propellers rotate smoothly in place, the rover remains planted while a tiny status light softly pulses, and water moves gently around the boat. Preserve the refined illustrated dusk lighting, dark teal shadows, warm amber highlights and exact composition. No people, no generated words, text, logos, flags, captions, UI, or watermark. No cuts, flashes, or dramatic camera movement.",
    ),
    "radio": (
        HERE / "assets/images/radio-closeup-source-v2.png",
        HERE / "assets/video/radio-closeup-omni-v2.mp4",
        "Animate this exact vertical 9:16 close-up MATRO radio illustration as one continuous 8-second shot. Preserve the same wooden tabletop radio, single tuning hand, same bald bespectacled chibi character, lamp, table and exact illustration style. The only frequency-changing control is the existing small knob at the far lower-right of the radio face, below its horizontal frequency scale. The character's single hand remains naturally attached and touches only that existing lower-right knob. Keep the speaker area as a grille; do not create a large glowing dial or any additional buttons or knobs in the middle of the radio or on the hand. Move the lower-right knob only a few degrees and shift the illuminated horizontal scale very subtly. Do not change hand shape or add fingers. Let the existing amber radio light breathe once, then settle; add only a few tiny glints beside the speaker and subtle dust in the lamp beam. Keep the face relaxed, eyes natural and glasses stable, no mouth movement. Very gentle camera push-in. No cuts, no morphing, no new objects, no text, labels, fake writing, logos, subtitles, watermarks, or gibberish. No generated speech or music.",
    ),
}


def find_video_data(value):
    results = []

    def walk(node):
        if isinstance(node, dict):
            data = node.get("data")
            if isinstance(data, str) and len(data) > 10_000:
                mime = str(node.get("mime_type", ""))
                typ = str(node.get("type", ""))
                if "video" in (mime + typ).lower() or not mime:
                    results.append(data)
            for key, child in node.items():
                if key != "data":
                    walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    if not results:
        raise RuntimeError("Gemini yanıtında video verisi yok; hassas yanıt gövdesi gösterilmedi.")
    return base64.b64decode(results[-1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene", choices=sorted(SCENES))
    args = parser.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY ortam değişkeni tanımlı değil.")
    image_path, output_path, prompt = SCENES[args.scene]
    body = {
        "model": MODEL,
        "input": [
            {"type": "image", "data": base64.b64encode(image_path.read_bytes()).decode("ascii"), "mime_type": "image/png"},
            {"type": "text", "text": prompt},
        ],
        "response_format": {"type": "video", "aspect_ratio": "9:16"},
        "generation_config": {"video_config": {"task": "image_to_video"}},
    }
    request = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/interactions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key, "Api-Revision": "2026-05-20"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as error:
        raise SystemExit(f"Gemini üretimi başarısız (HTTP {error.code}); yanıt metni gizlendi.") from None
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = find_video_data(result)
    output_path.write_bytes(data)
    print(f"Üretildi: {output_path.relative_to(HERE)} ({len(data):,} bayt)")


if __name__ == "__main__":
    main()
