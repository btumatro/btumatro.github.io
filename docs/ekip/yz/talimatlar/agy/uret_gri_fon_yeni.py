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
    WORKSPACE, SCRATCH, LOG_FILE, get_api_key, b64_encode_image, get_all_uncropped_refs
)

OUT_DIR = os.path.join(WORKSPACE, "docs/ekip/yz/codex/gri-fon-yeni")
os.makedirs(OUT_DIR, exist_ok=True)
BILGEHAN_REF = os.path.join(WORKSPACE, "public/media/ekip/bilgehan-zeki-ozaytac.jpg")

PROMPTS = {
    "gulsiye-begum-gumus": (
        "Yukarıdaki ilk görseller kişinin kesilmemiş orijinal fotoğraflarıdır; son görsel ise hedef orta-gri stüdyo fonu ve "
        "stüdyo ışığı referansıdır (Bilgehan'ın fotoğrafı).\n"
        "Bu kişiyi (birebir aynı yüz hatları, aynı gülümseme, aynı gri/gümüş eşarp ve başının üstündeki gözlük, aynı bordo triko kazak ile) "
        "gerçek bir profesyonel fotoğraf stüdyosunda çekilmiş gibi 1:1 kare portre olarak üret:\n"
        "- Önceki denemede kişi çok küçük kalmıştı ve arka plandan kopuk (kesilip yapıştırılmış gibi) duruyordu. "
        "Bu kez Bilgehan'ın fotoğrafındaki gibi standart baş-omuz (head-and-shoulders) ölçeğinde, kadrajı dengeli dolduran, ortalı bir portre olsun.\n"
        "- Selfie tutan kol açısı olmasın; her iki omuz doğal ve dengeli dursun.\n"
        "- Başın ve gözlüğün üstünde yeterli gri stüdyo fonu boşluğu (headroom) bulunsun.\n"
        "- Yüzdeki ve eşarptaki dış mekan sıcak/sarı kafe ışığını kaldır; yüz ve kıyafet stüdyodaki yumuşak, nötr-soğuk stüdyo ışığıyla ve orta-gri fonla "
        "tamamen aynı ışık ortamında bütünleşsin."
    ),
    "melek-ozkeser": (
        "Yukarıdaki ilk görseller kişinin kesilmemiş orijinal fotoğraflarıdır; son görsel ise hedef orta-gri stüdyo fonu ve "
        "stüdyo ışığı referansıdır (Bilgehan'ın fotoğrafı).\n"
        "Bu kişiyi (birebir aynı yüz hatları, gözleri, burnu, hızması, dudakları, kahverengi saçları, başının üstündeki güneş gözlüğü ve "
        "beyaz delikli örgü kazağı/kolyesi ile) gerçek bir profesyonel fotoğraf stüdyosunda çekilmiş gibi 1:1 kare portre olarak üret:\n"
        "- Koltukta yatay/eğik uzanma ve üstten selfie açısını düzelt: kişi stüdyoda dik ve doğal bir duruşla kameraya göz hizasından baksın.\n"
        "- Önceki denemede kafasının ve saçının üstü kesilmişti! Başın ve saçın/güneş gözlüğünün tamamı eksiksiz görünsün ve üst kenarla "
        "baş arasında rahat bir gri stüdyo fonu boşluğu (%15 headroom) bulunsun.\n"
        "- Kadrajda baş-omuz ortalı olsun, yumuşak stüdyo ışığı yüz ve saçla tamamen bütünleşsin."
    ),
    "nusret-bircan-keser": (
        "Yukarıdaki ilk görseller kişinin kesilmemiş orijinal fotoğraflarıdır; son görsel ise hedef orta-gri stüdyo fonu ve "
        "stüdyo ışığı referansıdır (Bilgehan'ın fotoğrafı).\n"
        "Bu kişiyi (birebir aynı yüz hatları, gözleri, kaşları, sakalı/bıyığı, saç kesimi, beyaz tişörtü, koyu lacivert/siyah fermuarlı üstü ve "
        "boynundaki yeşil-beyaz atkısı ile) gerçek bir profesyonel fotoğraf stüdyosunda çekilmiş gibi 1:1 kare portre olarak üret:\n"
        "- Önceki denemede alttan çekilmiş selfie açısı (çene yukarıda, burun deliklerinden bakan açı) kalmıştı. "
        "Bu kez kamera tam göz hizasında olsun; baş dik, doğal ve karşıdan (hafif doğal stüdyo duruşuyla) görünsün, çene yukarı kalkık olmasın.\n"
        "- Baş-omuz kadrajda tam ortalı olsun, saçın üstünde yeterli gri stüdyo fonu boşluğu (%15 headroom) bulunsun ve her iki omuz dengeli görünsün.\n"
        "- Yüz ve kıyafet orta-gri stüdyo fonuyla aynı yumuşak stüdyo ışığında bütünleşsin."
    )
}

def generate_gri_fon_yeni(slug):
    refs, _ = get_all_uncropped_refs(slug)
    # Also include public/media/ekip/<slug>.jpg if not already covered so all originals + site are seen
    key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={key}"

    parts = []
    img_hashes = []
    for p in refs:
        b64, h, sz = b64_encode_image(p)
        img_hashes.append({"file": os.path.basename(p), "sha256_16": h, "size": sz})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})

    b64_ref, h_ref, sz_ref = b64_encode_image(BILGEHAN_REF)
    img_hashes.append({"file": "bilgehan-zeki-ozaytac.jpg", "sha256_16": h_ref, "size": sz_ref})
    parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64_ref}})

    prompt = PROMPTS[slug]
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
            "slug": slug, "task": "gri_fon_yeni_ek5",
            "refs": img_hashes, "elapsed_s": elapsed, "success": out_b64 is not None
        }, ensure_ascii=False) + "\n")

    if not out_b64:
        raise RuntimeError(f"No image returned for {slug}")
    import io
    im = Image.open(io.BytesIO(base64.b64decode(out_b64))).convert("RGB")
    im = im.resize((600, 600), Image.Resampling.LANCZOS)
    out_path = os.path.join(OUT_DIR, f"{slug}.jpg")
    im.save(out_path, "JPEG", quality=92)
    print(f"Saved {out_path} ({elapsed}s)")

if __name__ == "__main__":
    for s in ["gulsiye-begum-gumus", "melek-ozkeser", "nusret-bircan-keser"]:
        generate_gri_fon_yeni(s)
