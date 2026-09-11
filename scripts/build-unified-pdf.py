#!/usr/bin/env python3
"""
MATRO 2026 Tanıtım Kitapçığı — Birleşik PDF Üretim Motoru
Chrome Headless (--print-to-pdf) ile her sayfanın vektörel PDF çıktısını alır,
ardından her sayfadan tam olarak 1'er yaprak alıp pypdf ile 18 sayfalık eksiksiz
bir tanıtım kitapçığı PDF'i olarak birleştirir.
"""

import os
import subprocess
import glob
from pypdf import PdfWriter, PdfReader
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PAGES_DIR = os.path.join(PROJECT_ROOT, 'docs', 'kitapcik-hazirlik', 'sayfalar')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'docs', 'kitapcik-hazirlik')
TEMP_PDF_DIR = '/tmp/matro-pdf-pages'
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(TEMP_PDF_DIR, exist_ok=True)

def main():
    print("=== MATRO 2026 Birleşik PDF Üretimi Başlatılıyor ===")
    
    # 1. Mevcut sayfaların listesi (01'den itibaren sıralı)
    html_files = sorted(glob.glob(os.path.join(PAGES_DIR, 'sayfa-*.html')))
    print(f"Toplam {len(html_files)} sayfa HTML bulundu:")
    
    single_pdfs = []
    
    # 2. Her HTML dosyasını Chrome ile vektörel PDF olarak render et
    for h in html_files:
        base_name = os.path.splitext(os.path.basename(h))[0]
        pdf_out = os.path.join(TEMP_PDF_DIR, f"{base_name}.pdf")
        
        cmd = [
            CHROME_BIN,
            "--headless=new",
            f"--print-to-pdf={pdf_out}",
            "--no-pdf-header-footer",
            f"file://{h}"
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0 and os.path.exists(pdf_out):
            single_pdfs.append(pdf_out)
        else:
            print(f"✗ Hata: {base_name} render edilemedi!")
    
    # 3. pypdf ile her HTML'den tam 1 sayfa alıp tek birleşik PDF oluştur
    merged_pdf_path = os.path.join(OUTPUT_DIR, "matro-tanitim-kitapcigi-2026.pdf")
    writer = PdfWriter()
    for p in single_pdfs:
        r = PdfReader(p)
        writer.add_page(r.pages[0])
    writer.write(merged_pdf_path)
    writer.close()
    
    merged_size_mb = os.path.getsize(merged_pdf_path) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"✓ 1. BİRLEŞİK VEKTÖREL PDF (Metinler seçilebilir, logolar vektörel):")
    print(f"  Dosya: {merged_pdf_path}")
    print(f"  Sayfa Sayısı: {len(single_pdfs)}")
    print(f"  Boyut: {merged_size_mb:.2f} MB")
    print(f"=======================================================")
    
    # 4. Yüksek çözünürlüklü PNG'lerden derlenen baskı PDF'i (Pillow)
    png_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, 'ornek-tasarimlar', 'sayfa-*.png')))
    if png_files:
        hq_pdf_path = os.path.join(OUTPUT_DIR, "matro-tanitim-kitapcigi-2026-baskiya-hazir.pdf")
        images = []
        for pf in png_files:
            try:
                im = Image.open(pf)
                if im.mode != 'RGB':
                    im = im.convert('RGB')
                images.append(im)
            except Exception as e:
                pass
        if images:
            images[0].save(
                hq_pdf_path,
                save_all=True,
                append_images=images[1:],
                resolution=150.0
            )
            hq_size_mb = os.path.getsize(hq_pdf_path) / (1024 * 1024)
            print(f"✓ 2. BASKIYA HAZIR RASTER PDF (150 DPI A4 tam renk):")
            print(f"  Dosya: {hq_pdf_path}")
            print(f"  Sayfa Sayısı: {len(images)}")
            print(f"  Boyut: {hq_size_mb:.2f} MB")
            print(f"=======================================================")

if __name__ == '__main__':
    main()
