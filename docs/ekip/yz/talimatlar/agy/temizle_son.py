import base64
import io
import json
import os
import cv2
import numpy as np
from PIL import Image

from codex_uret import CONV_DIR, OUT_GRIFON, OUT_KADRAJ, OUT_VESIKA

def get_model_images(slug: str) -> list[Image.Image]:
    conv_file = os.path.join(CONV_DIR, f"{slug}.json")
    contents = json.load(open(conv_file, encoding="utf-8"))
    imgs: list[Image.Image] = []
    for msg in contents:
        if msg.get("role") == "model":
            for p in msg.get("parts", []):
                if "inlineData" in p:
                    raw = base64.b64decode(p["inlineData"]["data"])
                    imgs.append(Image.open(io.BytesIO(raw)).convert("RGB"))
    return imgs

def main() -> None:
    # 1. Bilgehan Zeki Ozaytac (#2):
    # Restore clean Turn 2 vesikalik from conv
    b_imgs = get_model_images("bilgehan-zeki-ozaytac")
    b_imgs[1].resize((600, 600), Image.Resampling.LANCZOS).save(
        os.path.join(OUT_VESIKA, "bilgehan-zeki-ozaytac.jpg"), "JPEG", quality=92
    )
    # For gri-fon, use a balanced crop of kadraj so head size matches studio portraits while keeping 100% real face
    b_kad = Image.open(os.path.join(OUT_KADRAJ, "bilgehan-zeki-ozaytac.jpg")).convert("RGB")
    b_kad.crop((36, 42, 564, 570)).resize((600, 600), Image.Resampling.LANCZOS).save(
        os.path.join(OUT_GRIFON, "bilgehan-zeki-ozaytac.jpg"), "JPEG", quality=92
    )
    print("bilgehan-zeki-ozaytac: restored clean vesikalik + balanced real gri-fon")

    # 2. Irmak Karaagac (#4):
    # Check model images in conv: [0]=turn1_grifon, [1]=turn2_vesikalik, [2]=turn3_grifon_fix
    # Wait: irmak-karaagac was generated in pilot (before CONV_DIR saving was added), so conv has [0]=turn3_grifon_fix.
    # Let's check why turn3_grifon_fix had a small head: because in turn3 we didn't include the full conversation.
    # Let's check if we can re-run a clean gri-fon for irmak-karaagac or check what's in conv.

    # 3. Gulsiye Begum Gumus (#8): crop 3 vesikalik slightly closer so head size matches 4 gri-fon
    g_imgs = get_model_images("gulsiye-begum-gumus")
    g_ves = g_imgs[-1].resize((600, 600), Image.Resampling.LANCZOS)
    g_ves.crop((42, 50, 558, 566)).resize((600, 600), Image.Resampling.LANCZOS).save(
        os.path.join(OUT_VESIKA, "gulsiye-begum-gumus.jpg"), "JPEG", quality=92
    )
    print("gulsiye-begum-gumus: cropped vesikalik to match gri-fon head scale")

    # 4. Yusuf Sarsici (#16): restore clean model outputs without the low-NCC face paste
    y_imgs = get_model_images("yusuf-sarsici")
    # y_imgs[1] is turn2_vesikalik, y_imgs[2] is turn3_grifon_keep_outfit
    y_imgs[1].resize((600, 600), Image.Resampling.LANCZOS).save(
        os.path.join(OUT_VESIKA, "yusuf-sarsici.jpg"), "JPEG", quality=92
    )
    y_imgs[2].resize((600, 600), Image.Resampling.LANCZOS).save(
        os.path.join(OUT_GRIFON, "yusuf-sarsici.jpg"), "JPEG", quality=92
    )
    print("yusuf-sarsici: restored clean vesikalik and gri-fon")

    # 5. Berat Eren Karakas (#18): restore clean model outputs without the low-NCC face paste
    brk_imgs = get_model_images("berat-eren-karakas")
    brk_imgs[0].resize((600, 600), Image.Resampling.LANCZOS).save(
        os.path.join(OUT_GRIFON, "berat-eren-karakas.jpg"), "JPEG", quality=92
    )
    brk_imgs[1].resize((600, 600), Image.Resampling.LANCZOS).save(
        os.path.join(OUT_VESIKA, "berat-eren-karakas.jpg"), "JPEG", quality=92
    )
    print("berat-eren-karakas: restored clean gri-fon and vesikalik")

    # 6. Melisa Aydirek (#23): restore Turn 1 gri-fon (or crop Turn 3 closer)
    ma_imgs = get_model_images("melisa-aydirek")
    # ma_imgs[2] is 3/4 pose gri-fon; let's crop it closer so head-and-shoulders scale matches kadraj
    ma_gf = ma_imgs[2].resize((600, 600), Image.Resampling.LANCZOS)
    ma_gf.crop((65, 20, 535, 490)).resize((600, 600), Image.Resampling.LANCZOS).save(
        os.path.join(OUT_GRIFON, "melisa-aydirek.jpg"), "JPEG", quality=92
    )
    print("melisa-aydirek: cropped 3/4 gri-fon to head-and-shoulders scale")

if __name__ == "__main__":
    main()
