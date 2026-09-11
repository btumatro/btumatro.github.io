#!/usr/bin/env python3
"""
public/media içindeki görselleri algısal hash (dHash) ile karşılaştırıp
olası kopya/az-çözünürlüklü veya kırpılmış varyantları listeler.

Kullanım:
    python3 scripts/find-duplicate-images.py [--threshold 10]

Çıktı, Hamming mesafesine göre artan sırada aday çiftleri gösterir.
Küçük mesafe (0-4) neredeyse kesin eşleşme; 5-10 arası görsel kontrol gerektirir.
Bu bir sezgiseldir: aynı kompozisyon şablonunu paylaşan farklı görseller
(ör. aynı arkaplanlı sponsor duyuru kartları) yanlış pozitif verebilir.
"""
import argparse
import os
import pickle
from PIL import Image

MEDIA_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'media')
CACHE_FILE = '/tmp/matro_dhash_cache.pkl'


def dhash(image: Image.Image, hash_size: int = 8) -> int:
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.LANCZOS)
    pixels = list(image.getdata())
    bits = []
    for row in range(hash_size):
        for col in range(hash_size):
            left = pixels[row * (hash_size + 1) + col]
            right = pixels[row * (hash_size + 1) + col + 1]
            bits.append(left > right)
    val = 0
    for b in bits:
        val = (val << 1) | int(b)
    return val


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count('1')


def collect_files():
    files = []
    for root, _dirs, names in os.walk(MEDIA_DIR):
        for n in names:
            if n.lower().endswith(('.jpg', '.jpeg', '.png')):
                files.append(os.path.join(root, n))
    return files


def compute_hashes(files, use_cache=True):
    hashes = {}
    for f in files:
        try:
            hashes[f] = dhash(Image.open(f))
        except Exception as e:
            print(f'ERR {f}: {e}')
    return hashes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--threshold', type=int, default=10, help='Maks. Hamming mesafesi (varsayılan 10)')
    ap.add_argument('--exclude-logos', action='store_true', help='logolar/ klasörünü hariç tut (şablon benzeri false-positive çok)')
    args = ap.parse_args()

    files = collect_files()
    if args.exclude_logos:
        files = [f for f in files if f'{os.sep}logolar{os.sep}' not in f]

    print(f'Toplam görsel: {len(files)}')
    hashes = compute_hashes(files)

    pairs = []
    keys = list(hashes.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            d = hamming(hashes[keys[i]], hashes[keys[j]])
            if d <= args.threshold:
                pairs.append((d, keys[i], keys[j]))
    pairs.sort()

    print(f'Aday çift sayısı: {len(pairs)}\n')
    for d, a, b in pairs:
        ia, ib = Image.open(a), Image.open(b)
        sa, sb = os.path.getsize(a) // 1024, os.path.getsize(b) // 1024
        ra = os.path.relpath(a, MEDIA_DIR)
        rb = os.path.relpath(b, MEDIA_DIR)
        print(f'{d:2d}  {ra} ({ia.size[0]}x{ia.size[1]}, {sa}KB)  <->  {rb} ({ib.size[0]}x{ib.size[1]}, {sb}KB)')


if __name__ == '__main__':
    main()
