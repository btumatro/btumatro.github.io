#!/usr/bin/env node
/**
 * MATRO 2025–2026 Faaliyet Kitapçığı — A4 dikey, baskıya uygun PDF.
 *
 * Kaynak veri: docs/faaliyet-kitapcigi-2025-26/icerik.json (faaliyet raporundan
 * temizlenmiş metinler; bütçe alanları bilerek yok). Bu betik veriden tek bir HTML
 * üretir (kitapcik.html — tarayıcıda açılıp sayfa sayfa incelenebilir), ardından
 * Puppeteer ile CSS @page ölçüsünü kullanarak PDF basar.
 *
 * Rakamlar (faaliyet sayısı, toplam katılım, aylara göre dağılım, içindekiler sayfa
 * numaraları) elle yazılmaz, veriden hesaplanır.
 *
 * Kullanım:
 *   node scripts/build-faaliyet-kitapcigi.mjs            # HTML + PDF
 *   node scripts/build-faaliyet-kitapcigi.mjs --html     # yalnız HTML
 */
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'docs/faaliyet-kitapcigi-2025-26');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const data = JSON.parse(fs.readFileSync(path.join(DIR, 'icerik.json'), 'utf8'));
const sponsors = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/data/sponsors.json'), 'utf8'));

// ---------- yardımcılar ----------
const esc = (s = '') =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
/** '/media/x.jpg' → public/media; diğerleri kitapçık klasörüne göre. */
const src = (p) => (p.startsWith('/media/') ? `../../public${p}` : p);
const AYLAR = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];
const AY_KISA = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'];
function tarih(t, bitis) {
  const f = (s) => {
    const [y, m, d] = s.split('-');
    if (d) return `${+d} ${AYLAR[+m - 1]} ${y}`;
    if (m) return `${AYLAR[+m - 1]} ${y}`;
    return y;
  };
  if (!bitis) return f(t);
  const [y1, m1] = t.split('-');
  const [y2, m2] = bitis.split('-');
  if (y1 === y2 && m1 === m2) return `${+t.split('-')[2]}–${f(bitis)}`;
  if (y1 === y2) return `${+t.split('-')[2]} ${AYLAR[+m1 - 1]} – ${f(bitis)}`;
  return `${f(t)} – ${f(bitis)}`;
}
const sayi = (n) => n.toLocaleString('tr-TR');

// ---------- veriden türetilen rakamlar ----------
const F = data.faaliyetler;
const B = data.basarilar.filter((b) => b.katilim); // İKA derecesi proje olarak zaten sayılıyor
const P = data.projeler;
const toplamFaaliyet = F.length + B.length + P.length;
const toplamKatilim =
  F.reduce((a, f) => a + (f.katilim || 0), 0) +
  B.reduce((a, b) => a + b.katilim, 0) +
  P.reduce((a, p) => a + p.kisi, 0);
const bolumSay = (id) => F.filter((f) => f.bolum === id).length;
const gezi = F.filter((f) => f.bolum === 'sanayi' && /Gezi|Ziyaret/.test(f.ad));
const okulKatilim = F.filter((f) => f.bolum === 'okullar').reduce((a, f) => a + f.katilim, 0);
const projeKisi = P.reduce((a, p) => a + p.kisi, 0);
const kurumSay = new Set([...data.isbirlikleri, ...F.flatMap((f) => f.isbirligi || [])]).size;

// Aylara göre dağılım: yalnızca ay bilgisi olan kayıtlar (Eyl 2025 – Haz 2026).
const aylar = [];
for (let i = 0; i < 10; i++) {
  const d = new Date(2025, 8 + i, 1);
  aylar.push({ key: `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`, ad: AY_KISA[d.getMonth()] });
}
const tarihli = [...F.filter((f) => f.listede !== false), ...data.basarilar.filter((b) => b.katilim)]
  .filter((x) => /^\d{4}-\d{2}/.test(x.tarih));
for (const a of aylar) a.n = tarihli.filter((x) => x.tarih.startsWith(a.key)).length;
const ayMax = Math.max(...aylar.map((a) => a.n));

// ---------- sayfa parçaları ----------
let sayfaNo = 0;
const icindekiler = [];
const pages = [];
const DONEM = data.donem;

function page(inner, { cls = '', footer = true, bolum = '' } = {}) {
  sayfaNo += 1;
  const n = String(sayfaNo).padStart(2, '0');
  const foot = footer
    ? `<footer class="run"><span>MATRO · Faaliyet Raporu ${DONEM}</span>${bolum ? `<span class="run-b">${esc(bolum)}</span>` : ''}<span class="pn">${n}</span></footer>`
    : '';
  pages.push(`<section class="page ${cls}">${inner}${foot}</section>`);
  return sayfaNo;
}
const bolumBul = (id) => data.bolumler.find((b) => b.id === id);
const meta = (f) =>
  `<div class="meta"><span>${esc(tarih(f.tarih, f.bitis))}</span><span>${esc(f.yer)}</span>${f.katilim ? `<span>${sayi(f.katilim)} katılımcı</span>` : ''}</div>`;
const img = (p, alt = '', cls = '', konum = '') =>
  `<img class="${cls}" src="${esc(src(p))}" alt="${esc(alt)}"${konum ? ` style="object-position:${esc(konum)}"` : ''} />`;

function kart(f, { buyuk = false } = {}) {
  return `<article class="kart ${buyuk ? 'kart-l' : ''}">
    ${f.gorsel ? `<figure>${img(f.gorsel, f.ad)}</figure>` : ''}
    ${meta(f)}
    <h3>${esc(f.ad)}</h3>
    <p>${esc(f.ozet)}</p>
    ${f.isbirligi?.length ? `<p class="ib">İş birliği: ${esc(f.isbirligi.join(', '))}</p>` : ''}
  </article>`;
}

function bolumBaslik(id, { kisa = false } = {}) {
  const b = bolumBul(id);
  return `<header class="bb ${kisa ? 'bb-k' : ''}">
    <div class="bb-no">${b.no}</div>
    <div><p class="eyebrow">Bölüm ${b.no}</p><h2>${esc(b.baslik)}</h2>${kisa ? `<p class="lead">${esc(b.ozet)}</p>` : ''}</div>
  </header>`;
}

function acilis(id, { ekstra = '' } = {}) {
  const b = bolumBul(id);
  const liste = F.filter((f) => f.bolum === id && f.listede !== false);
  const no = page(
    `<figure class="acilis-foto">${img(b.kapak, b.baslik)}</figure>
    <div class="acilis-govde">
      ${bolumBaslik(id)}
      <div class="acilis-kolon">
        <p class="lead">${esc(b.ozet)}</p>
        <ol class="mini">${liste
          .map((f) => `<li><span class="mini-t">${esc(tarih(f.tarih, f.bitis))}</span><span>${esc(f.ad)}</span><span class="mini-k">${f.katilim ? sayi(f.katilim) : ''}</span></li>`)
          .join('')}</ol>
      </div>
      ${ekstra}
    </div>`,
    { cls: 'p-acilis', bolum: b.baslik },
  );
  icindekiler.push({ no: b.no, baslik: b.baslik, sayfa: no });
  return no;
}

// ---------- 1. Kapak ----------
const kapakFotolari = [
  'gorseller/turkish-technic-workshop-2000.jpg',
  '/media/galeri-matris-saha.jpg',
  '/media/galeri-zemheri-sara.jpg',
  '/media/galeri-tugay-ciner-atolye.jpg',
  '/media/galeri-lodos-detay.jpg',
  '/media/galeri-robot-gunleri-stant.jpg',
  '/media/galeri-turkish-technic-hangar.jpg',
];
page(
  `<div class="kapak-mozaik">${kapakFotolari.map((p, i) => `<div class="m m${i + 1}">${img(p)}</div>`).join('')}</div>
  <div class="kapak-alt">
    <div class="kapak-logolar"><img src="../../public/logo-matro-beyaz.png" alt="MATRO" /><span></span><img src="../../public/logo-btu-beyaz.png" alt="Bursa Teknik Üniversitesi" /></div>
    <p class="eyebrow volt">Bursa Teknik Üniversitesi · Makine Teknolojileri Robot ve Otomasyon Topluluğu</p>
    <h1>Faaliyet<br />Raporu</h1>
    <p class="kapak-donem">${DONEM}</p>
    <p class="kapak-sayilar"><b>${toplamFaaliyet}</b> faaliyet <i></i> <b>${sayi(toplamKatilim)}</b> katılım <i></i> <b>${P.length}</b> TEKNOFEST projesi</p>
  </div>`,
  { cls: 'p-kapak dark', footer: false },
);

// ---------- 2. Sunuş + içindekiler (numaralar sonradan doldurulur) ----------
const SUNUS_YER = pages.length;
page('', { cls: 'p-sunus' });

// ---------- 3. Sayılarla sezon ----------
page(
  `<header class="bb bb-k"><div><p class="eyebrow">Sezon özeti</p><h2>Sayılarla ${DONEM}</h2></div></header>
  <div class="stat-grid">
    <div class="stat big"><b>${toplamFaaliyet}</b><span>faaliyet</span><em>eğitim, gezi, stant, okul programı, yarışma ve sosyal etkinlik</em></div>
    <div class="stat big"><b>${sayi(toplamKatilim)}</b><span>toplam katılım</span><em>faaliyet başına bildirilen katılımcı sayılarının toplamı</em></div>
    <div class="stat"><b>${P.length}</b><span>TEKNOFEST projesi</span><em>${projeKisi} öğrenci görev aldı</em></div>
    <div class="stat"><b>${gezi.length}</b><span>teknik gezi</span><em>havacılık, savunma, Ar-Ge ve sanayi</em></div>
    <div class="stat"><b>${sayi(okulKatilim)}</b><span>okul öğrencisine ulaştık</span><em>${bolumSay('okullar')} okul programı</em></div>
    <div class="stat"><b>${kurumSay}+</b><span>kurumla iş birliği</span><em>sanayi, kamu, okul ve sivil toplum</em></div>
  </div>
  <div class="grafik">
    <p class="eyebrow">Aylara göre faaliyet sayısı</p>
    <div class="bars">${aylar
      .map((a) => `<div class="bar"><span class="bar-n">${a.n || ''}</span><i style="height:${a.n ? (a.n / ayMax) * 100 : 0}%"></i><span class="bar-a">${a.ad}</span></div>`)
      .join('')}</div>
    <p class="not">Tarihi ay düzeyinde bilinen faaliyetler; sürekli yürüyen TEKNOFEST proje çalışmaları dahil değildir.</p>
  </div>
  <div class="derece-serit">
    <p class="eyebrow">Sezonun dereceleri</p>
    <ul>${data.basarilar
      .filter((b) => b.derece)
      .map((b) => `<li><b>${esc(b.derece)}</b><span>${esc(b.baslik)}</span></li>`)
      .join('')}</ul>
  </div>`,
  { cls: 'p-sayilar', bolum: 'Sezon özeti' },
);

// ---------- 01 Topluluk ve Eğitim ----------
acilis('topluluk');
page(
  `${bolumBaslik('topluluk', { kisa: false })}
  <div class="grid-2x2">${F.filter((f) => f.bolum === 'topluluk').slice(1).map((f) => kart(f)).join('')}</div>`,
  { cls: 'p-grid', bolum: 'Topluluk ve Eğitim' },
);

// ---------- 02 Sanayi ile Buluşma ----------
const tt = F.find((f) => f.ad === 'Turkish Technic Teknik Gezisi');
acilis('sanayi', {
  ekstra: `<div class="one-cikan"><p class="eyebrow volt">Öne çıkan</p><h3>${esc(tt.ad)}</h3>${meta(tt)}<p>${esc(tt.ozet)}</p></div>`,
});
const ws = F.find((f) => f.ad === 'Turkish Technic Workshop');
page(
  `<figure class="tam-foto">${img(ws.gorsel, ws.ad)}</figure>
  <div class="ozellik">
    <div><p class="eyebrow">Kampüste sanayi</p><h2>${esc(ws.ad)}</h2>${meta(ws)}</div>
    <div><p class="lead">${esc(ws.ozet)}</p><p class="ib">İş birliği: ${esc(ws.isbirligi.join(', '))}</p></div>
  </div>`,
  { cls: 'p-ozellik', bolum: 'Sanayi ile Buluşma' },
);
page(
  `${bolumBaslik('sanayi')}
  <div class="grid-3x2">${gezi.filter((f) => f !== tt).map((f) => kart(f)).join('')}</div>`,
  { cls: 'p-grid', bolum: 'Sanayi ile Buluşma' },
);

// ---------- 03 Fuarlar ve Stantlar ----------
{
  const no = page(
    `${bolumBaslik('stant', { kisa: true })}
    <div class="grid-2x2">${F.filter((f) => f.bolum === 'stant').map((f) => kart(f)).join('')}</div>`,
    { cls: 'p-grid', bolum: 'Fuarlar ve Stantlar' },
  );
  icindekiler.push({ no: '03', baslik: 'Fuarlar ve Stantlar', sayfa: no });
}

// ---------- 04 Yeni Nesil Mühendisler ----------
const armutlu = F.find((f) => f.one && f.bolum === 'okullar');
acilis('okullar', {
  ekstra: `<div class="one-cikan sayi-kutu"><b>${armutlu.katilim}</b><div><p class="eyebrow volt">Sezonun en kalabalık buluşması</p><h3>${esc(armutlu.ad)}</h3><p>${esc(armutlu.yer)} · ${esc(tarih(armutlu.tarih))}</p></div></div>`,
});
page(
  `${bolumBaslik('okullar')}
  <div class="grid-2x2">${F.filter((f) => f.bolum === 'okullar' && f.gorsel && f.ad !== 'Tugay Ciner İlköğretim Okulu Atölye Ziyareti').map((f) => kart(f)).join('')}</div>`,
  { cls: 'p-grid', bolum: 'Yeni Nesil Mühendisler' },
);

// ---------- 05 Deneyim ve Başarılar ----------
{
  const ana = data.basarilar[0];
  const no = page(
    `${bolumBaslik('basari', { kisa: true })}
    <div class="basari-ust">
      <figure>${img(ana.gorsel, ana.baslik)}</figure>
      <div class="basari-ana"><span class="madalya">${esc(ana.derece)}</span><p class="eyebrow">${esc(ana.kurum)} · ${esc(tarih(ana.tarih))}</p><h3>${esc(ana.baslik)}</h3><p>${esc(ana.ozet)}</p></div>
    </div>
    <ul class="basari-liste">${data.basarilar
      .slice(1)
      .map(
        (b) => `<li><span class="madalya ${b.derece ? '' : 'bos'}">${esc(b.derece || 'Katılım')}</span><div><h4>${esc(b.baslik)}</h4><p class="eyebrow">${esc(b.kurum)} · ${esc(tarih(b.tarih))}</p><p>${esc(b.ozet)}</p></div></li>`,
      )
      .join('')}</ul>`,
    { cls: 'p-basari', bolum: 'Deneyim ve Başarılar' },
  );
  icindekiler.push({ no: '05', baslik: 'Deneyim ve Başarılar', sayfa: no });
}
{
  const bes = data.basarilar.find((b) => b.baslik.includes('5 Dakikada'));
  const deneyim = F.filter((f) => f.bolum === 'basari' && f.listede !== false);
  const hack = data.basarilar.filter((b) => /Hackathon/.test(b.baslik));
  page(
    `<header class="bb bb-k"><div><p class="eyebrow">Bölüm 05</p><h2>Tecrübeyi paylaşmak</h2></div></header>
    <figure class="genis-foto">${img(bes.gorsel, bes.baslik)}<figcaption>${esc(bes.baslik)} · ${esc(bes.kurum)} · ${esc(tarih(bes.tarih))}</figcaption></figure>
    <div class="grid-2">
      ${deneyim.map((f) => `<article class="kart kart-yatay ${f.gorsel ? '' : 'tek'}">${f.gorsel ? `<figure>${img(f.gorsel, f.ad)}</figure>` : ''}<div>${meta(f)}<h3>${esc(f.ad)}</h3><p>${esc(f.ozet)}</p></div></article>`).join('')}
    </div>
    <div class="hack">${hack.map((h) => `<figure>${img(h.gorsel, h.baslik)}<figcaption><b>${esc(h.baslik)}</b> · ${esc(h.kurum)}</figcaption></figure>`).join('')}</div>`,
    { cls: 'p-deneyim', bolum: 'Deneyim ve Başarılar' },
  );
}

// ---------- 06 TEKNOFEST Projeleri ----------
{
  const no = page(
    `${bolumBaslik('teknofest', { kisa: true })}
    <div class="proje-ozet">
      <div class="stat big"><b>${P.length}</b><span>yarışma projesi</span></div>
      <div class="stat big"><b>${projeKisi}</b><span>öğrenci görev aldı</span></div>
      <div class="stat big"><b>1</b><span>Türkiye derecesi</span><em>MATROVER · İKA 3.lüğü</em></div>
    </div>
    <table class="proje-tablo">
      <thead><tr><th>Takım</th><th>Kategori</th><th class="r">Ekip</th></tr></thead>
      <tbody>${P.map((p) => `<tr><td><b>${esc(p.takim)}</b></td><td>${esc(p.kategori)}</td><td class="r">${p.kisi}</td></tr>`).join('')}</tbody>
    </table>
    <p class="not">Takım çalışmaları BTÜ Özdemir Bayraktar TEKNOFEST Atölyesi'nde yürütülür. İş birliği yapılan kurumlar arasında TEKNOFEST, TUSAŞ, ASELSAN, TENMAK, Luna Robotics ve Crowtec yer alır.</p>`,
    { cls: 'p-tf', bolum: 'TEKNOFEST Projeleri' },
  );
  icindekiler.push({ no: '06', baslik: 'TEKNOFEST Projeleri', sayfa: no });
}
function proje(p) {
  const foto = p.gorsel
    ? `<figure>${img(p.gorsel, p.takim, '', p.gorselKonum)}${p.gorselNotu ? `<figcaption>${esc(p.gorselNotu)}</figcaption>` : ''}</figure>`
    : `<figure class="tipo"><span>${esc(p.takim)}</span><em>${esc(p.kategori)}</em></figure>`;
  return `<article class="proje ${p.vurgu ? 'vurgu' : ''}">
    ${foto}
    <div class="proje-metin">
      <p class="eyebrow">TEKNOFEST · ${esc(p.kategori)}</p>
      <h3>${esc(p.takim)}</h3>
      <p>${esc(p.ozet)}</p>
      <ul class="etiket">${p.etiket.map((e) => `<li>${esc(e)}</li>`).join('')}</ul>
      <p class="ekip"><b>${p.kisi}</b> kişilik ekip</p>
    </div>
  </article>`;
}
for (let i = 0; i < P.length; i += 2) {
  page(`<div class="proje-sayfa">${proje(P[i])}${P[i + 1] ? proje(P[i + 1]) : ''}</div>`, {
    cls: 'p-proje',
    bolum: 'TEKNOFEST Projeleri',
  });
}

// ---------- 07 Takım Ruhu ----------
{
  const s = F.filter((f) => f.bolum === 'sosyal');
  const no = page(
    `${bolumBaslik('sosyal', { kisa: true })}
    <div class="sosyal">
      <article class="kart kart-l">${`<figure>${img(s[0].gorsel, s[0].ad)}</figure>`}${meta(s[0])}<h3>${esc(s[0].ad)}</h3><p>${esc(s[0].ozet)}</p></article>
      <div class="grid-2">${s.slice(1).map((f) => kart(f)).join('')}</div>
    </div>`,
    { cls: 'p-sosyal', bolum: 'Takım Ruhu' },
  );
  icindekiler.push({ no: '07', baslik: 'Takım Ruhu', sayfa: no });
}

// ---------- Sezon takvimi ----------
{
  const t = tarihli
    .map((x) => ({ ad: x.ad || x.baslik, tarih: x.tarih, bitis: x.bitis, yer: x.yer || x.kurum }))
    .sort((a, b) => a.tarih.localeCompare(b.tarih));
  const no = page(
    `<header class="bb bb-k"><div><p class="eyebrow">Kronoloji</p><h2>Sezon takvimi</h2></div></header>
    <ol class="takvim">${t
      .map((x) => `<li><span class="tk-t">${esc(tarih(x.tarih, x.bitis))}</span><span class="tk-a">${esc(x.ad)}</span><span class="tk-y">${esc(x.yer)}</span></li>`)
      .join('')}</ol>`,
    { cls: 'p-takvim', bolum: 'Sezon takvimi' },
  );
  icindekiler.push({ no: '', baslik: 'Sezon takvimi', sayfa: no });
}

// ---------- İş birlikleri ve destekçiler ----------
{
  const pk = ['Platin', 'Altın', 'Gümüş', 'Bronz'];
  const sira = (s) => (pk.includes(s.package) ? pk.indexOf(s.package) : pk.length);
  const logolar = sponsors.current
    .filter((s) => s.logo)
    .sort((a, b) => sira(a) - sira(b));
  const no = page(
    `<header class="bb bb-k"><div><p class="eyebrow">Teşekkür</p><h2>Birlikte ürettiklerimiz</h2><p class="lead">Bu sezon kapılarını açan kurumlara, atölyemize destek olan sponsorlarımıza ve bizi ağırlayan okullara teşekkür ederiz.</p></div></header>
    <p class="eyebrow">İş birliği yapılan kurumlar</p>
    <ul class="kurumlar">${data.isbirlikleri.map((k) => `<li>${esc(k)}</li>`).join('')}</ul>
    <p class="eyebrow">${esc('2025–2026 sponsorlarımız')}</p>
    <div class="logolar">${logolar
      .map((s) => `<figure><img src="../../public${esc(s.logo)}" alt="${esc(s.name)}" /><figcaption>${esc(s.package)}</figcaption></figure>`)
      .join('')}</div>`,
    { cls: 'p-destek', bolum: 'Teşekkür' },
  );
  icindekiler.push({ no: '', baslik: 'İş birlikleri ve sponsorlar', sayfa: no });
}

// ---------- Arka kapak ----------
page(
  `<div class="arka">
    <img class="arka-logo" src="../../public/logo-matro-beyaz.png" alt="MATRO" />
    <p class="arka-slogan">Atölyede başlayan fikirleri sahaya taşıyoruz.</p>
    <div class="arka-alt">
      <div class="qr"><img src="gorseller/qr-btumatro.svg" alt="btumatro.com" /></div>
      <dl>
        <dt>Web</dt><dd>btumatro.com</dd>
        <dt>E-posta</dt><dd>matroiletisim@gmail.com</dd>
        <dt>Atölye</dt><dd>BTÜ Özdemir Bayraktar TEKNOFEST Atölyesi</dd>
        <dt>Adres</dt><dd>Mimar Sinan Yerleşkesi, Yıldırım / Bursa</dd>
      </dl>
    </div>
    <p class="arka-not">Bursa Teknik Üniversitesi Makine Teknolojileri Robot ve Otomasyon Topluluğu · ${DONEM} Faaliyet Raporu</p>
  </div>`,
  { cls: 'p-arka dark', footer: false },
);

// ---------- Sunuş sayfasını içindekilerle doldur ----------
pages[SUNUS_YER] = `<section class="page p-sunus">
  <div class="sunus">
    <div>
      <p class="eyebrow">Sunuş</p>
      <h2>Bir sezon, ${toplamFaaliyet} faaliyet</h2>
      <p class="lead">MATRO; Bursa Teknik Üniversitesi'nde insansız hava, kara, deniz ve su altı sistemleri, robotik, haberleşme ve enerji teknolojileri alanlarında proje geliştiren öğrenci topluluğudur.</p>
      <p>${DONEM} döneminde yeni üyelerimizi eğitim kamplarıyla atölyeye hazırladık, sanayinin önde gelen kuruluşlarına teknik geziler düzenledik, fuar ve festivallerde stant açtık, ilkokuldan liseye yüzlerce öğrenciyle buluştuk ve ${P.length} farklı TEKNOFEST kategorisinde proje yürüttük.</p>
      <p>Bu kitapçık, topluluğumuzun üniversiteye sunduğu faaliyet raporundan derlenmiştir. Her sayfadaki tarih, yer ve katılımcı bilgisi o rapordaki kayda dayanır.</p>
    </div>
    <nav class="toc">
      <p class="eyebrow">İçindekiler</p>
      <ol>
        <li><span class="toc-no"></span><span>Sayılarla ${DONEM}</span><span class="toc-p">03</span></li>
        ${icindekiler
          .sort((a, b) => a.sayfa - b.sayfa)
          .map((i) => `<li><span class="toc-no">${i.no}</span><span>${esc(i.baslik)}</span><span class="toc-p">${String(i.sayfa).padStart(2, '0')}</span></li>`)
          .join('')}
      </ol>
    </nav>
  </div>
  <figure class="sunus-foto">${img('/media/galeri-tanisma-kahvaltisi-salon.jpg', 'Tanışma kahvaltısı')}</figure>
  <footer class="run"><span>MATRO · Faaliyet Raporu ${DONEM}</span><span class="run-b">Sunuş</span><span class="pn">02</span></footer>
</section>`;

// ---------- HTML ----------
const html = `<!doctype html>
<html lang="tr"><head><meta charset="utf-8" />
<title>MATRO Faaliyet Raporu ${DONEM}</title>
<link rel="stylesheet" href="kitapcik.css" />
</head><body>
${pages.join('\n')}
</body></html>`;
fs.writeFileSync(path.join(DIR, 'kitapcik.html'), html);
console.log(`HTML yazıldı: ${pages.length} sayfa, ${toplamFaaliyet} faaliyet, ${toplamKatilim} katılım`);
if (pages.length % 4) console.warn(`Uyarı: sayfa sayısı (${pages.length}) 4'ün katı değil — tel dikiş için boş sayfa gerekir.`);

if (process.argv.includes('--html')) process.exit(0);

// ---------- PDF ----------
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
const tab = await browser.newPage();
await tab.goto(pathToFileURL(path.join(DIR, 'kitapcik.html')).href, { waitUntil: 'networkidle0' });
await tab.evaluate(async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map((i) => (i.complete ? null : new Promise((r) => (i.onload = i.onerror = r)))));
});
const eksik = await tab.evaluate(() => [...document.images].filter((i) => !i.naturalWidth).map((i) => i.getAttribute('src')));
if (eksik.length) {
  console.error('Yüklenemeyen görseller:', eksik);
  process.exit(1);
}
const out = path.join(DIR, `matro-faaliyet-raporu-2025-2026.pdf`);
await tab.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
await browser.close();
console.log('PDF:', path.relative(ROOT, out));
