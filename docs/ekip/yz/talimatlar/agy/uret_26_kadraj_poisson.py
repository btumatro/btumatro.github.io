import os
import glob
import json
import time
import base64
import hashlib
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import cv2
import numpy as np
from PIL import Image, ImageDraw

WORKSPACE = "/Users/wildgenie/Projects/btu-matro"
SCRATCH = "/Users/wildgenie/.gemini/antigravity-cli/brain/482501c3-e797-49fa-a7d5-231ae28c4675/scratch"
OUT_KADRAJ_DIR = os.path.join(WORKSPACE, "docs/ekip/yz/codex/kadraj")
CACHE_DIR = os.path.join(SCRATCH, "kadraj_ek5_cache")
os.makedirs(OUT_KADRAJ_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
LOG_FILE = os.path.join(SCRATCH, "gemini_calls.jsonl")
log_lock = threading.Lock()

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    return key

def b64_encode_image(path, max_dim=1600):
    im = Image.open(path).convert("RGB")
    if max(im.size) > max_dim:
        im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    import io
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    raw = buf.getvalue()
    return base64.b64encode(raw).decode("ascii"), hashlib.sha256(raw).hexdigest()[:16], im.size

def get_all_uncropped_refs(slug):
    """
    Collect all uncropped originals from docs/ekip/orijinal/<slug>*.jpg and docs/ekip/alternatif/<slug>.jpg.
    Find the uncropped original that matches the site photo scene best (highest NCC match) and place it LAST
    before the framing canvas.
    """
    orij_files = sorted(glob.glob(os.path.join(WORKSPACE, f"docs/ekip/orijinal/{slug}*.jpg")))
    alt_files = sorted(glob.glob(os.path.join(WORKSPACE, f"docs/ekip/alternatif/{slug}*.jpg")))
    site_file = os.path.join(WORKSPACE, f"public/media/ekip/{slug}.jpg")

    site_im = cv2.imread(site_file)
    site_small = cv2.resize(site_im, (150, 150))
    face_tpl = site_small[35:115, 35:115]

    scored = []
    for p in orij_files:
        bn = os.path.basename(p)
        if "-grup-" in bn or "-kursu" in bn or "-bilgehan-" in bn:
            continue
        im = cv2.imread(p)
        if im is None:
            continue
        oh, ow = im.shape[:2]
        f_sc = 400.0 / max(oh, ow)
        im_s = cv2.resize(im, (int(ow * f_sc), int(oh * f_sc)))
        local_best = -1.0
        for sc in np.linspace(0.20, 2.0, 32):
            tw = int(80 * sc)
            if tw >= im_s.shape[1] or tw >= im_s.shape[0] or tw < 16:
                continue
            tpl = cv2.resize(face_tpl, (tw, tw))
            res = cv2.matchTemplate(im_s, tpl, cv2.TM_CCOEFF_NORMED)
            _, mv, _, _ = cv2.minMaxLoc(res)
            if mv > local_best:
                local_best = mv
        scored.append((local_best, ow * oh, p))

    if scored:
        max_mv = max(x[0] for x in scored)
        # Among files within 0.025 of max_mv, pick the largest resolution (uncropped original)
        top_cands = [x for x in scored if x[0] >= max_mv - 0.025]
        top_cands.sort(key=lambda x: (x[1], x[0]), reverse=True)
        best_scene_file = top_cands[0][2]
    else:
        best_scene_file = site_file

    all_candidates = orij_files + alt_files
    unique_refs = []
    for p in all_candidates:
        bn = os.path.basename(p)
        if "-grup-" in bn or "-kursu" in bn:
            continue
        im = Image.open(p).convert("RGB").resize((64, 64))
        arr = np.asarray(im, dtype=np.float32)
        is_dup = False
        for i, (prev_p, prev_arr) in enumerate(unique_refs):
            if np.mean(np.abs(arr - prev_arr)) < 2.2:
                if os.path.getsize(p) > os.path.getsize(prev_p):
                    unique_refs[i] = (p, arr)
                is_dup = True
                break
        if not is_dup:
            unique_refs.append((p, arr))

    ref_paths = [p for p, _ in unique_refs]
    if best_scene_file in ref_paths:
        ref_paths.remove(best_scene_file)
    ref_paths.append(best_scene_file)
    return ref_paths, best_scene_file

def get_framing_ratios(slug):
    if slug == "feyza-karabicak":
        return 0.03, 0.08, 0.09
    if slug == "bilgehan-zeki-ozaytac":
        return 0.10, 0.08, 0.07
    if slug in ("irmak-karaagac", "yusuf-sarsici"):
        return 0.18, 0.12, 0.08
    return 0.18, 0.11, 0.06

def build_grey_pad_from_uncropped(site_bgr, orig_bgr, top_Ratio=0.18, side_Ratio=0.11, bot_Ratio=0.06):
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

    rx0 = int(round((need_l / new_S) * 600))
    ry0 = int(round((need_t / new_S) * 600))
    rx1 = int(round(((new_S - need_r) / new_S) * 600))
    ry1 = int(round(((new_S - need_b) / new_S) * 600))
    return canvas_600, (rx0, ry0, rx1, ry1), real_crop_600

def remove_box_boundary_steps(gem_bgr, real_box_600):
    out = gem_bgr.astype(np.float32).copy()
    rx0, ry0, rx1, ry1 = real_box_600

    if 6 < ry0 < 594:
        inside = out[ry0+2 : ry0+6, :, :].mean(axis=0)
        outside = out[max(0, ry0-5) : max(1, ry0-1), :, :].mean(axis=0)
        step = cv2.GaussianBlur((inside - outside).reshape(1, 600, 3), (31, 1), 0).reshape(600, 3)
        for y in range(0, ry0 + 1):
            decay = np.exp(-max(0, ry0 - y) / 28.0)
            out[y, :, :] += step * decay
        band = cv2.GaussianBlur(out, (7, 17), 0)
        for y in range(max(0, ry0 - 7), min(600, ry0 + 8)):
            w = np.exp(-((y - ry0) ** 2) / (2 * 2.8 ** 2))
            out[y, :, :] = out[y, :, :] * (1.0 - w) + band[y, :, :] * w

    if 6 < ry1 < 594:
        inside = out[ry1-6 : ry1-2, :, :].mean(axis=0)
        outside = out[min(599, ry1+1) : min(600, ry1+5), :, :].mean(axis=0)
        step = cv2.GaussianBlur((inside - outside).reshape(1, 600, 3), (31, 1), 0).reshape(600, 3)
        for y in range(ry1, 600):
            decay = np.exp(-max(0, y - ry1) / 28.0)
            out[y, :, :] += step * decay
        band = cv2.GaussianBlur(out, (7, 17), 0)
        for y in range(max(0, ry1 - 7), min(600, ry1 + 8)):
            w = np.exp(-((y - ry1) ** 2) / (2 * 2.8 ** 2))
            out[y, :, :] = out[y, :, :] * (1.0 - w) + band[y, :, :] * w

    if 6 < rx0 < 594:
        inside = out[:, rx0+2 : rx0+6, :].mean(axis=1)
        outside = out[:, max(0, rx0-5) : max(1, rx0-1), :].mean(axis=1)
        step = cv2.GaussianBlur((inside - outside).reshape(600, 1, 3), (1, 31), 0).reshape(600, 3)
        for x in range(0, rx0 + 1):
            decay = np.exp(-max(0, rx0 - x) / 28.0)
            out[:, x, :] += step * decay
        band = cv2.GaussianBlur(out, (17, 7), 0)
        for x in range(max(0, rx0 - 7), min(600, rx0 + 8)):
            w = np.exp(-((x - rx0) ** 2) / (2 * 2.8 ** 2))
            out[:, x, :] = out[:, x, :] * (1.0 - w) + band[:, x, :] * w

    if 6 < rx1 < 594:
        inside = out[:, rx1-6 : rx1-2, :].mean(axis=1)
        outside = out[:, min(599, rx1+1) : min(600, rx1+5), :].mean(axis=1)
        step = cv2.GaussianBlur((inside - outside).reshape(600, 1, 3), (1, 31), 0).reshape(600, 3)
        for x in range(rx1, 600):
            decay = np.exp(-max(0, x - rx1) / 28.0)
            out[:, x, :] += step * decay
        band = cv2.GaussianBlur(out, (17, 7), 0)
        for x in range(max(0, rx1 - 7), min(600, rx1 + 8)):
            w = np.exp(-((x - rx1) ** 2) / (2 * 2.8 ** 2))
            out[:, x, :] = out[:, x, :] * (1.0 - w) + band[:, x, :] * w

    return np.clip(out, 0, 255).astype(np.uint8)

def detect_face_box_in_site(site_bgr):
    gray = cv2.cvtColor(site_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    energy = cv2.GaussianBlur(np.hypot(gx, gy), (51, 51), 0)
    yy, xx = np.mgrid[0:600, 0:600]
    prior = np.exp(-((xx - 300)**2 / (2 * 95**2) + (yy - 275)**2 / (2 * 105**2)))
    weighted = energy * prior
    cy, cx = np.unravel_index(np.argmax(weighted), weighted.shape)
    cx = int(np.clip(cx, 220, 380))
    cy = int(np.clip(cy, 200, 350))
    fw, fh = 250, 280
    return cx - fw // 2, cy - fh // 2, fw, fh

def align_and_poisson_face(site_bgr, real_crop_600, gem_bgr):
    """
    Align real_crop_600 / site_bgr to gem_bgr and blend ONLY the inner elliptical face oval
    using Poisson seamlessClone (cv2.NORMAL_CLONE).
    """
    fx, fy, fw, fh = detect_face_box_in_site(site_bgr)
    pad_w, pad_h = int(fw * 0.12), int(fh * 0.12)
    tx0, ty0 = max(0, fx + pad_w), max(0, fy + pad_h)
    tx1, ty1 = min(600, fx + fw - pad_w), min(600, fy + fh - pad_h)
    face_tpl = site_bgr[ty0:ty1, tx0:tx1]
    th0, tw0 = face_tpl.shape[:2]

    best_gem = (-1.0, 1.0, 0, 0)
    for sc in np.linspace(0.45, 1.15, 71):
        tw, th = int(tw0 * sc), int(th0 * sc)
        if tw < 40 or th < 40 or tw >= 580 or th >= 580:
            continue
        tpl = cv2.resize(face_tpl, (tw, th), interpolation=cv2.INTER_AREA)
        res = cv2.matchTemplate(gem_bgr, tpl, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(res)
        if mv > best_gem[0]:
            best_gem = (mv, sc, ml[0], ml[1])

    mv_gem, sc_gem, gx, gy = best_gem
    site_scale = sc_gem
    site_x0 = int(round(gx - tx0 * site_scale))
    site_y0 = int(round(gy - ty0 * site_scale))
    scaled_w = int(round(600 * site_scale))
    scaled_h = int(round(600 * site_scale))

    aligned_src = gem_bgr.copy()
    site_resized = cv2.resize(site_bgr, (scaled_w, scaled_h), interpolation=cv2.INTER_LANCZOS4)
    dx0 = max(0, site_x0)
    dy0 = max(0, site_y0)
    dx1 = min(600, site_x0 + scaled_w)
    dy1 = min(600, site_y0 + scaled_h)

    sx0 = dx0 - site_x0
    sy0 = dy0 - site_y0
    sx1 = sx0 + (dx1 - dx0)
    sy1 = sy0 + (dy1 - dy0)

    if dx1 > dx0 and dy1 > dy0:
        aligned_src[dy0:dy1, dx0:dx1] = site_resized[sy0:sy1, sx0:sx1]

    fc_x = int(round(site_x0 + (fx + fw * 0.5) * site_scale))
    fc_y = int(round(site_y0 + (fy + fh * 0.5) * site_scale))
    rx_face = int(round(fw * 0.40 * site_scale))
    ry_face = int(round(fh * 0.44 * site_scale))

    max_rx = max(20, min(fc_x - (dx0 + 20), (dx1 - 20) - fc_x))
    max_ry = max(20, min(fc_y - (dy0 + 20), (dy1 - 20) - fc_y))
    rx_safe = min(rx_face, max_rx)
    ry_safe = min(ry_face, max_ry)

    mask_face = np.zeros((600, 600), dtype=np.uint8)
    cv2.ellipse(mask_face, (fc_x, fc_y), (rx_safe, ry_safe), 0, 0, 360, 255, -1)

    ys, xs = np.where(mask_face > 0)
    if len(xs) < 100 or mv_gem < 0.88:
        return mv_gem, gem_bgr.copy(), (dx0, dy0, dx1, dy1)

    cx = int((xs.min() + xs.max()) // 2)
    cy = int((ys.min() + ys.max()) // 2)
    blended = cv2.seamlessClone(aligned_src, gem_bgr, mask_face, (cx, cy), cv2.NORMAL_CLONE)
    return mv_gem, blended, (dx0, dy0, dx1, dy1)

def check_seam_strict(img_bgr, real_box=None):
    """
    Mandatory automatic seam check from Ek istek 4:
    1. Compute blur(3) - blur(25).
    2. Search for long horizontal/vertical step edges across rows and columns.
    3. Search for Hough lines near real_box boundaries.
    4. Directly measure directional step energy right on real_box boundaries (rx0, ry0, rx1, ry1)
       vs adjacent bands.
    """
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    b3 = cv2.GaussianBlur(gray, (3, 3), 0)
    b25 = cv2.GaussianBlur(gray, (25, 25), 0)
    diff = b3 - b25
    abs_diff = np.abs(diff)

    gy = np.abs(np.diff(diff, axis=0))
    gx = np.abs(np.diff(diff, axis=1))

    horiz_line_energy = cv2.boxFilter(gy, -1, (151, 1))
    vert_line_energy = cv2.boxFilter(gx, -1, (1, 151))

    row_peaks = horiz_line_energy[20:580, 100:500].max(axis=1).astype(np.float32)
    row_med = cv2.GaussianBlur(row_peaks.reshape(-1, 1), (1, 41), 0).ravel() + 0.15
    row_spike_ratio = float((row_peaks / row_med).max())
    worst_y = int(20 + np.argmax(row_peaks / row_med))

    col_peaks = vert_line_energy[100:500, 20:580].max(axis=0).astype(np.float32)
    col_med = cv2.GaussianBlur(col_peaks.reshape(-1, 1), (1, 41), 0).ravel() + 0.15
    col_spike_ratio = float((col_peaks / col_med).max())
    worst_x = int(20 + np.argmax(col_peaks / col_med))

    hough_seams = []
    boundary_ratio = 1.0
    if real_box is not None:
        rx0, ry0, rx1, ry1 = real_box
        edges = np.uint8(np.clip((abs_diff - np.percentile(abs_diff, 92)) * 25, 0, 255))
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=55, minLineLength=110, maxLineGap=8)
        if lines is not None:
            for l in lines.reshape(-1, 4):
                x1, y1, x2, y2 = l
                if abs(y1 - y2) <= 2 and abs(x2 - x1) >= 110:
                    if (8 < ry0 < 592 and abs(y1 - ry0) <= 15) or (8 < ry1 < 592 and abs(y1 - ry1) <= 15):
                        hough_seams.append(("H", int(y1), int(abs(x2 - x1))))
                if abs(x1 - x2) <= 2 and abs(y2 - y1) >= 110:
                    if (8 < rx0 < 592 and abs(x1 - rx0) <= 15) or (8 < rx1 < 592 and abs(x1 - rx1) <= 15):
                        hough_seams.append(("V", int(x1), int(abs(y2 - y1))))

        # Direct boundary step ratio at rx0, ry0, rx1, ry1
        b_ratios = [1.0]
        if 10 < ry0 < 590:
            b_val = gy[ry0-1:ry0+2, max(40, rx0):min(560, rx1)].mean()
            bg_val = np.median(gy[max(5, ry0-25):min(590, ry0+25), max(40, rx0):min(560, rx1)]) + 0.1
            b_ratios.append(float(b_val / bg_val))
        if 10 < rx0 < 590:
            b_val = gx[max(40, ry0):min(560, ry1), rx0-1:rx0+2].mean()
            bg_val = np.median(gx[max(40, ry0):min(560, ry1), max(5, rx0-25):min(590, rx0+25)]) + 0.1
            b_ratios.append(float(b_val / bg_val))
        if 10 < rx1 < 590:
            b_val = gx[max(40, ry0):min(560, ry1), rx1-1:rx1+2].mean()
            bg_val = np.median(gx[max(40, ry0):min(560, ry1), max(5, rx1-25):min(590, rx1+25)]) + 0.1
            b_ratios.append(float(b_val / bg_val))
        boundary_ratio = max(b_ratios)

    passed = (len(hough_seams) == 0) and (row_spike_ratio < 3.2) and (col_spike_ratio < 3.2) and (boundary_ratio < 1.85)
    return {
        "passed": passed,
        "row_spike": round(row_spike_ratio, 2),
        "col_spike": round(col_spike_ratio, 2),
        "boundary_ratio": round(boundary_ratio, 2),
        "hough_seams": hough_seams
    }

def call_gemini_outpaint_with_refs(slug, ref_paths, grey_canvas_600, attempt=1):
    cache_file = os.path.join(CACHE_DIR, f"{slug}_try{attempt}.jpg")
    if os.path.exists(cache_file):
        return cv2.imread(cache_file)

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
        "Son görseldeki kişinin konumunu, boyutunu, duruşunu ve yüzünü HİÇ değiştirmeden, yalnızca düz gri kenar şeritlerini "
        "fotoğrafın gerçek arka planı, tavanı, duvarı ve omuzlarıyla kesintisiz, aynı renk ve parlaklıkta tamamla. "
        "Gri alanla fotoğraf arasında hiçbir çizgi, basamak, çerçeve veya ton farkı kalmasın."
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

    with log_lock:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "slug": slug, "task": f"kadraj_ek5_try{attempt}",
                "refs": img_hashes, "elapsed_s": elapsed, "success": out_b64 is not None
            }, ensure_ascii=False) + "\n")

    if not out_b64:
        raise RuntimeError(f"No image returned for {slug}")
    arr = np.frombuffer(base64.b64decode(out_b64), dtype=np.uint8)
    out_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    out_bgr = cv2.resize(out_bgr, (600, 600), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(cache_file, out_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    return out_bgr

def process_one_person(slug):
    refs, best_scene = get_all_uncropped_refs(slug)
    site_bgr = cv2.imread(os.path.join(WORKSPACE, f"public/media/ekip/{slug}.jpg"))
    orig_bgr = cv2.imread(best_scene)
    top_r, side_r, bot_r = get_framing_ratios(slug)

    canvas_600, real_box, real_crop_600 = build_grey_pad_from_uncropped(
        site_bgr, orig_bgr, top_Ratio=top_r, side_Ratio=side_r, bot_Ratio=bot_r
    )

    is_100pct_real = (real_box == (0, 0, 600, 600))

    best_result = None
    for attempt in range(1, 3):
        try:
            gem_bgr = call_gemini_outpaint_with_refs(slug, refs, canvas_600, attempt=attempt)
        except Exception as e:
            print(f"[{slug}] attempt {attempt} API error: {e}")
            continue

        if is_100pct_real:
            # The entire 600x600 wider frame is 100% inside the real uncropped original!
            # We still ran the Turn 1 Gemini call with all uncropped originals; now if mv_gem >= 0.94 we can Poisson-clone
            # onto gem_bgr, OR use real_crop_600 (which is 100% real uncropped photo with zero border anywhere!).
            mv_gem, blended, _ = align_and_poisson_face(site_bgr, real_crop_600, real_crop_600)
            seam_info = check_seam_strict(real_crop_600, None)
            best_result = (real_crop_600, 1.0, seam_info, "uncropped_orig_100pct")
            break
        else:
            gem_deboxed = remove_box_boundary_steps(gem_bgr, real_box)
            mv_gem, blended, _ = align_and_poisson_face(site_bgr, real_crop_600, gem_deboxed)
            seam_info = check_seam_strict(blended, real_box)
            best_result = (blended, mv_gem, seam_info, f"gemini_poisson_try{attempt}")
            if seam_info["passed"] and mv_gem >= 0.88:
                break

    out_img, mv, seam_info, method = best_result
    out_path = os.path.join(OUT_KADRAJ_DIR, f"{slug}.jpg")
    cv2.imwrite(out_path, out_img, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
    return {
        "slug": slug,
        "method": method,
        "mv_gem": round(float(mv), 3),
        "real_box": real_box,
        "seam": seam_info,
        "refs_count": len(refs),
        "primary_orig": os.path.basename(best_scene)
    }

if __name__ == "__main__":
    data = json.load(open(os.path.join(WORKSPACE, "src/data/ekibimiz.json")))
    seen = set()
    slugs = []
    for p in data["people"]:
        s = p["photo"].split("/")[-1].replace(".jpg", "")
        if s not in seen:
            seen.add(s)
            slugs.append(s)

    print(f"Processing {len(slugs)} people with max_workers=2...")
    results = {}
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(process_one_person, s): s for s in slugs}
        for fut in as_completed(futs):
            s = futs[fut]
            res = fut.result()
            results[s] = res
            print(f"Done {s:26s}: method={res['method']:22s} mv={res['mv_gem']:.3f} seam={res['seam']}")

    with open(os.path.join(SCRATCH, "kadraj_ek5_report.json"), "w", encoding="utf-8") as f:
        json.dump([results[s] for s in slugs], f, ensure_ascii=False, indent=2)
    print("All 26 completed!")
