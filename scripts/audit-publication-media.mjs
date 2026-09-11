/** Gerçek görsel ölçülerini ve kaynak manifesti sapmalarını kaydeder. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(root, 'docs/kitapcik-hazirlik');
fs.mkdirSync(out, { recursive: true });
const assets = JSON.parse(fs.readFileSync(path.join(root, 'src/data/assets.json'))).assets;
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'docs/web-site-medya-manifest.json')));
const rows = [];
for (const file of fs.readdirSync(path.join(root, 'public/media'), { recursive: true }).filter(f => /\.(jpe?g|png|webp)$/i.test(f))) {
  const source = path.join(root, 'public/media', file);
  const meta = await sharp(source).metadata();
  const entry = assets.find(a => a.file === '/media/' + file);
  rows.push({
    file: '/media/' + file, width: meta.width, height: meta.height,
    bytes: fs.statSync(source).size, format: meta.format,
    a4PortraitPpi: Math.min(meta.width / (210 / 25.4), meta.height / (297 / 25.4)),
    catalog: entry ? { width: entry.width, height: entry.height, sizeKb: entry.sizeKb } : null,
    dimensionsMismatch: Boolean(entry && (entry.width !== meta.width || entry.height !== meta.height)),
    sizeMismatch: Boolean(entry && Math.abs(entry.sizeKb - fs.statSync(source).size / 1024) > 2),
  });
}
fs.writeFileSync(path.join(out, 'medya-olculeri.json'), JSON.stringify(rows, null, 2) + '\n');
const missing = manifest.filter(a => !fs.existsSync(path.join(root, 'public', a.file))).map(a => a.file);
fs.writeFileSync(path.join(out, 'eski-manifest-yollari.json'), JSON.stringify(missing, null, 2) + '\n');
console.log(JSON.stringify({ images: rows.length, dimensionsMismatch: rows.filter(r => r.dimensionsMismatch).length, metadataMismatch: rows.filter(r => r.dimensionsMismatch || r.sizeMismatch).length, missingManifestPaths: missing.length }));
