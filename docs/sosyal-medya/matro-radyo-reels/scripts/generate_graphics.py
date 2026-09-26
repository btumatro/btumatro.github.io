#!/usr/bin/env python3
"""Recreate the transparent title layers and closing poster with Pillow."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parents[1]
ASSETS = HERE / "assets"
GRAPHICS = ASSETS / "graphics"
W, H = 720, 1280
WHITE = (247, 247, 240, 255)
TEAL = (117, 213, 208, 255)
MUTED = (224, 231, 227, 255)
BG = (5, 15, 19)


def get_font(size: int, bold: bool = True):
    candidates = (
        ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf"]
        if bold else
        ["/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"]
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    raise SystemExit("Arial fontu bulunamadı. generate_graphics.py içinde get_font() yolunu sistem fontunuza göre ayarlayın.")


def text(draw, point, value, size, color=WHITE, bold=True):
    draw.text(point, value, font=get_font(size, bold), fill=color)


def gradient(image, y0, y1, max_alpha, reverse=False):
    pixels = image.load()
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        alpha = int(max_alpha * (1 - t if reverse else t))
        for x in range(W):
            pixels[x, y] = (*BG, alpha)


def new_layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def fit_cover(image):
    image = image.convert("RGB")
    sw, sh = image.size
    scale = max(W / sw, H / sh)
    image = image.resize((int(sw * scale), int(sh * scale)), Image.Resampling.LANCZOS)
    left, top = (image.width - W) // 2, (image.height - H) // 2
    return image.crop((left, top, left + W, top + H)).convert("RGBA")


def main():
    GRAPHICS.mkdir(parents=True, exist_ok=True)
    logo_matro = Image.open(ASSETS / "logos" / "matro-beyaz.png").convert("RGBA")
    logo_btu = Image.open(ASSETS / "logos" / "btu-beyaz.png").convert("RGBA")

    # Site scene overlay.
    layer = new_layer()
    gradient(layer, 0, 350, 180)
    gradient(layer, 970, 1280, 235)
    draw = ImageDraw.Draw(layer)
    layer.alpha_composite(logo_matro.resize((64, 64), Image.Resampling.LANCZOS), (48, 54))
    draw = ImageDraw.Draw(layer)
    text(draw, (128, 58), "BTÜ MATRO", 27)
    text(draw, (130, 95), "ROBOTİK VE OTOMASYON TOPLULUĞU", 16, MUTED)
    text(draw, (50, 168), "ATÖLYEDE BAŞLAR.", 43)
    text(draw, (50, 218), "SAHADA KANITLANIR.", 39, TEAL)
    text(draw, (50, 1058), "HAVADA  ·  KARADA  ·  DENİZDE", 21, MUTED)
    text(draw, (50, 1100), "btumatro.com", 43)
    draw.rounded_rectangle((50, 1170, 670, 1174), 2, fill=TEAL)
    text(draw, (50, 1191), "Profildeki linke tıklayın.", 20, TEAL)
    layer.save(GRAPHICS / "site-yazi-katmani.png")

    # Radio scene overlay.
    layer = new_layer()
    gradient(layer, 0, 280, 170)
    gradient(layer, 990, 1280, 230)
    draw = ImageDraw.Draw(layer)
    text(draw, (48, 66), "MATRO RADYO", 43)
    text(draw, (50, 119), "ATÖLYEDEN SAHAYA", 22, TEAL)
    text(draw, (48, 1032), "Atölyede Başlar", 37)
    text(draw, (50, 1080), "Topluluk şarkıları  ·  MATRO hikâyeleri", 22, MUTED)
    text(draw, (50, 1180), "Sitedeki Radyo düğmesine dokun.", 20, TEAL)
    layer.save(GRAPHICS / "radyo-yazi-katmani.png")

    # Opening title band masks transient model-generated pseudo-text.
    layer = new_layer()
    draw = ImageDraw.Draw(layer)
    draw.rectangle((0, 126, W, 276), fill=(5, 15, 19, 255))
    layer.alpha_composite(logo_matro.resize((68, 68), Image.Resampling.LANCZOS), (48, 165))
    draw = ImageDraw.Draw(layer)
    text(draw, (140, 166), "MATRO RADYO", 35)
    text(draw, (142, 209), "FREKANS BULUNDU", 20, TEAL)
    layer.save(GRAPHICS / "acilis-yazisi.png")

    # Closing poster uses a still from the same chibi Omni opener.
    poster = fit_cover(Image.open(ASSETS / "image" / "kapanis-kare-kaynagi.png"))
    shade = new_layer()
    gradient(shade, 0, 400, 205)
    gradient(shade, 1030, 1280, 235)
    poster.alpha_composite(shade)
    draw = ImageDraw.Draw(poster)
    poster.alpha_composite(logo_matro.resize((100, 100), Image.Resampling.LANCZOS), (48, 48))
    poster.alpha_composite(logo_btu.resize((248, 58), Image.Resampling.LANCZOS), (420, 70))
    draw = ImageDraw.Draw(poster)
    text(draw, (46, 207), "ATÖLYEDE BAŞLAR.", 39)
    text(draw, (46, 260), "SAHADA KANITLANIR.", 36, TEAL)
    text(draw, (49, 321), "Takımlar · Projeler · Başarılar", 21, MUTED)
    draw.rounded_rectangle((34, 1080, 686, 1238), 24, fill=(5, 15, 19, 240), outline=TEAL, width=2)
    text(draw, (64, 1101), "MATRO RADYO", 26, TEAL)
    text(draw, (64, 1142), "Topluluk şarkıları ve hikâyeler.", 19, WHITE, False)
    draw.rounded_rectangle((430, 1120, 658, 1202), 18, fill=TEAL)
    label = "btumatro.com"
    font = get_font(23)
    box = draw.textbbox((0, 0), label, font=font)
    draw.text((544 - (box[2] - box[0]) / 2, 1148), label, font=font, fill=(5, 15, 19, 255))
    poster.convert("RGB").save(GRAPHICS / "kapanis-afisi.png", quality=96)
    print("Başlık katmanları ve kapanış afişi güncellendi.")


if __name__ == "__main__":
    main()
