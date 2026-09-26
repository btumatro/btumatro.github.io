#!/usr/bin/env node
/**
 * Radyodaki konuşmalı parçalara (podcast bölümleri, radyo araları) müzik yatağı ekler.
 *
 * Yatak: sözsüz lo-fi "The Bursa Shift" (docs/topluluk-sarkisi/ses/07-the-bursa-shift.mp4).
 * Akış: müzik GIRIS sn tam seste açılır, konuşma girerken YATAK seviyesine iner ve
 * konuşma boyunca arkada kısık çalar; konuşma bitince CIKIS sn yükselip kaybolur.
 * Her parça yatağın farklı bir yerinden başlar ki girişler birbirini tekrar etmesin.
 *
 * Karışım şarkılarla aynı ses seviyesine gelsin diye 2 dB yükseltilir.
 * Kaynak konuşmalar değişmez; çıktı public/media/ses/ altındaki radyo dosyalarının
 * üzerine yazılır. Kullanım: node scripts/radyo-miks.mjs
 */
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const YATAK = path.join(ROOT, 'docs/topluluk-sarkisi/ses/07-the-bursa-shift.mp4');
const GIRIS = 2.2; // konuşmadan önce müziğin tam seste çaldığı süre
const TAM = 0.55; // giriş/çıkış müzik seviyesi
const YATAK_SEVIYE = 0.11; // konuşma altındaki müzik seviyesi
const CIKIS = 3.0; // konuşmadan sonra müziğin sürdüğü süre

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
  const konusma = path.join(ROOT, kaynak);
  const k = sure(konusma);
  const toplam = GIRIS + k + CIKIS;
  const bas = Math.max(0, Math.min(ofset, yatakSure - toplam - 1));
  const inis = GIRIS - 0.4; // müzik bu andan itibaren 0.8 sn'de yatak seviyesine iner
  const kalkis = GIRIS + k + 0.2; // konuşma bitince 0.8 sn'de yükselir
  const zarf =
    `if(lt(t,${inis}),${TAM},` +
    `if(lt(t,${inis + 0.8}),${TAM}-(${TAM - YATAK_SEVIYE})*(t-${inis})/0.8,` +
    `if(lt(t,${kalkis}),${YATAK_SEVIYE},` +
    `if(lt(t,${kalkis + 0.8}),${YATAK_SEVIYE}+(${TAM - YATAK_SEVIYE})*(t-${kalkis})/0.8,${TAM}))))`;
  const filtre = [
    `[0:a]atrim=${bas}:${bas + toplam},asetpts=PTS-STARTPTS,aresample=44100,volume='${zarf}':eval=frame,` +
      `afade=t=in:st=0:d=0.6,afade=t=out:st=${toplam - 2.2}:d=2.2[m]`,
    `[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,adelay=${Math.round(GIRIS * 1000)}|${Math.round(GIRIS * 1000)}[s]`,
    `[m][s]amix=inputs=2:duration=first:normalize=0,volume=1.26,alimiter=limit=0.95[o]`,
  ].join(';');
  const cikti = path.join(ROOT, 'public/media/ses', hedef);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', YATAK, '-i', konusma, '-filter_complex', filtre, '-map', '[o]',
    '-ar', '44100', '-ac', '2', '-c:a', 'libmp3lame', '-b:a', '112k', cikti]);
  console.log(`${hedef}: ${k.toFixed(1)} sn konuşma -> ${sure(cikti).toFixed(1)} sn (yatak ${bas} sn'den)`);
}
