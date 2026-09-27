/** Takım sunumlarındaki seçilmiş özgün fotoğrafları web boyutuna indirger. */
import { execFileSync } from 'node:child_process';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { homedir, tmpdir } from 'node:os';
import { join } from 'node:path';
import sharp from 'sharp';

const presentationsDir = process.env.MATRO_PRESENTATIONS_DIR || join(homedir(), 'Downloads');
const kaynaklar = {
  ashina: join(presentationsDir, 'ASHİNA TEKNOLOJİ TAKIM TANITIM kopyası_20260923_232826_0000.pdf'),
  zemheri: join(presentationsDir, 'zemheri.pptx'),
  matris: join(presentationsDir, 'matrisTanisma (2).pptx'),
  sirius: join(presentationsDir, 'SIRIUS — Topluluk Sunumu (1).pptx'),
};

// Kaynak PDF/PPTX medya kimliği, hedef dosya. Tekrar eden veya slayt grafiği olanlar alınmaz.
const secim = [
  ['ashina', 'img-015.jpg', 'galeri-ashina-sunum-elektronik.jpg'],
  ['ashina', 'img-016.jpg', 'galeri-ashina-sunum-elektronik-masa.jpg'],
  ['ashina', 'img-023.jpg', 'galeri-ashina-sunum-gece-montaj.jpg'],
  ['ashina', 'img-029.jpg', 'galeri-ashina-sunum-ekip-iha.jpg'],
  ['zemheri', 'image4.jpeg', 'galeri-zemheri-sunum-atolye-genis.jpg'],
  ['zemheri', 'image5.jpeg', 'galeri-zemheri-sunum-govde-montaj.jpg'],
  ['zemheri', 'image7.png', 'galeri-zemheri-sunum-calisma-masasi.jpg'],
  ['zemheri', 'image9.png', 'galeri-zemheri-sunum-elektronik-kontrol.jpg'],
  ['zemheri', 'image12.jpeg', 'galeri-zemheri-sunum-gece-su-testi.jpg'],
  ['zemheri', 'image14.png', 'galeri-zemheri-sunum-yarisma-hazirligi.jpg'],
  ['zemheri', 'image16.png', 'galeri-zemheri-sunum-yarisma-kontrol.jpg'],
  ['zemheri', 'image18.png', 'galeri-zemheri-sunum-roket-inceleme.jpg'],
  ['zemheri', 'image19.jpeg', 'galeri-zemheri-sunum-ekip-arac.jpg'],
  ['matris', 'image2.jpg', 'galeri-matris-sunum-masa-montaj.jpg'],
  ['matris', 'image3.jpg', 'galeri-matris-sunum-saha-iki-iha.jpg'],
  ['matris', 'image6.jpg', 'galeri-matris-sunum-yakin-montaj.jpg'],
  ['matris', 'image7.png', 'galeri-matris-sunum-saha-test.jpg'],
  ['sirius', 'image3.jpeg', 'galeri-sirius-sunum-ekip-arac.jpg'],
  ['sirius', 'image5.jpeg', 'galeri-sirius-sunum-arac-mudahale.jpg'],
  ['sirius', 'image7.png', 'galeri-sirius-sunum-yarisma-parkuru.jpg'],
];

const hedefKlasor = new URL('../public/media/', import.meta.url).pathname;
await mkdir(hedefKlasor, { recursive: true });
const gecici = await mkdtemp(join(tmpdir(), 'matro-sunum-'));
try {
  execFileSync('pdfimages', ['-all', kaynaklar.ashina, join(gecici, 'img')]);
  for (const [takim, kaynakAd, hedefAd] of secim) {
    const girdi = takim === 'ashina'
      ? await readFile(join(gecici, kaynakAd))
      : execFileSync('unzip', ['-p', kaynaklar[takim], `ppt/media/${kaynakAd}`], { maxBuffer: 30 * 1024 * 1024 });
    const hedef = join(hedefKlasor, hedefAd);
    await sharp(girdi).rotate().resize({ width: 1600, withoutEnlargement: true })
      .jpeg({ quality: 82, mozjpeg: true }).toFile(hedef);
    console.log(hedefAd);
  }
} finally {
  await rm(gecici, { recursive: true, force: true });
}
