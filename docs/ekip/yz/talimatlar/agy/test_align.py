import os
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

def align_and_blend(src_img: Image.Image, gen_img: Image.Image, out_size: int = 600) -> tuple[Image.Image, float, tuple[int, int, int]]:
    """
    Uses OpenCV C++ SIMD template matching (TM_CCOEFF_NORMED) to find the exact
    (scale, x, y) where src_img's central face/torso region matches gen_img,
    warps gen_img or places src_img at the exact aligned coordinates, applies
    spatially-varying low-frequency color correction, and blends with a soft mask.
    """
    C = 780
    gen = gen_img.convert("RGB").resize((C, C), Image.Resampling.LANCZOS)
    src_orig = src_img.convert("RGB")

    gen_gray = cv2.cvtColor(np.asarray(gen), cv2.COLOR_RGB2GRAY)
    src_gray_orig = cv2.cvtColor(np.asarray(src_orig), cv2.COLOR_RGB2GRAY)

    best_score = -1.0
    best_params = (600, 90, 150)

    # Search over scales P_cand in [440, 720]
    for P_cand in range(440, 724, 6):
        s_gray = cv2.resize(src_gray_orig, (P_cand, P_cand), interpolation=cv2.INTER_AREA)
        m0 = int(P_cand * 0.15)
        m1 = int(P_cand * 0.85)
        tpl = s_gray[m0:m1, m0:m1]
        res = cv2.matchTemplate(gen_gray, tpl, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        x_full = max_loc[0] - m0
        y_full = max_loc[1] - m0
        if max_val > best_score:
            best_score = float(max_val)
            best_params = (P_cand, x_full, y_full)

    # Refine around best_params with step=1
    P_coarse, _, _ = best_params
    for P_cand in range(max(430, P_coarse - 6), min(740, P_coarse + 7), 1):
        s_gray = cv2.resize(src_gray_orig, (P_cand, P_cand), interpolation=cv2.INTER_AREA)
        m0 = int(P_cand * 0.15)
        m1 = int(P_cand * 0.85)
        tpl = s_gray[m0:m1, m0:m1]
        res = cv2.matchTemplate(gen_gray, tpl, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        x_full = max_loc[0] - m0
        y_full = max_loc[1] - m0
        if max_val > best_score:
            best_score = float(max_val)
            best_params = (P_cand, x_full, y_full)

    P, X, Y = best_params
    src_scaled = src_orig.resize((P, P), Image.Resampling.LANCZOS)
    s_arr = np.asarray(src_scaled, dtype=np.float32)
    g_arr = np.asarray(gen, dtype=np.float32)

    # Compute valid overlap box between [X, X+P] x [Y, Y+P] and [0, C] x [0, C]
    gx0 = max(0, X)
    gy0 = max(0, Y)
    gx1 = min(C, X + P)
    gy1 = min(C, Y + P)
    sx0 = gx0 - X
    sy0 = gy0 - Y
    sx1 = sx0 + (gx1 - gx0)
    sy1 = sy0 + (gy1 - gy0)

    diff_box = s_arr[sy0:sy1, sx0:sx1] - g_arr[gy0:gy1, gx0:gx1]
    # Extrapolate diff_box outside [gx0:gx1, gy0:gy1] using OpenCV border replication + large Gaussian blur
    pad_top = gy0
    pad_bot = C - gy1
    pad_left = gx0
    pad_right = C - gx1
    diff_full = cv2.copyMakeBorder(
        diff_box, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_REPLICATE
    )
    diff_smooth = cv2.GaussianBlur(diff_full, (81, 81), 28)

    g_corrected = np.clip(g_arr + diff_smooth, 0, 255).astype(np.uint8)
    gen_corr_img = Image.fromarray(g_corrected)

    # Create soft feathered mask for pasting src_scaled
    margin = max(28, int(P * 0.07))
    mask = Image.new("L", (C, C), 0)
    mx0 = gx0 + margin if gx0 > 6 else gx0
    my0 = gy0 + margin if gy0 > 6 else gy0
    mx1 = gx1 - 1 - margin if gx1 < C - 6 else gx1 - 1
    my1 = gy1 - 1 - margin if gy1 < C - 6 else gy1 - 1
    ImageDraw.Draw(mask).rounded_rectangle((mx0, my0, mx1, my1), radius=margin, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=margin // 2))

    canv = Image.new("RGB", (C, C))
    canv.paste(src_scaled, (X, Y))
    gen_corr_img.paste(canv, (0, 0), mask)

    return gen_corr_img.resize((out_size, out_size), Image.Resampling.LANCZOS), best_score, best_params

if __name__ == "__main__":
    test_slugs = [
        "mehmet-onur-genc",
        "zeynep-seher-yolasigmaz",
        "nusret-bircan-keser",
        "muhammed-efe-coskunpinar",
        "melek-ozkeser",
        "melisa-aydirek",
        "eslem-kilic",
        "esma-demirkiyik",
    ]
    out_dir = "/Users/wildgenie/.gemini/antigravity-cli/brain/482501c3-e797-49fa-a7d5-231ae28c4675/scratch/test_out"
    os.makedirs(out_dir, exist_ok=True)
    sheet = Image.new("RGB", (600 * 4, 300 * 4), (20, 20, 20))
    for idx, s in enumerate(test_slugs):
        src = Image.open(f"public/media/ekip/{s}.jpg")
        # Test both docs/ekip/yz/kadraj/{s}.jpg and docs/ekip/yz/kadraj2/{s}.jpg
        gen = Image.open(f"docs/ekip/yz/kadraj/{s}.jpg")
        res, score, params = align_and_blend(src, gen)
        print(f"{s:28s}: NCC={score:.4f}, params={params}")
        res.save(f"{out_dir}/{s}.jpg", quality=92)
        col = (idx % 2) * 1200
        row = (idx // 2) * 300
        sheet.paste(src.resize((300, 300)), (col, row))
        sheet.paste(Image.open(f"docs/ekip/yz/kadraj2/{s}.jpg").resize((300, 300)), (col + 300, row))
        sheet.paste(gen.resize((300, 300)), (col + 600, row))
        sheet.paste(res.resize((300, 300)), (col + 900, row))
    sheet.save(f"{out_dir}/sheet.jpg", quality=90)
