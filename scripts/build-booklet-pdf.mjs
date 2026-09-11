#!/usr/bin/env node
/**
 * Kitapçık sayfalarını (docs/kitapcik-hazirlik/sayfalar/*.html) tek bir A4 PDF'e
 * birleştirir. Puppeteer'ın page.pdf() API'si, ham `chrome --print-to-pdf`
 * komutundan farklı olarak sayfa boyutunu doğrudan piksel cinsinden alır;
 * bu yüzden @page CSS kuralıyla body boyutu uyuşmazlığından kaynaklanan
 * fazladan boş sayfa sorunu oluşmaz.
 *
 * Kullanım:
 *   node scripts/build-booklet-pdf.mjs                # tüm sayfalar, sıralı
 *   node scripts/build-booklet-pdf.mjs sayfa-01-kapak  # tek sayfa (kontrol için)
 */
import puppeteer from 'puppeteer-core';
import { PDFDocument } from 'pdf-lib';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const PAGES_DIR = path.join(ROOT, 'docs/kitapcik-hazirlik/sayfalar');
const OUT_DIR = path.join(ROOT, 'docs/kitapcik-hazirlik/cikti');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

// body.page-sheet { width: 1240px; height: 1754px } — A4 @ ~150dpi (ekran/PNG önizleme için).
//
// ÖNEMLİ: Chrome'un print-to-PDF motoru, body tam olarak 1754px olduğunda
// (ekranda tam sığsa bile) sayfanın en altındaki footer'ı neredeyse boş bir
// ikinci sayfaya taşırıyor — CSS Paged Media'da overflow:hidden baskı
// sayfalamasını engellemiyor, sadece görünürlüğü etkiliyor. Ölçüldü:
// 1680px güvenli, 1700px+ taşıyor. Bu yüzden SADECE PDF üretiminde
// (ekran görüntülerini etkilemeden) body yüksekliğini bir miktar küçültüp
// payı flex `justify-content: space-between` boşluklarından alıyoruz.
const PAGE_PX = { width: 1240, height: 1754 };
const PDF_HEIGHT_START_PX = 1700;
const PDF_HEIGHT_STEP_PX = 20;
const PDF_HEIGHT_MIN_PX = 1500;

function listPages(filter) {
  const all = fs
    .readdirSync(PAGES_DIR)
    .filter((f) => /^sayfa-\d{2}-.*\.html$/.test(f))
    .sort();
  if (!filter) return all;
  return all.filter((f) => f.startsWith(filter) || f === `${filter}.html`);
}

async function main() {
  const arg = process.argv[2];
  const files = listPages(arg);
  if (files.length === 0) {
    console.error('Eşleşen sayfa bulunamadı:', arg);
    process.exit(1);
  }

  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
  const page = await browser.newPage();
  await page.setViewport(PAGE_PX);

  const pdfBuffers = [];
  for (const file of files) {
    const full = path.join(PAGES_DIR, file);
    await page.goto(`file://${full}`, { waitUntil: 'networkidle0' });
    // Google Fonts @import tamamen yüklensin diye kısa bekleme.
    await new Promise((r) => setTimeout(r, 300));

    let buf;
    let pageCount;
    let usedHeight;
    for (
      let h = PDF_HEIGHT_START_PX;
      h >= PDF_HEIGHT_MIN_PX;
      h -= PDF_HEIGHT_STEP_PX
    ) {
      await page.evaluate((height) => {
        let tag = document.getElementById('__pdf_height_override');
        if (!tag) {
          tag = document.createElement('style');
          tag.id = '__pdf_height_override';
          document.head.appendChild(tag);
        }
        tag.textContent = `body.page-sheet { height: ${height}px !important; }`;
      }, h);
      buf = await page.pdf({
        width: `${PAGE_PX.width}px`,
        height: `${PAGE_PX.height}px`,
        printBackground: true,
        preferCSSPageSize: false,
        margin: { top: 0, bottom: 0, left: 0, right: 0 },
      });
      const doc = await PDFDocument.load(buf);
      pageCount = doc.getPageCount();
      usedHeight = h;
      if (pageCount === 1) break;
    }
    if (pageCount !== 1) {
      throw new Error(
        `${file}: ${PDF_HEIGHT_MIN_PX}px'e kadar küçültülmesine rağmen tek sayfaya sığmadı (son deneme ${pageCount} sayfa). Sayfa içeriği elle kontrol edilmeli.`
      );
    }
    if (usedHeight !== PAGE_PX.height) {
      console.log(`  (not: ${file} için baskı yüksekliği ${usedHeight}px'e küçültüldü, ekran önizlemesi etkilenmez)`);
    }
    const outPath = path.join(OUT_DIR, file.replace('.html', '.pdf'));
    fs.writeFileSync(outPath, buf);
    console.log('Yazıldı:', path.relative(ROOT, outPath), `(${(buf.length / 1024).toFixed(0)} KB, 1 sayfa)`);
    pdfBuffers.push(outPath);
  }

  await browser.close();
  console.log(`\n${pdfBuffers.length} sayfa render edildi.`);

  if (pdfBuffers.length > 1) {
    const merged = await PDFDocument.create();
    for (const p of pdfBuffers) {
      const src = await PDFDocument.load(fs.readFileSync(p));
      const [copied] = await merged.copyPages(src, [0]);
      merged.addPage(copied);
    }
    const mergedPath = path.join(OUT_DIR, 'matro-tanitim-kitapcigi.pdf');
    fs.writeFileSync(mergedPath, await merged.save());
    console.log('Birleştirilmiş kitapçık:', path.relative(ROOT, mergedPath));
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
