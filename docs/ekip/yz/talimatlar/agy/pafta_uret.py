import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def get_people_list() -> list[tuple[int, str, str]]:
    data = json.load(open("src/data/ekibimiz.json", encoding="utf-8"))
    seen = set()
    people = []
    idx = 1
    for p in data["people"]:
        slug = os.path.basename(p["photo"])[:-4]
        if slug not in seen:
            seen.add(slug)
            people.append((idx, p["name"], slug))
            idx += 1
    return people

def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for fp in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf",
    ):
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

def build_sheet(target_slugs: list[str] | None, out_path: str) -> None:
    all_people = get_people_list()
    if target_slugs:
        people = [p for p in all_people if p[2] in target_slugs]
    else:
        people = all_people

    thumb = 220
    gap_inner = 4
    group_w = thumb * 4 + gap_inner * 3
    cols = 2 if len(people) > 3 else 1
    rows = (len(people) + cols - 1) // cols

    pad_x = 28
    pad_top = 64
    gap_col = 32
    label_h = 34
    row_h = thumb + label_h + 14

    W = pad_x * 2 + cols * group_w + (cols - 1) * gap_col
    H = pad_top + rows * row_h + 20

    sheet = Image.new("RGB", (W, H), (18, 18, 20))
    draw = ImageDraw.Draw(sheet)
    font_title = load_font(22)
    font_name = load_font(17)
    font_num = load_font(15)

    draw.text(
        (pad_x, 18),
        "Her kişide: 1 mevcut | 2 kadraj | 3 vesikalık | 4 gri fon",
        fill=(245, 245, 245),
        font=font_title,
    )

    folders = [
        ("1", "public/media/ekip"),
        ("2", "docs/ekip/yz/codex/kadraj"),
        ("3", "docs/ekip/yz/codex/vesikalik"),
        ("4", "docs/ekip/yz/codex/gri-fon"),
    ]

    for i, (num, name, slug) in enumerate(people):
        c = i % cols
        r = i // cols
        x0 = pad_x + c * (group_w + gap_col)
        y0 = pad_top + r * row_h

        for j, (badge, folder) in enumerate(folders):
            px = x0 + j * (thumb + gap_inner)
            py = y0
            img_p = os.path.join(folder, f"{slug}.jpg")
            if os.path.exists(img_p):
                im = Image.open(img_p).convert("RGB").resize((thumb, thumb), Image.Resampling.LANCZOS)
            else:
                im = Image.new("RGB", (thumb, thumb), (45, 45, 50))
            sheet.paste(im, (px, py))
            if j == 0:
                draw.rectangle((px, py, px + thumb - 1, py + thumb - 1), outline=(235, 130, 30), width=2)
            # Draw badge number in top-left corner
            draw.rectangle((px + 4, py + 4, px + 22, py + 24), fill=(0, 0, 0))
            draw.text((px + 8, py + 5), badge, fill=(255, 255, 255), font=font_num)

        draw.text((x0, y0 + thumb + 6), f"{num}. {name} ({slug})", fill=(245, 175, 70), font=font_name)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    sheet.save(out_path, "JPEG", quality=90)
    print(f"Saved sheet to {out_path} ({W}x{H})")

if __name__ == "__main__":
    out_p = sys.argv[1] if len(sys.argv) > 1 else "docs/ekip/kontrol/codex-karsilastirma.jpg"
    slugs = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    build_sheet(slugs, out_p)
