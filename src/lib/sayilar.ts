/**
 * Sitedeki sayıların tek kaynağı.
 *
 * Elle girilen sayılar `src/data/sayilar.json` dosyasındadır (panelde "Sayılar").
 * Değeri boş olan anahtarlar `achievements.json`'dan hesaplanır; böylece bir derece
 * eklendiğinde ana sayfa, Başarılar sayfası ve metinler birlikte güncellenir.
 * Metinlerde `{anahtar}` yazan yerler `sayiMetni()` ile doldurulur.
 */
import veri from '../data/sayilar.json';
import achievements from '../data/achievements.json';
import { achievementSummary, degreeRank } from './utils';

export interface Sayi {
  anahtar: string;
  deger: number;
  ek: string;
  etiket: string;
  not: string;
}

const ozet = achievementSummary(achievements.items);
const hesaplanan: Record<string, number> = {
  kayitliDerece: ozet.records,
  birincilik: ozet.firstPlaces,
  uluslararasi: ozet.international,
  teknofestFinalist2026: ozet.finalists2026,
  ozelOdul: achievements.items.filter((a) => {
    const r = degreeRank(a.degree);
    return r === 90 || (r < 80 && /ödül/i.test(a.degree));
  }).length,
};

type Kayit = { anahtar: string; deger?: number; ek?: string; etiket?: string; not?: string; yuvarla?: boolean };

export const SAYILAR: Record<string, Sayi> = Object.fromEntries(
  (veri.sayilar as Kayit[]).map((s) => {
    let deger = typeof s.deger === 'number' ? s.deger : (hesaplanan[s.anahtar] ?? 0);
    // "+" ile gösterilen hesaplanmış sayılar 5'in katına aşağı yuvarlanır (51 → 50+).
    if (s.yuvarla && deger >= 10) deger = Math.floor(deger / 5) * 5;
    return [s.anahtar, { anahtar: s.anahtar, deger, ek: s.ek ?? '', etiket: s.etiket ?? '', not: s.not ?? '' }];
  }),
);

/** "50+" gibi gösterim metni. */
export function sayiYaz(anahtar: string): string {
  const s = SAYILAR[anahtar];
  return s ? `${s.deger.toLocaleString('tr-TR')}${s.ek}` : `{${anahtar}}`;
}

/** Metindeki {anahtar} yer tutucularını sayılarla doldurur. */
export function sayiMetni(metin?: string | null): string {
  return (metin ?? '').replace(/\{([a-zA-Z0-9]+)\}/g, (tam, k) => (SAYILAR[k] ? sayiYaz(k) : tam));
}

/** StatGrid için anahtar listesinden sayaç verisi. */
export function sayaclar(anahtarlar: string[]) {
  return anahtarlar
    .filter((k) => SAYILAR[k])
    .map((k) => ({ value: SAYILAR[k].deger, suffix: SAYILAR[k].ek, label: SAYILAR[k].etiket, note: SAYILAR[k].not }));
}
