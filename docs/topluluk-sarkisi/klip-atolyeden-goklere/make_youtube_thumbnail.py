#!/usr/bin/env python3
"""Build the 1280x720 YouTube thumbnail from the generated backdrop and real marks."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BG = ROOT / "assets" / "youtube-thumbnail-bg.png"
MATRO = ROOT.parents[2] / "src" / "assets" / "logo-kaynak" / "MATRO3.png"
BTU = ROOT.parents[2] / "src" / "assets" / "logo-kaynak" / "BTU-beyaz-yatay.png"
OUT = ROOT / "youtube-thumbnail-atolyeden-goklere.jpg"

W, H = 1280, 720
image = Image.open(BG).convert("RGB")
iw, ih = image.size
target_ratio = W / H
if iw / ih > target_ratio:
    nw = round(ih * target_ratio)
    left = (iw - nw) // 2
    image = image.crop((left, 0, left + nw, ih))
else:
    nh = round(iw / target_ratio)
    top = (ih - nh) // 2
    image = image.crop((0, top, iw, top + nh))
image = image.resize((W, H), Image.Resampling.LANCZOS).convert("RGBA")

# Subtle dark veil under the copy, fading before the aircraft.
veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vp = veil.load()
for x in range(760):
    alpha = round(76 * max(0, 1 - x / 760) ** 1.45)
    for y in range(H):
        vp[x, y] = (3, 12, 19, alpha)
image = Image.alpha_composite(image, veil)
draw = ImageDraw.Draw(image)

font_dir = Path("/System/Library/Fonts/Supplemental")
font_regular = ImageFont.truetype(str(font_dir / "Arial.ttf"), 21)
font_kicker = ImageFont.truetype(str(font_dir / "Arial Bold.ttf"), 25)
font_line1 = ImageFont.truetype(str(font_dir / "Arial Bold.ttf"), 64)
font_line2 = ImageFont.truetype(str(font_dir / "Arial Bold.ttf"), 100)
font_tagline = ImageFont.truetype(str(font_dir / "Arial.ttf"), 21)


def paste_mark(path: Path, xy: tuple[int, int], target_h: int, max_w: int) -> int:
    mark = Image.open(path).convert("RGBA")
    alpha = mark.getchannel("A")
    bounds = alpha.getbbox()
    if bounds:
        mark = mark.crop(bounds)
    scale = min(target_h / mark.height, max_w / mark.width)
    mark = mark.resize((round(mark.width * scale), round(mark.height * scale)), Image.Resampling.LANCZOS)
    image.alpha_composite(mark, xy)
    return mark.width


matro_w = paste_mark(MATRO, (58, 48), 70, 76)
draw.line((58 + matro_w + 19, 49, 58 + matro_w + 19, 118), fill=(231, 238, 239, 155), width=2)
paste_mark(BTU, (58 + matro_w + 40, 54), 58, 235)

draw.text((64, 267), "BTÜ MATRO  /  MÜZİK KLİBİ", font=font_kicker, fill=(255, 174, 111, 255))
draw.text((58, 322), "ATÖLYEDEN", font=font_line1, fill=(249, 249, 246, 255), stroke_width=1, stroke_fill=(0, 0, 0, 130))
draw.text((54, 380), "GÖKLERE", font=font_line2, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 150))
draw.rounded_rectangle((64, 510, 414, 516), radius=3, fill=(255, 155, 86, 245))
draw.text((64, 538), "Atölyede başlar. Sahada kanıtlanır.", font=font_tagline, fill=(226, 234, 235, 250))

image.convert("RGB").save(OUT, "JPEG", quality=93, optimize=True, progressive=True, subsampling=0)
print(f"{OUT}  {W}x{H}")
