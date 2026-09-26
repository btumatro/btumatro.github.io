#!/usr/bin/env python3
"""Build the MATRO Radyo vertical reel from the checked-in source assets."""

from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parents[1]
ASSETS = HERE / "assets"
OUTPUT = HERE / "output" / "MATRO-Radyo-Reels-final.mp4"
W, H, FPS = 720, 1280, 24
DURATION = 30.958


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def require(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def make_segment(source: Path, overlay: Path, output: Path, duration: float,
                 overlay_end: float | None = None) -> None:
    """Scale one scene, composite a transparent PNG, and encode silent H.264."""
    enable = "1" if overlay_end is None else f"between(t,0,{overlay_end})"
    graph = (
        f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
        f"crop={W}:{H},fps={FPS},setsar=1[base];"
        f"[base][1:v]overlay=0:0:format=auto:enable='{enable}',"
        "format=yuv420p[v]"
    )
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(require(source)), "-loop", "1", "-framerate", str(FPS),
        "-i", str(require(overlay)), "-filter_complex", graph,
        "-map", "[v]", "-an", "-t", str(duration),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", str(FPS), str(output),
    ])


def main() -> None:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg PATH içinde bulunamadı.")
    video = ASSETS / "video"
    graphics = ASSETS / "graphics"
    audio = ASSETS / "audio"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="matro-reel-") as temp:
        tmp = Path(temp)
        opening, site, radio, poster = (tmp / f"scene-{n}.mp4" for n in range(4))
        make_segment(video / "chibi-acilis-omni.mp4", graphics / "acilis-yazisi.png",
                     opening, 10.0, 3.5)
        make_segment(video / "omni-site-sahnesi.mp4", graphics / "site-yazi-katmani.png",
                     site, 8.0)
        make_segment(video / "omni-radyo-sahnesi.mp4", graphics / "radyo-yazi-katmani.png",
                     radio, 8.0)

        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-loop", "1", "-framerate", str(FPS), "-i",
            str(require(graphics / "kapanis-afisi.png")), "-t", "6",
            "-an", "-vf", f"scale={W}:{H}:flags=lanczos,format=yuv420p",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-r", str(FPS), str(poster),
        ])

        video_graph = (
            "[0:v][1:v]xfade=transition=fade:duration=0.35:offset=9.65[x1];"
            "[x1][2:v]xfade=transition=fade:duration=0.35:offset=17.30[x2];"
            "[x2][3:v]xfade=transition=fade:duration=0.35:offset=24.95,"
            "format=yuv420p[v]"
        )

        # Keep the supplied MATRO jingle under the narration, lower it while
        # either speaker talks, and make the opening radio hiss easy to hear.
        audio_graph = (
            f"[4:a]atrim=0:{DURATION},asetpts=PTS-STARTPTS,volume=0.42,"
            "afade=t=in:st=1.3:d=0.7,afade=t=out:st=29.8:d=1.15[music];"
            "[5:a]loudnorm=I=-16:TP=-1.5:LRA=7,adelay=1500|1500,"
            "asplit=2[voice][duckkey];"
            "[music][duckkey]sidechaincompress=threshold=0.035:ratio=7:"
            "attack=25:release=420[ducked];"
            "[ducked][voice]amix=inputs=2:duration=first:normalize=0[spoken];"
            "anoisesrc=color=pink:duration=1.5:amplitude=0.18:sample_rate=48000,"
            "highpass=f=350,lowpass=f=6200,afade=t=out:st=0.75:d=0.75[hiss];"
            "[spoken][hiss]amix=inputs=2:duration=first:normalize=0,"
            "alimiter=limit=0.96[a]"
        )
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(opening), "-i", str(site), "-i", str(radio), "-i", str(poster),
            "-i", str(require(audio / "saha-bizim-jingle-kaynagi.mp4")),
            "-i", str(require(audio / "ayse-can-seslendirme.mp3")),
            "-filter_complex", video_graph + ";" + audio_graph,
            "-map", "[v]", "-map", "[a]", "-t", str(DURATION),
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            str(OUTPUT),
        ])
    print(f"Üretildi: {OUTPUT}")


if __name__ == "__main__":
    main()
