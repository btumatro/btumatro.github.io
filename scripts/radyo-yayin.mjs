#!/usr/bin/env node
/**
 * MATRO Radyo yayın blokları (bkz. docs/podcast/RADYO-YAYIN-PLANI.md).
 *
 * Blok türleri:
 *   hikaye     Konuşma (bir ya da birkaç kayıt) hikâye yatağının üstünde; müzikli giriş ve çıkış.
 *   bulten     Konuşma bülten yatağının üstünde.
 *   linkSarki  DJ bağlantısı yatak üstünde; son cümle başlarken şarkı altta girer (talk-up),
 *              cümle bitince tam sese çıkar. Bağlantı ve şarkı tek dosyadır, arada boşluk kalmaz.
 *
 * Her konuşmada replik aralarına NEFES kadar sessizlik eklenir; müzik yatağı konuşma
 * sürerken sidechain ile kısılır. Çıktılar public/media/ses/blok-*.mp3.
 * Kullanım: node scripts/radyo-yayin.mjs
 */
import { execFileSync, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SES = path.join(ROOT, 'docs/topluluk-sarkisi/ses');
const KONUSMA = path.join(ROOT, 'docs/podcast/ses');
const CIKTI = path.join(ROOT, 'public/media/ses');
const GECICI = fs.mkdtempSync(path.join(os.tmpdir(), 'matro-radyo-'));

const YATAK = {
  dj: path.join(SES, '09-dj-yatagi-the-hourly-brief.mp4'),
  hikaye: path.join(SES, '10-hikaye-yatagi-a-measure-of-intent.mp4'),
  bulten: path.join(SES, '11-bulten-yatagi-unfolding-blueprints.mp4'),
  gece: path.join(SES, '12-gece-yatagi-the-midnight-invention.mp4'),
};
const SARKI = (ad) => path.join(SES, `${ad}.mp4`);

const NEFES = 0.4; // replik aralarına eklenen sessizlik (sn)
const BOSLUK_ESIK = 0.25;
const MUZIK = 0.5; // yatağın konuşma yokken seviyesi
// Seviye hedefleri: her kayıt ölçülüp bu değerlere çekilir (bloklar arasında ses zıplamasın).
const HEDEF_KONUSMA = -15; // mono konuşma; stereoya açılınca ~-12 LUFS
const HEDEF_SARKI = -12;
const KISMA_YATAK = 'sidechaincompress=threshold=0.03:ratio=3:attack=80:release=900:makeup=1';
const KISMA_SARKI = 'sidechaincompress=threshold=0.03:ratio=4:attack=60:release=1200:makeup=1';
const MP3 = ['-ar', '44100', '-ac', '2', '-c:a', 'libmp3lame', '-b:a', '128k'];

/** Dosyanın tümleşik ses yüksekliği (LUFS). */
const lufs = (f) => {
  const e = spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', f, '-af', 'ebur128', '-f', 'null', '-'], { encoding: 'utf8' }).stderr;
  const r = [...e.matchAll(/I:\s+(-?[\d.]+) LUFS/g)];
  return Number(r[r.length - 1][1]);
};
const kazanc = (f, hedef) => `volume=${(hedef - lufs(f)).toFixed(2)}dB`;
const sure = (f) => Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());
const sessizlikler = (f) => {
  const e = spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', f, '-af', `silencedetect=noise=-38dB:d=${BOSLUK_ESIK}`, '-f', 'null', '-'], { encoding: 'utf8' }).stderr;
  const bas = [...e.matchAll(/silence_start: ([\d.]+)/g)].map((m) => Number(m[1]));
  const bit = [...e.matchAll(/silence_end: ([\d.]+)/g)].map((m) => Number(m[1]));
  return bas.slice(0, bit.length).map((b, i) => [b, bit[i]]);
};
const ffmpeg = (girdiler, filtre, cikti) =>
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...girdiler.flatMap((g) => ['-i', g]), '-filter_complex', filtre, '-map', '[o]', ...MP3, cikti]);

/** Konuşmayı replik aralarından bölüp NEFES ekler; birden fazla kayıt 1 sn arayla birleşir. */
function hazirla(kayitlar, ad) {
  const parcalar = [];
  kayitlar.forEach((k, ki) => {
    const d = sure(k);
    const kes = sessizlikler(k).map(([a, b]) => (a + b) / 2).filter((t) => t > 0.5 && t < d - 0.5);
    const n = [0, ...kes, d];
    n.slice(0, -1).forEach((a, i) => {
      const son = i === n.length - 2;
      const ek = son ? (ki < kayitlar.length - 1 ? 1.0 : 0) : NEFES;
      parcalar.push({ girdi: ki, a, b: n[i + 1], ek });
    });
  });
  const filtre = parcalar.map((p, i) => `[${p.girdi}:a]atrim=${p.a}:${p.b},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=mono${p.ek ? `,apad=pad_dur=${p.ek}` : ''}[p${i}]`).join(';') +
    `;${parcalar.map((_, i) => `[p${i}]`).join('')}concat=n=${parcalar.length}:v=0:a=1[o]`;
  const ham = path.join(GECICI, `${ad}-ham.wav`);
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...kayitlar.flatMap((k) => ['-i', k]), '-filter_complex', filtre, '-map', '[o]', ham]);
  const cikti = path.join(GECICI, `${ad}.wav`);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', ham, '-af', kazanc(ham, HEDEF_KONUSMA), cikti]);
  return cikti;
}

/** Konuşma yatak üstünde: giriş, kısılan yatak, çıkış. */
function yatakli(konusma, yatak, ofset, cikti, giris = 4, cikis = 5) {
  const k = sure(konusma);
  const toplam = giris + k + cikis;
  const bas = Math.max(0, Math.min(ofset, sure(yatak) - toplam - 1));
  const g = Math.round(giris * 1000);
  ffmpeg([yatak, konusma], [
    `[0:a]atrim=${bas}:${bas + toplam},asetpts=PTS-STARTPTS,aresample=44100,volume=${MUZIK},afade=t=in:st=0:d=0.8,afade=t=out:st=${toplam - 2.5}:d=2.5[m]`,
    `[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,adelay=${g}|${g},apad=whole_dur=${toplam},asplit=2[s][k]`,
    `[m][k]${KISMA_YATAK}[mk]`,
    `[mk][s]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[o]`,
  ].join(';'), cikti);
}

/** DJ bağlantısı yatak üstünde; son cümle şarkının girişi üstünde (talk-up). */
function linkSarki(konusma, yatak, ofset, sarki, cikti, giris = 3) {
  const k = sure(konusma);
  const sesz = sessizlikler(konusma);
  const sonReplik = sesz.length ? sesz[sesz.length - 1][1] : Math.max(0, k - 3);
  const sarkiBas = giris + sonReplik - 0.6;
  const toplam = sarkiBas + sure(sarki);
  const yatakSon = sarkiBas + 2.5;
  const bas = Math.max(0, Math.min(ofset, sure(yatak) - yatakSon - 1));
  const g = Math.round(giris * 1000);
  const sg = Math.round(sarkiBas * 1000);
  ffmpeg([yatak, konusma, sarki], [
    `[0:a]atrim=${bas}:${bas + yatakSon},asetpts=PTS-STARTPTS,aresample=44100,volume=${MUZIK},afade=t=in:st=0:d=0.8,afade=t=out:st=${sarkiBas - 0.3}:d=2.5,apad=whole_dur=${toplam}[m]`,
    `[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,adelay=${g}|${g},apad=whole_dur=${toplam},asplit=3[s][k1][k2]`,
    `[m][k1]${KISMA_YATAK}[mk]`,
    `[2:a]aresample=44100,aformat=channel_layouts=stereo,${kazanc(sarki, HEDEF_SARKI)},adelay=${sg}|${sg},apad=whole_dur=${toplam}[sr]`,
    `[sr][k2]${KISMA_SARKI}[srk]`,
    `[mk][s][srk]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.95[o]`,
  ].join(';'), cikti);
  return { sonReplik: giris + sonReplik, sarkiBas };
}

const kayit = (ad) => path.join(KONUSMA, ad);
const v2 = (ad) => kayit(`radyo-v2/${ad}.mp3`);
const bloklar = [
  ['blok-01-hikaye-1', (h) => yatakli(hazirla([kayit('sekans-01.wav')], 'h1'), YATAK.hikaye, 0, h)],
  ['blok-02-atolyede-baslar', (h) => linkSarki(hazirla([v2('l1-atolyede-baslar')], 'l1'), YATAK.dj, 5, SARKI('01-atolyede-baslar'), h)],
  ['blok-03-gece-yarisi-mesaisi', (h) => linkSarki(hazirla([v2('l2-gece-yarisi-mesaisi')], 'l2'), YATAK.dj, 40, SARKI('04-gece-yarisi-mesaisi'), h)],
  ['blok-04-hikaye-2', (h) => yatakli(hazirla([v2('l3-hikaye-2'), v2('hikaye-2')], 'h2'), YATAK.hikaye, 30, h)],
  ['blok-05-bulten', (h) => yatakli(hazirla([v2('bulten')], 'bt'), YATAK.bulten, 10, h, 3, 4)],
  ['blok-06-atolyeden-goklere', (h) => linkSarki(hazirla([v2('l4-atolyeden-goklere')], 'l4'), YATAK.dj, 70, SARKI('03-atolyeden-goklere'), h)],
  ['blok-07-suru', (h) => linkSarki(hazirla([v2('l5-suru')], 'l5'), YATAK.dj, 100, SARKI('06-suru'), h)],
  ['blok-08-derinden-goklere', (h) => linkSarki(hazirla([v2('l6-derinden-goklere')], 'l6'), YATAK.dj, 20, SARKI('05-derinden-goklere'), h)],
  ['blok-09-atolyede-baslar-2', (h) => linkSarki(hazirla([v2('l7-atolyede-baslar-2')], 'l7'), YATAK.dj, 120, SARKI('02-atolyede-baslar-v2'), h)],
  ['blok-10-the-bursa-shift', (h) => linkSarki(hazirla([v2('l8-the-bursa-shift')], 'l8'), YATAK.gece, 30, SARKI('07-the-bursa-shift'), h)],
  ['blok-11-hikaye-3', (h) => yatakli(hazirla([kayit('sekans-03.wav')], 'h3'), YATAK.hikaye, 45, h)],
];

// İsteğe bağlı: yalnızca adı verilen blokları üret (ör. node scripts/radyo-yayin.mjs bulten).
const secim = process.argv.slice(2);
for (const [ad, uret] of bloklar) {
  if (secim.length && !secim.some((s) => ad.includes(s))) continue;
  const hedef = path.join(CIKTI, `${ad}.mp3`);
  const bilgi = uret(hedef);
  console.log(`${ad}: ${sure(hedef).toFixed(1)} sn${bilgi?.sarkiBas ? `, şarkı ${bilgi.sarkiBas.toFixed(1)}. sn'de giriyor` : ''}`);
}
fs.rmSync(GECICI, { recursive: true, force: true });
