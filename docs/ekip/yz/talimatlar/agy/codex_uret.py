import base64
import concurrent.futures as cf
import glob
import hashlib
import io
import json
import os
import sys
import threading
import time
import urllib.request
from PIL import Image, ImageOps

KEY = os.environ.get("GEMINI_API_KEY", "")
if not KEY:
    raise RuntimeError("GEMINI_API_KEY ortam degiskeni bulunamadi.")

OUT_BASE = "docs/ekip/yz/codex"
OUT_KADRAJ = os.path.join(OUT_BASE, "kadraj")
OUT_VESIKA = os.path.join(OUT_BASE, "vesikalik")
OUT_GRIFON = os.path.join(OUT_BASE, "gri-fon")
for d in (OUT_KADRAJ, OUT_VESIKA, OUT_GRIFON):
    os.makedirs(d, exist_ok=True)

SCRATCH_DIR = "/Users/wildgenie/.gemini/antigravity-cli/brain/482501c3-e797-49fa-a7d5-231ae28c4675/scratch"
CONV_DIR = os.path.join(SCRATCH_DIR, "conv")
os.makedirs(CONV_DIR, exist_ok=True)
LOG_PATH = os.path.join(SCRATCH_DIR, "gemini_calls.jsonl")
CLAUDE_REF_DIR = "/private/tmp/claude-501/-Users-wildgenie-Projects-btu-matro/c4790c33-2952-44d6-b402-a148a7fb5c92/scratchpad/ref"
LOG_LOCK = threading.Lock()

CANVA_BY_SLUG: dict[str, list[str]] = {}
def _build_canva_map() -> None:
    orij_md5: dict[str, str] = {}
    for p in glob.glob("docs/ekip/orijinal/*.jpg"):
        h = hashlib.md5(open(p, "rb").read()).hexdigest()
        orij_md5[h] = os.path.basename(p)
    for cp in sorted(glob.glob("docs/ekip/canva-DAHYwyJ6SQc/*.jpg")):
        h = hashlib.md5(open(cp, "rb").read()).hexdigest()
        bname = orij_md5.get(h, "")
        if bname:
            slug = bname[:-4].replace("-canva", "").replace("-kare", "")
            CANVA_BY_SLUG.setdefault(slug, []).append(cp)
    CANVA_BY_SLUG.setdefault("feyza-karabicak", []).append(
        "docs/ekip/canva-DAHYwyJ6SQc/c744f2b0-26fb-408f-8195-7f85815c6174.jpg"
    )
    CANVA_BY_SLUG.setdefault("gulsiye-begum-gumus", []).append(
        "docs/ekip/canva-DAHYwyJ6SQc/d1f9c4d7-d0d4-48f1-bc0f-77780fc65e98.jpg"
    )

_build_canva_map()

PERSON_NOTES = {
    "mehmet-onur-genc": (
        "Academic advisor (Associate Professor). Round-oval face, short dark hair with slight curl on top, full short dark beard and moustache, warm smile, wearing dark suit jacket, light blue shirt, and dark blue tie."
    ),
    "bilgehan-zeki-ozaytac": (
        "Bald head, short full dark beard and moustache, hazel-green eyes, wearing a dark grey/black pinstripe collared shirt."
    ),
    "muhammed-ataman": (
        "Thick wavy dark hair parted near middle, full short dark beard and moustache, warm dark brown eyes, wearing a light cream/beige jacket and dark grey striped scarf."
    ),
    "irmak-karaagac": (
        "In the outdoor photo she wears a navy headscarf and white cap; in her indoor close-up reference photo she wears a brown headscarf without a cap. "
        "Keep her exact long oval face, thick straight dark eyebrows, warm olive skin, and gentle smile. For vesikalik, do NOT put a baseball cap or lanyard—use a clean headscarf look as in her indoor reference."
    ),
    "omer-cihan-demir": (
        "21-year-old student: long narrow face, thick straight dark eyebrows, deep-set eyes, straight nose, short dark hair, full dark beard, wearing an olive jacket over an orange hoodie."
    ),
    "duygu-solak": (
        "Long wavy dark brown hair parted in the middle, oval face, large almond brown eyes, small beauty mark on upper nose bridge, wearing a white off-shoulder ribbed knit top."
    ),
    "zeynep-seher-yolasigmaz": (
        "Short/tied dark hair with wispy bangs on forehead, thin dark-framed geometric glasses, rosy cheeks, warm gentle smile, wearing a dark navy/black crew-neck top."
    ),
    "gulsiye-begum-gumus": (
        "Wearing a grey silk headscarf with white border stripes, sunglasses resting on top of head (remove top sunglasses for vesikalik, keep for gri-fon if natural), burgundy/maroon sweater, warm smile."
    ),
    "nusret-bircan-keser": (
        "Young man with thick dark hair styled up, light stubble beard/moustache, wearing a dark zip jacket with a green-and-white Bursaspor scarf around neck."
    ),
    "rumeysa-akarsu": (
        "Soft round-oval face, warm skin tone, gentle closed-lip smile, wearing a patterned mauve/brown satin headscarf and brown jacket."
    ),
    "emine-sultan-gunes": (
        "Wearing a royal blue satin headscarf and sparkly dark blue/black top, fair skin, soft gentle smile."
    ),
    "almina-yanar": (
        "Wearing a dark navy headscarf and light blue collared shirt/jacket, fair skin, cat-eye eyeliner, soft smile."
    ),
    "elif-melisa-kose": (
        "Curly dark brown updo hair with curly bangs, red-and-white horizontal striped long-sleeve top, warm friendly smile."
    ),
    "zehra-bulut": (
        "Wearing a dark brown/black headscarf and dark brown jacket/top, wide bright smile, expressive dark eyes."
    ),
    "adem-baglan": (
        "Short dark hair, goatee beard and moustache (chin beard + moustache, clean cheeks), wearing a denim-blue polo shirt with red/navy collar trim."
    ),
    "yusuf-sarsici": (
        "In his field photo he wears a white safety hard hat and yellow high-vis vest. For gri-fon keep his natural look from the photo; for vesikalik remove the safety hard hat and neon vest and show his normal short dark hair and dark jacket/shirt while keeping his exact narrow face, eyebrows, nose, and thin moustache."
    ),
    "elif-naz-koksoy": (
        "Long straight dark brown hair parted in center, wearing a grey blazer over a black top, subtle confident smile."
    ),
    "berat-eren-karakas": (
        "Short curly brown hair, thin wire-rimmed glasses, light beard and moustache, black crew-neck t-shirt."
    ),
    "muhammed-efe-coskunpinar": (
        "Thick wavy dark hair parted in middle, clean-shaven face, wide jaw, warm smile, wearing a plain black crew-neck t-shirt."
    ),
    "ela-ural": (
        "Long straight medium-brown hair, fair skin, dark eyebrows, warm smile, wearing a blue/yellow/white striped top."
    ),
    "feyza-karabicak": (
        "Wearing a dark brown headscarf, thin round wire-rimmed glasses, cream knit sweater, gentle smile."
    ),
    "melek-ozkeser": (
        "Long dark brown wavy hair, sunglasses on top of head (remove top sunglasses for vesikalik), wearing a white open-knit sweater over a dark top. In her original photo she is leaning against a cushion; for gri-fon and vesikalik place her upright against the studio background while keeping her exact face, nose ring/stud, eyes, and lips."
    ),
    "melisa-aydirek": (
        "Long straight dark brown hair, warm tan skin, dark brown eyes, red lipstick, slight playful smile, wearing a beige/gold sleeveless top."
    ),
    "eslem-kilic": (
        "Long wavy medium-brown/dark-blonde hair, dark-framed cat-eye glasses, light olive/beige shirt over white top."
    ),
    "esma-demirkiyik": (
        "Long wavy dark brown hair, white sleeveless top with gold necklaces. In her original photo her right hand is raised to her temple and sunglasses rest on her head; for both gri-fon and vesikalik lower/remove the raised hand so only her head, hair, and shoulders are visible, and remove the top sunglasses for vesikalik while keeping her exact facial features."
    ),
    "aslihan-okumus": (
        "Wearing a warm terracotta/brown headscarf and beige jacket, bright warm smile."
    ),
}

def collect_refs(slug: str) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    site_p = f"public/media/ekip/{slug}.jpg"
    if os.path.exists(site_p):
        candidates.append(("Current 600x600 site portrait", site_p))

    for p in sorted(glob.glob(f"docs/ekip/orijinal/{slug}*.jpg")):
        bn = os.path.basename(p)
        if "-grup-" in bn or "-bilgehan-" in bn or "-kursu" in bn:
            continue
        candidates.append((f"Original photo ({bn})", p))

    alt_p = f"docs/ekip/alternatif/{slug}.jpg"
    if os.path.exists(alt_p):
        candidates.append((f"Alternative square crop ({os.path.basename(alt_p)})", alt_p))

    ref_p = os.path.join(CLAUDE_REF_DIR, f"{slug}.jpg")
    if os.path.exists(ref_p):
        candidates.append((f"Close-up face reference ({slug})", ref_p))

    for cp in CANVA_BY_SLUG.get(slug, []):
        if os.path.exists(cp):
            candidates.append((f"Canva raw image ({os.path.basename(cp)})", cp))

    by_hash: dict[str, tuple[list[str], str]] = {}
    order: list[str] = []
    for label, path in candidates:
        h = hashlib.md5(open(path, "rb").read()).hexdigest()
        if h not in by_hash:
            by_hash[h] = ([label], path)
            order.append(h)
        else:
            by_hash[h][0].append(label)

    result: list[tuple[str, str]] = []
    for h in order:
        labels, path = by_hash[h]
        result.append((" / ".join(labels), path))
    return result

def encode_pil(im: Image.Image, max_dim: int = 1280, quality: int = 92) -> dict:
    im = ImageOps.exif_transpose(im).convert("RGB")
    if max(im.size) > max_dim:
        im = im.copy()
        im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    b = io.BytesIO()
    im.save(b, "JPEG", quality=quality)
    return {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}}

def encode_path(path: str, max_dim: int = 1280, quality: int = 92) -> dict:
    return encode_pil(Image.open(path), max_dim=max_dim, quality=quality)

def sanitize_for_log(obj):
    if isinstance(obj, dict):
        if "inlineData" in obj and "data" in obj["inlineData"]:
            raw = obj["inlineData"]["data"]
            return {
                "inlineData": {
                    "mimeType": obj["inlineData"].get("mimeType", "image/jpeg"),
                    "sha256": hashlib.sha256(raw.encode()).hexdigest()[:16],
                    "base64_len": len(raw),
                }
            }
        return {k: sanitize_for_log(v) for k, v in obj.items() if k != "thoughtSignature"}
    if isinstance(obj, list):
        return [sanitize_for_log(x) for x in obj]
    return obj

def call_gemini(contents: list[dict], slug: str, step_name: str) -> tuple[Image.Image | None, dict | None, str]:
    body = {
        "contents": contents,
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": "1:1"},
        },
    }
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent"
    last_err = ""
    for attempt in range(3):
        t0 = time.time()
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(body).encode("utf-8"),
                headers={"Content-Type": "application/json", "x-goog-api-key": KEY},
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                j = json.loads(resp.read().decode("utf-8"))
            cand = j["candidates"][0]
            content = cand["content"]
            out_img = None
            for p in content.get("parts", []):
                if "inlineData" in p:
                    raw_bytes = base64.b64decode(p["inlineData"]["data"])
                    out_img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
            log_entry = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "slug": slug,
                "step": step_name,
                "attempt": attempt + 1,
                "duration_s": round(time.time() - t0, 2),
                "note": "REST generateContent used per CODEX-GOREV.md (multi-turn conversation with imageConfig.aspectRatio=1:1 and thoughtSignature preservation)",
                "request": sanitize_for_log(body),
                "response_finish_reason": cand.get("finishReason"),
                "response": sanitize_for_log(content),
                "has_image": out_img is not None,
            }
            with LOG_LOCK:
                with open(LOG_PATH, "a", encoding="utf-8") as lf:
                    lf.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            if out_img is not None:
                return out_img, content, ""
            last_err = f"No image in response (finishReason={cand.get('finishReason')})"
        except Exception as e:
            last_err = str(e)[:200]
            time.sleep(2)
    return None, None, last_err

def process_person(slug: str, force: bool = False) -> str:
    grifon_path = os.path.join(OUT_GRIFON, f"{slug}.jpg")
    vesika_path = os.path.join(OUT_VESIKA, f"{slug}.jpg")
    kadraj_path = os.path.join(OUT_KADRAJ, f"{slug}.jpg")

    if not force and os.path.exists(grifon_path) and os.path.exists(vesika_path) and os.path.exists(kadraj_path):
        return f"{slug}: ZATEN VAR"

    refs = collect_refs(slug)
    extra_note = PERSON_NOTES.get(slug, "")
    bilgehan_ref = "public/media/ekip/bilgehan-zeki-ozaytac.jpg"

    # TURN 1: All original references + face-preserved kadraj + Bilgehan grey studio ref -> Natural grey studio portrait (gri-fon)
    t1_parts: list[dict] = [
        {
            "text": (
                f"We are creating studio portraits for team member '{slug}' in a multi-turn conversation. "
                f"First, here are ALL available original reference photographs of this exact person ({len(refs)} unique photos):"
            )
        }
    ]
    for label, rpath in refs:
        t1_parts.append({"text": f"Reference photo — {label}:"})
        t1_parts.append(encode_path(rpath, max_dim=1280))

    t1_parts.append(
        {
            "text": (
                "Here is the framing-corrected portrait (`kadraj`) of this person where their original face is 100% preserved and the head-and-shoulders framing is centered with headroom:"
            )
        }
    )
    t1_parts.append(encode_path(kadraj_path, max_dim=1024, quality=95))

    t1_parts.append(
        {
            "text": (
                "And here is our target medium-grey studio backdrop reference (`bilgehan-zeki-ozaytac.jpg` — note the medium-grey seamless studio background with subtle vignette and clean studio lighting):"
            )
        }
    )
    t1_parts.append(encode_path(bilgehan_ref, max_dim=1024, quality=92))

    t1_parts.append(
        {
            "text": (
                "TASK 1 (Natural Medium-Grey Studio Portrait / Gri Fon): "
                "Using the framing-corrected portrait and all original reference photos of this person above, produce a natural head-and-shoulders studio portrait on a flat medium-grey studio background matching Bilgehan's studio backdrop (NOT pure white, NOT black). "
                "IMPORTANT:\n"
                "1. NO stiff biometric/ID rules: preserve the person's natural head angle, posture, authentic expression/smile, hairstyle or headscarf wrap, glasses (if worn), and clothing from their framing-corrected photo.\n"
                "2. Keep their face 100% faithful to the real person—do NOT beautify, smooth skin texture, slim the face, change eye/nose/lip/eyebrow shape, or alter age.\n"
                "3. Head-and-shoulders framing with comfortable headroom above the hair/headscarf and both shoulders visible. If a hand is raised to the face/hair in a selfie, remove/lower the hand cleanly.\n"
                "4. Soft, even professional studio lighting on the subject that matches the medium-grey backdrop, sharp focus across the subject, no shallow depth-of-field blur, no text or logos. "
                + (f"\nPerson details: {extra_note}" if extra_note else "")
            )
        }
    )

    contents: list[dict] = [{"role": "user", "parts": t1_parts}]
    gen_grifon, c1_content, err1 = call_gemini(contents, slug, "turn1_grifon")
    if gen_grifon is None or c1_content is None:
        return f"{slug}: TURN 1 (gri-fon) HATA: {err1}"

    grifon_final = gen_grifon.resize((600, 600), Image.Resampling.LANCZOS)
    grifon_final.save(grifon_path, "JPEG", quality=92)
    contents.append(c1_content)

    # TURN 2: Standard white-background studio vesikalik in the SAME conversation
    t2_parts: list[dict] = [
        {
            "text": (
                "TASK 2 (Standard White-Background Studio Vesikalık): "
                "Now, in the same conversation for this EXACT same person, create a standard white-background studio portrait (vesikalık) for our team cards. "
                "IMPORTANT:\n"
                "1. Plain pure white seamless studio background (#FFFFFF).\n"
                "2. Front-facing head-and-shoulders portrait, centered, eyes at ~40% from the top, comfortable headroom above the hair/headscarf, both shoulders visible, soft even studio lighting.\n"
                "3. Preserve the exact same person's facial identity from the original photos and previous turn—do NOT beautify, slim, smooth skin, or change eye shape, eyebrow arch, nose shape, lips, jawline, or glasses.\n"
                "4. Keep their own clothing tidied up (remove outdoor caps, safety hard hats, or sunglasses resting on top of the head if any; keep prescription eyeglasses and headscarves). No hands, no text, no logos. Photorealistic studio camera photo. "
                + (f"\nPerson details: {extra_note}" if extra_note else "")
            )
        }
    ]
    contents.append({"role": "user", "parts": t2_parts})
    gen_vesika, c2_content, err2 = call_gemini(contents, slug, "turn2_vesikalik")
    if gen_vesika is None or c2_content is None:
        return f"{slug}: TURN 2 (vesikalik) HATA: {err2}"

    vesika_final = gen_vesika.resize((600, 600), Image.Resampling.LANCZOS)
    vesika_final.save(vesika_path, "JPEG", quality=92)
    contents.append(c2_content)

    # Save conversation state so we can add a Turn 3 correction in the exact same conversation if needed
    conv_file = os.path.join(CONV_DIR, f"{slug}.json")
    with open(conv_file, "w", encoding="utf-8") as cf_out:
        json.dump(contents, cf_out)

    return f"{slug}: TAMAM (refs={len(refs)})"

if __name__ == "__main__":
    all_slugs = sorted(os.path.basename(p)[:-4] for p in glob.glob("public/media/ekip/*.jpg"))
    force_flag = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--force"]
    targets = args[0].split(",") if args else all_slugs
    # Rule: Ayni anda en cok iki Gemini isi calistir (max_workers=2)
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        futures = [ex.submit(process_person, s, force_flag) for s in targets]
        for fut in cf.as_completed(futures):
            print(fut.result(), flush=True)
