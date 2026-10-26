import os
import json
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = "/Users/wildgenie/Projects/btu-matro"
SCRATCH = "/Users/wildgenie/.gemini/antigravity-cli/brain/482501c3-e797-49fa-a7d5-231ae28c4675/scratch"

def load_font(size):
    for p in [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf"
    ]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def build_sheets():
    data = json.load(open(os.path.join(WORKSPACE, "src/data/ekibimiz.json")))
    seen = set()
    people = []
    for p in data["people"]:
        s = p["photo"].split("/")[-1].replace(".jpg", "")
        if s not in seen:
            seen.add(s)
            people.append((s, p["name"]))

    # 1. Build 2x visual inspection sheets (600x600 full resolution side by side: original | yeni kadraj)
    for part_idx, chunk in enumerate([people[:13], people[13:]], 1):
        w = 20 + 2 * 620
        h = 20 + len(chunk) * 645
        canvas = Image.new("RGB", (w, h), (242, 242, 242))
        draw = ImageDraw.Draw(canvas)
        fnt = load_font(20)
        for r_i, (s, name) in enumerate(chunk):
            num = (part_idx - 1) * 13 + r_i + 1
            y0 = 10 + r_i * 645
            draw.text((15, y0 + 6), f"{num:02d}. {name} ({s})", fill=(20, 20, 20), font=fnt)
            p_orig = os.path.join(WORKSPACE, f"public/media/ekip/{s}.jpg")
            p_kad = os.path.join(WORKSPACE, f"docs/ekip/yz/codex/kadraj/{s}.jpg")
            if os.path.exists(p_orig):
                canvas.paste(Image.open(p_orig).convert("RGB").resize((600, 600)), (15, y0 + 36))
            if os.path.exists(p_kad):
                canvas.paste(Image.open(p_kad).convert("RGB").resize((600, 600)), (635, y0 + 36))
        out_2x = os.path.join(SCRATCH, f"kadraj_2x_part{part_idx}.jpg")
        canvas.save(out_2x, "JPEG", quality=94)
        print("Saved 2x inspection sheet:", out_2x)

    # 2. Build docs/ekip/kontrol/agy-eksikler.jpg:
    # 2 columns of people (13 rows x 2 macro-columns), each person has:
    # numara + isim; orijinal | yeni kadraj | (varsa) yeni gri fon
    cell = 280
    gap = 12
    macro_w = 3 * (cell + gap) + 30
    macro_h = cell + 46
    rows_count = 13
    sheet_w = 2 * macro_w + 30
    sheet_h = rows_count * macro_h + 70

    sheet = Image.new("RGB", (sheet_w, sheet_h), (248, 248, 248))
    draw = ImageDraw.Draw(sheet)
    title_fnt = load_font(22)
    lbl_fnt = load_font(16)
    sub_fnt = load_font(13)

    draw.text(
        (20, 16),
        "BTU MATRO — Ek İstek 4 & 5 Kontrol Paftası (1: Orijinal | 2: Yeni Kadraj | 3: Varsa Yeni Gri Fon)",
        fill=(15, 15, 15),
        font=title_fnt
    )

    for idx, (s, name) in enumerate(people):
        num = idx + 1
        col_group = idx // rows_count
        row_idx = idx % rows_count
        x_base = 20 + col_group * macro_w
        y_base = 60 + row_idx * macro_h

        draw.text((x_base, y_base), f"{num:02d}. {name} ({s})", fill=(20, 20, 20), font=lbl_fnt)

        p_orig = os.path.join(WORKSPACE, f"public/media/ekip/{s}.jpg")
        p_kad = os.path.join(WORKSPACE, f"docs/ekip/yz/codex/kadraj/{s}.jpg")
        p_gri_yeni = os.path.join(WORKSPACE, f"docs/ekip/yz/codex/gri-fon-yeni/{s}.jpg")

        items = [
            ("1 orijinal", p_orig),
            ("2 yeni kadraj", p_kad),
            ("3 yeni gri fon", p_gri_yeni if os.path.exists(p_gri_yeni) else None)
        ]
        for c_i, (sub_lbl, fp) in enumerate(items):
            cx = x_base + c_i * (cell + gap)
            cy = y_base + 24
            if fp and os.path.exists(fp):
                im = Image.open(fp).convert("RGB").resize((cell, cell), Image.Resampling.LANCZOS)
                sheet.paste(im, (cx, cy))
                draw.rectangle([cx, cy + cell - 20, cx + 115, cy + cell], fill=(0, 0, 0))
                draw.text((cx + 5, cy + cell - 18), sub_lbl, fill=(255, 255, 255), font=sub_fnt)
            else:
                draw.rectangle([cx, cy, cx + cell, cy + cell], outline=(210, 210, 210), fill=(238, 238, 238))
                if c_i == 1:
                    draw.text((cx + 40, cy + cell // 2 - 8), "TESLİM EDİLMEDİ", fill=(180, 40, 40), font=sub_fnt)
                else:
                    draw.text((cx + 65, cy + cell // 2 - 8), "(mevcut korundu)", fill=(140, 140, 140), font=sub_fnt)

    out_pafta = os.path.join(WORKSPACE, "docs/ekip/kontrol/agy-eksikler.jpg")
    os.makedirs(os.path.dirname(out_pafta), exist_ok=True)
    sheet.save(out_pafta, "JPEG", quality=93)
    print("Saved final pafta:", out_pafta, sheet.size)

if __name__ == "__main__":
    build_sheets()
