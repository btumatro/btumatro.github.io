#!/usr/bin/env node
/**
 * MATRO tanıtım podcasti — yalnızca ses (Gemini TTS, çok konuşmacılı).
 *
 * podcast-generator projesindeki AudioSynthesizer ile aynı yöntem: sekans başına tek istek,
 * "Can: ..." / "Ayse: ..." satırları, model gemini-2.5-flash-preview-tts, sesler
 * Alnilam (Can) ve Aoede (Ayse). Çıkan 24 kHz s16le PCM, ffmpeg ile WAV/MP3'e çevrilir.
 * Zamanlama/altyazı ve video bu betiğin kapsamında değil.
 *
 * Kullanım (GEMINI_API_KEY ortamda tanımlı olmalı):
 *   node scripts/podcast-tts.mjs --demo            # ilk sekansın ilk 6 repliği
 *   node scripts/podcast-tts.mjs                   # tüm sekanslar + birleşik MP3 + müzikli MP3
 *   node scripts/podcast-tts.mjs --sadece-miks     # TTS'siz; mevcut MP3'ten müzikli sürümü yeniden üret
 *   node scripts/podcast-tts.mjs --senaryo docs/podcast/radyo-aralari/01-x.json --cikti radyo/01-x
 *                                                  # başka bir senaryo; müziksiz tek MP3 (radyo araları)
 */
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'docs/podcast');
const OUT = path.join(DIR, 'ses');
const MODEL = process.env.TTS_MODEL || 'gemini-2.5-flash-preview-tts';
const VOICES = { Can: 'Alnilam', Ayse: 'Aoede' };
const KEY = process.env.GEMINI_API_KEY;

const arg = (ad) => { const i = process.argv.indexOf(ad); return i > -1 ? process.argv[i + 1] : undefined; };
const senaryoYolu = arg('--senaryo');
const ciktiAdi = arg('--cikti');
const script = JSON.parse(fs.readFileSync(senaryoYolu ? path.resolve(ROOT, senaryoYolu) : path.join(DIR, 'matro-tanitim-podcast-senaryo.json'), 'utf8'));
const demo = process.argv.includes('--demo');
const sequences = demo
  ? [{ ...script.sequences[0], sequenceId: 0, dialogues: script.sequences[0].dialogues.slice(0, 6) }]
  : script.sequences;
fs.mkdirSync(OUT, { recursive: true });

async function tts(text) {
  if (!KEY) throw new Error('GEMINI_API_KEY tanımlı değil.');
  const body = {
    contents: [{ parts: [{ text }] }],
    generationConfig: {
      responseModalities: ['AUDIO'],
      speechConfig: {
        multiSpeakerVoiceConfig: {
          speakerVoiceConfigs: Object.entries(VOICES).map(([speaker, voiceName]) => ({ speaker, voiceConfig: { prebuiltVoiceConfig: { voiceName } } })),
        },
      },
    },
  };
  for (let deneme = 1; deneme <= 4; deneme++) {
    const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY },
      body: JSON.stringify(body),
    });
    const j = await r.json();
    const data = j.candidates?.[0]?.content?.parts?.find((p) => p.inlineData?.data)?.inlineData?.data;
    if (r.ok && data) return Buffer.from(data, 'base64');
    console.warn(`Deneme ${deneme} başarısız: ${r.status} ${JSON.stringify(j.error ?? j.candidates?.[0]?.finishReason ?? '').slice(0, 200)}`);
    await new Promise((s) => setTimeout(s, 2000 * deneme));
  }
  throw new Error('Gemini TTS ses döndürmedi.');
}

/**
 * Müzikli sürüm: "Atölyede Başlar" şarkısının nakaratı açılışta, final bölümü kapanışta.
 * Kesim noktaları şarkının gömülü altyazı zamanlarından ve ses seviyesi ölçümünden seçildi
 * (docs/topluluk-sarkisi/sozler/01-atolyede-baslar.md):
 *   - ACILIS: 51–71 sn (nakarattan önceki geçiş + "Atölyede başlar... / MATRO'nun sesi...").
 *     Konuşma ACILIS.konusmaBaslar saniyesinde girer; müzik 1 sn içinde %15'e iner,
 *     arkada devam edip ACILIS.kapanisBaslar'dan itibaren 4 sn'de kaybolur.
 *   - KAPANIS: 148,5–172 sn ("Bir, iki, üç... MATRO!" + final nakarat), konuşma bittikten
 *     KAPANIS.bosluk sn sonra girer, son 3 sn'de kısılır.
 */
const SARKI = path.join(ROOT, 'docs/topluluk-sarkisi/ses/01-atolyede-baslar.mp4');
const ACILIS = { bas: 51, son: 71, seviye: 0.8, altSeviye: 0.15, konusmaBaslar: 11, kapanisBaslar: 15.5 };
const KAPANIS = { bas: 148.5, son: 172, seviye: 0.8, bosluk: 0.8 };
const sureOku = (f) => Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());

function muzikliSurum(konusma, hedef) {
  const A = ACILIS;
  const K = KAPANIS;
  const kisilma = A.konusmaBaslar - 0.5;
  const kapanisGecikme = Math.round((A.konusmaBaslar + sureOku(konusma) + K.bosluk) * 1000);
  const kapanisUzunluk = K.son - K.bas;
  const filtre = [
    `[0:a]atrim=${A.bas}:${A.son},asetpts=PTS-STARTPTS,aresample=44100,` +
      `volume='if(lt(t,${kisilma}),${A.seviye},if(lt(t,${kisilma + 1}),${A.seviye}-${A.seviye - A.altSeviye}*(t-${kisilma}),${A.altSeviye}))':eval=frame,` +
      `afade=t=in:st=0:d=1,afade=t=out:st=${A.kapanisBaslar}:d=4[acilis]`,
    `[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,adelay=${A.konusmaBaslar * 1000}|${A.konusmaBaslar * 1000}[ses]`,
    `[0:a]atrim=${K.bas}:${K.son},asetpts=PTS-STARTPTS,aresample=44100,volume=${K.seviye},` +
      `afade=t=in:st=0:d=0.8,afade=t=out:st=${kapanisUzunluk - 3}:d=3,adelay=${kapanisGecikme}|${kapanisGecikme}[kapanis]`,
    `[acilis][ses][kapanis]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.95[o]`,
  ].join(';');
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', SARKI, '-i', konusma, '-filter_complex', filtre, '-map', '[o]', '-ar', '44100', '-ac', '2', '-c:a', 'libmp3lame', '-q:a', '2', hedef]);
  const t = sureOku(hedef);
  console.log(`Müzikli MP3: ${path.relative(ROOT, hedef)} (${Math.floor(t / 60)} dk ${Math.round(t % 60)} sn)`);
}

if (process.argv.includes('--sadece-miks')) {
  muzikliSurum(path.join(OUT, 'matro-tanitim-podcast.mp3'), path.join(OUT, 'matro-tanitim-podcast-muzikli.mp3'));
  process.exit(0);
}

const wavlar = [];
for (const s of sequences) {
  const metin = s.dialogues.map((d) => `${d.speaker}: ${d.text}`).join('\n');
  const ad = demo ? 'demo' : ciktiAdi ? `${ciktiAdi}-sekans-${String(s.sequenceId).padStart(2, '0')}` : `sekans-${String(s.sequenceId).padStart(2, '0')}`;
  console.log(`Sekans ${s.sequenceId} (${s.dialogues.length} replik, ${metin.split(/\s+/).length} kelime)...`);
  const pcm = await tts(metin);
  fs.mkdirSync(path.dirname(path.join(OUT, ad)), { recursive: true });
  const pcmYol = path.join(OUT, `${ad}.pcm`);
  const wav = path.join(OUT, `${ad}.wav`);
  fs.writeFileSync(pcmYol, pcm);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', pcmYol, wav]);
  fs.rmSync(pcmYol);
  const sure = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav]).toString());
  console.log(`  -> ${path.relative(ROOT, wav)} (${sure.toFixed(1)} sn)`);
  wavlar.push(wav);
}

// Sekanslar arasına 0,6 sn sessizlik koyup tek MP3'e birleştir.
const hedef = path.join(OUT, demo ? 'matro-tanitim-demo.mp3' : ciktiAdi ? `${ciktiAdi}.mp3` : 'matro-tanitim-podcast.mp3');
const girdiler = wavlar.flatMap((w) => ['-i', w]);
const filtre = wavlar.length > 1
  ? wavlar.map((_, i) => `[${i}:a]apad=pad_dur=0.6[a${i}];`).join('') + wavlar.map((_, i) => `[a${i}]`).join('') + `concat=n=${wavlar.length}:v=0:a=1[o]`
  : '[0:a]anull[o]';
execFileSync('ffmpeg', ['-v', 'error', '-y', ...girdiler, '-filter_complex', filtre, '-map', '[o]', '-ar', '24000', '-ac', '1', '-c:a', 'libmp3lame', '-q:a', '2', hedef]);
const toplam = sureOku(hedef);
console.log(`MP3: ${path.relative(ROOT, hedef)} (${Math.floor(toplam / 60)} dk ${Math.round(toplam % 60)} sn)`);
if (!demo && !ciktiAdi) muzikliSurum(hedef, path.join(OUT, 'matro-tanitim-podcast-muzikli.mp3'));
// Tek sekanslı çıktılarda ara WAV dosyası MP3'e dönüştükten sonra silinir.
if (ciktiAdi) wavlar.forEach((w) => fs.rmSync(w));
