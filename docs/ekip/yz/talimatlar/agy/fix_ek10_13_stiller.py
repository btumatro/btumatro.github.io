import os
import json
import time
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from uret_ek10_stil_ve_sheet import (
    WORKSPACE,
    SCRATCH,
    STIL_DIR,
    KONTROL_DIR,
    CACHE_DIR,
    PEOPLE_SPECS,
    STYLES,
    b64_encode_image,
    call_gemini_image,
    get_person_reference_parts,
)

# The 13 cells that had split-screen or Style-A dark lamp carryover when Style A was in history[1]:
TO_REGEN = [
    ("adem-baglan", "b"),
    ("adem-baglan", "c"),
    ("adem-baglan", "d"),
    ("adem-baglan", "e"),
    ("adem-baglan", "f"),
    ("irmak-karaagac", "b"),
    ("irmak-karaagac", "d"),
    ("irmak-karaagac", "e"),
    ("irmak-karaagac", "f"),
    ("muhammed-ataman", "b"),
    ("muhammed-ataman", "d"),
    ("muhammed-ataman", "e"),
    ("muhammed-ataman", "f"),
]


def regen_single_style(slug, style_code):
    person = next(p for p in PEOPLE_SPECS if p["slug"] == slug)
    st = next(s for s in STYLES if s["code"] == style_code)
    traits = person["traits"]

    ref_parts, ref_hashes = get_person_reference_parts(slug)
    gri_path = os.path.join(WORKSPACE, f"docs/ekip/yz/codex/gri-fon/{slug}.jpg")
    gri_b64, _, _ = b64_encode_image(gri_path, max_dim=1024)

    # Turn 1 of the person's multi-turn conversation: all uncropped originals + gri-fon portrait anchored
    turn1_user = {
        "role": "user",
        "parts": ref_parts + [
            {
                "text": (
                    f"Bu görseller ekip üyemiz {person['name']}'ın kesilmemiş orijinal fotoğrafları ve düz orta-gri stüdyo portresidir. "
                    f"Sabit kimlik özellikleri: {traits} "
                    f"Sonraki adımda bu kişiyi farklı bir illüstrasyon stilinde, kimliğini ve kıyafetini hiç değiştirmeden çizeceğiz."
                )
            }
        ],
    }
    turn1_model = {
        "role": "model",
        "parts": [
            {
                "text": (
                    f"Anlaşıldı. {person['name']}'ın yüz kemik yapısı, göz-kaş-burun-ağız oranları, saç/başörtüsü/sakal biçimi "
                    f"ve kıyafet detayları referans fotoğraflardan ve gri fon portresinden sabitlendi."
                )
            },
            {"inlineData": {"mimeType": "image/jpeg", "data": gri_b64}},
        ],
    }

    # Turn 2: Request the specific style as a SINGLE centered 1:1 portrait (no split-screen!)
    turn2_parts = []
    turn2_hashes = list(ref_hashes)
    for sref in st["style_refs"]:
        crop_box = (0, 0, 750, 1350) if "KARAKTER_KIMLIK_PAFTASI" in sref else None
        sb64, sh, ssz = b64_encode_image(sref, max_dim=1200, crop_box=crop_box)
        turn2_hashes.append({"file": os.path.basename(sref), "role": "yalnız stil referansı", "sha256_16": sh, "size": ssz})
        turn2_parts.append({"inlineData": {"mimeType": "image/jpeg", "data": sb64}})

    prompt_text = (
        f"GÖREV: {person['name']} için TEK BİR tam kare (1:1) baş-omuz (head-and-shoulders, ortalı) portre üret.\n"
        f"SABİT KİMLİK ÇAPALARI: {traits}\n"
        f"KESİN KURALLAR:\n"
        f"- Görseli ASLA ikiye bölme; yan yana karşılaştırma (split-screen, before/after) veya çoklu panel ÇİZME. Tuvalde yalnızca TEK bir portre olsun.\n"
        f"- Arka plana masa lambası veya oda eşyası ÇİZME; yalnızca bu stilin kendi düz arka planını kullan.\n"
        f"- Yüzü güzelleştirme, gözleri büyütme veya başka bir modele benzetme YOK; kişinin gerçek yüz oranları birebir korunmalı.\n"
        f"- Görsel içinde hiçbir yazı, etiket veya çerçeve OLMASIN.\n\n"
        f"{st['prompt']}"
    )
    turn2_parts.append({"text": prompt_text})

    contents = [turn1_user, turn1_model, {"role": "user", "parts": turn2_parts}]
    out_b64, _ = call_gemini_image(
        contents,
        aspect_ratio="1:1",
        log_meta={"slug": slug, "task": f"stil_{style_code}_v2", "refs": turn2_hashes},
    )
    arr = np.frombuffer(base64.b64decode(out_b64), dtype=np.uint8)
    im_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    im_600 = cv2.resize(im_bgr, (600, 600), interpolation=cv2.INTER_AREA)

    out_path = os.path.join(STIL_DIR, f"{style_code}-{slug}.jpg")
    cache_path = os.path.join(CACHE_DIR, f"{style_code}-{slug}.jpg")
    cv2.imwrite(cache_path, im_600, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    cv2.imwrite(out_path, im_600, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
    print(f"[FIXED] {style_code}-{slug}.jpg")
    return f"{style_code}-{slug}.jpg"


def rebuild_pafta():
    cell_w, cell_h = 320, 320
    pad_x, pad_y = 18, 22
    left_label_w = 270
    header_h = 110

    cols = [
        ("0. Referans (Gri Fon)", "ref"),
        ("1. a) Zeki Reels Sahne", "a"),
        ("2. b) Zeki Karakter Paftası", "b"),
        ("3. c) Yumuşak 3B Animasyon", "c"),
        ("4. d) Düz Vektör / Flat", "d"),
        ("5. e) Suluboya Portre", "e"),
        ("6. f) Çizgi Roman (Halftone)", "f"),
    ]

    n_rows = len(PEOPLE_SPECS)
    n_cols = len(cols)

    total_w = left_label_w + n_cols * (cell_w + pad_x) + pad_x
    total_h = header_h + n_rows * (cell_h + pad_y) + pad_y

    sheet = Image.new("RGB", (total_w, total_h), (245, 245, 247))
    draw = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
        font_col = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
        font_row = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    except Exception:
        font_title = ImageFont.load_default()
        font_col = font_title
        font_row = font_title
        font_sub = font_title

    draw.text(
        (pad_x, 18),
        "BTU MATRO - Stilize Karakter Örnek Paftası (3 Kişi x 6 Stil Karşılaştırması)",
        fill=(20, 20, 25),
        font=font_title,
    )

    for c_idx, (col_title, _) in enumerate(cols):
        cx = left_label_w + c_idx * (cell_w + pad_x)
        cy = 64
        draw.rounded_rectangle([cx, cy, cx + cell_w, cy + 38], radius=6, fill=(32, 36, 45))
        draw.text((cx + 12, cy + 9), col_title, fill=(255, 255, 255), font=font_col)

    for r_idx, person in enumerate(PEOPLE_SPECS):
        slug = person["slug"]
        ry = header_h + r_idx * (cell_h + pad_y)

        draw.rounded_rectangle([pad_x, ry, left_label_w - 12, ry + cell_h], radius=8, fill=(232, 233, 238))
        draw.text((pad_x + 14, ry + 120), f"{person['num']}. {person['name']}", fill=(20, 20, 25), font=font_row)
        draw.text((pad_x + 14, ry + 150), f"({slug})", fill=(90, 92, 100), font=font_sub)

        for c_idx, (col_title, code) in enumerate(cols):
            cx = left_label_w + c_idx * (cell_w + pad_x)
            if code == "ref":
                img_path = os.path.join(WORKSPACE, f"docs/ekip/yz/codex/gri-fon/{slug}.jpg")
            else:
                img_path = os.path.join(STIL_DIR, f"{code}-{slug}.jpg")

            if os.path.exists(img_path):
                im = Image.open(img_path).convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS)
                sheet.paste(im, (cx, ry))
                badge = "Gri Fon" if code == "ref" else f"{code}) {col_title.split(') ')[1]}"
                draw.rectangle([cx, ry + cell_h - 26, cx + 215, ry + cell_h], fill=(0, 0, 0))
                draw.text((cx + 7, ry + cell_h - 22), badge, fill=(255, 255, 255), font=font_sub)

    out_pafta = os.path.join(KONTROL_DIR, "stil-ornekleri.jpg")
    sheet.save(out_pafta, "JPEG", quality=93)
    print(f"[REBUILT PAFTA] {out_pafta} ({sheet.size[0]}x{sheet.size[1]})")


if __name__ == "__main__":
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = [ex.submit(regen_single_style, s, c) for s, c in TO_REGEN]
        for f in as_completed(futs):
            f.result()
    rebuild_pafta()
    print(f"Finished fixing 13 styles in {round(time.time() - t0, 1)}s")
