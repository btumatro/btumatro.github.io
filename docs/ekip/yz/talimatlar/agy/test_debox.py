import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import base64, hashlib, json, time, urllib.request

from test_poisson_pilot import (
    WORKSPACE, SCRATCH, LOG_FILE, get_api_key, b64_encode_image,
    get_all_uncropped_refs, detect_face_box_in_site, align_and_poisson_blend, check_seam_strict
)

def build_grey_pad_from_uncropped(site_bgr, orig_bgr, top_Ratio=0.18, side_Ratio=0.11, bot_Ratio=0.06):
    """
    Locate site_bgr (600x600) inside uncropped orig_bgr.
    Extract the desired wider square from orig_bgr so all real pixels (top, bottom, left, right)
    available in orig_bgr are used!
    Only where the desired square extends outside orig_bgr, pad with solid neutral grey (128,128,128).
    Returns:
      canvas_600: 600x600 BGR image
      real_box_600: (rx0, ry0, rx1, ry1) inside 600x600 where pixels are 100% from orig_bgr
      real_crop_600: 600x600 BGR image with reflected (non-grey) border for clean reference
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
    if mv < 0.65:
        orig_bgr = site_bgr
        oh, ow = 600, 600
        sx0, sy0, S = 0, 0, 600
    else:
        S = int(round((150 * sc) / f_sc))
        sx0 = int(round((fx - 35 * sc) / f_sc))
        sy0 = int(round((fy - 35 * sc) / f_sc))

    pad_top = int(round(S * top_Ratio))
    pad_bot = int(round(S * bot_Ratio))
    pad_side = int(round(S * side_Ratio))

    new_S = S + max(pad_top + pad_bot, 2 * pad_side)
    cx = sx0 + S // 2
    nx0 = cx - new_S // 2
    ny0 = sy0 - pad_top
    nx1 = nx0 + new_S
    ny1 = ny0 + new_S

    need_l = max(0, -nx0)
    need_t = max(0, -ny0)
    need_r = max(0, nx1 - ow)
    need_b = max(0, ny1 - oh)

    ext_grey = cv2.copyMakeBorder(orig_bgr, need_t, need_b, need_l, need_r, cv2.BORDER_CONSTANT, value=(128, 128, 128))
    crop_grey = ext_grey[ny0 + need_t : ny1 + need_t, nx0 + need_l : nx1 + need_l]
    canvas_600 = cv2.resize(crop_grey, (600, 600), interpolation=cv2.INTER_LANCZOS4)

    ext_ref = cv2.copyMakeBorder(orig_bgr, need_t, need_b, need_l, need_r, cv2.BORDER_REFLECT_101)
    crop_ref = ext_ref[ny0 + need_t : ny1 + need_t, nx0 + need_l : nx1 + need_l]
    real_crop_600 = cv2.resize(crop_ref, (600, 600), interpolation=cv2.INTER_LANCZOS4)

    # Real box coordinates in 600x600:
    rx0 = int(round((need_l / new_S) * 600))
    ry0 = int(round((need_t / new_S) * 600))
    rx1 = int(round(((new_S - need_r) / new_S) * 600))
    ry1 = int(round(((new_S - need_b) / new_S) * 600))
    return canvas_600, (rx0, ry0, rx1, ry1), real_crop_600

def remove_box_boundary_steps(gem_bgr, real_box_600):
    """
    If Gemini leaves any faint horizontal/vertical step along rx0, ry0, rx1, ry1 where the grey border was,
    measure the low-frequency step right across each boundary line and subtract a smooth decaying ramp
    on the outpainted side, plus blend a 14px band across the boundary in gradient/Laplacian domain!
    """
    out = gem_bgr.astype(np.float32).copy()
    rx0, ry0, rx1, ry1 = real_box_600

    # Top boundary at y = ry0
    if 8 < ry0 < 592:
        inside = out[ry0+2 : ry0+6, :, :].mean(axis=0) # (600, 3)
        outside = out[max(0, ry0-5) : max(1, ry0-1), :, :].mean(axis=0)
        step = cv2.GaussianBlur((inside - outside).reshape(1, 600, 3), (31, 1), 0).reshape(600, 3)
        for y in range(0, ry0 + 1):
            decay = np.exp(-max(0, ry0 - y) / 28.0)
            out[y, :, :] += step * decay
        # Also feather the 5px transition band at ry0
        band = cv2.GaussianBlur(out, (7, 15), 0)
        for y in range(max(0, ry0 - 6), min(600, ry0 + 7)):
            w = np.exp(-((y - ry0) ** 2) / (2 * 2.5 ** 2))
            out[y, :, :] = out[y, :, :] * (1.0 - w) + band[y, :, :] * w

    # Bottom boundary at y = ry1
    if 8 < ry1 < 592:
        inside = out[ry1-6 : ry1-2, :, :].mean(axis=0)
        outside = out[min(599, ry1+1) : min(600, ry1+5), :, :].mean(axis=0)
        step = cv2.GaussianBlur((inside - outside).reshape(1, 600, 3), (31, 1), 0).reshape(600, 3)
        for y in range(ry1, 600):
            decay = np.exp(-max(0, y - ry1) / 28.0)
            out[y, :, :] += step * decay
        band = cv2.GaussianBlur(out, (7, 15), 0)
        for y in range(max(0, ry1 - 6), min(600, ry1 + 7)):
            w = np.exp(-((y - ry1) ** 2) / (2 * 2.5 ** 2))
            out[y, :, :] = out[y, :, :] * (1.0 - w) + band[y, :, :] * w

    # Left boundary at x = rx0
    if 8 < rx0 < 592:
        inside = out[:, rx0+2 : rx0+6, :].mean(axis=1) # (600, 3)
        outside = out[:, max(0, rx0-5) : max(1, rx0-1), :].mean(axis=1)
        step = cv2.GaussianBlur((inside - outside).reshape(600, 1, 3), (1, 31), 0).reshape(600, 3)
        for x in range(0, rx0 + 1):
            decay = np.exp(-max(0, rx0 - x) / 28.0)
            out[:, x, :] += step * decay
        band = cv2.GaussianBlur(out, (15, 7), 0)
        for x in range(max(0, rx0 - 6), min(600, rx0 + 7)):
            w = np.exp(-((x - rx0) ** 2) / (2 * 2.5 ** 2))
            out[:, x, :] = out[:, x, :] * (1.0 - w) + band[:, x, :] * w

    # Right boundary at x = rx1
    if 8 < rx1 < 592:
        inside = out[:, rx1-6 : rx1-2, :].mean(axis=1)
        outside = out[:, min(599, rx1+1) : min(600, rx1+5), :].mean(axis=1)
        step = cv2.GaussianBlur((inside - outside).reshape(600, 1, 3), (1, 31), 0).reshape(600, 3)
        for x in range(rx1, 600):
            decay = np.exp(-max(0, x - rx1) / 28.0)
            out[:, x, :] += step * decay
        band = cv2.GaussianBlur(out, (15, 7), 0)
        for x in range(max(0, rx1 - 6), min(600, rx1 + 7)):
            w = np.exp(-((x - rx1) ** 2) / (2 * 2.5 ** 2))
            out[:, x, :] = out[:, x, :] * (1.0 - w) + band[:, x, :] * w

    return np.clip(out, 0, 255).astype(np.uint8)

def call_gemini_outpaint_with_refs(slug, ref_paths, grey_canvas_600):
    key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={key}"

    parts = []
    img_hashes = []
    for p in ref_paths:
        b64, h, sz = b64_encode_image(p)
        img_hashes.append({"file": os.path.basename(p), "sha256_16": h, "size": sz})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})

    _, buf = cv2.imencode(".jpg", grey_canvas_600, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
    raw_c = buf.tobytes()
    b64_c = base64.b64encode(raw_c).decode("ascii")
    img_hashes.append({"file": "grey_canvas_600.jpg", "sha256_16": hashlib.sha256(raw_c).hexdigest()[:16], "size": [600, 600]})
    parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64_c}})

    prompt = (
        "İlk görseller kişinin kesilmemiş orijinal referans fotoğraflarıdır. "
        "SON GÖRSELDE ise fotoğraf kadrajı genişletilmiş ve fotoğrafta eksik kalan dar kenar şeritleri düz gri (RGB 128,128,128) ile işaretlenmiştir. "
        "Son görseldeki kişinin konumunu, boyutunu ve yüzünü HİÇ değiştirmeden, yalnızca düz gri kenar şeritlerini "
        "fotoğrafın gerçek arka planı, tavanı, duvarı ve omuzlarıyla kesintisiz, aynı renk ve parlaklıkta tamamla. "
        "Gri alanla fotoğraf arasında hiçbir çizgi, basamak veya ton farkı kalmasın."
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
            "slug": slug, "task": "kadraj_uncropped_poisson",
            "refs": img_hashes, "elapsed_s": elapsed, "success": out_b64 is not None
        }, ensure_ascii=False) + "\n")

    arr = np.frombuffer(base64.b64decode(out_b64), dtype=np.uint8)
    out_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return cv2.resize(out_bgr, (600, 600), interpolation=cv2.INTER_LANCZOS4)

if __name__ == "__main__":
    s = "emine-sultan-gunes"
    refs, best_scene = get_all_uncropped_refs(s)
    site_bgr = cv2.imread(os.path.join(WORKSPACE, f"public/media/ekip/{s}.jpg"))
    orig_bgr = cv2.imread(best_scene)
    canvas_600, real_box, real_crop_600 = build_grey_pad_from_uncropped(site_bgr, orig_bgr)
    print("real_box:", real_box)
    gem_bgr = call_gemini_outpaint_with_refs(s, refs, canvas_600)
    gem_deboxed = remove_box_boundary_steps(gem_bgr, real_box)
    res = align_and_poisson_blend(site_bgr, orig_bgr, gem_deboxed)
    c_raw = check_seam_strict(gem_bgr, real_box)
    c_deb = check_seam_strict(res["poisson_face"], real_box)
    print("mv_gem:", res["mv_gem"])
    print("seam raw    :", c_raw)
    print("seam deboxed:", c_deb)
    cv2.imwrite(os.path.join(SCRATCH, "emine_deboxed_poisson.jpg"), res["poisson_face"])
