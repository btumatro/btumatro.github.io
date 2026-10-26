import os
import json
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = "/Users/wildgenie/Projects/btu-matro"
SCRATCH = "/Users/wildgenie/.gemini/antigravity-cli/brain/482501c3-e797-49fa-a7d5-231ae28c4675/scratch"

TARGET_8 = [
    "adem-baglan",
    "almina-yanar",
    "duygu-solak",
    "ela-ural",
    "zeynep-seher-yolasigmaz",
    "melisa-aydirek",
    "nusret-bircan-keser",
    "eslem-kilic",
]

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

def build_pafta():
    data = json.load(open(os.path.join(WORKSPACE, "src/data/ekibimiz.json")))
    seen = set()
    people_map = {}
    idx_counter = 0
    for p in data["people"]:
        s = p["photo"].split("/")[-1].replace(".jpg", "")
        if s not in seen:
            seen.add(s)
            idx_counter += 1
            people_map[s] = (idx_counter, p["name"])

    # Build docs/ekip/kontrol/kadraj-eksikler.jpg
    # 2 macro-columns x 4 rows (8 people total), each cell 420x420 for crystal-clear inspection!
    cell = 420
    gap = 16
    macro_w = 2 * (cell + gap) + 30
    macro_h = cell + 52
    rows_count = 4
    sheet_w = 2 * macro_w + 30
    sheet_h = rows_count * macro_h + 75

    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    title_fnt = load_font(22)
    lbl_fnt = load_font(17)
    sub_fnt = load_font(14)

    draw.text(
        (20, 18),
        "BTU MATRO — Ek İstek 9: 8 Eksik Kadraj Kontrol Paftası (1: Sitede | 2: Yeni Kadraj)",
        fill=(15, 15, 15),
        font=title_fnt
    )

    for i, s in enumerate(TARGET_8):
        num, name = people_map.get(s, (i + 1, s))
        col_group = i // rows_count
        row_idx = i % rows_count
        x_base = 20 + col_group * macro_w
        y_base = 65 + row_idx * macro_h

        draw.text((x_base, y_base), f"{num:02d}. {name} ({s})", fill=(20, 20, 20), font=lbl_fnt)

        p_site = os.path.join(WORKSPACE, f"public/media/ekip/{s}.jpg")
        p_kad = os.path.join(WORKSPACE, f"docs/ekip/yz/codex/kadraj/{s}.jpg")

        for c_i, (sub_lbl, fp) in enumerate([("1 sitede", p_site), ("2 yeni kadraj", p_kad)]):
            cx = x_base + c_i * (cell + gap)
            cy = y_base + 26
            if os.path.exists(fp):
                im = Image.open(fp).convert("RGB").resize((cell, cell), Image.Resampling.LANCZOS)
                sheet.paste(im, (cx, cy))
                draw.rectangle([cx, cy + cell - 22, cx + 115, cy + cell], fill=(0, 0, 0))
                draw.text((cx + 6, cy + cell - 20), sub_lbl, fill=(255, 255, 255), font=sub_fnt)
            else:
                draw.rectangle([cx, cy, cx + cell, cy + cell], outline=(200, 80, 80), fill=(240, 230, 230))
                draw.text((cx + 90, cy + cell // 2 - 10), "TESLİM EDİLMEDİ", fill=(180, 30, 30), font=lbl_fnt)

    out_path = os.path.join(WORKSPACE, "docs/ekip/kontrol/kadraj-eksikler.jpg")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    sheet.save(out_path, "JPEG", quality=94)
    print("Saved:", out_path, sheet.size)

if __name__ == "__main__":
    build_pafta()
