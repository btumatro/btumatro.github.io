import os
import glob
import json
import time
import base64
import hashlib
import urllib.request
import cv2
import numpy as np
from PIL import Image, ImageDraw

from test_poisson_pilot import (
    WORKSPACE, SCRATCH, LOG_FILE, get_api_key, b64_encode_image,
    get_all_uncropped_refs, detect_face_box_in_site, align_and_poisson_blend, check_seam_strict
)

def build_soft_guide_from_uncropped(site_bgr, orig_bgr, top_Ratio=0.20, side_Ratio=0.12, bot_Ratio=0.06):
    """
    Locate where site_bgr (600x600) sits inside the uncropped orig_bgr.
    Extract the wider square (with extra top headroom, side width, and bottom shoulder room)
    DIRECTLY from orig_bgr wherever real pixels exist!
    Where the desired box extends beyond orig_bgr, fill with heavily blurred reflection + smooth cosine ramp
    so there is NO sharp edge or grey box anywhere in the guide image.
    """
    oh, ow = orig_bgr.shape[:2]
    site_small = cv2.resize(site_bgr, (150, 150))
    face_tpl = site_small[35:115, 35:115]

    f_sc = 450.0 / max(oh, ow)
    orig_s = cv2.resize(orig_bgr, (int(ow * f_sc), int(oh * f_sc)))
    best = (-1.0, 1.0, 0, 0)
    for sc in np.linspace(0.20, 2.2, 45):
        tw = int(80 * sc)
        if tw >= orig_s.shape[1] or tw >= orig_s.shape[0] or tw < 16:
            continue
        tpl = cv2.resize(face_tpl, (tw, tw))
        res = cv2.matchTemplate(orig_s, tpl, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(res)
        if mv > best[0]:
            best = (mv, sc, ml[0], ml[1])

    mv, sc, fx, fy = best
    if mv < 0.70:
        # Fallback to site_bgr if orig_bgr is a different scene
        orig_bgr = site_bgr
        oh, ow = 600, 600
        sx0, sy0, S = 0, 0, 600
    else:
        S = int(round((150 * sc) / f_sc))
        sx0 = int(round((fx - 35 * sc) / f_sc))
        sy0 = int(round((fy - 35 * sc) / f_sc))

    # Desired expanded square in orig_bgr coordinates:
    pad_top = int(round(S * top_Ratio))
    pad_bot = int(round(S * bot_Ratio))
    pad_side = int(round(S * side_Ratio))

    new_S = S + max(pad_top + pad_bot, 2 * pad_side)
    # Center horizontally around sx0 + S/2, and shift up by pad_top
    cx = sx0 + S // 2
    nx0 = cx - new_S // 2
    ny0 = sy0 - pad_top
    nx1 = nx0 + new_S
    ny1 = ny0 + new_S

    # How much outside [0..ow, 0..oh] do we go?
    need_l = max(0, -nx0)
    need_t = max(0, -ny0)
    need_r = max(0, nx1 - ow)
    need_b = max(0, ny1 - oh)

    if need_l == 0 and need_t == 0 and need_r == 0 and need_b == 0:
        # 100% REAL UNCROPPED PHOTOGRAPH! Zero outpainting needed!
        crop = orig_bgr[ny0:ny1, nx0:nx1]
        return cv2.resize(crop, (600, 600), interpolation=cv2.INTER_LANCZOS4), True

    # Extend orig_bgr with reflected border, then heavily blur the outer reflected zone with a smooth feather
    ext = cv2.copyMakeBorder(orig_bgr, need_t, need_b, need_l, need_r, cv2.BORDER_REFLECT_101)
    crop = ext[ny0 + need_t : ny1 + need_t, nx0 + need_l : nx1 + need_l]
    crop_600 = cv2.resize(crop, (600, 600), interpolation=cv2.INTER_LANCZOS4)

    # Create a mask of which pixels came from inside the real orig_bgr
    real_mask = np.zeros((oh, ow), dtype=np.float32)
    # Taper the outer 24px of real_mask smoothly so there is NEVER a sharp edge in the guide
    taper = max(12, int(round(min(oh, ow) * 0.04)))
    real_mask[taper:oh-taper, taper:ow-taper] = 1.0
    real_mask = cv2.GaussianBlur(real_mask, (0, 0), sigmaX=taper*0.6)
    ext_mask = cv2.copyMakeBorder(real_mask, need_t, need_b, need_l, need_r, cv2.BORDER_CONSTANT, value=0.0)
    mask_600 = cv2.resize(ext_mask[ny0 + need_t : ny1 + need_t, nx0 + need_l : nx1 + need_l], (600, 600))
    mask_600 = cv2.GaussianBlur(mask_600, (51, 51), 0)[:, :, None]

    blurred_bg = cv2.GaussianBlur(crop_600, (101, 101), 0)
    soft_guide = np.clip(crop_600 * mask_600 + blurred_bg * (1.0 - mask_600), 0, 255).astype(np.uint8)
    return soft_guide, False

def call_gemini_with_guide(slug, ref_paths, guide_bgr):
    key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={key}"

    parts = []
    img_hashes = []
    for p in ref_paths:
        b64, h, sz = b64_encode_image(p)
        img_hashes.append({"file": os.path.basename(p), "sha256_16": h, "size": sz})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})

    # Encode soft guide
    _, buf = cv2.imencode(".jpg", guide_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    raw_g = buf.tobytes()
    b64_g = base64.b64encode(raw_g).decode("ascii")
    img_hashes.append({"file": "soft_guide.jpg", "sha256_16": hashlib.sha256(raw_g).hexdigest()[:16], "size": [600, 600]})
    parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64_g}})

    prompt = (
        "İlk görseller kişinin kesilmemiş orijinal fotoğraflarıdır. "
        "SON GÖRSEL ise istediğimiz 1:1 kare kadraj yerleşimidir (baş ortada, üstte boşluk, altta omuzlar; kenarlardaki eksik kısımlar bulanıklaştırılmıştır). "
        "Son görseldeki kafa konumunu, boyutunu ve kadrajı BİREBİR koruyarak, bulanık kenarları orijinal fotoğraflardaki gerçek arka plan ve kıyafet dokusuyla "
        "kesintisiz, net ve doğal biçimde tamamla. Kişinin yüzünü, bakışını, kıyafetini ve ışığını hiç değiştirme; hiçbir çerçeve veya geçiş izi kalmasın."
    )
    parts.append({"text": prompt})

    body = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": "1:1"}
        }
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST"
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as resp:
        resp_data = json.loads(resp.read().decode("utf-8"))
    elapsed = round(time.time() - t0, 2)

    out_b64 = None
    for cand in resp_data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "inlineData" in part:
                out_b64 = part["inlineData"]["data"]
                break

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "slug": slug, "task": "kadraj_soft_guide_test",
            "refs": img_hashes, "elapsed_s": elapsed, "success": out_b64 is not None
        }, ensure_ascii=False) + "\n")

    arr = np.frombuffer(base64.b64decode(out_b64), dtype=np.uint8)
    out_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return cv2.resize(out_bgr, (600, 600), interpolation=cv2.INTER_LANCZOS4)

if __name__ == "__main__":
    test_slugs = ["emine-sultan-gunes", "duygu-solak", "irmak-karaagac", "feyza-karabicak"]
    rows = []
    for s in test_slugs:
        refs, best_scene = get_all_uncropped_refs(s)
        site_bgr = cv2.imread(os.path.join(WORKSPACE, f"public/media/ekip/{s}.jpg"))
        orig_bgr = cv2.imread(best_scene)
        # For feyza-karabicak, her head already has huge top margin in site_bgr, so top_Ratio=0.05, side=0.10, bot=0.10
        top_r = 0.04 if s == "feyza-karabicak" else 0.20
        guide_bgr, is_pure_real = build_soft_guide_from_uncropped(site_bgr, orig_bgr, top_Ratio=top_r)
        print(f"[{s}] is_pure_real={is_pure_real} primary={os.path.basename(best_scene)}")
        gem_bgr = call_gemini_with_guide(s, refs, guide_bgr)
        res = align_and_poisson_blend(site_bgr, orig_bgr, gem_bgr)
        c_pf = check_seam_strict(res["poisson_face"], res["site_box"])
        print(f"  mv_gem={res['mv_gem']:.3f} poisson_face seam_check={c_pf}")
        rows.append((s, site_bgr, guide_bgr, gem_bgr, res["poisson_face"]))

    canvas = Image.new("RGB", (4 * 620 + 20, len(rows) * 650 + 20), (240, 240, 240))
    draw = ImageDraw.Draw(canvas)
    for r_i, (s, im1, im2, im3, im4) in enumerate(rows):
        y0 = 10 + r_i * 650
        for c_i, (lbl, bgr) in enumerate([("1_site", im1), ("2_soft_guide", im2), ("3_gem_out", im3), ("4_poisson_face", im4)]):
            x0 = 10 + c_i * 620
            canvas.paste(Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)), (x0, y0 + 35))
            draw.text((x0 + 5, y0 + 8), f"{s} - {lbl}", fill=(0, 0, 0))
    out_p = os.path.join(SCRATCH, "pilot_soft_guide_test.jpg")
    canvas.save(out_p, "JPEG", quality=95)
    print("Saved", out_p)
