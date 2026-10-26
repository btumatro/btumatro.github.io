import json
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from codex_uret import (
    CONV_DIR,
    OUT_GRIFON,
    OUT_KADRAJ,
    OUT_VESIKA,
    call_gemini,
    encode_path,
    encode_pil,
)

def blend_real_face_onto_studio(
    kadraj_img: Image.Image,
    studio_img: Image.Image,
    face_box_rel: tuple[float, float, float, float] = (0.24, 0.16, 0.76, 0.72),
) -> tuple[Image.Image, float]:
    """
    Aligns kadraj_img to studio_img via OpenCV template matching on the face box,
    matches low-frequency skin tone/illumination, and blends the real face oval
    onto studio_img so facial identity is 100% preserved.
    """
    S = 600
    src = kadraj_img.convert("RGB").resize((S, S), Image.Resampling.LANCZOS)
    dst = studio_img.convert("RGB").resize((S, S), Image.Resampling.LANCZOS)

    src_gray = cv2.cvtColor(np.asarray(src), cv2.COLOR_RGB2GRAY)
    dst_gray = cv2.cvtColor(np.asarray(dst), cv2.COLOR_RGB2GRAY)

    fx0 = int(S * face_box_rel[0])
    fy0 = int(S * face_box_rel[1])
    fx1 = int(S * face_box_rel[2])
    fy1 = int(S * face_box_rel[3])
    fw = fx1 - fx0
    fh = fy1 - fy0

    best_score = -1.0
    best_params = (1.0, fx0, fy0)

    for scale_pct in range(82, 122, 2):
        sc = scale_pct / 100.0
        tw = int(fw * sc)
        th = int(fh * sc)
        if tw >= S or th >= S:
            continue
        tpl = cv2.resize(src_gray[fy0:fy1, fx0:fx1], (tw, th), interpolation=cv2.INTER_AREA)
        res = cv2.matchTemplate(dst_gray, tpl, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > best_score:
            best_score = float(max_val)
            best_params = (sc, max_loc[0], max_loc[1])

    sc, dx, dy = best_params
    tw = int(fw * sc)
    th = int(fh * sc)
    face_crop = src.crop((fx0, fy0, fx1, fy1)).resize((tw, th), Image.Resampling.LANCZOS)

    f_arr = np.asarray(face_crop, dtype=np.float32)
    d_arr = np.asarray(dst, dtype=np.float32)
    dst_patch = d_arr[dy : dy + th, dx : dx + tw]

    # Match low-frequency studio lighting of dst_patch onto face_crop so skin texture/features are 100% real
    # while lighting matches the studio portrait
    f_low = cv2.GaussianBlur(f_arr, (45, 45), 15)
    d_low = cv2.GaussianBlur(dst_patch, (45, 45), 15)
    # Use 60% studio illumination transfer + 40% original skin tone so it looks completely natural
    f_relit = np.clip(f_arr + 0.60 * (d_low - f_low), 0, 255).astype(np.uint8)
    face_relit_img = Image.fromarray(f_relit)

    # Elliptical soft mask covering eyes, eyebrows, nose, mouth, cheeks
    mask = Image.new("L", (tw, th), 0)
    mx = int(tw * 0.10)
    my = int(th * 0.10)
    ImageDraw.Draw(mask).ellipse((mx, my, tw - mx - 1, th - my - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=max(10, int(min(tw, th) * 0.09))))

    out = dst.copy()
    out.paste(face_relit_img, (dx, dy), mask)
    return out, best_score

def refine_in_conversation(slug: str, out_path: str, step_name: str, prompt_text: str, extra_imgs: list[dict]) -> bool:
    conv_file = os.path.join(CONV_DIR, f"{slug}.json")
    if os.path.exists(conv_file):
        contents = json.load(open(conv_file, encoding="utf-8"))
    else:
        contents = []

    parts = extra_imgs + [{"text": prompt_text}]
    contents.append({"role": "user", "parts": parts})
    im, content, err = call_gemini(contents, slug, step_name)
    if im is None or content is None:
        print(f"{slug} {step_name} HATA: {err}", flush=True)
        return False
    im.resize((600, 600), Image.Resampling.LANCZOS).save(out_path, "JPEG", quality=92)
    contents.append(content)
    with open(conv_file, "w", encoding="utf-8") as f:
        json.dump(contents, f)
    print(f"{slug} {step_name} TAMAM", flush=True)
    return True

def main() -> None:
    bilgehan_ref = "public/media/ekip/bilgehan-zeki-ozaytac.jpg"

    # 1. Bilgehan Zeki Ozaytac (#2): kadraj IS already medium-grey studio portrait; copy kadraj -> gri-fon,
    # and lock 100% real face onto vesikalik.
    b_kadraj = Image.open(os.path.join(OUT_KADRAJ, "bilgehan-zeki-ozaytac.jpg"))
    b_kadraj.save(os.path.join(OUT_GRIFON, "bilgehan-zeki-ozaytac.jpg"), "JPEG", quality=92)
    b_ves = Image.open(os.path.join(OUT_VESIKA, "bilgehan-zeki-ozaytac.jpg"))
    b_ves_fixed, sc = blend_real_face_onto_studio(b_kadraj, b_ves)
    b_ves_fixed.save(os.path.join(OUT_VESIKA, "bilgehan-zeki-ozaytac.jpg"), "JPEG", quality=92)
    print(f"bilgehan-zeki-ozaytac: gri-fon=kadraj, vesikalik face-locked (NCC={sc:.3f})")

    # 2. Berat Eren Karakas (#18): kadraj is already studio grey wall; lock 100% real face onto gri-fon and vesikalik
    brk_kadraj = Image.open(os.path.join(OUT_KADRAJ, "berat-eren-karakas.jpg"))
    for p in (os.path.join(OUT_GRIFON, "berat-eren-karakas.jpg"), os.path.join(OUT_VESIKA, "berat-eren-karakas.jpg")):
        st = Image.open(p)
        fixed, sc = blend_real_face_onto_studio(brk_kadraj, st)
        fixed.save(p, "JPEG", quality=92)
        print(f"berat-eren-karakas: face-locked {os.path.basename(os.path.dirname(p))} (NCC={sc:.3f})")

    # 3. Omer Cihan Demir (#5): crop gri-fon slightly closer so head scale matches kadraj and vesikalik
    ocd_gf = Image.open(os.path.join(OUT_GRIFON, "omer-cihan-demir.jpg"))
    # Crop (50, 55, 550, 555) -> resize to 600x600
    ocd_gf.crop((48, 52, 552, 556)).resize((600, 600), Image.Resampling.LANCZOS).save(
        os.path.join(OUT_GRIFON, "omer-cihan-demir.jpg"), "JPEG", quality=92
    )
    print("omer-cihan-demir: gri-fon head scale matched")

    # 4. Muhammed Ataman (#3): vesikalik was zoomed out; generate closer head-and-shoulders vesikalik matching gri-fon face
    refine_in_conversation(
        "muhammed-ataman",
        os.path.join(OUT_VESIKA, "muhammed-ataman.jpg"),
        "turn3_vesikalik_zoom",
        (
            "In the white-background portrait (vesikalık) you zoomed out too far showing his waist, and his face became small. "
            "Using the medium-grey portrait above where his face and head-and-shoulders scale are right, produce the white-background portrait (#FFFFFF) at the EXACT same close head-and-shoulders framing scale (head height ~42% of image height, cropped at upper chest/shoulders) keeping his exact face, hair, beard, scarf, and beige jacket."
        ),
        [
            {"text": "Keep this exact face and head-and-shoulders framing scale from his grey-background portrait:"},
            encode_path(os.path.join(OUT_GRIFON, "muhammed-ataman.jpg"), max_dim=1024),
        ],
    )

    # 5. Irmak Karaagac (#4): fix gri-fon (remove fake '(2)' logo on shirt and keep exact narrower oval face from kadraj)
    ok = refine_in_conversation(
        "irmak-karaagac",
        os.path.join(OUT_GRIFON, "irmak-karaagac.jpg"),
        "turn3_grifon_fix",
        (
            "Edit this grey-background portrait of Irmak: keep the exact medium-grey studio background, but make her face 100% identical to the first image (her real outdoor photo—do not widen her cheeks or jaw) and remove the white circular logo on her bottom-right shirt so the dark navy top is plain."
        ),
        [
            {"text": "Real photo with her exact face proportions:"},
            encode_path(os.path.join(OUT_KADRAJ, "irmak-karaagac.jpg"), max_dim=1024),
        ],
    )
    if ok:
        ik_kad = Image.open(os.path.join(OUT_KADRAJ, "irmak-karaagac.jpg"))
        ik_gf = Image.open(os.path.join(OUT_GRIFON, "irmak-karaagac.jpg"))
        ik_fixed, sc = blend_real_face_onto_studio(ik_kad, ik_gf, (0.28, 0.24, 0.70, 0.68))
        ik_fixed.save(os.path.join(OUT_GRIFON, "irmak-karaagac.jpg"), "JPEG", quality=92)
        print(f"irmak-karaagac: gri-fon face-locked (NCC={sc:.3f})")

    # 6. Gulsiye Begum Gumus (#8): make vesikalik keep the exact same face/expression as her excellent gri-fon portrait
    refine_in_conversation(
        "gulsiye-begum-gumus",
        os.path.join(OUT_VESIKA, "gulsiye-begum-gumus.jpg"),
        "turn3_vesikalik_fix",
        (
            "Look at her medium-grey studio portrait (attached): her face, smile, eyes, and headscarf look 100% like her real self, whereas in the white-background version her face changed. "
            "Take this exact medium-grey portrait, keep her face, expression, headscarf, and maroon sweater 100% identical, only remove the sunglasses perched on top of her head and change the background to a pure white seamless studio background (#FFFFFF)."
        ),
        [
            {"text": "Her approved medium-grey portrait with exact likeness:"},
            encode_path(os.path.join(OUT_GRIFON, "gulsiye-begum-gumus.jpg"), max_dim=1024),
        ],
    )

    # 7. Yusuf Sarsici (#16): in gri-fon, keep his actual photo look (white hard hat + yellow vest from kadraj) on the grey studio background, and lock his real face onto vesikalik
    ok_y = refine_in_conversation(
        "yusuf-sarsici",
        os.path.join(OUT_GRIFON, "yusuf-sarsici.jpg"),
        "turn3_grifon_keep_outfit",
        (
            "For the medium-grey studio portrait (gri-fon), keep the person exactly as in his original photo (attached)—including his exact face, expression, white safety helmet, and high-visibility vest—and ONLY replace the outdoor landscape background with the flat medium-grey studio background matching Bilgehan's studio backdrop."
        ),
        [
            {"text": "His framing-corrected original photo:"},
            encode_path(os.path.join(OUT_KADRAJ, "yusuf-sarsici.jpg"), max_dim=1024),
            {"text": "Target medium-grey studio backdrop:"},
            encode_path(bilgehan_ref, max_dim=1024),
        ],
    )
    ys_kad = Image.open(os.path.join(OUT_KADRAJ, "yusuf-sarsici.jpg"))
    ys_ves = Image.open(os.path.join(OUT_VESIKA, "yusuf-sarsici.jpg"))
    ys_ves_fixed, sc = blend_real_face_onto_studio(ys_kad, ys_ves, (0.28, 0.25, 0.72, 0.68))
    ys_ves_fixed.save(os.path.join(OUT_VESIKA, "yusuf-sarsici.jpg"), "JPEG", quality=92)
    print(f"yusuf-sarsici: vesikalik face-locked (NCC={sc:.3f})")
    if ok_y:
        ys_gf = Image.open(os.path.join(OUT_GRIFON, "yusuf-sarsici.jpg"))
        ys_gf_fixed, sc2 = blend_real_face_onto_studio(ys_kad, ys_gf, (0.28, 0.25, 0.72, 0.68))
        ys_gf_fixed.save(os.path.join(OUT_GRIFON, "yusuf-sarsici.jpg"), "JPEG", quality=92)
        print(f"yusuf-sarsici: gri-fon face-locked (NCC={sc2:.3f})")

    # 8. Feyza Karabicak (#21): gri-fon zoomed out too far; regenerate gri-fon matching the exact scale and face of kadraj / vesikalik
    refine_in_conversation(
        "feyza-karabicak",
        os.path.join(OUT_GRIFON, "feyza-karabicak.jpg"),
        "turn3_grifon_zoom",
        (
            "In the medium-grey portrait you zoomed out too far showing her waist. "
            "Take her framing-corrected portrait (attached first image) and her white-background portrait (attached second image): keep that exact close head-and-shoulders framing scale (head height ~42% of image height, cropped at chest/shoulders) and her exact face, glasses, brown headscarf, and cream sweater on the flat medium-grey studio backdrop."
        ),
        [
            {"text": "Framing-corrected original portrait:"},
            encode_path(os.path.join(OUT_KADRAJ, "feyza-karabicak.jpg"), max_dim=1024),
            {"text": "Approved head-and-shoulders scale from vesikalik:"},
            encode_path(os.path.join(OUT_VESIKA, "feyza-karabicak.jpg"), max_dim=1024),
        ],
    )

    # 9. Melek Ozkeser (#22): keep her exact face, head angle, and close-up framing from kadraj for gri-fon (replacing only the pillow/wall with medium-grey studio backdrop), then make vesikalik from gri-fon
    ok_m = refine_in_conversation(
        "melek-ozkeser",
        os.path.join(OUT_GRIFON, "melek-ozkeser.jpg"),
        "turn3_grifon_fix",
        (
            "In the previous turns her face changed and became too small. "
            "For the medium-grey studio portrait (gri-fon), keep her EXACT face, eye shape, nose stud, full lips, narrower chin, wavy dark hair with sunglasses on top, white open-knit sweater, and natural head tilt/scale from the attached `kadraj` photo—ONLY replace the cushion/wall behind her with a seamless medium-grey studio backdrop matching Bilgehan's studio backdrop."
        ),
        [
            {"text": "Keep her exact face, head angle, and scale from this photo:"},
            encode_path(os.path.join(OUT_KADRAJ, "melek-ozkeser.jpg"), max_dim=1024),
            {"text": "Target medium-grey studio backdrop:"},
            encode_path(bilgehan_ref, max_dim=1024),
        ],
    )
    if ok_m:
        mk_kad = Image.open(os.path.join(OUT_KADRAJ, "melek-ozkeser.jpg"))
        mk_gf = Image.open(os.path.join(OUT_GRIFON, "melek-ozkeser.jpg"))
        mk_fixed, sc = blend_real_face_onto_studio(mk_kad, mk_gf, (0.25, 0.16, 0.72, 0.65))
        if sc > 0.70:
            mk_fixed.save(os.path.join(OUT_GRIFON, "melek-ozkeser.jpg"), "JPEG", quality=92)
            print(f"melek-ozkeser: gri-fon face-locked (NCC={sc:.3f})")
        refine_in_conversation(
            "melek-ozkeser",
            os.path.join(OUT_VESIKA, "melek-ozkeser.jpg"),
            "turn4_vesikalik_fix",
            (
                "Now using this improved portrait of Melek, create her white-background portrait (#FFFFFF) at the same close head-and-shoulders scale, keeping her exact facial features (narrow chin, full lips, almond eyes, nose stud, dark wavy hair, white knit top) without changing her face into someone else."
            ),
            [
                {"text": "Keep this exact face and scale:"},
                encode_path(os.path.join(OUT_GRIFON, "melek-ozkeser.jpg"), max_dim=1024),
            ],
        )

    # 10. Melisa Aydirek (#23): keep her natural 3/4 pose and exact face from kadraj for gri-fon, then update vesikalik
    ok_mel = refine_in_conversation(
        "melisa-aydirek",
        os.path.join(OUT_GRIFON, "melisa-aydirek.jpg"),
        "turn3_grifon_fix",
        (
            "For the medium-grey studio portrait (gri-fon), do NOT force a front-facing pose that changes her face! "
            "Keep her exact 3/4 pose, head tilt, playful side smile, red lipstick, dark brown eyes, long straight dark brown hair, and gold/beige sleeveless top from the attached `kadraj` photo—ONLY replace the background with the seamless medium-grey studio backdrop matching Bilgehan's studio portrait and unify the studio lighting."
        ),
        [
            {"text": "Keep her exact pose and face from this photo:"},
            encode_path(os.path.join(OUT_KADRAJ, "melisa-aydirek.jpg"), max_dim=1024),
            {"text": "Target medium-grey studio backdrop:"},
            encode_path(bilgehan_ref, max_dim=1024),
        ],
    )
    if ok_mel:
        ma_kad = Image.open(os.path.join(OUT_KADRAJ, "melisa-aydirek.jpg"))
        ma_gf = Image.open(os.path.join(OUT_GRIFON, "melisa-aydirek.jpg"))
        ma_fixed, sc = blend_real_face_onto_studio(ma_kad, ma_gf, (0.24, 0.16, 0.72, 0.68))
        if sc > 0.70:
            ma_fixed.save(os.path.join(OUT_GRIFON, "melisa-aydirek.jpg"), "JPEG", quality=92)
            print(f"melisa-aydirek: gri-fon face-locked (NCC={sc:.3f})")

    # 11. Eslem Kilic (#24): gri-fon is great; make vesikalik match gri-fon's exact face and closer head-and-shoulders framing on pure white background
    refine_in_conversation(
        "eslem-kilic",
        os.path.join(OUT_VESIKA, "eslem-kilic.jpg"),
        "turn3_vesikalik_fix",
        (
            "Look at her medium-grey studio portrait (attached): the face, glasses, hair, and head-and-shoulders scale are spot-on, whereas the white-background version zoomed out too far. "
            "Take this exact medium-grey portrait and place her on a pure white seamless studio background (#FFFFFF) at the exact same close head-and-shoulders scale, keeping her face 100% identical."
        ),
        [
            {"text": "Her approved medium-grey studio portrait:"},
            encode_path(os.path.join(OUT_GRIFON, "eslem-kilic.jpg"), max_dim=1024),
        ],
    )

    # 12. Esma Demirkiyik (#25): crop gri-fon closer to proper head-and-shoulders scale, and generate vesikalik directly from that cropped gri-fon so her face matches
    ed_gf = Image.open(os.path.join(OUT_GRIFON, "esma-demirkiyik.jpg"))
    ed_gf_cropped = ed_gf.crop((55, 18, 545, 508)).resize((600, 600), Image.Resampling.LANCZOS)
    ed_gf_cropped.save(os.path.join(OUT_GRIFON, "esma-demirkiyik.jpg"), "JPEG", quality=92)
    print("esma-demirkiyik: gri-fon cropped to proper head-and-shoulders scale")
    refine_in_conversation(
        "esma-demirkiyik",
        os.path.join(OUT_VESIKA, "esma-demirkiyik.jpg"),
        "turn3_vesikalik_fix",
        (
            "In the previous white-background portrait her face looked like a different person, whereas in the medium-grey portrait (attached) her face, eyebrows, nose, full lips, and wavy hair look like her real self. "
            "Using this exact medium-grey portrait and her original photo, create the white-background studio portrait (#FFFFFF) at this same head-and-shoulders scale, keeping her exact facial features from the medium-grey portrait and original photo."
        ),
        [
            {"text": "Keep her exact facial features and scale from this medium-grey portrait:"},
            encode_pil(ed_gf_cropped, max_dim=1024),
            {"text": "Original photo for exact face verification:"},
            encode_path(os.path.join(OUT_KADRAJ, "esma-demirkiyik.jpg"), max_dim=1024),
        ],
    )

if __name__ == "__main__":
    main()
