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

WORKSPACE = "/Users/wildgenie/Projects/btu-matro"
SCRATCH = "/Users/wildgenie/.gemini/antigravity-cli/brain/482501c3-e797-49fa-a7d5-231ae28c4675/scratch"
OUT_KADRAJ_DIR = os.path.join(WORKSPACE, "docs/ekip/yz/codex/kadraj")
CACHE_DIR = os.path.join(SCRATCH, "kadraj_ek9_cache")
os.makedirs(OUT_KADRAJ_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
LOG_FILE = os.path.join(SCRATCH, "gemini_calls.jsonl")

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

# Explicit optimal crop boxes (x0, y0, x1, y1) in the uncropped original photo coordinates
# that maximize the use of REAL uncropped background first (Ek istek 9 rule) while centering
# the head with headroom above and shoulders below:
UNCROPPED_SPECS = {
    # adem-baglan-canva.jpg is 576x713; site was (29,109)-(552,632) [S=523].
    # Taking (-22, 18, 598, 638) [S=620] uses 99px of REAL top wall and 100% real height! Only 22px left/right is outside 576.
    "adem-baglan": ("docs/ekip/orijinal/adem-baglan-canva.jpg", (-22, 18, 598, 638), (0, 0, 576, 713)),

    # almina-yanar.jpg is 1800x2400; site was (183,114)-(1616,1547) [S=1433].
    # Taking (0, -130, 1800, 1670) [S=1800] uses 100% real left, right, and bottom! Only 130px (~43px in 600) at top is outside.
    "almina-yanar": ("docs/ekip/orijinal/almina-yanar.jpg", (0, -130, 1800, 1670), (0, 0, 1800, 2400)),

    # duygu-solak.jpg is 1876x2048; site was (150,14)-(1652,1516) [S=1502].
    # Taking (0, -210, 1876, 1666) [S=1876] uses 100% real left, right, and bottom! Only 210px (~67px in 600) at top is outside.
    "duygu-solak": ("docs/ekip/orijinal/duygu-solak.jpg", (0, -210, 1876, 1666), (0, 0, 1876, 2048)),

    # ela-ural.jpg is 929x2048; site was (-6,440)-(937,1383) [S=943].
    # Taking (-95, 325, 1025, 1445) [S=1120] uses 115px of REAL top park trees and 62px of REAL bottom shoulders!
    # Also we trim x_valid_min=55 on the left so the sliver of the 2nd person's hair at x=0..50 is replaced by park background!
    "ela-ural": ("docs/ekip/orijinal/ela-ural.jpg", (-95, 325, 1025, 1445), (55, 0, 929, 2048)),

    # zeynep-seher-yolasigmaz-canva.jpg is 2016x1512; site was (307,13)-(1774,1480) [S=1467].
    # Taking (148, -228, 1888, 1512) [S=1740] uses 100% REAL left, right, and bottom! Only top 228px (~78px in 600) is outside.
    "zeynep-seher-yolasigmaz": ("docs/ekip/orijinal/zeynep-seher-yolasigmaz-canva.jpg", (148, -228, 1888, 1512), (0, 0, 2016, 1512)),

    # melisa-aydirek-canva.jpg is 720x1280; site was (0,36)-(720,761) [S=720].
    # Taking (-65, -80, 785, 770) [S=850] uses 100% REAL bottom and all 36px of real top!
    "melisa-aydirek": ("docs/ekip/orijinal/melisa-aydirek-canva.jpg", (-65, -80, 785, 770), (0, 0, 720, 1280)),

    # nusret-bircan-keser.jpg is 900x1600; site was (0,190)-(900,1097) [S=900].
    # Taking (-65, 55, 965, 1085) [S=1030] uses 135px of REAL top wall (100% real top and bottom)! Only 65px (~38px in 600) left/right is outside.
    "nusret-bircan-keser": ("docs/ekip/orijinal/nusret-bircan-keser.jpg", (-65, 55, 965, 1085), (0, 0, 900, 1600)),

    # eslem-kilic-canva.jpg is 1200x1599; site was (14,14)-(1187,1187) [S=1173].
    # Taking (-85, -165, 1285, 1205) [S=1370] uses 100% REAL bottom! Only top 165px (~72px in 600) and 85px (~37px in 600) left/right is outside.
    "eslem-kilic": ("docs/ekip/orijinal/eslem-kilic-canva.jpg", (-85, -165, 1285, 1205), (0, 0, 1200, 1599)),
}

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

def build_canvas_from_spec(slug):
    orig_rel, (nx0, ny0, nx1, ny1), (vx0, vy0, vx1, vy1) = UNCROPPED_SPECS[slug]
    orig_path = os.path.join(WORKSPACE, orig_rel)
    orig_bgr = cv2.imread(orig_path)
    oh, ow = orig_bgr.shape[:2]

    # Create valid mask in orig_bgr coordinates (respecting vx0, vy0, vx1, vy1)
    valid_orig = np.zeros((oh, ow), dtype=np.uint8)
    valid_orig[vy0:vy1, vx0:vx1] = 255

    # If vx0 > 0 (like ela-ural where x=0..55 has another person's hair), paint that strip grey in orig_bgr too
    orig_clean = orig_bgr.copy()
    if vx0 > 0:
        orig_clean[:, :vx0] = (128, 128, 128)
    if vy0 > 0:
        orig_clean[:vy0, :] = (128, 128, 128)
    if vx1 < ow:
        orig_clean[:, vx1:] = (128, 128, 128)
    if vy1 < oh:
        orig_clean[vy1:, :] = (128, 128, 128)

    need_l = max(0, -nx0)
    need_t = max(0, -ny0)
    need_r = max(0, nx1 - ow)
    need_b = max(0, ny1 - oh)

    ext_grey = cv2.copyMakeBorder(orig_clean, need_t, need_b, need_l, need_r, cv2.BORDER_CONSTANT, value=(128, 128, 128))
    crop_grey = ext_grey[ny0 + need_t : ny1 + need_t, nx0 + need_l : nx1 + need_l]
    canvas_600 = cv2.resize(crop_grey, (600, 600), interpolation=cv2.INTER_LANCZOS4)

    # Also build reflected/extrapolated real_crop_600 so valid pixels are 100% authentic orig_bgr
    # For ela-ural (vx0 > 0), reflect from vx0 onwards so the 2nd person's hair is never reflected
    orig_for_ref = orig_bgr[:, vx0:vx1]
    ext_ref = cv2.copyMakeBorder(
        orig_for_ref,
        need_t, need_b, need_l + vx0, need_r + (ow - vx1),
        cv2.BORDER_REFLECT_101
    )
    crop_ref = ext_ref[ny0 + need_t : ny1 + need_t, nx0 + need_l : nx1 + need_l]
    real_crop_600 = cv2.resize(crop_ref, (600, 600), interpolation=cv2.INTER_LANCZOS4)

    ext_valid = cv2.copyMakeBorder(valid_orig, need_t, need_b, need_l, need_r, cv2.BORDER_CONSTANT, value=0)
    crop_valid = ext_valid[ny0 + need_t : ny1 + need_t, nx0 + need_l : nx1 + need_l]
    valid_600 = cv2.resize(crop_valid, (600, 600), interpolation=cv2.INTER_NEAREST)

    ys, xs = np.where(valid_600 > 127)
    real_box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    return canvas_600, real_crop_600, valid_600, real_box, orig_path

def solve_harmonic_offset(real_crop_600, gem_bgr, valid_600):
    """
    Solve Laplace's equation (harmonic membrane interpolation) outside the interior of valid_600
    so that (gem_bgr + offset) matches real_crop_600 with 0.000 step along the boundary of valid_600!
    """
    rx0, ry0, rx1, ry1 = (
        int(np.where(valid_600 > 127)[1].min()),
        int(np.where(valid_600 > 127)[0].min()),
        int(np.where(valid_600 > 127)[1].max()) + 1,
        int(np.where(valid_600 > 127)[0].max()) + 1,
    )
    # Erode valid_600 by 6px so our boundary condition is sampled strictly inside the clean real image
    kernel = np.ones((13, 13), np.uint8)
    interior = cv2.erode(valid_600, kernel) > 127

    diff = real_crop_600.astype(np.float32) - gem_bgr.astype(np.float32)
    # Smooth diff along the boundary so noise isn't propagated into the outer strip
    diff_smooth = cv2.GaussianBlur(diff, (21, 21), 0)

    # Multi-scale Jacobi relaxation on 150x150 grid (fast, exact smooth harmonic field)
    interior_s = cv2.resize(interior.astype(np.uint8) * 255, (150, 150), interpolation=cv2.INTER_NEAREST) > 127
    u_s = cv2.resize(diff_smooth, (150, 150), interpolation=cv2.INTER_AREA)
    fixed_s = u_s.copy()

    for _ in range(250):
        # Average 4 neighbors with Neumann (zero-derivative) boundary condition at outer borders
        up = np.pad(u_s[:-1, :, :], ((1, 0), (0, 0), (0, 0)), mode="edge")
        dn = np.pad(u_s[1:, :, :], ((0, 1), (0, 0), (0, 0)), mode="edge")
        lf = np.pad(u_s[:, :-1, :], ((0, 0), (1, 0), (0, 0)), mode="edge")
        rt = np.pad(u_s[:, 1:, :], ((0, 0), (0, 1), (0, 0)), mode="edge")
        u_s = 0.25 * (up + dn + lf + rt)
        u_s[interior_s] = fixed_s[interior_s]

    u_full = cv2.resize(u_s, (600, 600), interpolation=cv2.INTER_CUBIC)
    gem_corrected = np.clip(gem_bgr.astype(np.float32) + u_full, 0, 255).astype(np.uint8)
    return gem_corrected, interior

def multiband_blend(real_crop_600, gem_corrected, valid_600, levels=5):
    """
    Burt-Adelson Laplacian pyramid blending between real_crop_600 (inside valid_600)
    and gem_corrected (outside valid_600), using a slightly curved/feathered mask inside the
    margin of valid_600 so 100% of the face and interior background remain exact original pixels,
    while the transition has zero step at all spatial frequencies.
    """
    # Erode by 10px so transition happens strictly inside the valid region (away from the raw grey border line)
    k_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
    mask_base = cv2.erode(valid_600, k_erode).astype(np.float32) / 255.0
    # Smooth mask over 15px
    mask = cv2.GaussianBlur(mask_base, (25, 25), 0)[:, :, None]

    # Guarantee that the core interior (eroded by 24px) is 100.0% untouched real_crop_600
    k_core = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (49, 49))
    core_mask = (cv2.erode(valid_600, k_core) > 127)

    A = real_crop_600.astype(np.float32)
    B = gem_corrected.astype(np.float32)
    M = mask.astype(np.float32)

    gpA, gpB, gpM = [A], [B], [M]
    for _ in range(levels):
        gpA.append(cv2.pyrDown(gpA[-1]))
        gpB.append(cv2.pyrDown(gpB[-1]))
        gpM.append(cv2.pyrDown(gpM[-1]))

    lpA = [gpA[levels]]
    lpB = [gpB[levels]]
    for i in range(levels, 0, -1):
        size = (gpA[i - 1].shape[1], gpA[i - 1].shape[0])
        lpA.append(gpA[i - 1] - cv2.pyrUp(gpA[i], dstsize=size))
        lpB.append(gpB[i - 1] - cv2.pyrUp(gpB[i], dstsize=size))

    LS = []
    for la, lb, gm in zip(lpA, lpB, gpM[::-1]):
        if gm.ndim == 2:
            gm = gm[:, :, None]
        LS.append(la * gm + lb * (1.0 - gm))

    out = LS[0]
    for i in range(1, levels + 1):
        size = (LS[i].shape[1], LS[i].shape[0])
        out = cv2.pyrUp(out, dstsize=size) + LS[i]

    out = np.clip(out, 0, 255).astype(np.uint8)
    out[core_mask] = real_crop_600[core_mask]
    return out, core_mask

def call_gemini_strip_outpaint(slug, canvas_600, attempt=1):
    cache_path = os.path.join(CACHE_DIR, f"{slug}_try{attempt}.jpg")
    if os.path.exists(cache_path):
        return cv2.imread(cache_path)

    # Also check if kadraj_ek5_cache already has a good raw generation for this person when real_box matches
    orij_files = sorted(glob.glob(os.path.join(WORKSPACE, f"docs/ekip/orijinal/{slug}*.jpg")))
    alt_files = sorted(glob.glob(os.path.join(WORKSPACE, f"docs/ekip/alternatif/{slug}*.jpg")))
    all_refs = [p for p in (orij_files + alt_files) if "-grup-" not in os.path.basename(p) and "-kursu" not in os.path.basename(p)]

    key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={key}"

    parts = []
    img_hashes = []
    for p in all_refs:
        b64, h, sz = b64_encode_image(p)
        img_hashes.append({"file": os.path.basename(p), "sha256_16": h, "size": sz})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})

    _, buf = cv2.imencode(".jpg", canvas_600, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
    raw_c = buf.tobytes()
    b64_c = base64.b64encode(raw_c).decode("ascii")
    img_hashes.append({"file": "canvas_600.jpg", "sha256_16": hashlib.sha256(raw_c).hexdigest()[:16], "size": [600, 600]})
    parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64_c}})

    extra_note = ""
    if slug == "ela-ural":
        extra_note = "Sol ve sağ kenardaki gri şeritleri yalnızca parktaki yeşil çalılar, ağaçlar ve yürüyüş yoluyla doldur; kenarlara başka insan, yüz veya saç ÇİZME."
    elif slug in ("zeynep-seher-yolasigmaz", "melisa-aydirek", "nusret-bircan-keser", "eslem-kilic", "adem-baglan", "duygu-solak"):
        extra_note = "Üst ve yan kenarlardaki gri şeritleri mevcut duvarın/dolabın/saçın düz ve doğal devamı olarak doldur; yeni raf, çizgi, kiriş veya farklı bir oda detayı EKLEME."

    prompt = (
        "İlk görseller kişinin kesilmemiş orijinal fotoğraflarıdır. "
        "SON GÖRSELDE fotoğrafın kenarlarındaki eksik dar şeritler düz gri (RGB 128,128,128) ile işaretlenmiştir. "
        "Son görselin iç kısmındaki görüntüyü (yüzü, saçları ve mevcut arka planı) HİÇ değiştirmeden ve yeniden çizmeden, "
        "yalnızca gri şeritleri hemen yanındaki mevcut arka planın düz ve doğal devamı olarak doldur. "
        + extra_note
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
            "slug": slug, "task": f"kadraj_ek9_try{attempt}",
            "refs": img_hashes, "elapsed_s": elapsed, "success": out_b64 is not None
        }, ensure_ascii=False) + "\n")

    if not out_b64:
        raise RuntimeError(f"No image returned for {slug}")
    arr = np.frombuffer(base64.b64decode(out_b64), dtype=np.uint8)
    out_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    out_bgr = cv2.resize(out_bgr, (600, 600), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(cache_path, out_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    return out_bgr

def align_gem_to_real_crop(real_crop_600, valid_600, gem_bgr):
    """
    Ensure gem_bgr is pixel-aligned with real_crop_600 (in case Gemini slightly shifted/scaled the image by a few pixels)
    before running harmonic offset + multiband blend!
    """
    # Use the central 360x360 region of real_crop_600 (which is guaranteed inside valid_600) as template
    tpl0 = real_crop_600[140:500, 120:480]
    th0, tw0 = tpl0.shape[:2]
    best = (-1.0, 1.0, 120, 140)
    for sc in np.linspace(0.92, 1.08, 33):
        tw, th = int(round(tw0 * sc)), int(round(th0 * sc))
        if tw >= 600 or th >= 600:
            continue
        tpl = cv2.resize(tpl0, (tw, th), interpolation=cv2.INTER_AREA)
        res = cv2.matchTemplate(gem_bgr, tpl, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(res)
        if mv > best[0]:
            best = (mv, sc, ml[0], ml[1])

    mv, sc, gx, gy = best
    if abs(sc - 1.0) < 0.01 and abs(gx - 120) <= 2 and abs(gy - 140) <= 2:
        return gem_bgr, mv

    # Warp gem_bgr so that (gx, gy) with scale sc maps back to (120, 140) with scale 1.0
    M = np.array([
        [1.0 / sc, 0.0, 120.0 - gx / sc],
        [0.0, 1.0 / sc, 140.0 - gy / sc]
    ], dtype=np.float32)
    warped = cv2.warpAffine(gem_bgr, M, (600, 600), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    return warped, mv

def verify_background_and_seam(final_bgr, real_crop_600, core_mask, real_box):
    """
    1. Check that 100% of core_mask (face + original background) has 0.0 difference from real_crop_600.
    2. Check blur(3) - blur(25) for any straight seam along real_box boundary.
    """
    core_diff = float(np.abs(final_bgr[core_mask].astype(np.float32) - real_crop_600[core_mask].astype(np.float32)).mean())

    gray = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    diff = cv2.GaussianBlur(gray, (3, 3), 0) - cv2.GaussianBlur(gray, (25, 25), 0)
    gy = np.abs(np.diff(diff, axis=0))
    gx = np.abs(np.diff(diff, axis=1))

    rx0, ry0, rx1, ry1 = real_box
    # Eroded transition boundary is ~12px inside real_box
    ty0, ty1 = ry0 + 12, ry1 - 12
    tx0, tx1 = rx0 + 12, rx1 - 12

    b_ratios = [1.0]
    if 15 < ty0 < 585:
        b_val = gy[ty0-2:ty0+3, max(40, tx0):min(560, tx1)].mean()
        bg_val = np.median(gy[max(5, ty0-30):min(590, ty0+30), max(40, tx0):min(560, tx1)]) + 0.12
        b_ratios.append(float(b_val / bg_val))
    if 15 < tx0 < 585:
        b_val = gx[max(40, ty0):min(560, ty1), tx0-2:tx0+3].mean()
        bg_val = np.median(gx[max(40, ty0):min(560, ty1), max(5, tx0-30):min(590, tx0+30)]) + 0.12
        b_ratios.append(float(b_val / bg_val))
    if 15 < tx1 < 585:
        b_val = gx[max(40, ty0):min(560, ty1), tx1-2:tx1+3].mean()
        bg_val = np.median(gx[max(40, ty0):min(560, ty1), max(5, tx1-30):min(590, tx1+30)]) + 0.12
        b_ratios.append(float(b_val / bg_val))

    max_b_ratio = max(b_ratios)
    passed = (core_diff < 0.01) and (max_b_ratio < 1.65)
    return {
        "passed": passed,
        "core_bg_diff": round(core_diff, 4),
        "core_preserved_pct": round(float(core_mask.mean() * 100), 1),
        "boundary_step_ratio": round(max_b_ratio, 2),
        "real_box": real_box
    }

if __name__ == "__main__":
    results = []
    for s in TARGET_8:
        canvas_600, real_crop_600, valid_600, real_box, orig_path = build_canvas_from_spec(s)
        gem_raw = call_gemini_strip_outpaint(s, canvas_600, attempt=1)
        gem_aligned, mv = align_gem_to_real_crop(real_crop_600, valid_600, gem_raw)
        gem_corr, _ = solve_harmonic_offset(real_crop_600, gem_aligned, valid_600)
        final_bgr, core_mask = multiband_blend(real_crop_600, gem_corr, valid_600, levels=5)
        check = verify_background_and_seam(final_bgr, real_crop_600, core_mask, real_box)
        print(f"[{s:24s}] mv={mv:.3f} check={check}")
        out_path = os.path.join(OUT_KADRAJ_DIR, f"{s}.jpg")
        cv2.imwrite(out_path, final_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
        results.append((s, final_bgr, check))
