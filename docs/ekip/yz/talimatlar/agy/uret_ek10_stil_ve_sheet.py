import os
import io
import glob
import json
import time
import base64
import hashlib
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = "/Users/wildgenie/Projects/btu-matro"
SCRATCH = "/Users/wildgenie/.gemini/antigravity-cli/brain/482501c3-e797-49fa-a7d5-231ae28c4675/scratch"
STIL_DIR = os.path.join(WORKSPACE, "docs/ekip/yz/codex/stil-ornekleri")
SHEET_DIR = os.path.join(WORKSPACE, "docs/ekip/yz/codex/karakter-sheet")
KONTROL_DIR = os.path.join(WORKSPACE, "docs/ekip/kontrol")
CACHE_DIR = os.path.join(SCRATCH, "stil_ek10_cache")
LOG_FILE = os.path.join(SCRATCH, "gemini_calls.jsonl")

os.makedirs(STIL_DIR, exist_ok=True)
os.makedirs(SHEET_DIR, exist_ok=True)
os.makedirs(KONTROL_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

REF_ZEKI_SAHNE_1 = "/Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/morph_07_yakin_plan_mimik.jpg"
REF_ZEKI_SAHNE_2 = "/Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/10_sahne_zeki_kisisel_itiraf_cene_elde_05_38.jpg"
REF_ZEKI_PAFTA = "/Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/KARAKTER_KIMLIK_PAFTASI_v1.jpg"

PEOPLE_SPECS = [
    {
        "slug": "adem-baglan",
        "num": "15",
        "name": "Adem Bağlan",
        "traits": (
            "Kısa siyah saç (yanları kısa kesim, üstü hafif dalgalı), dikdörtgen-oval yüz yapısı, "
            "belirgin siyah kaşlar, bıyık ve çene sakalı birleşik (keçi sakalı, yanaklar seyrek/temiz), "
            "melanj kot mavisi polo yaka tişört; lacivert yakasında ince beyaz ve turuncu-kırmızı şeritler, "
            "yaka içi turuncu-kırmızı patlı ve iki açık renk düğmeli."
        ),
        "full_body_outfit": (
            "Üstte melanj kot mavisi polo yaka tişört (lacivert yakasında ince beyaz ve turuncu-kırmızı şeritler, "
            "turuncu-kırmızı iç pat ve iki düğme), altta koyu lacivert düz kesim kot pantolon ve koyu gri-beyaz tabanlı sade spor ayakkabı."
        ),
    },
    {
        "slug": "irmak-karaagac",
        "num": "01",
        "name": "Irmak Karaağaç",
        "traits": (
            "Yüzü düzgünce çevreleyen ve boyun etrafında yumuşak katlarla sarılı düz mat siyah başörtüsü, "
            "açık buğday ten, simetrik oval yüz, belirgin düzgün kavisli koyu kaşlar, sıcak kahverengi gözler, "
            "dişleri hafif görünen doğal ve samimi gülümseme, üzerinde düz koyu lacivert bisiklet yaka uzun kollu üst."
        ),
        "full_body_outfit": (
            "Düz mat siyah başörtüsü, koyu lacivert uzun kollu tunik/üst, koyu gri-lacivert bol kesim pantolon ve sade siyah düz ayakkabı."
        ),
    },
    {
        "slug": "muhammed-ataman",
        "num": "02",
        "name": "Muhammed Ataman",
        "traits": (
            "Orta uzunlukta gür ve hafif dalgalı siyah-kırçıllı saçlar, kısa tam sakal ve bıyık, "
            "sakin ve içten ifade, boynunda siyah ve koyu gri yatay çizgili örgü atkı, "
            "üzerinde dik yakalı ve fermuar detaylı açık krem/ekru kapitone şişme mont."
        ),
        "full_body_outfit": (
            "Boynunda siyah ve koyu gri çizgili örgü atkı, açık krem/ekru kapitone şişme mont, koyu antrasit pantolon ve siyah bot."
        ),
    },
]

STYLES = [
    {
        "code": "a",
        "num": 1,
        "title": "1. a) Zeki Reels Sahne Tarzı",
        "short_title": "a) Zeki Reels Sahne",
        "style_refs": [REF_ZEKI_SAHNE_1, REF_ZEKI_SAHNE_2],
        "prompt": (
            "STİL A (Zeki Reels Sahne Tarzı): Eklenen son iki görseli YALNIZCA çizim üslubu, mürekkep kontur kalınlığı, "
            "boyama tekniği, sinematik ışık ve arka plan atmosferi referansı olarak kullan (referans görseldeki kel/gözlüklü kişinin yüzünü ASLA kopyalama). "
            "Bu ekip üyesinin baş-omuz (head-and-shoulders) 1:1 portresini çizgi roman / grafik roman illüstrasyonu tarzında üret: "
            "ince ve net koyu mürekkep konturlar, yumuşak geçişli boyalı gölgeleme (cel + soft painted shading), "
            "yandan vuran sıcak kehribar masa lambası ışığı vurgusu ve soğuk lacivert gölge dolgusu. "
            "Arka plan: referans sahne karelerindeki gibi sade koyu lacivert-gri (#1e2631) duvar, sağ alt tarafa doğru hafif sıcak kehribar ışık halesi. "
            "Gerçekçi insan yüz oranlarını birebir koru; büyük göz, karikatür abartısı veya güzelleştirme yapma."
        ),
    },
    {
        "code": "b",
        "num": 2,
        "title": "2. b) Zeki Karakter Paftası Tarzı",
        "short_title": "b) Zeki Karakter Paftası",
        "style_refs": [REF_ZEKI_PAFTA],
        "prompt": (
            "STİL B (Zeki Karakter Paftası Tarzı): Eklenen son görseli YALNIZCA çizim tekniği, kontur yapısı, düz boyama ve arka plan rengi referansı olarak kullan "
            "(referans paftadaki karakterlerin yüzünü veya kıyafetini ASLA kopyalama). "
            "Aynı ekip üyesinin baş-omuz (head-and-shoulders) 1:1 portresini düz 2B çizgi film (clean 2D cartoon character sheet) tarzında üret: "
            "temiz ve belirgin koyu kontur çizgileri, gradyansız düz renk yüzeyleri ve tek kademeli yumuşak cel-gölge. "
            "Arka plan: referans paftadakiyle aynı düz, homojen sıcak gri-bej (#bfb6a8) fon. "
            "Gerçekçi yüz oranlarını, saç/başörtüsü/sakal yapısını ve kendi kıyafetini birebir koru; büyük göz veya anime abartısı yapma."
        ),
    },
    {
        "code": "c",
        "num": 3,
        "title": "3. c) Yumuşak 3B Animasyon",
        "short_title": "c) Yumuşak 3B Animasyon",
        "style_refs": [],
        "prompt": (
            "STİL C (Yumuşak 3B Animasyon Filmi Karakteri): Aynı ekip üyesinin baş-omuz (head-and-shoulders) 1:1 portresini "
            "yüksek kaliteli yumuşak 3B animasyon filmi karakteri (stylized 3D animated feature film portrait) tarzında üret: "
            "yumuşak cilt alt saçılımı (subsurface scattering), doğal dokulu saç/başörtüsü ve kumaş yüzeyi, "
            "yumuşak stüdyo anahtar ışığı ve zarif kenar ışığı (rim light). "
            "Arka plan: düz orta-gri stüdyo fonu (#6e7075). "
            "Kişinin gerçek yüz kemik yapısını, göz büyüklüğünü, burun ve çene oranlarını birebir koru; "
            "büyük bebek gözü veya çocuksu karikatür abartısı yapma, kişi arkadaşları tarafından ilk bakışta tanınmalı."
        ),
    },
    {
        "code": "d",
        "num": 4,
        "title": "4. d) Düz Vektör / Flat",
        "short_title": "d) Düz Vektör / Flat",
        "style_refs": [],
        "prompt": (
            "STİL D (Düz Vektör / Flat İllüstrasyon): Aynı ekip üyesinin baş-omuz (head-and-shoulders) 1:1 portresini "
            "modern düz vektör portre illüstrasyonu (clean flat vector editorial portrait illustration) tarzında üret: "
            "net geometrik renk katmanları, keskin ve temiz kenarlı düz ton bloklarıyla tanımlanan yüz hacmi, "
            "minimum çizgi, uyumlu mat renk paleti. "
            "Arka plan: sade düz sıcak açık gri-krem (#dcd8d0) fon. "
            "Kişinin yüz hatlarını, ifadesini, saç/başörtüsü/sakal şeklini ve kendi kıyafetini birebir koru; yüzü basitleştirirken kimliği kaybettirme."
        ),
    },
    {
        "code": "e",
        "num": 5,
        "title": "5. e) Suluboya Portre",
        "short_title": "e) Suluboya Portre",
        "style_refs": [],
        "prompt": (
            "STİL E (Suluboya Portre): Aynı ekip üyesinin baş-omuz (head-and-shoulders) 1:1 portresini "
            "geleneksel el yapımı suluboya portre (fine art watercolor portrait on cold-press textured cotton paper) tarzında üret: "
            "ince kurşun kalem ve mürekkep eskiz çizgileri üzerinde saydam suluboya katmanları, doğal fırça darbeleri, "
            "yumuşak su ve pigment geçişleri. "
            "Arka plan: hafif suluboya yıkama geçişli açık krem pamuklu kağıt dokusu (#f2ece1). "
            "Kişinin gerçek yüz oranlarını, bakışını, saç/başörtüsü/sakal yapısını ve kendi kıyafetini birebir koru."
        ),
    },
    {
        "code": "f",
        "num": 6,
        "title": "6. f) Çizgi Roman (Halftone)",
        "short_title": "f) Çizgi Roman (Halftone)",
        "style_refs": [],
        "prompt": (
            "STİL F (Çizgi Roman - Kalın Kontur ve Halftone): Aynı ekip üyesinin baş-omuz (head-and-shoulders) 1:1 portresini "
            "klasik çizgi roman portresi (classic comic book ink portrait with bold black brush outlines, ink cross-hatching, and subtle Ben-Day halftone dots) tarzında üret: "
            "güçlü siyah fırça mürekkep konturlar, grafik tarama gölgeleri ve gölge geçişlerinde ince halftone nokta dokusu, canlı ama doğal çizgi roman renkleri. "
            "Arka plan: hafif halftone noktalı sade açık sıcak gri-krem (#e4dfd3) çizgi roman fonu. "
            "Kişinin gerçek yüz oranlarını, saç/başörtüsü/sakal yapısını ve kendi kıyafetini birebir koru; abartılı süper kahraman çenesi veya büyük göz çizme."
        ),
    },
]


def get_api_key():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")
    return key


def b64_encode_image(path, max_dim=1400, crop_box=None):
    im = Image.open(path).convert("RGB")
    if crop_box is not None:
        im = im.crop(crop_box)
    if max(im.size) > max_dim:
        im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    raw = buf.getvalue()
    return base64.b64encode(raw).decode("ascii"), hashlib.sha256(raw).hexdigest()[:16], im.size


def call_gemini_image(contents, aspect_ratio="1:1", log_meta=None):
    key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key={key}"
    body = {
        "contents": contents,
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": aspect_ratio},
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as resp:
        resp_data = json.loads(resp.read().decode("utf-8"))
    elapsed = round(time.time() - t0, 2)

    out_b64 = None
    out_text = ""
    for cand in resp_data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "inlineData" in part and not out_b64:
                out_b64 = part["inlineData"]["data"]
            elif "text" in part:
                out_text += part["text"]

    if log_meta is not None:
        entry = dict(log_meta)
        entry["elapsed_s"] = elapsed
        entry["success"] = out_b64 is not None
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    if not out_b64:
        raise RuntimeError(f"No image returned from Gemini ({log_meta})")
    return out_b64, out_text


def get_person_reference_parts(slug):
    orij_files = sorted(glob.glob(os.path.join(WORKSPACE, f"docs/ekip/orijinal/{slug}*.jpg")))
    alt_files = sorted(glob.glob(os.path.join(WORKSPACE, f"docs/ekip/alternatif/{slug}*.jpg")))
    gri_file = os.path.join(WORKSPACE, f"docs/ekip/yz/codex/gri-fon/{slug}.jpg")

    all_files = [
        p for p in (orij_files + alt_files)
        if "-grup-" not in os.path.basename(p) and "-kursu" not in os.path.basename(p)
    ]
    if os.path.exists(gri_file):
        all_files.append(gri_file)

    parts = []
    hashes = []
    for idx, p in enumerate(all_files, 1):
        b64, h, sz = b64_encode_image(p, max_dim=1400)
        role = "gri fon stüdyo portresi (ana duruş ve baş-omuz kadraj referansı)" if p == gri_file else f"kesilmemiş orijinal fotoğraf #{idx} (yüz/kimlik referansı)"
        hashes.append({"file": os.path.basename(p), "role": role, "sha256_16": h, "size": sz})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})
    return parts, hashes


def generate_person_6_styles(person):
    slug = person["slug"]
    traits = person["traits"]
    ref_parts, ref_hashes = get_person_reference_parts(slug)

    # We keep a running multi-turn conversation history for this person so all 6 styles
    # (and the character sheet) remain anchored to the same person's identity!
    history = []

    for idx, st in enumerate(STYLES):
        code = st["code"]
        out_path = os.path.join(STIL_DIR, f"{code}-{slug}.jpg")
        cache_path = os.path.join(CACHE_DIR, f"{code}-{slug}.jpg")

        if os.path.exists(cache_path) and os.path.exists(out_path):
            print(f"[SKIP cached] {code}-{slug}.jpg")
            # Still append to history if it was Turn 1 so subsequent turns have Turn 1 context
            if idx == 0:
                b64_cached, _, _ = b64_encode_image(cache_path, max_dim=1024)
                turn_parts = list(ref_parts)
                for sref in st["style_refs"]:
                    sb64, _, _ = b64_encode_image(sref, max_dim=1200)
                    turn_parts.append({"inlineData": {"mimeType": "image/jpeg", "data": sb64}})
                turn_parts.append({"text": f"KİLİT KİMLİK ÖZELLİKLERİ: {traits}\n\n{st['prompt']}"})
                history.append({"role": "user", "parts": turn_parts})
                history.append({"role": "model", "parts": [{"inlineData": {"mimeType": "image/jpeg", "data": b64_cached}}]})
            continue

        turn_parts = []
        turn_hashes = []
        if idx == 0:
            # First turn in the person's conversation: include all uncropped originals + gri-fon portrait
            turn_parts.extend(ref_parts)
            turn_hashes.extend(ref_hashes)

        # Attach style-specific reference images (only for style a and style b)
        for sref in st["style_refs"]:
            # For KARAKTER_KIMLIK_PAFTASI_v1.jpg in style b, pass the left crop showing the 2D character style clearly
            crop_box = (0, 0, 1200, 1400) if "KARAKTER_KIMLIK_PAFTASI" in sref else None
            sb64, sh, ssz = b64_encode_image(sref, max_dim=1200, crop_box=crop_box)
            turn_hashes.append({"file": os.path.basename(sref), "role": "yalnız stil referansı", "sha256_16": sh, "size": ssz})
            turn_parts.append({"inlineData": {"mimeType": "image/jpeg", "data": sb64}})

        prompt_text = (
            f"GÖREV: Görsellerdeki gerçek ekip üyesinin ({person['name']}) kimliğini, yüz kemik yapısını, "
            f"göz-kaş-burun-ağız oranlarını, saç/başörtüsü/sakal biçimini ve kendi kıyafetini BİREBİR koruyarak "
            f"1:1 kare baş-omuz (head-and-shoulders, göğüs üstünden baş üstünde rahat boşlukla ortalı) portresini üret.\n"
            f"SABİT KİMLİK ÇAPALARI (her stilde değişmez): {traits}\n"
            f"KESİN KISITLAR: Yüzü güzelleştirme, gençleştirme, başka bir modele benzetme, gözleri büyütme YOK. "
            f"Görselin içinde hiçbir yazı, etiket, imza veya çerçeve OLMASIN.\n\n"
            f"{st['prompt']}"
        )
        turn_parts.append({"text": prompt_text})

        # Keep conversation context lean yet anchored: Turn 1 (with all identity photos + Style A) + current turn
        if idx == 0:
            req_contents = [{"role": "user", "parts": turn_parts}]
        else:
            req_contents = [
                history[0],
                history[1],
                {"role": "user", "parts": turn_parts},
            ]

        out_b64, _ = call_gemini_image(
            req_contents,
            aspect_ratio="1:1",
            log_meta={"slug": slug, "task": f"stil_{code}", "refs": turn_hashes},
        )
        arr = np.frombuffer(base64.b64decode(out_b64), dtype=np.uint8)
        im_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        im_600 = cv2.resize(im_bgr, (600, 600), interpolation=cv2.INTER_AREA)
        cv2.imwrite(cache_path, im_600, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        cv2.imwrite(out_path, im_600, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
        print(f"[DONE] {code}-{slug}.jpg")

        if idx == 0:
            history.append({"role": "user", "parts": turn_parts})
            history.append({"role": "model", "parts": [{"inlineData": {"mimeType": "image/jpeg", "data": out_b64}}]})

    return slug, history


def generate_character_sheets_for_adem(adem_spec):
    """
    Item 3 of Ek istek 10: Generate character identity sheets in style a) and style b)
    for Adem Bağlan in the same conversation context (using his uncropped originals + gri-fon + approved style portrait + layout reference).
    """
    slug = adem_spec["slug"]
    ref_parts, ref_hashes = get_person_reference_parts(slug)

    for style_code, style_desc, bg_desc, style_ref_path in [
        (
            "a",
            "Zeki Reels Sahne Tarzı (ince koyu mürekkep kontur, yumuşak geçişli boyalı gölgeleme, sıcak kehribar anahtar ışık ve soğuk lacivert gölge dolgu)",
            "düz açık sıcak gri-bej pafta zemini (#d8d2c7) üzerinde her karakter ve ifade net okunur",
            REF_ZEKI_SAHNE_1,
        ),
        (
            "b",
            "Zeki Karakter Paftası Tarzı (düz 2B çizgi film, temiz koyu konturlar, gradyansız düz renkler + tek ton yumuşak cel-gölge)",
            "referans karakter paftasıyla aynı düz homojen sıcak gri-bej (#bfb6a8) pafta zemini",
            REF_ZEKI_PAFTA,
        ),
    ]:
        out_sheet_path = os.path.join(SHEET_DIR, f"{style_code}-{slug}.jpg")
        if os.path.exists(out_sheet_path):
            print(f"[SKIP cached sheet] {out_sheet_path}")
            continue

        stil_portrait_path = os.path.join(STIL_DIR, f"{style_code}-{slug}.jpg")
        parts = list(ref_parts)
        hashes = list(ref_hashes)

        # Attach approved stylized portrait of Adem in this exact style as primary character anchor
        sp_b64, sp_h, sp_sz = b64_encode_image(stil_portrait_path, max_dim=1024)
        hashes.append({"file": os.path.basename(stil_portrait_path), "role": "onaylı stilize karakter portresi (ana karakter çapası)", "sha256_16": sp_h, "size": sp_sz})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": sp_b64}})

        # Attach KARAKTER_KIMLIK_PAFTASI_v1.jpg as layout reference
        pafta_b64, pafta_h, pafta_sz = b64_encode_image(REF_ZEKI_PAFTA, max_dim=1400)
        hashes.append({"file": os.path.basename(REF_ZEKI_PAFTA), "role": "yalnız sayfa düzeni referansı", "sha256_16": pafta_h, "size": pafta_sz})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": pafta_b64}})

        if style_ref_path != REF_ZEKI_PAFTA:
            sr_b64, sr_h, sr_sz = b64_encode_image(style_ref_path, max_dim=1200)
            hashes.append({"file": os.path.basename(style_ref_path), "role": "yalnız çizim ve ışık stili referansı", "sha256_16": sr_h, "size": sr_sz})
            parts.append({"inlineData": {"mimeType": "image/jpeg", "data": sr_b64}})

        prompt = (
            f"Girdi görsellerinin rolleri:\n"
            f"- İlk görseller: Adem Bağlan'ın kesilmemiş orijinal fotoğrafları ve gri fon stüdyo portresi (yalnızca yüz ve kimlik kaynağı).\n"
            f"- Sonraki kare portre: Adem Bağlan'ın onaylı {style_code}) stilize portresi (ana karakter ve kıyafet çapası).\n"
            f"- Çoklu karakter içeren yatay görsel: YALNIZCA sayfa düzeni (layout) referansı (oradaki kel/gözlüklü veya diğer karakterleri ASLA kopyalama).\n\n"
            f"GÖREV: Adem Bağlan için yatay 16:9 (1600x900) profesyonel bir KARAKTER KİMLİK PAFTASI (Character Turnaround & Expression Sheet) üret.\n"
            f"ÇİZİM STİLİ: {style_desc}. Gerçekçi insan oranları (7.5 baş boy oranı, büyük göz veya karikatür abartısı yok).\n"
            f"SABİT KİMLİK VE KIYAFET (tüm pozlarda ve ifadelerde 100% aynı kalmalı): {adem_spec['traits']} {adem_spec['full_body_outfit']}\n\n"
            f"SAYFA DÜZENİ:\n"
            f"1. ÜST BÖLÜM (Sol-Orta): Aynı boy ölçeğinde ve hizada 4 tam boy dönüş (turnaround) pozu yan yana: "
            f"\"ÖNDEN\", \"ÜÇ ÇEYREK\", \"YANDAN\", \"ARKADAN\" (her birinin altında küçük, temiz büyük harf Türkçe etiket).\n"
            f"2. ALT BÖLÜM (Sol-Orta): 4 adet baş-omuz yüz ifadesi büstü yan yana: "
            f"\"GÜLÜMSEME\", \"CİDDİ\", \"ŞAŞKIN\", \"KONUŞURKEN\" (her birinin altında küçük Türkçe etiket).\n"
            f"3. SAĞ PANEL: Dikey renk paleti kutucukları (Ten, Siyah Saç/Sakal, Melanj Mavi Polo, Lacivert-Turuncu Yaka, Koyu Kot) "
            f"ve kısa Türkçe oran notu (\"7.5 Baş Oranı | Doğal Portre Ölçeği\"). Üstte temiz Türkçe başlık: \"ADEM BAĞLAN - KARAKTER KİMLİK PAFTASI\" (birebir, emoji yok).\n"
            f"ARKA PLAN: {bg_desc}."
        )
        parts.append({"text": prompt})

        out_b64, _ = call_gemini_image(
            [{"role": "user", "parts": parts}],
            aspect_ratio="16:9",
            log_meta={"slug": slug, "task": f"karakter_sheet_{style_code}", "refs": hashes},
        )
        arr = np.frombuffer(base64.b64decode(out_b64), dtype=np.uint8)
        im_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        cv2.imwrite(out_sheet_path, im_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
        print(f"[DONE sheet] {out_sheet_path} ({im_bgr.shape[1]}x{im_bgr.shape[0]})")

    # Also copy style a as default adem-baglan.jpg in karakter-sheet/
    a_sheet = os.path.join(SHEET_DIR, f"a-{slug}.jpg")
    default_sheet = os.path.join(SHEET_DIR, f"{slug}.jpg")
    if os.path.exists(a_sheet):
        im = cv2.imread(a_sheet)
        cv2.imwrite(default_sheet, im, [int(cv2.IMWRITE_JPEG_QUALITY), 94])


def build_stil_ornekleri_paftasi():
    """
    Build docs/ekip/kontrol/stil-ornekleri.jpg:
    Rows = 3 people (15. Adem Bağlan, 01. Irmak Karaağaç, 02. Muhammed Ataman)
    Columns = [0. Gri Fon (Referans)] + 6 numbered styles (1. a) Zeki Reels Sahne .. 6. f) Çizgi Roman (Halftone))
    """
    cell_w, cell_h = 320, 320
    pad_x, pad_y = 18, 22
    left_label_w = 230
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

    # Column headers
    for c_idx, (col_title, _) in enumerate(cols):
        cx = left_label_w + c_idx * (cell_w + pad_x)
        cy = 64
        draw.rounded_rectangle([cx, cy, cx + cell_w, cy + 38], radius=6, fill=(32, 36, 45))
        draw.text((cx + 12, cy + 9), col_title, fill=(255, 255, 255), font=font_col)

    # Rows
    for r_idx, person in enumerate(PEOPLE_SPECS):
        slug = person["slug"]
        ry = header_h + r_idx * (cell_h + pad_y)

        # Row label card on the left
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
                # Small corner badge
                badge = "Gri Fon" if code == "ref" else f"{code}) {col_title.split(') ')[1]}"
                draw.rectangle([cx, ry + cell_h - 26, cx + 195, ry + cell_h], fill=(0, 0, 0))
                draw.text((cx + 7, ry + cell_h - 22), badge, fill=(255, 255, 255), font=font_sub)

    out_pafta = os.path.join(KONTROL_DIR, "stil-ornekleri.jpg")
    sheet.save(out_pafta, "JPEG", quality=93)
    print(f"[SAVED PAFTA] {out_pafta} ({sheet.size[0]}x{sheet.size[1]})")


if __name__ == "__main__":
    t_start = time.time()
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = [ex.submit(generate_person_6_styles, p) for p in PEOPLE_SPECS]
        for f in as_completed(futs):
            slug, _ = f.result()
            print(f"Completed all 6 styles for {slug}")

    build_stil_ornekleri_paftasi()
    generate_character_sheets_for_adem(PEOPLE_SPECS[0])
    print(f"All done in {round(time.time() - t_start, 1)}s")
