#!/usr/bin/env node
/**
 * MATRO Dergi Sayı 01 — örnek baskı PDF'i.
 *
 * docs/dergi-sayi-01/*.md yazılarını (pandoc ile HTML'e çevirerek) ve sitenin
 * verilerini (takımlar, başarılar, sponsorlar, basın, başvurular) tek bir akışkan
 * HTML belgesinde birleştirir; Chrome'un sayfalı medya desteğiyle (adlandırılmış
 * sayfalar, @page kenar kutularında sayfa numarası) A4 PDF basar.
 *
 * - Yazılardaki "Dizgi notu" ve "Dizgi uyarısı" blokları basılmaz.
 * - "*Görsel: ...*" satırları public/media'daki fotoğraflara dönüştürülür.
 * - Henüz yazılmamış içerik (röportaj cevapları, künye adları, foto-röportaj alt
 *   yazıları) lorem ipsum ile doldurulur: bu bir ÖRNEK baskıdır.
 * - İçindekiler sayfa numaraları iki geçişte bulunur: ilk PDF'in metninde her
 *   yazının görünmez işareti aranır, ikinci geçişte numaralar yazılır.
 * - Toplam sayfa sayısı 4'ün katına, arka kapaktan önce ilan alanı sayfalarıyla tamamlanır.
 *
 * Kullanım: node scripts/build-dergi-sayi-01.mjs
 */
import puppeteer from 'puppeteer-core';
import yaml from 'js-yaml';
import QRCode from 'qrcode';
import { PDFDocument } from 'pdf-lib';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const YAZI = path.join(ROOT, 'docs/dergi-sayi-01');
const OUT = path.join(YAZI, 'ornek-baski');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const oku = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
fs.mkdirSync(OUT, { recursive: true });

const site = oku('src/data/site.json');
const ach = oku('src/data/achievements.json');
const sponsors = oku('src/data/sponsors.json');
const paket = oku('src/data/sponsorship.json');
const basin = oku('src/data/basinda-biz.json');
const join = oku('src/data/join.json');
const about = oku('src/data/about.json');

const esc = (s = '') => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
/** Görsel yolu: HTML dosyası ornek-baski/ içinde. */
function gorselYolu(ad) {
  const adaylar = [
    [`public/media/${ad}.jpg`, `../../../public/media/${ad}.jpg`],
    [`docs/faaliyet-kitapcigi-2025-26/gorseller/${ad}.jpg`, `../../faaliyet-kitapcigi-2025-26/gorseller/${ad}.jpg`],
  ];
  for (const [disk, url] of adaylar) if (fs.existsSync(path.join(ROOT, disk))) return url;
  return null;
}
const img = (ad, alt = '', konum = '') => {
  const u = ad.startsWith('../') ? ad : gorselYolu(ad);
  return u ? `<img src="${esc(u)}" alt="${esc(alt)}"${konum ? ` style="object-position:${konum}"` : ''} />` : '';
};

// ---------- lorem ipsum ----------
const LOREM = [
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
  'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
  'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
  'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
  'Curabitur pretium tincidunt lacus, nulla gravida orci a odio, nullam varius turpis et commodo pharetra.',
  'Integer in mauris eu nibh euismod gravida, duis ac tellus et risus vulputate vehicula donec lobortis risus.',
];
let li = 0;
const lorem = (n = 2) => Array.from({ length: n }, () => LOREM[li++ % LOREM.length]).join(' ');

// ---------- Markdown → HTML ----------
const pandoc = (md) => execFileSync('pandoc', ['-f', 'gfm', '-t', 'html5', '--wrap=none'], { input: md }).toString();

function gorselBlok(metin) {
  if (/Görsel: (yok|QR)/.test(metin)) return '';
  const adlar = [...new Set(metin.match(/[a-z0-9]+(?:-[a-z0-9]+)+/g) || [])].filter((a) => gorselYolu(a));
  if (!adlar.length) return '';
  const genis = /tam sayfa|yarım sayfa/.test(metin) || adlar.length > 1;
  const cls = /tam sayfa/.test(metin) ? 'genis tam' : genis ? 'genis' : '';
  return `\n\n<div class="fotolar ${cls} n${Math.min(adlar.length, 4)}">${adlar
    .slice(0, 4)
    .map((a) => `<figure>${img(a)}</figure>`)
    .join('')}</div>\n\n`;
}

function temizle(md) {
  return md
    .split(/\n{2,}/)
    .map((blok) => {
      const b = blok.trim();
      if (/^> \*\*Dizgi notu/.test(b)) return '';
      if (/^\*Dizgi uyarısı/.test(b)) return '';
      if (/^\*(\()?(Görsel|Fotoğraf)/.test(b)) return gorselBlok(b);
      if (/^> \*\*(İnfografik|Diyagram|Rakam şeridi|Zaman çizelgesi)/.test(b)) {
        const m = b.replace(/^> /gm, '').match(/^\*\*([^*]+?)(:)?\*\*:?\s*([\s\S]*)$/);
        return `\n\n<div class="infografik"><span>${esc((m?.[1] || '').replace(/ —.*/, '').replace(/:$/, ''))}</span><p>${esc(
          (m?.[3] || '').replace(/\n/g, ' '),
        )}</p></div>\n\n`;
      }
      if (/^\*\*Önerilen kişi/.test(b)) return '';
      if (/^> \*\*Tablo/.test(b)) return '';
      const satirlar = [];
      let uyari = false;
      for (const l of blok.split('\n')) {
        if (uyari) { if (/\*\s*$/.test(l)) uyari = false; continue; }
        if (/^\*Dizgi uyarısı/.test(l)) { uyari = !/\*\s*$/.test(l.slice(1)); continue; }
        if (/^\*(\()?(Görsel|Fotoğraf)/.test(l)) { satirlar.push(gorselBlok(l)); continue; }
        if (/^> \*(Dizgi|\[Kaptan kontrolü)/.test(l)) continue;
        satirlar.push(l);
      }
      return satirlar.join('\n').replace(/\[Ad Soyad\]/g, 'Lorem Ipsum').replace(/★ /g, '');
    })
    .filter(Boolean)
    .join('\n\n');
}

function yazi(dosya, { kicker = '', sinif = '', altSayfa = false } = {}) {
  let md = fs.readFileSync(path.join(YAZI, dosya), 'utf8');
  const baslik = md.match(/^# (.+)$/m)[1];
  md = md.replace(/^# .+$/m, '');
  // Oklar (→) yazı tiplerinin alt kümelerinde yok; tipografik › ile değiştirilir.
  let html = pandoc(temizle(md)).replace(/^\s*<hr \/>/, '').replace(/→/g, '›');
  html = html
    .replace(/<blockquote>\s*<p><strong>Kutu — ([^<]+?):?<\/strong>:?/g, '<aside class="kutu"><p><strong class="kutu-b">$1</strong>')
    .replace(/<blockquote>/g, '<aside class="kutu">')
    .replace(/<\/blockquote>/g, '</aside>')
    .replace(/<p><strong>Spot:<\/strong>\s*/g, '<p class="spot">')
    .replace(/<p>(Kaynaklar?:)/g, '<p class="kaynak">$1')
    .replace(/<hr \/>/g, altSayfa ? '<hr class="sayfa" />' : '<hr />');
  return { baslik, html, kicker, sinif };
}

// ---------- içindekiler işaretleri ----------
const toc = [];
let tocNo = 0;
function isaret(baslik, grup = false, gizli = false) {
  const id = `ZQ${String(++tocNo).padStart(2, '0')}QZ`;
  if (!gizli) toc.push({ id, baslik, grup });
  return `<span class="isaret">${id}</span>`;
}

// ---------- parçalar ----------
function makale(dosya, secenek = {}) {
  const y = yazi(dosya, secenek);
  const acilis = secenek.acilis
    ? `<section class="acilis-tam">${img(secenek.acilis, y.baslik, secenek.acilisKonum)}<div class="acilis-yazi">${isaret(y.baslik)}<p class="kicker">${esc(
        y.kicker,
      )}</p><h1>${esc(secenek.acilisBaslik || y.baslik)}</h1>${secenek.acilisSpot ? `<p>${esc(secenek.acilisSpot)}</p>` : ''}</div></section>`
    : '';
  return `${acilis}<article class="makale ${y.sinif}">
    ${acilis ? '' : secenek.basliksiz ? isaret(y.baslik, false, true) : `<header class="m-bas">${isaret(y.baslik)}<p class="kicker">${esc(y.kicker)}</p><h1>${esc(y.baslik)}</h1></header>`}
    <div class="govde">${y.html}</div>
  </article>`;
}

function bolumAcilis(no, ad, foto, alt, konum) {
  return `<section class="bolum-tam ${foto ? '' : 'koyu'}">${foto ? img(foto, ad, konum) : ''}<div class="b-yazi">${isaret(ad, true)}<span class="b-no">${no}</span><h1>${esc(
    ad,
  )}</h1><p>${esc(alt)}</p></div></section>`;
}

// Kapak
const kapak = `<section class="kapak">
  ${img('mavi-vatan-ekipler', 'Mavi Vatan etkinliğinde MATRO takımları', '58% center')}
  <div class="kapak-ust">
    <div class="logolar"><img src="../../../public/logo-matro-beyaz.png" alt="MATRO" /><i></i><img src="../../../public/logo-btu-beyaz.png" alt="Bursa Teknik Üniversitesi" /></div>
    <div class="masthead">MATRO<span>DERGİ</span></div>
    <div class="kapak-serit"><span>Sayı 01</span><span>Ekim 2026</span><span>Bursa Teknik Üniversitesi Öğrenci Dergisi</span><span>Ücretsizdir</span></div>
  </div>
  <div class="kapak-alt">
    <p class="kicker">Kapak dosyası</p>
    <h2>Bir aracın doğuşu: Fikirden final alanına</h2>
    <ul>
      <li><b>TEKNOFEST 2026</b>Diyarbakır'dan Şanlıurfa'ya</li>
      <li><b>Yapay zekâ</b>Stanford raporundan 8 çıkarım</li>
      <li><b>Sezon dosyası</b>2025–2026'da 45 faaliyet</li>
      <li><b>Kendin yap</b>İlk robotun: çizgi izleyen araç</li>
    </ul>
  </div>
</section>`;

// İç kapak: platin sponsorlar
const platin = sponsors.current.filter((s) => s.package === 'Platin');
const icKapak = `<section class="sayfa-tek ic-kapak">
  <p class="kicker">Bu sayı, destekçilerimizle mümkün oldu</p>
  <h2>Platin sponsorlarımız</h2>
  <div class="platin-logolar">${platin.map((s) => `<figure><img src="../../../public${esc(s.logo)}" alt="${esc(s.name)}" /><figcaption>${esc(s.name)}</figcaption></figure>`).join('')}</div>
  <div class="ilan-ornek"><span>İlan alanı (örnek)</span><p>${lorem(2)}</p></div>
</section>`;

// İçindekiler + künye (ikinci geçişte numaralar dolar)
const tocYer = '<!--TOC-->';

// Takımlar
const takimSira = ['ashina', 'tika-ika', 'insansiz-deniz-araci', 'insansiz-su-alti', 'su-alti-roketi', 'suru-iha', 'sanayide-dijital', 'ashina-h', 'cevre-enerji', 'burkut', 'cagri', 'girisimcilik', 'ashina-inovasyon'];
function takimlar() {
  const kart = (dosya) => {
    const s = fs.readFileSync(path.join(ROOT, `src/content/teams/${dosya}.md`), 'utf8');
    const d = yaml.load(s.match(/^---\n([\s\S]*?)\n---/)[1]);
    const foto = (d.image || '').replace(/^\/media\/|\.jpg$/g, '');
    return `<article class="takim">
      <figure>${img(foto, d.title)}${d.badge ? `<span class="rozet">${esc(d.badge)}</span>` : ''}</figure>
      <div><p class="kicker">${esc(d.category)}</p><h3>${esc(d.title)}</h3><p class="alt">${esc(d.subtitle)}</p>
      <p>${esc(d.summary)}</p>
      <ul>${d.achievements.slice(0, 4).map((a) => `<li>${esc(a)}</li>`).join('')}</ul></div>
    </article>`;
  };
  return `<article class="makale"><header class="m-bas">${isaret('Takımlarımız')}<p class="kicker">MATRO</p><h1>Takımlarımız</h1>
    <p class="spot">On üç proje takımı, onlarca alt ekip. Hava, kara, deniz ve su altı araçlarından endüstriyel robotiğe, haberleşmeden enerjiye; hepsi Özdemir Bayraktar TEKNOFEST Atölyesi'nde.</p></header>
    <div class="takimlar">${takimSira.map(kart).join('')}</div></article>`;
}

// 2026 finalleri
function finaller() {
  const f = ach.items.filter((i) => i.year === 2026 && /finalist/i.test(i.degree));
  const yer = { ASHİNA: 'Malatya', 'LUNA İKA': 'Mardin', PUSULA: 'Diyarbakır', MATRİS: 'Gaziantep', LODOS: 'Mavi Vatan · Gölcük', PRUSA: 'Mavi Vatan · Gölcük', ZEMHERİ: 'Mavi Vatan · Gölcük' };
  return `<article class="makale finaller"><header class="m-bas">${isaret('2026 finalleri')}<p class="kicker">Harita</p><h1>2026: sekiz takım finalde</h1></header>
    <div class="final-grid">${f
      .map((i) => `<div><b>${esc(i.team)}</b><span>${esc(i.category)}</span><em>${esc(yer[i.team] || 'Final alanı')}</em></div>`)
      .join('')}</div>
    <div class="fotolar genis n2"><figure>${img('galeri-zemheri-final')}</figure><figure>${img('galeri-matrover-arazi-test')}</figure></div></article>`;
}

// Röportaj (sorular şablondan, cevaplar lorem ipsum)
function roportaj(bolumNo, baslik, foto, kicker) {
  const md = fs.readFileSync(path.join(YAZI, '10-roportaj-sablonlari.md'), 'utf8');
  const blok = md.split(/\n## /).find((b) => b.startsWith(`${bolumNo}.`));
  const sorular = [...blok.matchAll(/^\d+\. (.+)$/gm)].map((m) => m[1]);
  const b = blok.split('\n')[0].replace(/^\d+\. /, '');
  return `<article class="makale roportaj"><header class="m-bas">${isaret(baslik)}<p class="kicker">${esc(kicker)}</p><h1>${esc(b.replace(/^[^:]+: /, '').replace(/"/g, ''))}</h1>
    <p class="spot">${lorem(2)}</p></header>
    <div class="rop-ust"><figure class="portre">${img(foto)}<figcaption>Lorem Ipsum · Örnek görsel</figcaption></figure>
    <p class="cekme">“${LOREM[0]}”</p></div>
    <div class="govde">${sorular.map((s) => `<p class="soru">${esc(s)}</p><p>${lorem(2)}</p>`).join('')}</div></article>`;
}

function yeniUyeler() {
  const md = fs.readFileSync(path.join(YAZI, '10-roportaj-sablonlari.md'), 'utf8');
  const blok = md.split(/\n## /).find((b) => b.startsWith('5.'));
  const sorular = [...blok.matchAll(/^\d+\. (.+)$/gm)].map((m) => m[1]);
  return `<article class="makale"><header class="m-bas">${isaret('İlk dönemim')}<p class="kicker">Röportaj</p><h1>Yeni üyeler: "İlk dönemim"</h1></header>
    <div class="uyeler">${[1, 2, 3, 4]
      .map((i) => `<div class="uye"><span class="avatar">${i}</span><h3>Lorem Ipsum</h3><p class="alt">Makine Mühendisliği, 1. sınıf</p>${sorular
        .map((s) => `<p class="soru">${esc(s)}</p><p>${lorem(1)}</p>`)
        .join('')}</div>`)
      .join('')}</div></article>`;
}

function atolyedeBirGun() {
  const md = fs.readFileSync(path.join(YAZI, '11-atolyede-bir-gun.md'), 'utf8');
  const satirlar = [...md.matchAll(/^\| (\d\d\.\d\d) \| ([^|]+) \| "([^"]+)" \|$/gm)];
  const fotolar = ['galeri-ashina-atolye', 'galeri-pusula-atolye', 'galeri-ashina-kompozit-uretim', 'galeri-zemheri-atolye', 'galeri-iss-atolye-ekip', 'webmedya-sanayide-dijital-24', 'galeri-burkut-calisma', 'galeri-alhazen-laboratuvar', 'galeri-lodos-deniz-test', 'galeri-luna-batarya', 'galeri-iss-auv-havuz', 'galeri-matris-test-alani'];
  return `<article class="makale"><header class="m-bas">${isaret('Atölyede bir gün')}<p class="kicker">Foto-röportaj</p><h1>Atölyede bir gün</h1>
    <p class="spot">Kampüsün en geç kapanan kapısı. Bir sezon içi günü, saat saat. <em>(Örnek görseller; gerçek çekim sonrası değiştirilecek.)</em></p></header>
    <div class="gun">${satirlar
      .map((m, i) => `<figure>${img(fotolar[i % fotolar.length])}<figcaption><b>${m[1]}</b>${esc(m[3].replace(/\[[^\]]+\]/g, 'Lorem').replace(/…/g, 'lorem ipsum'))}</figcaption></figure>`)
      .join('')}</div></article>`;
}

function arsiv() {
  return `<article class="makale arsiv"><header class="m-bas">${isaret('Başarı arşivi')}<p class="kicker">Arşiv</p><h1>${ach.items.length} derece, 13 yıl</h1><p class="spot">${esc(ach.intro)}</p></header>
    <table><thead><tr><th>Yıl</th><th>Yarışma</th><th>Kategori</th><th>Derece</th><th>Takım</th></tr></thead><tbody>${ach.items
      .map((i) => `<tr class="${i.featured ? 'one' : ''}"><td class="m">${i.year}</td><td>${esc(i.competition)}</td><td>${esc(i.category)}</td><td class="d ${/(^|[^0-9])1\.|dünya/i.test(i.degree) ? 'altin' : ''}">${esc(i.degree)}</td><td class="t">${esc(i.team)}</td></tr>`)
      .join('')}</tbody></table></article>`;
}

function basindaBiz() {
  return `<article class="makale"><header class="m-bas">${isaret('Basında biz')}<p class="kicker">Arşiv</p><h1>Basında MATRO</h1><p class="spot">${esc(basin.intro)}</p></header>
    <div class="basin">${basin.items.map((b) => `<article><figure>${img(b.image.replace(/^\/media\/|\.jpg$/g, ''), b.outlet)}</figure><p class="kicker">${esc(b.outlet)} · ${b.date.slice(0, 4)}</p><h3>${esc(b.headline)}</h3></article>`).join('')}</div></article>`;
}

function sponsorDuvari() {
  const PK = ['Platin', 'Altın', 'Gümüş', 'Bronz', 'Gönüllü'];
  return `<article class="makale"><header class="m-bas">${isaret('Sponsorlarımız')}<p class="kicker">Teşekkür</p><h1>${sponsors.current.length} destekçi, tek atölye</h1><p class="spot">${esc(sponsors.intro)}</p></header>
    ${PK.map((k) => {
      const l = sponsors.current.filter((s) => s.package === k);
      return l.length
        ? `<div class="sp-grup ${k.toLocaleLowerCase('tr')}"><p class="kicker">${k} · ${l.length}</p><div class="sp">${l
            .map((s) => (s.logo ? `<figure><img src="../../../public${esc(s.logo)}" alt="${esc(s.name)}" /><figcaption>${esc(s.name)}</figcaption></figure>` : `<figure class="yazi"><span>${esc(s.name)}</span></figure>`))
            .join('')}</div></div>`
        : '';
    }).join('')}</article>`;
}

function sponsorOl(qr) {
  return `<article class="makale"><header class="m-bas">${isaret('Sponsor olun')}<p class="kicker">Sponsorluk</p><h1>Bir sonraki sezonu birlikte kuralım</h1><p class="spot">${esc(paket.hero.description)}</p></header>
    <div class="paketler">${paket.packages.map((p) => `<div class="pk ${p.name.toLocaleLowerCase('tr')}"><p class="kicker">${esc(p.name)}</p><h3>${esc(p.range)}</h3><ul>${p.benefits.map((b) => `<li>${esc(b)}</li>`).join('')}</ul></div>`).join('')}</div>
    <div class="iletisim"><div><p class="kicker">Sponsorluk ekibi</p><h3>${esc(site.contact.emails[0])}</h3><p>${esc(paket.officialForm.description)}</p></div><div class="qr">${qr}<span>btumatro.com/sponsorluk</span></div></div></article>`;
}

function bizeKatil(qrlar) {
  return `<article class="makale"><header class="m-bas">${isaret('Bize katıl')}<p class="kicker">Aramıza katıl</p><h1>Atölyenin kapısı açık</h1><p class="spot">${esc(join.hero.description)}</p></header>
    <div class="basvurular">${join.applications.map((a, i) => `<div><div class="qr">${qrlar[i]}</div><h3>${esc(a.title)}</h3><p>${esc(a.description)}</p></div>`).join('')}</div>
    <ol class="adimlar">${join.steps.map((s, i) => `<li><span>${i + 1}</span><b>${esc(s.title)}</b><p>${esc(s.description)}</p></li>`).join('')}</ol></article>`;
}

const ilanSayfasi = () => `<section class="sayfa-tek ilan"><div><span>İlan alanı</span><h2>Markanız burada</h2><p>Tam sayfa ilan · 210 × 297 mm · 3 mm taşma payı</p><p class="lorem">${lorem(3)}</p></div></section>`;

const arkaKapak = (qr) => `<section class="arka">
  <img class="a-logo" src="../../../public/logo-matro-beyaz.png" alt="MATRO" />
  <p class="a-slogan">Atölyede başlar.<br />Sahada kanıtlanır.</p>
  <div class="a-alt"><div class="qr">${qr}</div><p>${esc(site.university)}<br />${esc(site.fullName)}<br /><b>btumatro.com</b> · @btumatro</p><img class="a-btu" src="../../../public/logo-btu-beyaz.png" alt="BTÜ" /></div>
</section>`;

// ---------- belge ----------
async function belge(tocHtml, ilanSayisi) {
  const qr = (u) => QRCode.toString(u, { type: 'svg', margin: 0, errorCorrectionLevel: 'M', color: { dark: '#0b1012', light: '#ffffff' } });
  const qrSponsor = await qr('https://btumatro.com/sponsorluk');
  const qrSite = await qr('https://btumatro.com');
  const qrJoin = await Promise.all(join.applications.map((a) => qr(a.url)));
  toc.length = 0;
  tocNo = 0;
  li = 0;
  const govde = [
    kapak,
    icKapak,
    tocHtml,
    makale('01-editorden.md', { kicker: 'Editörden', sinif: 'editor' }),
    makale('02-kisa-kisa.md', { kicker: 'Topluluktan', sinif: 'kisa' }),
    bolumAcilis('01', 'Gündem', 'galeri-lodos-teknofest', 'TEKNOFEST 2026, havacılık ve uzay, dünyada robotlar, gezdiğimiz yerlerden haberler', 'center 30%'),
    makale('15-gundem.md', { kicker: 'Gündem', altSayfa: true, basliksiz: true }),
    bolumAcilis('02', 'Yapay Zekâ', null, 'Stanford raporundan 8 çıkarım, ajanlar ve fiziksel yapay zekâ, öğrenci rehberi'),
    makale('16-yapay-zeka.md', { kicker: 'Yapay zekâ', altSayfa: true, basliksiz: true }),
    makale('03-kapak-dosyasi.md', { kicker: 'Kapak dosyası', acilis: 'takim-zemheri', acilisBaslik: 'Bir aracın doğuşu', acilisSpot: 'Fikirden final alanına: bir TEKNOFEST aracının on aylık yolculuğu.' }),
    finaller(),
    bolumAcilis('03', 'MATRO', 'galeri-matrover-arazi-test', 'Sezon dosyası, takımlarımız, röportaj, atölyede bir gün, başarı arşivi'),
    makale('21-sezon-dosyasi.md', { kicker: 'Sezon dosyası', sinif: 'sezon' }),
    takimlar(),
    roportaj(1, 'Röportaj: Takım kaptanı', 'galeri-zemheri-takim', 'Röportaj'),
    atolyedeBirGun(),
    arsiv(),
    bolumAcilis('04', 'Nasıl Çalışır?', 'takim-iss-sualti-araci', 'Su altında yön bulmak, sürü İHA, karıştırmaya karşı haberleşme, PLC'),
    makale('04-nasil-calisir-auv.md', { kicker: 'Nasıl çalışır?' }),
    makale('05-nasil-calisir-suru.md', { kicker: 'Nasıl çalışır?' }),
    makale('06-nasil-calisir-haberlesme.md', { kicker: 'Nasıl çalışır?' }),
    makale('20-plc-otomasyon.md', { kicker: 'Nasıl çalışır?' }),
    bolumAcilis('05', 'Kampüs ve Kariyer', 'galeri-tanisma-toplantisi-amfi', 'TEKNOFEST rehberi, Bursa ekosistemi, uzay, kampüs ve staj, röportajlar'),
    makale('07-teknofest-dosyasi.md', { kicker: 'Dosya' }),
    makale('08-bursa-ekosistemi.md', { kicker: 'Sektör' }),
    makale('09-uzay.md', { kicker: 'Uzay' }),
    makale('17-kampus-rehberi.md', { kicker: 'Kampüs' }),
    makale('12-ilk-yil-rehberi.md', { kicker: 'Rehber' }),
    yeniUyeler(),
    roportaj(2, 'Röportaj: Mezun', 'galeri-ashina-saha', 'Röportaj'),
    bolumAcilis('06', 'Keyif', 'galeri-bahar-piknigi-grup', 'Kendin yap, öneriler, sözlük ve bulmaca'),
    makale('18-evde-robot.md', { kicker: 'Kendin yap' }),
    makale('19-oneriler.md', { kicker: 'Öneriler' }),
    makale('13-sozluk.md', { kicker: 'Sözlük', sinif: 'sozluk' }),
    makale('14-bulmaca.md', { kicker: 'Bulmaca', sinif: 'bulmaca' }),
    basindaBiz(),
    sponsorDuvari(),
    sponsorOl(qrSponsor),
    bizeKatil(qrJoin),
    Array.from({ length: ilanSayisi }, ilanSayfasi).join(''),
    arkaKapak(qrSite),
  ].join('\n');
  return `<!doctype html><html lang="tr"><head><meta charset="utf-8" /><title>MATRO Dergi Sayı 01 (örnek baskı)</title>
<link rel="stylesheet" href="dergi.css" /></head><body>${govde}</body></html>`;
}

function tocSayfasi(numaralar) {
  const satir = (t) => `<li class="${t.grup ? 'grup' : ''}"><span class="p">${numaralar?.[t.id] ? String(numaralar[t.id]).padStart(2, '0') : '00'}</span><span>${esc(t.baslik)}</span></li>`;
  return `<section class="sayfa-tek icindekiler">
  <div class="ic-sol"><p class="kicker">Bu sayıda</p><ol>${toc.map(satir).join('')}</ol></div>
  <div class="kunye"><p class="kicker">Künye</p>
    <dl>
      <dt>Sahibi</dt><dd>Bursa Teknik Üniversitesi Makine Teknolojileri Robot ve Otomasyon Topluluğu (MATRO) adına Lorem Ipsum</dd>
      <dt>Genel yayın yönetmeni</dt><dd>Lorem Ipsum</dd>
      <dt>Editörler</dt><dd>Lorem Ipsum, Dolor Sit</dd>
      <dt>Yazarlar</dt><dd>MATRO Organizasyon ve Sosyal Medya ekipleri</dd>
      <dt>Fotoğraflar</dt><dd>MATRO takımları arşivi</dd>
      <dt>Tasarım</dt><dd>Lorem Ipsum</dd>
      <dt>Baskı</dt><dd>[Matbaa adı ve adresi]</dd>
      <dt>Yayın türü</dt><dd>Yerel süreli, altı ayda bir, ücretsiz</dd>
      <dt>İletişim</dt><dd>${esc(site.contact.emails[0])} · btumatro.com</dd>
      <dt>Adres</dt><dd>${esc(site.contact.address)}</dd>
    </dl>
    <p class="not">Bu bir örnek baskıdır. Lorem ipsum ile doldurulan alanlar (röportaj cevapları, künye adları, foto-röportaj alt yazıları) gerçek içerikle değiştirilecektir. Dergide yer alan yazılar yazarlarına aittir; kaynak gösterilerek alıntı yapılabilir.</p>
  </div>
</section>`;
}

// ---------- iki geçişli basım ----------
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
async function bas(html, pdf) {
  const dosya = path.join(OUT, 'dergi.html');
  fs.writeFileSync(dosya, html);
  const tab = await browser.newPage();
  await tab.goto(pathToFileURL(dosya).href, { waitUntil: 'networkidle0' });
  await tab.evaluate(() => document.fonts.ready);
  const eksik = await tab.evaluate(() => [...document.images].filter((i) => !i.naturalWidth).map((i) => i.getAttribute('src')));
  if (eksik.length) throw new Error('Yüklenemeyen görseller: ' + eksik.join(', '));
  await tab.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
  await tab.close();
  return (await PDFDocument.load(fs.readFileSync(pdf))).getPageCount();
}
function numaralariBul(pdf, sayfa) {
  const n = {};
  for (let p = 1; p <= sayfa; p++) {
    const t = execFileSync('pdftotext', ['-f', String(p), '-l', String(p), pdf, '-']).toString();
    for (const m of t.matchAll(/ZQ\d\dQZ/g)) n[m[0]] ??= p;
  }
  return n;
}

const tmp = path.join(OUT, 'gecis.pdf');
await belge('', 0); // toc listesini doldurmak için
let html = await belge(tocSayfasi(null), 0);
let sayfa = await bas(html, tmp);
const ilan = (4 - (sayfa % 4)) % 4;
html = await belge(tocSayfasi(null), ilan);
sayfa = await bas(html, tmp);
const numaralar = numaralariBul(tmp, sayfa);
html = await belge(tocSayfasi(numaralar), ilan);
const son = path.join(OUT, 'matro-dergi-sayi-01-ornek.pdf');
sayfa = await bas(html, son);
fs.rmSync(tmp);
await browser.close();
const eksikNo = toc.filter((t) => !numaralar[t.id]).map((t) => t.baslik);
if (eksikNo.length) console.warn('İçindekilerde sayfası bulunamayan:', eksikNo);
console.log(`PDF: ${path.relative(ROOT, son)} · ${sayfa} sayfa (${ilan} ilan sayfası eklendi)`);
