#!/usr/bin/env python3
"""Regenerate the site or radio image-to-video scene with Gemini Omni."""

import argparse
import base64
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


HERE = Path(__file__).resolve().parents[1]
ASSETS = HERE / "assets"
MODEL = "gemini-omni-1.1-flash"
REVISION = "2026-05-20"  # API revision used to create the checked-in source clips.
PROMPTS = {
    "site": (
        "site-sahne-kaynagi.png", "omni-site-sahnesi.mp4",
        "Animate this exact vertical 9:16 robotics illustration into one elegant 8-second cinematic shot. Preserve its exact drone, field rover, underwater ROV and dusk landscape; no morphing or new machinery. Gentle camera push-in with subtle parallax. Drone rotors turn slowly, rover lights glow softly, underwater particles drift. Keep same premium photographic illustration, dark teal and amber grade. Absolutely no text, lettering, logos, UI, subtitles, people or watermarks. No cuts, no flashing."
    ),
    "radio": (
        "radyo-sahne-kaynagi.png", "omni-radyo-sahnesi.mp4",
        "Animate this exact vertical 9:16 vintage radio workshop illustration into one elegant 8-second cinematic shot. Preserve the same radio, tuning hand and workshop. The hand turns the frequency knob slightly; the amber dial brightens gently; a few small analog sound waves shimmer near the speaker, subtle dust drifts through the warm light. Keep the same premium illustrated style, dark teal and copper palette. No text, lettering, logos, UI, subtitles, or watermarks. No cuts, no morphs, no new objects, no flashing."
    ),
}


def extract_video(payload):
    candidates = []

    def walk(value):
        if isinstance(value, dict):
            data = value.get("data")
            if isinstance(data, str) and len(data) > 10_000:
                mime = str(value.get("mime_type", ""))
                kind = str(value.get("type", ""))
                if "video" in mime or "video" in kind or not mime:
                    candidates.append(data)
            for key, child in value.items():
                if key != "data":
                    walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)
    if not candidates:
        raise RuntimeError("Gemini yanıtında video verisi bulunamadı; yanıt içeriği yazdırılmadı.")
    return base64.b64decode(candidates[-1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene", choices=sorted(PROMPTS))
    args = parser.parse_args()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("GEMINI_API_KEY ortam değişkeni tanımlı değil.")

    image_name, output_name, prompt = PROMPTS[args.scene]
    image_path = ASSETS / "image" / image_name
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
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
            "Api-Revision": REVISION,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            payload = json.loads(response.read())
    except urllib.error.HTTPError as error:
        # Keep response text private: provider errors may echo request details.
        raise SystemExit(f"Gemini isteği başarısız oldu (HTTP {error.code}).") from None

    video = extract_video(payload)
    destination = ASSETS / "video" / output_name
    destination.write_bytes(video)
    print(f"Üretildi: {destination.relative_to(HERE)} ({len(video):,} bayt)")


if __name__ == "__main__":
    main()
