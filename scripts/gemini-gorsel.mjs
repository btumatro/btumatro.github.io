#!/usr/bin/env node
/**
 * Gemini ile görsel üretir (kapak, illüstrasyon).
 *
 * Kullanım (GEMINI_API_KEY ortamda tanımlı olmalı):
 *   node scripts/gemini-gorsel.mjs --prompt "..." --cikti public/media/ses/kapak.jpg [--oran 1:1] [--genislik 480]
 *
 * Çıktı JPEG'e çevrilip istenen genişliğe küçültülür (sharp, mozjpeg); ham görsel
 * saklanmaz. Promptlarda gerçek kişi, marka logosu veya kurum amblemi istenmemeli.
 */
import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const arg = (ad, varsayilan) => { const i = process.argv.indexOf(ad); return i > -1 ? process.argv[i + 1] : varsayilan; };
const prompt = arg('--prompt');
const cikti = arg('--cikti');
const oran = arg('--oran', '1:1');
const genislik = Number(arg('--genislik', '480'));
const MODEL = process.env.GORSEL_MODEL || 'gemini-3-pro-image';
const KEY = process.env.GEMINI_API_KEY;
if (!prompt || !cikti) { console.error('Kullanım: --prompt "..." --cikti yol.jpg'); process.exit(1); }
if (!KEY) { console.error('GEMINI_API_KEY tanımlı değil.'); process.exit(1); }

const govde = {
  contents: [{ parts: [{ text: prompt }] }],
  generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: oran } },
};
for (let deneme = 1; deneme <= 3; deneme++) {
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY },
    body: JSON.stringify(govde),
  });
  const j = await r.json();
  const veri = j.candidates?.[0]?.content?.parts?.find((p) => p.inlineData?.data)?.inlineData?.data;
  if (r.ok && veri) {
    fs.mkdirSync(path.dirname(cikti), { recursive: true });
    await sharp(Buffer.from(veri, 'base64')).resize(genislik, null, { withoutEnlargement: true })
      .jpeg({ quality: 84, mozjpeg: true }).toFile(cikti);
    console.log(`Görsel: ${cikti}`);
    process.exit(0);
  }
  console.warn(`Deneme ${deneme} başarısız: ${r.status} ${JSON.stringify(j.error ?? j.candidates?.[0]?.finishReason ?? '').slice(0, 200)}`);
  await new Promise((s) => setTimeout(s, 3000 * deneme));
}
process.exit(1);
