import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import base64, hashlib, json, time, urllib.request

from test_poisson_pilot import (
    WORKSPACE, SCRATCH, LOG_FILE, get_api_key, b64_encode_image,
    get_all_uncropped_refs, detect_face_box_in_site, align_and_poisson_blend, check_seam_strict
)
from test_soft_guide import build_soft_guide_from_uncropped

def prepare_clean_target_ref(site_bgr, orig_bgr):
    """
    If orig_bgr has real uncropped pixels around site_bgr, extract the largest 100% REAL (unpadded, unblurred)
    crop around the head & shoulders from orig_bgr so Gemini gets all available real background pixels
    without any artificial border!
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
        return site_bgr, False

    S = int(round((150 * sc) / f_sc))
    sx0 = int(round((fx - 35 * sc) / f_sc))
    sy0 = int(round((fy - 35 * sc) / f_sc))

    # Desired ideal box: top_pad = 0.22 * S, bot_pad = 0.08 * S, side_pad = 0.15 * S
    ideal_S = int(round(S * 1.30))
    cx = sx0 + S // 2
    nx0 = cx - ideal_S // 2
    ny0 = sy0 - int(round(S * 0.22))
    nx1 = nx0 + ideal_S
    ny1 = ny0 + ideal_S

    if nx0 >= 0 and ny0 >= 0 and nx1 <= ow and ny1 <= oh:
        # 100% of the ideal wider square exists inside orig_bgr!
        crop = orig_bgr[ny0:ny1, nx0:nx1]
        return cv2.resize(crop, (600, 600), interpolation=cv2.INTER_LANCZOS4), True

    # Otherwise, clamp to the real bounds of orig_bgr around the person (up to 1.45 * S) so we never include
    # artificial borders, while giving Gemini the maximum real uncropped background around the head/shoulders!
    rx0 = max(0, sx0 - int(S * 0.25))
    ry0 = max(0, sy0 - int(S * 0.30))
    rx1 = min(ow, sx0 + S + int(S * 0.25))
    ry1 = min(oh, sy0 + S + int(S * 0.25))
    return orig_bgr[ry0:ry1, rx0:rx1], False

def call_gemini_clean_zoomout(slug, ref_paths, clean_target_bgr, is_already_framed=False):
    key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={key}"

    parts = []
    img_hashes = []
    for p in ref_paths:
        b64, h, sz = b64_encode_image(p)
        img_hashes.append({"file": os.path.basename(p), "sha256_16": h, "size": sz})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})

    _, buf = cv2.imencode(".jpg", clean_target_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
    raw_t = buf.tobytes()
    b64_t = base64.b64encode(raw_t).decode("ascii")
    img_hashes.append({"file": "clean_target_crop.jpg", "sha256_16": hashlib.sha256(raw_t).hexdigest()[:16], "size": [clean_target_bgr.shape[1], clean_target_bgr.shape[0]]})
    parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64_t}})

    if is_already_framed:
        prompt = (
            "Yukarıda kişinin kesilmemiş orijinal fotoğrafları ve son görselde orijinal fotoğraftan alınmış "
            "1:1 kare baş-omuz kadrajı verilmiştir. Son görseldeki bu 1:1 kare fotoğrafı, kişinin yüzünü, ifadesini, "
            "kıyafetini, arka planını ve kadrajını BİREBİR koruyarak, hiçbir kenar çizgisi veya bulanık çerçeve olmadan temiz 1:1 kare olarak üret."
        )
    else:
        prompt = (
            "Yukarıdaki ilk görseller kişinin kesilmemiş orijinal fotoğraflarıdır. "
            "SON GÖRSELDEKİ fotoğrafı temel al: bu fotoğrafta kamera kişiye biraz fazla yakın olduğu için baş üst kenara yakın duruyor. "
            "Aynı fotoğrafı, kamerayı %20 oranında geri çekerek (zoom out / outpaint yaparak) 1:1 kare formatta yeniden kadrajla:\n"
            "- Kişinin yüzü, bakışı, ifadesi, saç/başörtüsü/gözlüğü, kıyafeti ve sahne ışığı BİREBİR aynı kalsın.\n"
            "- Baş karenin yatayda tam ortasında ve dikeyde biraz daha aşağıda dursun; başın/saçın/başörtüsünün üstünde arka plandan en az %16-%20 oranında geniş ve doğal bir boşluk (headroom) aç.\n"
            "- Alt kısımda her iki omuz rahatça görünsün.\n"
            "- Arka planı (duvar, tavan, araç içi, gökyüzü vb.) kesintisiz ve net biçimde devam ettir; ASLA bulanık kenar (blur border), çerçeve, dikdörtgen kutu izi veya çizgi oluşturma."
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
            "slug": slug, "task": "kadraj_clean_zoomout",
            "refs": img_hashes, "elapsed_s": elapsed, "success": out_b64 is not None
        }, ensure_ascii=False) + "\n")

    arr = np.frombuffer(base64.b64decode(out_b64), dtype=np.uint8)
    out_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return cv2.resize(out_bgr, (600, 600), interpolation=cv2.INTER_LANCZOS4)

if __name__ == "__main__":
    for s in ["emine-sultan-gunes", "irmak-karaagac"]:
        refs, best_scene = get_all_uncropped_refs(s)
        site_bgr = cv2.imread(os.path.join(WORKSPACE, f"public/media/ekip/{s}.jpg"))
        orig_bgr = cv2.imread(best_scene)
        clean_t, is_framed = prepare_clean_target_ref(site_bgr, orig_bgr)
        gem_bgr = call_gemini_clean_zoomout(s, refs, clean_t, is_already_framed=is_framed)
        # If is_framed is True, clean_t IS the 100% real uncropped 600x600 frame, so we can also align clean_t directly!
        base_for_face = clean_t if is_framed else site_bgr
        res = align_and_poisson_blend(base_for_face, orig_bgr, gem_bgr)
        c_pf = check_seam_strict(res["poisson_face"], res["site_box"])
        print(f"[{s}] is_framed={is_framed} mv_gem={res['mv_gem']:.3f} seam_check={c_pf}")
        cv2.imwrite(os.path.join(SCRATCH, f"clean_zoom_{s}.jpg"), res["poisson_face"])
