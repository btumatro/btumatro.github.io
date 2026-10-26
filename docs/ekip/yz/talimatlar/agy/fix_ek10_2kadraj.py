import os
import cv2
import numpy as np

WORKSPACE = "/Users/wildgenie/Projects/btu-matro"
SCRATCH = "/Users/wildgenie/.gemini/antigravity-cli/brain/482501c3-e797-49fa-a7d5-231ae28c4675/scratch"
OUT_KADRAJ_DIR = os.path.join(WORKSPACE, "docs/ekip/yz/codex/kadraj")


def solve_Boundary_Laplace(real_bgr, gem_bgr, valid_mask):
    """
    True Dirichlet Laplace solver for the outer strip (valid_mask == 0):
    1. Inside valid_mask, the offset u = real_bgr - gem_bgr is known along the boundary band.
    2. Outside valid_mask, we NEVER look at real_bgr (which has border reflections!).
       Instead, we initialize u outside valid_mask from the mean boundary offset and solve
       Laplace's equation (Δu = 0) with Dirichlet boundary conditions on the interior boundary
       and Neumann (zero-slope) boundary conditions on the outer canvas edges.
    """
    k_erode = np.ones((9, 9), np.uint8)
    interior = cv2.erode(valid_mask, k_erode, borderType=cv2.BORDER_REPLICATE) > 127
    k_inner = np.ones((25, 25), np.uint8)
    deep_interior = cv2.erode(valid_mask, k_inner, borderType=cv2.BORDER_REPLICATE) > 127
    boundary_band = interior & (~deep_interior)

    diff = real_bgr.astype(np.float32) - gem_bgr.astype(np.float32)
    # Smooth diff along the boundary band only (normalized convolution over interior)
    w_mask = interior.astype(np.float32)[:, :, None]
    num = cv2.GaussianBlur(diff * w_mask, (31, 31), 0)
    den = cv2.GaussianBlur(w_mask, (31, 31), 0)[:, :, None] + 1e-5
    diff_clean = num / den

    # Initialize exterior with row/col nearest boundary value (NOT real_bgr!)
    u_s = cv2.resize(diff_clean, (150, 150), interpolation=cv2.INTER_AREA)
    int_s = cv2.resize(interior.astype(np.uint8) * 255, (150, 150), interpolation=cv2.INTER_NEAREST) > 127

    # Fill ~int_s initially with the mean of the boundary band so relaxation converges immediately without reflection contamination
    if boundary_band.any():
        b_mean = diff[boundary_band].mean(axis=0)
    else:
        b_mean = np.zeros(3, dtype=np.float32)
    u_s[~int_s] = b_mean
    fixed_s = u_s.copy()

    for _ in range(600):
        up = np.pad(u_s[:-1, :, :], ((1, 0), (0, 0), (0, 0)), mode="edge")
        dn = np.pad(u_s[1:, :, :], ((0, 1), (0, 0), (0, 0)), mode="edge")
        lf = np.pad(u_s[:, :-1, :], ((0, 0), (1, 0), (0, 0)), mode="edge")
        rt = np.pad(u_s[:, 1:, :], ((0, 0), (0, 1), (0, 0)), mode="edge")
        u_s = 0.25 * (up + dn + lf + rt)
        u_s[int_s] = fixed_s[int_s]

    u_full = cv2.resize(u_s, (600, 600), interpolation=cv2.INTER_CUBIC)
    gem_corr = np.clip(gem_bgr.astype(np.float32) + u_full, 0, 255).astype(np.uint8)
    return gem_corr


def blend_top_strip(real_bgr, gem_corr, valid_mask):
    """
    Smoothly transition across the valid_mask boundary using BORDER_REPLICATE during erosion
    so the left, right, and bottom edges of the 600x600 frame are NEVER eroded when they are already valid!
    """
    k_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
    eroded = cv2.erode(valid_mask, k_erode, borderType=cv2.BORDER_REPLICATE).astype(np.float32) / 255.0
    alpha = cv2.GaussianBlur(eroded, (25, 25), 0, borderType=cv2.BORDER_REPLICATE)[:, :, None]

    out = real_bgr.astype(np.float32) * alpha + gem_corr.astype(np.float32) * (1.0 - alpha)
    out = np.clip(out, 0, 255).astype(np.uint8)

    # Guarantee 100% untouched original pixels deeper than 20px inside valid_mask
    k_core = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
    core = cv2.erode(valid_mask, k_core, borderType=cv2.BORDER_REPLICATE) > 127
    out[core] = real_bgr[core]
    return out, core


def fix_duygu_solak():
    # duygu-solak.jpg is 1876x2048; site crop was (150, 14) -> (1652, 1516) [S=1502].
    # At x=0..42, y=1000..1550 in duygu-solak.jpg there is a black picture-frame edge on the far left wall.
    # By starting at x0=52 (still 98px wider on the left than the site crop, and 224px wider on the right!),
    # 100% of left, right, and bottom are REAL uncropped original without the black strip on the left!
    orig_path = os.path.join(WORKSPACE, "docs/ekip/orijinal/duygu-solak.jpg")
    orig_bgr = cv2.imread(orig_path)
    oh, ow = orig_bgr.shape[:2]

    nx0, ny0, nx1, ny1 = 52, -196, 1876, 1628  # 1824x1824 square
    need_t = -ny0  # 196px at top (~64px in 600x600)

    ext_orig = cv2.copyMakeBorder(orig_bgr, need_t, 0, 0, 0, cv2.BORDER_REPLICATE)
    crop_orig = ext_orig[0 : ny1 + need_t, nx0:nx1]
    # Use INTER_AREA for anti-aliased downsampling (zero Moiré on hair!)
    real_600 = cv2.resize(crop_orig, (600, 600), interpolation=cv2.INTER_AREA)

    valid_orig = np.zeros((oh, ow), dtype=np.uint8)
    valid_orig[:, :] = 255
    ext_valid = cv2.copyMakeBorder(valid_orig, need_t, 0, 0, 0, cv2.BORDER_CONSTANT, value=0)
    crop_valid = ext_valid[0 : ny1 + need_t, nx0:nx1]
    valid_600 = cv2.resize(crop_valid, (600, 600), interpolation=cv2.INTER_NEAREST)

    # Align kadraj_ek9_cache/duygu-solak_try1.jpg (which has clean wall + top hair tips at y=0..68) to real_600
    gem_raw = cv2.imread(os.path.join(SCRATCH, "kadraj_ek9_cache/duygu-solak_try1.jpg"))
    tpl = real_600[100:500, 100:500]
    best = (-1.0, 1.0, 100, 100)
    for sc in np.linspace(0.95, 1.05, 41):
        tw = int(round(400 * sc))
        t_rs = cv2.resize(tpl, (tw, tw), interpolation=cv2.INTER_AREA)
        res = cv2.matchTemplate(gem_raw, t_rs, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(res)
        if mv > best[0]:
            best = (mv, sc, ml[0], ml[1])
    mv, sc, gx, gy = best
    M = np.array([[1.0 / sc, 0.0, 100.0 - gx / sc], [0.0, 1.0 / sc, 100.0 - gy / sc]], dtype=np.float32)
    gem_aligned = cv2.warpAffine(gem_raw, M, (600, 600), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    gem_corr = solve_Boundary_Laplace(real_600, gem_aligned, valid_600)
    out, core = blend_top_strip(real_600, gem_corr, valid_600)
    out_path = os.path.join(OUT_KADRAJ_DIR, "duygu-solak.jpg")
    cv2.imwrite(out_path, out, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
    print("duygu-solak fixed: mv=", round(mv, 3), "core_pct=", round(float(core.mean() * 100), 1))


def fix_zeynep_seher():
    # zeynep-seher-yolasigmaz-canva.jpg is 2016x1512; site crop was (307, 13) -> (1774, 1480) [S=1467].
    # Taking (148, -228, 1888, 1512) [S=1740] uses 100% REAL left, right, and bottom!
    # Only top 79px (y=0..79) is outside the uncropped original, and her hair does NOT even touch y=79
    # (her hair starts below y=85; at y=79 there is only the white cabinet side on the left, cabinet top in middle, and cream wall on right).
    orig_path = os.path.join(WORKSPACE, "docs/ekip/orijinal/zeynep-seher-yolasigmaz-canva.jpg")
    orig_bgr = cv2.imread(orig_path)
    oh, ow = orig_bgr.shape[:2]

    nx0, ny0, nx1, ny1 = 148, -228, 1888, 1512
    need_t = -ny0  # 228px

    ext_orig = cv2.copyMakeBorder(orig_bgr, need_t, 0, 0, 0, cv2.BORDER_REPLICATE)
    crop_orig = ext_orig[0 : ny1 + need_t, nx0:nx1]
    real_600 = cv2.resize(crop_orig, (600, 600), interpolation=cv2.INTER_AREA)

    valid_orig = np.zeros((oh, ow), dtype=np.uint8)
    valid_orig[:, :] = 255
    ext_valid = cv2.copyMakeBorder(valid_orig, need_t, 0, 0, 0, cv2.BORDER_CONSTANT, value=0)
    crop_valid = ext_valid[0 : ny1 + need_t, nx0:nx1]
    valid_600 = cv2.resize(crop_valid, (600, 600), interpolation=cv2.INTER_NEAREST)

    # Use kadraj_ek5_cache/zeynep-seher-yolasigmaz_try2.jpg which has NO second head at the top (only cabinet + wall)!
    gem_raw = cv2.imread(os.path.join(SCRATCH, "kadraj_ek5_cache/zeynep-seher-yolasigmaz_try2.jpg"))
    tpl = real_600[120:520, 100:500]
    best = (-1.0, 1.0, 100, 120)
    for sc in np.linspace(0.90, 1.10, 41):
        tw = int(round(400 * sc))
        if tw >= 600:
            continue
        t_rs = cv2.resize(tpl, (tw, tw), interpolation=cv2.INTER_AREA)
        res = cv2.matchTemplate(gem_raw, t_rs, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(res)
        if mv > best[0]:
            best = (mv, sc, ml[0], ml[1])
    mv, sc, gx, gy = best
    M = np.array([[1.0 / sc, 0.0, 100.0 - gx / sc], [0.0, 1.0 / sc, 120.0 - gy / sc]], dtype=np.float32)
    gem_aligned = cv2.warpAffine(gem_raw, M, (600, 600), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    gem_corr = solve_Boundary_Laplace(real_600, gem_aligned, valid_600)
    out, core = blend_top_strip(real_600, gem_corr, valid_600)
    out_path = os.path.join(OUT_KADRAJ_DIR, "zeynep-seher-yolasigmaz.jpg")
    cv2.imwrite(out_path, out, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
    print("zeynep-seher-yolasigmaz fixed: mv=", round(mv, 3), "core_pct=", round(float(core.mean() * 100), 1))


if __name__ == "__main__":
    fix_duygu_solak()
    fix_zeynep_seher()
