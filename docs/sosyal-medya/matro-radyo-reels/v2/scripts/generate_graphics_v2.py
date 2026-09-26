#!/usr/bin/env python3
"""Create v2 title overlays and the poster from the selected chibi artwork."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parents[1]
SHARED = HERE.parent / "assets"
ASSETS = HERE / "assets"
OUT = ASSETS / "graphics"
W, H = 720, 1280
WHITE = (247, 247, 240, 255)
TEAL = (117, 213, 208, 255)
MUTED = (224, 231, 227, 255)
BG = (5, 15, 19)


def font(size, bold=True):
    path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
    if not Path(path).is_file():
        raise SystemExit("Arial fontu bulunamadı; font() içindeki yolu sistem fontunuza göre değiştirin.")
    return ImageFont.truetype(path, size)


def label(draw, point, value, size, color=WHITE, bold=True):
    draw.text(point, value, font=font(size, bold), fill=color)


def dark_gradient(image, y0, y1, alpha_max):
    pixels = image.load()
    for y in range(y0, y1):
        alpha = int(alpha_max * (y - y0) / max(1, y1 - y0 - 1))
        for x in range(W):
            pixels[x, y] = (*BG, alpha)


def fit_portrait(image):
    image = image.convert("RGB")
    scale = max(W / image.width, H / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left, top = (image.width - W) // 2, (image.height - H) // 2
    return image.crop((left, top, left + W, top + H)).convert("RGBA")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    matro = Image.open(SHARED / "logos/matro-beyaz.png").convert("RGBA")
    btu = Image.open(SHARED / "logos/btu-beyaz.png").convert("RGBA")

    # Keep the upper drone unobstructed: only the compact identity lockup stays at top.
    site = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dark_gradient(site, 0, 160, 175)
    dark_gradient(site, 970, 1280, 235)
    site.alpha_composite(matro.resize((64, 64), Image.Resampling.LANCZOS), (48, 54))
    draw = ImageDraw.Draw(site)
    label(draw, (128, 58), "BTÜ MATRO", 27)
    label(draw, (130, 95), "ROBOTİK VE OTOMASYON TOPLULUĞU", 16, MUTED)
    label(draw, (50, 1058), "HAVADA  ·  KARADA  ·  DENİZDE", 21, MUTED)
    label(draw, (50, 1100), "btumatro.com", 43)
    draw.rounded_rectangle((50, 1170, 670, 1174), 2, fill=TEAL)
    label(draw, (50, 1191), "Profildeki linke tıklayın.", 20, TEAL)
    site.save(OUT / "site-yazi-katmani-v2.png")

    source = Image.open(ASSETS / "images/chibi-laptop-site-source-v2.png")
    poster = fit_portrait(source)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dark_gradient(shade, 0, 400, 205)
    dark_gradient(shade, 1030, 1280, 235)
    poster.alpha_composite(shade)
    poster.alpha_composite(matro.resize((100, 100), Image.Resampling.LANCZOS), (48, 48))
    poster.alpha_composite(btu.resize((248, 58), Image.Resampling.LANCZOS), (420, 70))
    draw = ImageDraw.Draw(poster)
    label(draw, (46, 207), "ATÖLYEDE BAŞLAR.", 39)
    label(draw, (46, 260), "SAHADA KANITLANIR.", 36, TEAL)
    label(draw, (49, 321), "Takımlar · Projeler · Başarılar", 21, MUTED)
    draw.rounded_rectangle((34, 1080, 686, 1238), 24, fill=(5, 15, 19, 240), outline=TEAL, width=2)
    label(draw, (64, 1101), "MATRO RADYO", 26, TEAL)
    label(draw, (64, 1142), "Topluluk şarkıları ve hikâyeler.", 19, WHITE, False)
    draw.rounded_rectangle((430, 1120, 658, 1202), 18, fill=TEAL)
    f = font(23)
    box = draw.textbbox((0, 0), "btumatro.com", font=f)
    draw.text((544 - (box[2] - box[0]) / 2, 1148), "btumatro.com", font=f, fill=(5, 15, 19, 255))
    poster.convert("RGB").save(OUT / "kapanis-afisi-v2.png", quality=96)
    print("V2 site yazıları ve karakter içermeyen MacBook kapanış afişi hazır.")


if __name__ == "__main__":
    main()
