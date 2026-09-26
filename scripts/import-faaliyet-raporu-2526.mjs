#!/usr/bin/env node
/**
 * "MATRO Faaliyet Raporu 25-26.docx" içindeki fotoğrafları siteye alır.
 *
 * Kullanım:
 *   node scripts/import-faaliyet-raporu-2526.mjs "~/Downloads/MATRO Faaliyet Raporu 25-26.docx"
 *
 * docx bir zip arşividir; fotoğraflar word/media/imageN.* altında durur. Her görsel
 * açılıp raporda hangi faaliyetin altında olduğu ve fotoğrafta ne göründüğü tek tek
 * kontrol edildi (bkz. AGENTS.md "Kaynak doğrulama"). Aşağıdaki JOBS listesi o
 * eşleştirmenin sonucudur:
 *   - Sitede zaten bulunan kareler (image5, 6, 14, 36, 37, 39, 40, 44, 45) alınmadı.
 *   - image18/19 (Formula Student) başka bir takımın (TU Bursa Racing) afişi/uzak
 *     çekimi; image41 (altı bacaklı robot) ve image42 (CAD ekran görüntüsü) hangi
 *     takıma ait olduğu fotoğraftan doğrulanamadı — alınmadı.
 *   - image21 fotoğraftaki okul tabelası rapordaki okul adıyla uyuşmuyor; bu yüzden
 *     yalnız okul adı geçmeyen genel mentörlük galerisine kondu.
 */
import sharp from 'sharp';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, 'public/media');

// [docx görseli, hedef dosya, azami genişlik]
const JOBS = [
  ['image1.png', 'galeri-tanisma-toplantisi-amfi.jpg', 1600],
  ['image2.png', 'galeri-tanisma-kahvaltisi-salon.jpg', 1600],
  ['image3.png', 'galeri-robot-gunleri-stant.jpg', 1600],
  ['image4.png', 'galeri-tubitak-mam-atolye.jpg', 1600],
  ['image7.png', 'galeri-genel-egitim-2025.jpg', 1200],
  ['image8.png', 'galeri-egitim-kampi-1.jpg', 1200],
  ['image9.png', 'galeri-egitim-kampi-2.jpg', 1200],
  ['image10.png', 'galeri-ermetal-baretler.jpg', 1600],
  ['image11.jpeg', 'galeri-turkish-technic-workshop-grup.jpg', 1600],
  ['image12.png', 'galeri-meexx-stant-foto.jpg', 1200],
  ['image13.png', 'galeri-devfest-stant.jpg', 1200],
  ['image15.png', 'galeri-hali-saha-2026.jpg', 1600],
  ['image16.png', 'galeri-bahar-piknigi-grup.jpg', 1600],
  ['image17.png', 'galeri-voleybol.jpg', 1200],
  ['image20.png', 'galeri-bilim-cafe.jpg', 1200],
  ['image21.jpeg', 'galeri-okul-ziyareti-ortaokul.jpg', 1200],
  ['image22.png', 'galeri-buyuk-kolej-bilim-haftasi.jpg', 1200],
  ['image23.png', 'galeri-murat-hudavendigar-atolye.jpg', 1200],
  ['image24.png', 'galeri-arduino-egitimi-lise.jpg', 1200],
  ['image25.png', 'galeri-velikoy-lise-amfi.jpg', 1200],
  ['image26.png', 'galeri-velikoy-lise-atolye.jpg', 1200],
  ['image27.png', 'galeri-tugay-ciner-atolye.jpg', 1600],
  ['image28.png', 'haber-guhem-ziyareti.jpg', 1200],
  ['image29.png', 'haber-tusas-teknik-gezi-xl.jpg', 1200],
  ['image30.jpeg', 'galeri-genc-ticaret-odul.jpg', 1200],
  ['image31.png', 'galeri-teknofest-5dk-anlat-odul.jpg', 1600],
  ['image32.png', 'galeri-advance-up-hackathon.jpg', 1200],
  ['image33.png', 'galeri-astro-hackathon.jpg', 1200],
  ['image34.png', 'galeri-uhalfest-stant.jpg', 1200],
  ['image35.png', 'galeri-ashina-atolye.jpg', 1200],
  ['image38.jpeg', 'galeri-iss-atolye-ekip.jpg', 1600],
  ['image43.jpeg', 'galeri-ika-sasi.jpg', 1200],
  ['image46.png', 'takim-ashina-inovasyon.jpg', 1200],
];

const docx = process.argv[2];
if (!docx || !fs.existsSync(docx)) {
  console.error('docx yolu verilmedi veya bulunamadı:', docx);
  process.exit(1);
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'matro-rapor-'));
execFileSync('unzip', ['-q', '-o', docx, 'word/media/*', '-d', tmp]);

for (const [src, dest, width] of JOBS) {
  const from = path.join(tmp, 'word/media', src);
  await sharp(from)
    .flatten({ background: '#ffffff' })
    .resize(width, null, { withoutEnlargement: true })
    .jpeg({ quality: 82, mozjpeg: true })
    .toFile(path.join(OUT, dest));
  console.log(src, '->', dest);
}

fs.rmSync(tmp, { recursive: true, force: true });
