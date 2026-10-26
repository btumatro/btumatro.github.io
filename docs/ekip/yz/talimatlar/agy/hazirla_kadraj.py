import base64
import glob
import io
import json
import os
import urllib.request
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from test_align import align_and_blend

KEY = os.environ.get("GEMINI_API_KEY", "")
OUT_KADRAJ = "docs/ekip/yz/codex/kadraj"
os.makedirs(OUT_KADRAJ, exist_ok=True)

# The 7 slugs where align_and_blend(site, docs/ekip/yz/kadraj/<slug>.jpg) produced a clean, seamless result:
USE_ALIGNED_KADRAJ1 = {
    "mehmet-onur-genc",
    "zeynep-seher-yolasigmaz",
    "nusret-bircan-keser",
    "muhammed-efe-coskunpinar",
    "melek-ozkeser",
    "melisa-aydirek",
    "eslem-kilic",
}

def outpaint_single_clean(slug: str, C: int = 720, X: int = 60, Y: int = 95) -> Image.Image:
    """
    Outpaints ONLY the grey border around public/media/ekip/{slug}.jpg with no distracting extra images,
    then aligns and blends with spatially-varying low-frequency color correction.
    """
    src = Image.open(f"public/media/ekip/{slug}.jpg").convert("RGB")
    can = Image.new("RGB", (C, C), (128, 128, 128))
    can.paste(src, (X, Y))
    b = io.BytesIO()
    can.save(b, "JPEG", quality=95)
    parts = [
        {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}},
        {
            "text": (
                "This photo is placed on a flat grey canvas. Outpaint: replace ONLY the flat grey border areas "
                "(top, left, right, bottom) by naturally extending the existing scene, background, hair, sunglasses, "
                "headscarf, shoulders and clothing so it looks like the original wider photo. Do not move, scale, or "
                "change anything inside the existing photo area; the person's face must stay in the exact same position "
                "and pixel-identical. Return the full 1:1 square image."
            )
        },
    ]
    body = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}},
    }
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": KEY},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        j = json.loads(resp.read().decode("utf-8"))
    for p in j["candidates"][0]["content"]["parts"]:
        if "inlineData" in p:
            gen = Image.open(io.BytesIO(base64.b64decode(p["inlineData"]["data"]))).convert("RGB").resize(
                (C, C), Image.Resampling.LANCZOS
            )
            # Local spatially-varying low-frequency color matching at exact (X, Y, 600, 600)
            P = 600
            s_arr = np.asarray(src, dtype=np.float32)
            g_arr = np.asarray(gen, dtype=np.float32)
            diff_box = s_arr - g_arr[Y : Y + P, X : X + P]
            diff_full = cv2.copyMakeBorder(
                diff_box, Y, C - (Y + P), X, C - (X + P), borderType=cv2.BORDER_REPLICATE
            )
            diff_smooth = cv2.GaussianBlur(diff_full, (81, 81), 28)
            g_corr = np.clip(g_arr + diff_smooth, 0, 255).astype(np.uint8)
            gen_corr = Image.fromarray(g_corr)

            margin = 36
            mask = Image.new("L", (C, C), 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                (X + margin, Y + margin, X + P - 1 - margin, Y + P - 1 - margin), radius=margin, fill=255
            )
            mask = mask.filter(ImageFilter.GaussianBlur(radius=18))
            canv = Image.new("RGB", (C, C))
            canv.paste(src, (X, Y))
            gen_corr.paste(canv, (0, 0), mask)
            return gen_corr.resize((600, 600), Image.Resampling.LANCZOS)
    raise RuntimeError(f"Failed to outpaint {slug}")

def main() -> None:
    slugs = sorted(os.path.basename(p)[:-4] for p in glob.glob("public/media/ekip/*.jpg"))
    for s in slugs:
        out_p = os.path.join(OUT_KADRAJ, f"{s}.jpg")
        src = Image.open(f"public/media/ekip/{s}.jpg").convert("RGB")
        if s in USE_ALIGNED_KADRAJ1:
            gen = Image.open(f"docs/ekip/yz/kadraj/{s}.jpg").convert("RGB")
            res, score, params = align_and_blend(src, gen, out_size=600)
            res.save(out_p, "JPEG", quality=92)
            print(f"{s:28s}: aligned from kadraj1 (NCC={score:.3f}, params={params})")
        elif s == "esma-demirkiyik":
            res = outpaint_single_clean(s, C=720, X=60, Y=95)
            res.save(out_p, "JPEG", quality=92)
            print(f"{s:28s}: freshly outpainted + spatially color-matched")
        else:
            # Use the clean grey-canvas outpaint from kadraj2
            k2 = Image.open(f"docs/ekip/yz/kadraj2/{s}.jpg").convert("RGB").resize((600, 600), Image.Resampling.LANCZOS)
            k2.save(out_p, "JPEG", quality=92)
            print(f"{s:28s}: copied clean kadraj2")

if __name__ == "__main__":
    main()
