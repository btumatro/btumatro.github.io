#!/usr/bin/env python3
"""Render MATRO Radyo Reels v2 using v1's shared intro, music and narration."""

from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parents[1]
SHARED = HERE.parent / "assets"
ASSETS = HERE / "assets"
OUTPUT = HERE / "output" / "MATRO-Radyo-Reels-v2.mp4"
W, H, FPS = 720, 1280, 24
DURATION = 30.958
MUSIC_FADE_OUT = 2.8


def run(args):
    subprocess.run(args, check=True)


def scene(source, overlay, target, duration, overlay_end=None):
    enabled = "1" if overlay_end is None else f"between(t,0,{overlay_end})"
    graph = (
        f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
        f"fps={FPS},setsar=1[base];[base][1:v]overlay=0:0:format=auto:"
        f"enable='{enabled}',format=yuv420p[v]"
    )
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-loop", "1", "-framerate", str(FPS), "-i", str(overlay),
        "-filter_complex", graph, "-map", "[v]", "-an", "-t", str(duration),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", str(FPS), str(target),
    ])


def main():
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg PATH içinde bulunamadı.")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="matro-reel-v2-") as tmpdir:
        tmp = Path(tmpdir)
        opening, site, radio, poster = (tmp / f"scene-{i}.mp4" for i in range(4))
        scene(ASSETS / "video/chibi-opening-omni-v2.mp4", SHARED / "graphics/acilis-yazisi.png", opening, 8.0, 3.5)
        scene(ASSETS / "video/site-robots-omni-v2.mp4", ASSETS / "graphics/site-yazi-katmani-v2.png", site, 8.0)
        scene(ASSETS / "video/radio-closeup-omni-v2.mp4", ASSETS / "graphics/radyo-yazi-katmani-v2.png", radio, 8.0)
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1",
            "-framerate", str(FPS), "-i", str(ASSETS / "graphics/kapanis-afisi-v2.png"),
            "-t", "8", "-an", "-vf", f"scale={W}:{H}:flags=lanczos,format=yuv420p",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), str(poster),
        ])

        video_graph = (
            "[0:v][1:v]xfade=transition=fade:duration=0.35:offset=7.65[x1];"
            "[x1][2:v]xfade=transition=fade:duration=0.35:offset=15.30[x2];"
            "[x2][3:v]xfade=transition=fade:duration=0.35:offset=22.95,format=yuv420p[v]"
        )
        audio_graph = (
            f"[4:a]atrim=0:{DURATION},asetpts=PTS-STARTPTS,volume=0.42,"
            f"afade=t=in:st=1.3:d=0.7,afade=t=out:st={DURATION - MUSIC_FADE_OUT:.3f}:d={MUSIC_FADE_OUT}[music];"
            "[5:a]loudnorm=I=-16:TP=-1.5:LRA=7,adelay=1500|1500,asplit=2[voice][duckkey];"
            f"[duckkey]apad=whole_dur={DURATION}[duckpad];"
            "[music][duckpad]sidechaincompress=threshold=0.035:ratio=7:attack=25:release=420[ducked];"
            "[ducked][voice]amix=inputs=2:duration=first:normalize=0[spoken];"
            "anoisesrc=color=pink:duration=1.5:amplitude=0.18:sample_rate=48000,"
            "highpass=f=350,lowpass=f=6200,afade=t=out:st=0.75:d=0.75[hiss];"
            "[spoken][hiss]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.96[a]"
        )
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(opening), "-i", str(site), "-i", str(radio), "-i", str(poster),
            "-i", str(SHARED / "audio/saha-bizim-jingle-kaynagi.mp4"),
            "-i", str(SHARED / "audio/ayse-can-seslendirme.mp3"),
            "-filter_complex", video_graph + ";" + audio_graph, "-map", "[v]", "-map", "[a]",
            "-t", str(DURATION), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(OUTPUT),
        ])
    print(f"Üretildi: {OUTPUT}")


if __name__ == "__main__":
    main()
