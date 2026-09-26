#!/usr/bin/env python3
"""Build a complete YouTube-ready MATRO Radyo video with track artwork and audio-reactive visuals."""

from __future__ import annotations

import argparse
import json
from functools import lru_cache
from pathlib import Path
import subprocess
import tempfile
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUTPUT_DIR = HERE / "output"
OUTPUT = OUTPUT_DIR / "MATRO-Radyo-YouTube.mp4"
THUMBNAIL = HERE / "MATRO-Radyo-YouTube-kapak.jpg"
METADATA = HERE / "youtube-aciklama-ve-bolumler.txt"
WIDTH, HEIGHT, FPS = 1280, 720, 24
TEAL = (117, 213, 208, 255)
WHITE = (248, 249, 244, 255)
MUTED = (192, 204, 201, 255)
BG = (5, 13, 17, 255)
FONT_REGULAR = str(ROOT / "node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2")
FONT_REGULAR_EXT = str(ROOT / "node_modules/@fontsource-variable/inter/files/inter-latin-ext-wght-normal.woff2")
FONT_BOLD = str(ROOT / "node_modules/@fontsource/barlow/files/barlow-latin-700-normal.woff2")
FONT_BOLD_EXT = str(ROOT / "node_modules/@fontsource/barlow/files/barlow-latin-ext-700-normal.woff2")
FONT_MONO = str(ROOT / "node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2")
FONT_MONO_EXT = str(ROOT / "node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-ext-wght-normal.woff2")
# Fontsource splits Turkish dotless/dotted I and G/S cedilla into latin-ext;
# Ö/Ü/Ç and their lowercase forms already belong to its latin subset.
EXTENDED = set("ĞİŞğıış")
BACKGROUND = ASSETS / "radyo-youtube-arka-plan.png"
MATRO_LOGO = ROOT / "docs/sosyal-medya/matro-radyo-reels/assets/logos/matro-beyaz.png"
BTU_LOGO = ROOT / "docs/sosyal-medya/matro-radyo-reels/assets/logos/btu-beyaz.png"


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


@lru_cache(maxsize=64)
def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return load_font(FONT_BOLD if bold else FONT_REGULAR, size)


def mono(size: int) -> ImageFont.FreeTypeFont:
    return load_font(FONT_MONO, size)


def text_width(value: str, size: int, bold: bool = False, monospace: bool = False) -> float:
    base = load_font(FONT_MONO if monospace else FONT_BOLD if bold else FONT_REGULAR, size)
    ext = load_font(FONT_MONO_EXT if monospace else FONT_BOLD_EXT if bold else FONT_REGULAR_EXT, size)
    return sum((ext if char in EXTENDED else base).getlength(char) for char in value)


def draw_text(draw: ImageDraw.ImageDraw, point: tuple[int, int], value: str, size: int, color, bold: bool = False, monospace: bool = False) -> None:
    x, y = point
    active_font = None
    run = ""
    for char in value + "\0":
        use_ext = char in EXTENDED
        next_font = load_font(
            FONT_MONO_EXT if monospace and use_ext else FONT_MONO if monospace
            else FONT_BOLD_EXT if bold and use_ext else FONT_BOLD if bold
            else FONT_REGULAR_EXT if use_ext else FONT_REGULAR,
            size,
        ) if char != "\0" else None
        if active_font is not None and next_font is not active_font:
            draw.text((x, y), run, font=active_font, fill=color)
            x += active_font.getlength(run)
            run = ""
        if char != "\0":
            active_font = next_font
            run += char


def duration(path: Path) -> float:
    value = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True,
    )
    return float(value.strip())


def round_cover(path: Path, size: int = 220) -> Image.Image:
    cover = Image.open(path).convert("RGB")
    side = min(cover.size)
    left = (cover.width - side) // 2
    top = (cover.height - side) // 2
    cover = cover.crop((left, top, left + side, top + side)).resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=22, fill=255)
    result = cover.convert("RGBA")
    result.putalpha(mask)
    return result


def fit_background() -> Image.Image:
    image = Image.open(BACKGROUND).convert("RGB")
    scale = max(WIDTH / image.width, HEIGHT / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    x = (image.width - WIDTH) // 2
    y = (image.height - HEIGHT) // 2
    return image.crop((x, y, x + WIDTH, y + HEIGHT)).convert("RGBA")


def wrap_lines(value: str, max_chars: int = 26, max_lines: int = 3) -> list[str]:
    return textwrap.wrap(value, width=max_chars, break_long_words=False, break_on_hyphens=False)[:max_lines]


def wrap_to_width(value: str, width: int, size: int, bold: bool = True, max_lines: int = 3) -> list[str]:
    lines: list[str] = []
    line = ""
    for word in value.split():
        candidate = f"{line} {word}".strip()
        if line and text_width(candidate, size, bold=bold) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines[:max_lines]


def draw_timeline(draw: ImageDraw.ImageDraw, index: int, durations: list[float]) -> None:
    x, y, total_w, gap, h = 64, 681, 1152, 4, 4
    usable = total_w - gap * (len(durations) - 1)
    total = sum(durations)
    for i, seconds in enumerate(durations):
        w = max(4, round(usable * seconds / total))
        if i == len(durations) - 1:
            w = 64 + total_w - x
        color = (76, 154, 151, 255) if i < index - 1 else (255, 194, 71, 255) if i == index - 1 else (54, 68, 72, 255)
        draw.rounded_rectangle((x, y, x + w, y + h), radius=2, fill=color)
        x += w + gap


def make_frame(item: dict, index: int, total: int, cover_path: Path, target: Path, durations: list[float]) -> None:
    frame = fit_background()
    draw = ImageDraw.Draw(frame, "RGBA")

    # Keep the illustrated workshop visible; use typography and thin rules instead of generic cards.
    draw.line((676, 62, 676, 650), fill=(117, 213, 208, 112), width=2)

    matro = Image.open(MATRO_LOGO).convert("RGBA")
    matro.thumbnail((45, 45), Image.Resampling.LANCZOS)
    frame.alpha_composite(matro, (710, 76))
    draw_text(draw, (775, 75), "MATRO RADYO", 31, WHITE, bold=True)
    draw_text(draw, (778, 114), "ATÖLYEDEN SAHAYA", 12, MUTED, monospace=True)

    btu = Image.open(BTU_LOGO).convert("RGBA")
    btu.thumbnail((120, 39), Image.Resampling.LANCZOS)
    frame.alpha_composite(btu, (1094, 80))
    draw.line((710, 143, 1215, 143), fill=(117, 213, 208, 112), width=1)

    # Track card: authentic cover from the radio playlist, changing at every block.
    cover = round_cover(cover_path, size=208)
    cover_x, cover_y = 710, 220
    draw.rectangle((cover_x - 1, cover_y - 1, cover_x + 208, cover_y + 208), outline=(240, 240, 233, 100), width=1)
    frame.alpha_composite(cover, (cover_x, cover_y))

    right_x = 952
    draw_text(draw, (right_x, 223), f"{index:02d} / {total:02d}", 17, TEAL, monospace=True)
    draw_text(draw, (right_x, 256), item["tur"].upper(), 15, MUTED, bold=True)
    title_size = 35
    title_lines = wrap_to_width(item["baslik"], 264, title_size, max_lines=3)
    y = 297
    for line in title_lines:
        draw_text(draw, (right_x, y), line, title_size, WHITE, bold=True)
        y += 43

    draw.ellipse((right_x, 475, right_x + 9, 484), fill=TEAL)
    draw_text(draw, (right_x + 19, 469), "YAYINDA", 13, MUTED, monospace=True)

    # The live waveform sits directly on the artwork with no black widget behind it.
    draw_text(draw, (710, 531), "SES DALGASI", 12, MUTED, monospace=True)
    draw.line((710, 618, 1210, 618), fill=(117, 213, 208, 60), width=1)
    draw_text(draw, (710, 641), "MATRO · BURSA TEKNİK ÜNİVERSİTESİ", 10, MUTED, monospace=True)
    draw_timeline(draw, index, durations)
    frame.convert("RGB").save(target, quality=94)


def chapter_time(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


def write_metadata(items: list[dict], durations: list[float]) -> None:
    elapsed = 0.0
    chapters = []
    for item, seconds in zip(items, durations):
        chapters.append(f"{chapter_time(elapsed)} {item['baslik']}")
        elapsed += seconds
    body = [
        "YouTube başlığı önerisi:",
        "MATRO Radyo — Atölyeden Sahaya | Topluluk Şarkıları, Hikâyeler ve Podcast",
        "",
        "Açıklama:",
        "MATRO Radyo'nun tam yayını: topluluk hikâyeleri, takım spotları, bülten, şarkılar ve istasyon jingle'ları. Bursa Teknik Üniversitesi Makine Teknolojileri Robot ve Otomasyon Topluluğu.",
        "",
        "Bölümler:",
        *chapters,
        "",
        "Site: https://btumatro.com",
        "Instagram: https://instagram.com/btumatro/",
        "",
        "Bu dosya, radyo çalarının src/data/radyo.json içindeki 14 parçalık sırasını korur.",
    ]
    METADATA.write_text("\n".join(body) + "\n", encoding="utf-8")


def make_thumbnail(total_duration: float) -> None:
    frame = fit_background()
    draw = ImageDraw.Draw(frame, "RGBA")
    matro = Image.open(MATRO_LOGO).convert("RGBA")
    matro.thumbnail((64, 64), Image.Resampling.LANCZOS)
    frame.alpha_composite(matro, (712, 114))
    draw_text(draw, (794, 120), "MATRO RADYO", 38, WHITE, bold=True)
    draw.line((714, 207, 1202, 207), fill=(117, 213, 208, 145), width=2)
    draw_text(draw, (712, 256), "ATÖLYEDEN", 54, WHITE, bold=True)
    draw_text(draw, (712, 323), "SAHAYA", 72, TEAL, bold=True)
    draw_text(draw, (716, 427), "HİKÂYELER  ·  TAKIMLAR  ·  ŞARKILAR", 18, MUTED, bold=True)
    draw_text(draw, (716, 477), f"{chapter_time(total_duration)}  /  TAM RADYO YAYINI", 16, TEAL, monospace=True)
    draw.rounded_rectangle((716, 535, 850, 540), radius=2, fill=(255, 194, 71, 230))
    frame.convert("RGB").save(THUMBNAIL, quality=93, subsampling=0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit-seconds", type=float, help="Only render an initial excerpt (for checking the visual pipeline).")
    parser.add_argument("--skip-video", action="store_true", help="Only generate thumbnail and YouTube chapter metadata.")
    args = parser.parse_args()

    if not BACKGROUND.exists() or not MATRO_LOGO.exists() or not BTU_LOGO.exists():
        raise SystemExit("Arka plan veya logo eksik; README'deki varlık yollarını kontrol edin.")
    items = json.loads((ROOT / "src/data/radyo.json").read_text(encoding="utf-8"))["parcalar"]
    audio_paths = [ROOT / "public" / item["dosya"].lstrip("/") for item in items]
    cover_paths = [ROOT / "public" / item["kapak"].lstrip("/") for item in items]
    missing = [path for path in audio_paths + cover_paths if not path.is_file()]
    if missing:
        raise SystemExit("Eksik radyo medyası: " + ", ".join(str(p) for p in missing))

    durations = [duration(path) for path in audio_paths]
    write_metadata(items, durations)
    make_thumbnail(sum(durations))
    if args.skip_video:
        print(f"YouTube kapak ve bölüm bilgileri hazır. Yayın toplamı: {chapter_time(sum(durations))}.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="matro-youtube-radio-") as tmp:
        temp = Path(tmp)
        segment_videos: list[Path] = []
        rendered_duration = 0.0
        concat_video = temp / "video-list.txt"
        concat_audio = temp / "audio-list.txt"
        audio_lines = []

        for i, (item, audio, cover, length) in enumerate(zip(items, audio_paths, cover_paths, durations), 1):
            frame_path = temp / f"visual-{i:02d}.png"
            video_path = temp / f"segment-{i:02d}.mp4"
            make_frame(item, i, len(items), cover, frame_path, durations)
            if args.limit_seconds is not None:
                length = min(length, max(0.25, args.limit_seconds - sum(durations[:i - 1])))
                if sum(durations[:i - 1]) >= args.limit_seconds:
                    break
            graph = (
                f"[0:v]scale={WIDTH}:{HEIGHT},zoompan=z='1.0+0.004*sin(on/900)':d=1:s={WIDTH}x{HEIGHT}:fps={FPS}[base];"
                f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,"
                f"showwaves=s=470x82:mode=p2p:colors=0x75d5d0:scale=sqrt:draw=full:rate={FPS},format=rgb24,"
                "colorkey=0x000000:0.08:0.02,format=rgba[wave];"
                f"[base][wave]overlay=x=718:y=541:shortest=1:format=auto,format=yuv420p[v]"
            )
            run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-loop", "1", "-framerate", str(FPS), "-i", str(frame_path), "-i", str(audio),
                "-filter_complex", graph, "-map", "[v]", "-an", "-t", f"{length:.6f}",
                "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video_path),
            ])
            segment_videos.append(video_path)
            rendered_duration += length
            audio_lines.append(f"file '{audio.as_posix()}'")
            print(f"Görsel bölüm {i:02d}/{len(items):02d}: {item['baslik']} ({chapter_time(length)})", flush=True)
            if args.limit_seconds is not None and sum(durations[:i]) >= args.limit_seconds:
                break

        concat_video.write_text("".join(f"file '{p.as_posix()}'\n" for p in segment_videos), encoding="utf-8")
        concat_audio.write_text("\n".join(audio_lines) + "\n", encoding="utf-8")
        video_only = temp / "video-only.mp4"
        audio_only = temp / "full-audio.m4a"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_video), "-c", "copy", str(video_only)])
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_audio), "-t", f"{rendered_duration:.6f}", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(audio_only)])
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video_only), "-i", str(audio_only),
            "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", str(OUTPUT),
        ])

    print(f"YouTube videosu: {OUTPUT}")
    print(f"Thumbnail: {THUMBNAIL}")
    print(f"Toplam radyo süresi: {chapter_time(sum(durations))}")


if __name__ == "__main__":
    main()
