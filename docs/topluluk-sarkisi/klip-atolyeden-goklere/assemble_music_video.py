#!/usr/bin/env python3
"""Assemble the upload-ready 1080p Atölyeden Göklere music video."""
from __future__ import annotations

import csv
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "veo-ornekleri" / "videolar"
SONG = ROOT.parent / "ses" / "03-atolyeden-goklere.mp4"
OUT = ROOT / "atolyeden-goklere-final-1080p.mp4"
FPS = 30
W, H = 1920, 1080
BASE_FADE = 0.2


def still(path: str, move: str = "push", team: str | None = None) -> dict:
    return {"kind": "still", "file": path, "move": move, "team": team}


def video(name: str, team: str | None = None, start: float = 0.35) -> dict:
    return {"kind": "video", "file": f"veo-ornekleri/videolar/{name}-omni.mp4", "start": start, "team": team}


# Only already-cinematic Gemini keyframes/concepts and Omni generations derived
# from those frames are used. Source/archive photographs and raw-reference videos
# are intentionally excluded from this music-video timeline.
prelude = [
    still("assets/closing-title-plate.jpg", "push"),
    still("assets/opening-workshop-close.jpg", "slide-left"),
    still("assets/opening-workshop-wide.jpg", "pull"),
    still("assets/konsept-ashina-atolye.png", "pull"),
    still("ana-kareler/prusa-sinematik.png", "slide-right"),
    video("prusa-workshop-concept", start=0.4),
    still("assets/konsept-prusa-sualti.png", "pull"),
    still("ana-kareler/lodos-sinematik.png", "slide-left"),
    video("lodos-sahil-concept", start=0.5),
    still("assets/konsept-lodos-seyir.png", "slide-right"),
    still("ana-kareler/matris-sinematik.png", "push"),
    video("matris-field-concept", start=0.45),
    still("assets/konsept-matris-suru-ucus.png", "pull"),
    still("ana-kareler/zemheri-sinematik.png", "slide-right"),
    still("assets/konsept-gece-iskele.png", "push"),
    video("ashina-sinematik", start=0.6),
    still("assets/konsept-ashina-kalkis.png", "push"),
    video("ashina-flight-concept", start=0.55),
    still("assets/konsept-prusa-sualti.png", "slide-left"),
    still("assets/konsept-lodos-seyir.png", "push"),
    video("gece-iskele-concept", start=0.7),
    still("assets/konsept-prusa-atolye.png", "pull"),
    still("ana-kareler/zemheri-sinematik.png", "push"),
]
prelude_durations = [4.0] * 22 + [2.667]

# Timed to the sung team callouts: ASHİNA, LODOS, PRUSA, ZEMHERİ, MATRİS.
team_reveal = [
    video("ashina-kalkis-concept", "ASHİNA", 0.45),
    video("lodos-seyir-concept", "LODOS", 0.5),
    video("prusa-sualti-concept", "PRUSA", 0.5),
    video("gece-iskele-concept", "ZEMHERİ", 0.5),
    video("matris-ucus-concept", "MATRİS", 0.5),
]
team_durations = [4.0] * 5

refrain = [
    video("ashina-sinematik", start=2.2),
    video("lodos-sinematik", start=1.0),
    video("prusa-sinematik", start=1.4),
    video("matris-sinematik", start=2.0),
    video("zemheri-sinematik", start=2.0),
    video("ashina-vakum-concept", start=1.5),
    still("assets/konsept-ashina-atolye.png", "push"),
    still("assets/konsept-lodos-guncel-sahil.png", "pull"),
    video("prusa-workshop-concept", start=1.2),
    still("assets/konsept-prusa-sualti.png", "push"),
    video("matris-field-concept", start=1.0),
    still("assets/konsept-matris-suru-ucus.png", "slide-right"),
    still("assets/konsept-gece-iskele.png", "push"),
    video("ashina-flight-concept", start=2.0),
    video("lodos-seyir-concept", start=1.8),
    video("prusa-sualti-concept", start=2.0),
    still("assets/konsept-matris-saha.png", "push"),
]
refrain_durations = [4.0] * 16 + [1.333]
end_card = [still("assets/opening-workshop-wide.jpg", "pull")]
end_card_durations = [6.6]

shots = prelude + team_reveal + refrain + end_card
desired = prelude_durations + team_durations + refrain_durations + end_card_durations
assert len(shots) == len(desired) == 46
assert abs(sum(desired) - 182.6) < 0.002

# Most cuts are beat-led dissolves of three frames. Longer directional wipes
# distinguish the first refrain, team roll-call, second verse, last refrain,
# and the logo card without turning every edit into a generic transition.
fade_after = [BASE_FADE] * (len(shots) - 1) + [0.0]
transition_after = ["fade"] * (len(shots) - 1)
for idx, name, duration in [
    (14, "smoothleft", 0.25),
    (22, "slideleft", 0.25),
    (27, "fade", 0.25),
    (34, "smoothleft", 0.25),
    (44, "fade", 0.5),
]:
    transition_after[idx] = name
    fade_after[idx] = duration

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
OVERLAY_DIR = ROOT / "assets" / "lower-thirds"
OVERLAY_DIR.mkdir(parents=True, exist_ok=True)


def make_lower_third(filename: str, text: str, width: int = 920) -> Path:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype(FONT, 40)
    x, y, h = 116, 868, 112
    draw.rounded_rectangle((x, y, x + width, y + h), radius=12, fill=(5, 11, 18, 170))
    draw.rounded_rectangle((x, y, x + 7, y + h), radius=3, fill=(255, 155, 86, 245))
    draw.text((x + 34, y + 31), text, font=font, fill=(255, 255, 255, 250), stroke_width=1, stroke_fill=(0, 0, 0, 210))
    path = OVERLAY_DIR / filename
    layer.save(path)
    return path


team_overlays = [make_lower_third(f"team-{i+1}.png", name, 500) for i, name in enumerate(["ASHİNA", "LODOS", "PRUSA", "ZEMHERİ", "MATRİS"])]

base = ["ffmpeg", "-hide_banner", "-y", "-filter_complex_threads", "2"]
input_index = []
clip_lengths = []
for i, (shot, seconds) in enumerate(zip(shots, desired)):
    source = (ROOT / shot["file"]) if shot["kind"] == "still" else (ROOT / shot["file"])
    if shot["kind"] == "video":
        source = ROOT / shot["file"]
        start = shot.get("start", 0.4)
        base += ["-ss", str(start), "-i", str(source)]
    else:
        base += ["-i", str(source)]
    input_index.append(i)
    clip_lengths.append(seconds + fade_after[i])

audio_index = len(shots)
base += ["-i", str(SONG)]
overlay_indices = []
for overlay_path in team_overlays:
    overlay_indices.append(audio_index + 1 + len(overlay_indices))
    base += ["-loop", "1", "-framerate", str(FPS), "-i", str(overlay_path)]
filters: list[str] = []
for i, (shot, seconds, length) in enumerate(zip(shots, desired, clip_lengths)):
    frames = max(1, round(length * FPS))
    if shot["kind"] == "still":
        move = shot["move"]
        if move == "static":
            zoom, x, y = "1", "0", "0"
        elif move == "push":
            zoom, x, y = "min(zoom+0.00028,1.045)", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
        elif move == "pull":
            zoom, x, y = "if(eq(on,0),1.045,max(zoom-0.00028,1.0))", "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
        elif move == "slide-left":
            zoom, x, y = "1.055", "(iw-iw/zoom)*(1-on/{})".format(frames), "(ih-ih/zoom)/2"
        else:
            zoom, x, y = "1.055", "(iw-iw/zoom)*on/{}".format(frames), "(ih-ih/zoom)/2"
        filt = (
            f"[{i}:v]scale=2200:1238:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=2200:1238,"
            f"zoompan=z='{zoom}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},"
            f"trim=duration={length:.6f},setpts=PTS-STARTPTS,setsar=1,"
            "eq=contrast=1.025:saturation=0.985:brightness=0.002"
        )
    else:
        filt = (
            f"[{i}:v]trim=start=0:duration={length:.6f},setpts=PTS-STARTPTS,fps={FPS},"
            f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={W}:{H},setsar=1,"
            "eq=contrast=1.025:saturation=0.985:brightness=0.002"
        )
    filt += f",format=yuv420p[v{i}]"
    filters.append(filt)

previous = "v0"
raw_elapsed = clip_lengths[0]
prior_fades = 0.0
for i in range(1, len(shots)):
    trans_dur = fade_after[i - 1]
    offset = raw_elapsed - prior_fades - trans_dur
    dest = f"x{i}"
    filters.append(
        f"[{previous}][v{i}]xfade=transition={transition_after[i-1]}:"
        f"duration={trans_dur:.6f}:offset={offset:.6f}[{dest}]"
    )
    previous = dest
    prior_fades += trans_dur
    raw_elapsed += clip_lengths[i]

# Add crisp, correctly spelled typography as vector-like Pillow layers rather
# than asking a video model to draw logos or text.
overlay_filters = []
current = previous
overlay_specs = [(idx, 90.667 + n * 4.0, 93.55 + n * 4.0) for n, idx in enumerate(overlay_indices)]
for n, (input_no, start, end) in enumerate(overlay_specs):
    dest = f"o{n}"
    overlay_filters.append(
        f"[{current}][{input_no}:v]overlay=0:0:eof_action=pass:shortest=0:"
        f"enable='between(t,{start:.3f},{end:.3f})'[{dest}]"
    )
    current = dest
filters.extend(overlay_filters)

graph = ";".join(filters)
base += [
    "-filter_complex", graph,
    "-map", f"[{current}]", "-map", f"{audio_index}:a:0", "-map", f"{audio_index}:s:0?",
    "-t", "182.6",
    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-profile:v", "high", "-level:v", "4.1", "-pix_fmt", "yuv420p",
    "-r", str(FPS), "-g", str(FPS * 2), "-keyint_min", str(FPS * 2), "-sc_threshold", "0",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-c:a", "copy", "-c:s", "mov_text", "-movflags", "+faststart", str(OUT),
]

for shot in shots:
    path = ROOT / shot["file"]
    if not path.exists():
        raise SystemExit(f"Eksik girdi: {path}")
if not SONG.exists():
    raise SystemExit(f"Eksik ana ses: {SONG}")

# Keep a complete, reviewable shot list beside the result.
cursor = 0.0
manifest = []
for i, (shot, seconds) in enumerate(zip(shots, desired)):
    manifest.append({
        "shot": i + 1,
        "start": round(cursor, 3),
        "duration": round(seconds, 3),
        "kind": shot["kind"],
        "source": shot["file"],
        "movement": shot.get("move", "Gemini Omni camera/action movement"),
        "team_label": shot.get("team"),
        "transition_after": transition_after[i] if i < len(shots) - 1 else None,
        "transition_seconds": fade_after[i] if i < len(shots) - 1 else 0,
    })
    cursor += seconds
(ROOT / "final-shotlist.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

print(f"Rendering {len(shots)} shots at {W}x{H}, {FPS} fps; source audio copied unchanged.", flush=True)
subprocess.run(base, check=True)
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
