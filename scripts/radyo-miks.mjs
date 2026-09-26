#!/usr/bin/env node
/**
 * Radyodaki konuşmalı parçalara (podcast bölümleri, radyo araları) müzik yatağı ekler.
 *
 * Yatak: sözsüz lo-fi "The Bursa Shift" (docs/topluluk-sarkisi/ses/07-the-bursa-shift.mp4).
 * Akış: müzik GIRIS sn tam seste açılır; konuşma başlayınca otomatik kısma (sidechain)
 * ile iner, replik aralarında hafifçe geri gelir; konuşma bitince CIKIS sn çalıp kaybolur.
 * Replikler arası nefes için her sessizliğe NEFES sn eklenir.
 * Her parça yatağın farklı bir yerinden başlar ki girişler birbirini tekrar etmesin.
 *
 * Karışım şarkılarla aynı ses seviyesine gelsin diye 2 dB yükseltilir.
 * Kaynak konuşmalar değişmez; çıktı public/media/ses/ altındaki radyo dosyalarının
 * üzerine yazılır. Kullanım: node scripts/radyo-miks.mjs
 */
import { execFileSync, spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const YATAK = path.join(ROOT, 'docs/topluluk-sarkisi/ses/07-the-bursa-shift.mp4');
const GIRIS = 4.0; // konuşmadan önce müziğin tam seste çaldığı süre
const CIKIS = 5.0; // konuşmadan sonra müziğin sürdüğü süre
const MUZIK = 0.5; // müziğin konuşma olmadığı andaki seviyesi
const NEFES = 0.4; // replikler arasındaki her boşluğa eklenen süre (sn)
const BOSLUK_ESIK = 0.25; // bu süreden uzun sessizlikler replik arası sayılır
// Otomatik kısma (sidechain): konuşma varken müzik ~14 dB iner (konuşmanın ~17 dB altı), aralarda geri gelir.
const KISMA = 'sidechaincompress=threshold=0.03:ratio=3:attack=80:release=900:makeup=1';

const parcalar = [
  ['docs/podcast/ses/sekans-01.wav', 'podcast-bolum-01.mp3', 0],
  ['docs/podcast/ses/sekans-02.wav', 'podcast-bolum-02.mp3', 30],
  ['docs/podcast/ses/sekans-03.wav', 'podcast-bolum-03.mp3', 55],
  ['docs/podcast/ses/radyo/01-sirada-sarkimiz.mp3', 'ara-01-sirada-sarkimiz.mp3', 12],
  ['docs/podcast/ses/radyo/02-gokyuzundeki-takimlar.mp3', 'ara-02-gokyuzundeki-takimlar.mp3', 70],
  ['docs/podcast/ses/radyo/03-karada-ve-denizde.mp3', 'ara-03-karada-ve-denizde.mp3', 100],
  ['docs/podcast/ses/radyo/05-bunu-biliyor-muydunuz.mp3', 'ara-05-bunu-biliyor-muydunuz.mp3', 40],
  ['docs/podcast/ses/radyo/06-radyo-sozlugu.mp3', 'ara-06-radyo-sozlugu.mp3', 125],
  ['docs/podcast/ses/radyo/07-atolyede-bir-gece.mp3', 'ara-07-atolyede-bir-gece.mp3', 85],
  ['docs/podcast/ses/radyo/08-takim-spotu.mp3', 'ara-08-takim-spotu.mp3', 140],
];

const sure = (f) => Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());
const yatakSure = sure(YATAK);

for (const [kaynak, hedef, ofset] of parcalar) {
  const ham = path.join(ROOT, kaynak);
  // Sessizlik ortalarını bul, konuşmayı oradan bölüp aralara NEFES ekle.
  const stderr = spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', ham, '-af',
    `silencedetect=noise=-38dB:d=${BOSLUK_ESIK}`, '-f', 'null', '-'], { encoding: 'utf8' }).stderr;
  const baslar = [...stderr.matchAll(/silence_start: ([\d.]+)/g)].map((m) => Number(m[1]));
  const bitisler = [...stderr.matchAll(/silence_end: ([\d.]+)/g)].map((m) => Number(m[1]));
  const kesimler = baslar.slice(0, bitisler.length).map((b, i) => (b + bitisler[i]) / 2).filter((t) => t > 0.5 && t < sure(ham) - 0.5);
  const noktalar = [0, ...kesimler, sure(ham)];
  const parcaF = noktalar.slice(0, -1).map((a, i) =>
    `[1:a]atrim=${a}:${noktalar[i + 1]},asetpts=PTS-STARTPTS,aresample=44100${i < noktalar.length - 2 ? `,apad=pad_dur=${NEFES}` : ''}[p${i}]`);
  const birlestir = `${noktalar.slice(0, -1).map((_, i) => `[p${i}]`).join('')}concat=n=${noktalar.length - 1}:v=0:a=1,pan=stereo|c0=c0|c1=c0`;
  const k = sure(ham) + kesimler.length * NEFES;

  const toplam = GIRIS + k + CIKIS;
  const bas = Math.max(0, Math.min(ofset, yatakSure - toplam - 1));
  const filtre = [
    ...parcaF,
    `${birlestir},asplit=2[konus][anahtar]`,
    `[0:a]atrim=${bas}:${bas + toplam},asetpts=PTS-STARTPTS,aresample=44100,volume=${MUZIK},` +
      `afade=t=in:st=0:d=0.8,afade=t=out:st=${toplam - 2.5}:d=2.5[m]`,
    `[konus]adelay=${Math.round(GIRIS * 1000)}|${Math.round(GIRIS * 1000)},apad=whole_dur=${toplam}[s]`,
    `[anahtar]adelay=${Math.round(GIRIS * 1000)}|${Math.round(GIRIS * 1000)},apad=whole_dur=${toplam}[k]`,
    `[m][k]${KISMA}[mk]`,
    `[mk][s]amix=inputs=2:duration=first:normalize=0,volume=1.26,alimiter=limit=0.95[o]`,
  ].join(';');
  const cikti = path.join(ROOT, 'public/media/ses', hedef);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', YATAK, '-i', ham, '-filter_complex', filtre, '-map', '[o]',
    '-ar', '44100', '-ac', '2', '-c:a', 'libmp3lame', '-b:a', '112k', cikti]);
  console.log(`${hedef}: ${sure(ham).toFixed(1)} sn konuşma, ${kesimler.length} nefes -> ${sure(cikti).toFixed(1)} sn (yatak ${bas.toFixed(0)} sn'den)`);
}
