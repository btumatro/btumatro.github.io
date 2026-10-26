import os
import glob
import json
import time
import base64
import hashlib
import urllib.request
import urllib.error
import cv2
import numpy as np
from PIL import Image, ImageDraw

WORKSPACE = "/Users/wildgenie/Projects/btu-matro"
SCRATCH = "/Users/wildgenie/.gemini/antigravity-cli/brain/482501c3-e797-49fa-a7d5-231ae28c4675/scratch"
RAW_KADRAJ_DIR = os.path.join(SCRATCH, "raw_kadraj")
os.makedirs(RAW_KADRAJ_DIR, exist_ok=True)
LOG_FILE = os.path.join(SCRATCH, "gemini_calls.jsonl")

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
    Collect all uncropped originals from docs/ekip/orijinal/<slug>*.jpg and docs/ekip/alternatif/<slug>.jpg,
    putting the primary target scene uncropped original LAST so Gemini knows which photo to reframe
    while having all uncropped originals in Turn 1.
    """
    orij_files = sorted(glob.glob(os.path.join(WORKSPACE, f"docs/ekip/orijinal/{slug}*.jpg")))
    alt_files = sorted(glob.glob(os.path.join(WORKSPACE, f"docs/ekip/alternatif/{slug}*.jpg")))
    site_file = os.path.join(WORKSPACE, f"public/media/ekip/{slug}.jpg")

    site_im = cv2.imread(site_file)
    site_small = cv2.resize(site_im, (150, 150))
    face_tpl = site_small[35:115, 35:115]

    best_scene_file = orij_files[0] if orij_files else site_file
    best_score = -1.0
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
        if local_best > 0.65:
            # Prefer larger resolution uncropped file when matching the same scene
            score = local_best + (0.08 if (ow * oh) > (800 * 800) else 0.0)
            if score > best_score:
                best_score = score
                best_scene_file = p

    all_candidates = orij_files + alt_files
    # Keep all files except exact byte-identical or near-identical duplicates, keeping higher-res version
    unique_refs = []
    for p in all_candidates:
        bn = os.path.basename(p)
        # Skip 5-person wide group shots as advised in CODEX-GOREV ("Grup fotoğraflarını ... ya da hiç verme"),
        # but keep -canva, -yuz-N, -bilgehan-N, -luna-N, -yakin, -kare, and alternatif
        if "-grup-" in bn or "-kursu" in bn:
            continue
        im = Image.open(p).convert("RGB").resize((64, 64))
        arr = np.asarray(im, dtype=np.float32)
        is_dup = False
        for i, (prev_p, prev_arr) in enumerate(unique_refs):
            if np.mean(np.abs(arr - prev_arr)) < 2.5:
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

def call_gemini_kadraj(slug, ref_paths, force=False):
    cache_path = os.path.join(RAW_KADRAJ_DIR, f"{slug}.jpg")
    if os.path.exists(cache_path) and not force:
        with open(cache_path, "rb") as f:
            return f.read()

    key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={key}"

    parts = []
    img_hashes = []
    for p in ref_paths:
        b64, h, sz = b64_encode_image(p)
        img_hashes.append({"file": os.path.basename(p), "sha256_16": h, "size": sz})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})

    prompt = (
        "Yukarıda aynı kişinin kesilmemiş orijinal referans fotoğrafları verilmiştir. "
        "SON GÖRSELDEKİ fotoğrafı temel alarak, aynı sahneyi, aynı arka planı, aynı kıyafeti/başörtüsünü/gözlüğü ve "
        "kişinin birebir aynı yüzünü/ifadesini koruyarak 1:1 kare kadraj düzeltmesi yap:\n"
        "- Baş yatayda tam ortada olsun.\n"
        "- Başın, saçın veya başörtüsünün en üst noktası ile üst kenar arasında rahat bir boşluk (en az %12-%15 tavan/arka plan payı) bulunsun, kafa üst kenara değmesin.\n"
        "- Alt kısımda her iki omuz net biçimde görünsün.\n"
        "- Kişiyi çok küçültme veya aşırı uzaklaştırma; standart bir ekip kartı portresi ölçeğinde (baş-omuz) olsun.\n"
        "- Arka planı doğal dokusuyla kesintisiz devam ettir; hiçbir çerçeve, kutu izi, kenar çizgisi veya yapay nesne olmasın."
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
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
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

    log_entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "slug": slug,
        "task": "kadraj_ek4",
        "refs": img_hashes,
        "prompt": prompt,
        "elapsed_s": elapsed,
        "success": out_b64 is not None
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    if not out_b64:
        raise RuntimeError(f"No image returned for {slug}")
    raw_bytes = base64.b64decode(out_b64)
    with open(cache_path, "wb") as f:
        f.write(raw_bytes)
    return raw_bytes

def detect_face_box_in_site(site_bgr):
    """
    In 600x600 site portraits, locate the central face oval using skin/feature gradient energy
    around the central portrait zone.
    """
    gray = cv2.cvtColor(site_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    energy = cv2.GaussianBlur(np.hypot(gx, gy), (51, 51), 0)
    # Bias toward center (300, 275)
    yy, xx = np.mgrid[0:600, 0:600]
    prior = np.exp(-((xx - 300)**2 / (2 * 95**2) + (yy - 275)**2 / (2 * 105**2)))
    weighted = energy * prior
    cy, cx = np.unravel_index(np.argmax(weighted), weighted.shape)
    cx = int(np.clip(cx, 220, 380))
    cy = int(np.clip(cy, 200, 350))
    fw, fh = 250, 280
    return cx - fw // 2, cy - fh // 2, fw, fh

def align_and_poisson_blend(site_bgr, orig_bgr, gem_bgr):
    """
    1. Locate the person's face from site_bgr inside gem_bgr.
    2. Scale and shift site_bgr (and matching orig_bgr) so the face aligns pixel-accurately with gem_bgr.
    3. Produce:
       - gem: Raw Gemini output (100% seamless background & framing)
       - poisson_face: Inner face oval Poisson clone (cv2.seamlessClone, NORMAL_CLONE)
       - poisson_sil: Head + shoulders silhouette ellipse Poisson clone (cv2.seamlessClone, NORMAL_CLONE)
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
    valid_mask = np.zeros((600, 600), dtype=np.uint8)

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
        valid_mask[dy0:dy1, dx0:dx1] = 255

    # Erode valid_mask by 16px so our Poisson mask NEVER touches the rectangular boundary of site_resized!
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (33, 33))
    safe_valid = cv2.erode(valid_mask, kernel)

    fc_x = int(round(site_x0 + (fx + fw * 0.5) * site_scale))
    fc_y = int(round(site_y0 + (fy + fh * 0.5) * site_scale))
    rx_face = int(round(fw * 0.42 * site_scale))
    ry_face = int(round(fh * 0.46 * site_scale))

    # Mode A: Inner Face Oval Mask for Poisson Seamless Clone
    mask_face = np.zeros((600, 600), dtype=np.uint8)
    cv2.ellipse(mask_face, (fc_x, fc_y), (rx_face, ry_face), 0, 0, 360, 255, -1)
    mask_face = cv2.bitwise_and(mask_face, safe_valid)

    # Mode B: Head + Shoulders Silhouette Mask (strictly inside safe_valid, curved ellipse, no straight border)
    # Wait: if we intersect with safe_valid, and safe_valid is a rectangle, intersecting a huge ellipse with safe_valid
    # would clip the ellipse along the straight lines of safe_valid!
    # CRITICAL INSIGHT: Never clip an ellipse with a rectangle! Instead, size the ellipse so it stays strictly inside safe_valid!
    max_rx = max(20, min(fc_x - (dx0 + 18), (dx1 - 18) - fc_x))
    max_ry_top = max(20, fc_y - (dy0 + 18))
    max_ry_bot = max(20, (dy1 - 18) - fc_y)

    mask_sil = np.zeros((600, 600), dtype=np.uint8)
    rx_head = min(int(rx_face * 1.22), max_rx)
    ry_head = min(int(ry_face * 1.20), max_ry_top, max_ry_bot)
    cv2.ellipse(mask_sil, (fc_x, fc_y), (rx_head, ry_head), 0, 0, 360, 255, -1)

    # Also clamp mask_face radii so mask_face is a 100% pure unclipped ellipse!
    rx_f_safe = min(rx_face, max_rx)
    ry_f_safe = min(ry_face, max_ry_top, max_ry_bot)
    mask_face = np.zeros((600, 600), dtype=np.uint8)
    cv2.ellipse(mask_face, (fc_x, fc_y), (rx_f_safe, ry_f_safe), 0, 0, 360, 255, -1)

    def run_poisson(src_img, dst_img, m):
        ys, xs = np.where(m > 0)
        if len(xs) < 100:
            return dst_img.copy()
        cx = int((xs.min() + xs.max()) // 2)
        cy = int((ys.min() + ys.max()) // 2)
        return cv2.seamlessClone(src_img, dst_img, m, (cx, cy), cv2.NORMAL_CLONE)

    poisson_face = run_poisson(aligned_src, gem_bgr, mask_face)
    poisson_sil = run_poisson(aligned_src, gem_bgr, mask_sil)

    return {
        "mv_gem": mv_gem,
        "gem": gem_bgr,
        "poisson_face": poisson_face,
        "poisson_sil": poisson_sil,
        "mask_face": mask_face,
        "mask_sil": mask_sil,
        "site_box": (dx0, dy0, dx1, dy1)
    }

def check_seam_strict(img_bgr, site_box=None):
    """
    Mandatory automatic seam check from Ek istek 4:
    Compute blur(3) - blur(25) difference and search for long straight horizontal/vertical edges
    (consistent step across rows/columns or Hough lines).
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
    edges = np.uint8(np.clip((abs_diff - np.percentile(abs_diff, 92)) * 25, 0, 255))
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=55, minLineLength=110, maxLineGap=8)
    if lines is not None and site_box is not None:
        dx0, dy0, dx1, dy1 = site_box
        for l in lines.reshape(-1, 4):
            x1, y1, x2, y2 = l
            if abs(y1 - y2) <= 2 and abs(x2 - x1) >= 110:
                if (10 < dy0 < 590 and abs(y1 - dy0) <= 18) or (10 < dy1 < 590 and abs(y1 - dy1) <= 18):
                    hough_seams.append(("H", int(y1), int(abs(x2 - x1))))
            if abs(x1 - x2) <= 2 and abs(y2 - y1) >= 110:
                if (10 < dx0 < 590 and abs(x1 - dx0) <= 18) or (10 < dx1 < 590 and abs(x1 - dx1) <= 18):
                    hough_seams.append(("V", int(x1), int(abs(y2 - y1))))

    passed = (len(hough_seams) == 0) and (row_spike_ratio < 3.2) and (col_spike_ratio < 3.2)
    return {
        "passed": passed,
        "row_spike": round(row_spike_ratio, 2),
        "worst_y": worst_y,
        "col_spike": round(col_spike_ratio, 2),
        "worst_x": worst_x,
        "hough_seams": hough_seams
    }

if __name__ == "__main__":
    pilots = ["adem-baglan", "berat-eren-karakas", "emine-sultan-gunes", "feyza-karabicak"]
    rows_vis = []
    for s in pilots:
        refs, best_scene = get_all_uncropped_refs(s)
        print(f"[{s}] refs ({len(refs)}): {[os.path.basename(r) for r in refs]} (primary={os.path.basename(best_scene)})")
        raw_bytes = call_gemini_kadraj(s, refs)
        arr = np.frombuffer(raw_bytes, dtype=np.uint8)
        gem_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        gem_bgr = cv2.resize(gem_bgr, (600, 600), interpolation=cv2.INTER_LANCZOS4)

        site_bgr = cv2.imread(os.path.join(WORKSPACE, f"public/media/ekip/{s}.jpg"))
        orig_bgr = cv2.imread(best_scene)

        res = align_and_poisson_blend(site_bgr, orig_bgr, gem_bgr)
        c_gem = check_seam_strict(res["gem"], res["site_box"])
        c_face = check_seam_strict(res["poisson_face"], res["site_box"])
        c_sil = check_seam_strict(res["poisson_sil"], res["site_box"])
        print(f"  mv_gem={res['mv_gem']:.3f} site_box={res['site_box']}")
        print(f"  gem_raw     : {c_gem}")
        print(f"  poisson_face: {c_face}")
        print(f"  poisson_sil : {c_sil}")
        rows_vis.append((s, site_bgr, res["gem"], res["poisson_face"], res["poisson_sil"]))

    canvas = Image.new("RGB", (4 * 620 + 20, len(rows_vis) * 650 + 20), (240, 240, 240))
    draw = ImageDraw.Draw(canvas)
    for r_i, (s, im_site, im_gem, im_pf, im_ps) in enumerate(rows_vis):
        y0 = 10 + r_i * 650
        for c_i, (lbl, bgr) in enumerate([("1_site", im_site), ("2_gem_raw", im_gem), ("3_poisson_face", im_pf), ("4_poisson_sil", im_ps)]):
            x0 = 10 + c_i * 620
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            canvas.paste(Image.fromarray(rgb), (x0, y0 + 35))
            draw.text((x0 + 5, y0 + 8), f"{s} - {lbl}", fill=(0, 0, 0))
    out_p = os.path.join(SCRATCH, "pilot_poisson_test.jpg")
    canvas.save(out_p, "JPEG", quality=95)
    print("Saved", out_p)
