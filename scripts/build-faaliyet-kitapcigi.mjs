#!/usr/bin/env node
/**
 * MATRO 2025–2026 Faaliyet Raporu — A4 dikey, kitap düzeninde baskıya uygun PDF.
 *
 * Kaynaklar:
 *   docs/faaliyet-kitapcigi-2025-26/icerik.json   faaliyet künyeleri (rapordan)
 *   docs/faaliyet-kitapcigi-2025-26/metinler.json kart gövde metinleri
 *   src/data/*.json, src/content/teams/*.md         topluluk bilgileri, takımlar, başarılar
 *
 * Her faaliyet numaralı bir karttadır (numara, ad, fotoğraf, açıklama, künye: tarih,
 * yer, katılımcı, bütçe, araç gereç, iş birliği). Rakamlar (faaliyet, katılım, bütçe,
 * derece sayıları, içindekiler sayfa numaraları) veriden hesaplanır.
 *
 * Sayfa düzeni kitap gibidir: tek numaralı sayfalar sağda, çiftler solda; cilt payı ve
 * sayfa numarası buna göre yer değiştirir. Kart metni taşarsa fotoğraf yüksekliği
 * otomatik küçültülür; hâlâ taşan kart varsa betik uyarır.
 *
 * Kullanım:
 *   node scripts/build-faaliyet-kitapcigi.mjs            # HTML + PDF
 *   node scripts/build-faaliyet-kitapcigi.mjs --html     # yalnız HTML
 */
import puppeteer from 'puppeteer-core';
import yaml from 'js-yaml';
import sharp from 'sharp';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'docs/faaliyet-kitapcigi-2025-26');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const oku = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
const data = oku('docs/faaliyet-kitapcigi-2025-26/icerik.json');
const metinler = oku('docs/faaliyet-kitapcigi-2025-26/metinler.json');
const sponsors = oku('src/data/sponsors.json');
const site = oku('src/data/site.json');
const about = oku('src/data/about.json');
const ach = oku('src/data/achievements.json');
const ekip = oku('src/data/ekibimiz.json');
const basin = oku('src/data/basinda-biz.json');

// ---------- yardımcılar ----------
const esc = (s = '') => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const src = (p) => (p.startsWith('/media/') ? `../../public${p}` : p);
const img = (p, alt = '', konum = '') => `<img src="${esc(src(p))}" alt="${esc(alt)}"${konum ? ` style="object-position:${esc(konum)}"` : ''} />`;
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
const tl = (s) => (s ? Number(String(s).replace(/[^\d]/g, '')) : 0);
const para = (n) => `${sayi(n)} TL`;
function mdDosya(p) {
  const s = fs.readFileSync(path.join(ROOT, p), 'utf8');
  return yaml.load(s.match(/^---\n([\s\S]*?)\n---/)[1]);
}

// ---------- numaralı faaliyet listesi ----------
const F = data.faaliyetler;
const P = data.projeler;
const DONEM = data.donem;
const BOLUM_SIRA = ['topluluk', 'sanayi', 'stant', 'okullar', 'basari', 'teknofest', 'sosyal'];
const bolumBul = (id) => data.bolumler.find((b) => b.id === id);
const tarihSira = (t) => (t || '9999').padEnd(10, '-');
const kayitlar = [];
for (const bolum of BOLUM_SIRA) {
  let grup;
  if (bolum === 'teknofest') {
    grup = P.map((p) => ({
      bolum, anahtar: p.takim, ad: p.takim, altBaslik: `TEKNOFEST ${p.kategori}`, gorsel: p.gorsel, gorselNotu: p.gorselNotu, gorselKonum: p.gorselKonum,
      ozet: p.ozet, tarih: p.tarih, yer: p.yer, katilim: p.kisi, butce: p.butce, arac: p.arac, isbirligi: p.isbirligi,
      derece: p.vurgu ? 'Türkiye 3.sü' : '',
    }));
  } else {
    grup = F.filter((f) => f.bolum === bolum).map((f) => ({ ...f, anahtar: f.ad }));
    if (bolum === 'basari')
      grup.push(
        ...data.basarilar
          .filter((b) => b.katilim)
          .map((b) => ({ bolum, anahtar: b.baslik, ad: b.baslik, gorsel: b.gorsel, ozet: b.ozet, tarih: b.tarih, yer: b.kurum, katilim: b.katilim, butce: b.butce, arac: b.arac, isbirligi: b.isbirligi, derece: b.derece })),
      );
    grup.sort((a, b) => tarihSira(a.tarih).localeCompare(tarihSira(b.tarih)));
  }
  kayitlar.push(...grup);
}
kayitlar.forEach((k, i) => {
  k.no = String(i + 1).padStart(2, '0');
  k.metin = metinler[k.anahtar] || '';
});
// Fotoğraf oranına göre kart düzeni: yatay fotoğraflar kartın üstünde geniş, dikey ve
// kareye yakın olanlar solda dikey sütunda durur; böylece kişiler ve araçlar kırpılmaz.
const diskYolu = (p) => (p.startsWith('/media/') ? path.join(ROOT, 'public', p) : path.join(DIR, p));
for (const k of kayitlar) {
  if (!k.gorsel) continue;
  const m = await sharp(diskYolu(k.gorsel)).metadata();
  k.oran = m.width / m.height;
}
const eksik = kayitlar.filter((k) => !k.gorsel || !k.metin).map((k) => `${k.ad}${k.gorsel ? '' : ' (fotoğraf)'}${k.metin ? '' : ' (metin)'}`);
if (eksik.length) throw new Error('Eksik içerik: ' + eksik.join(', '));

// ---------- rakamlar ----------
const toplamFaaliyet = kayitlar.length;
const toplamKatilim = kayitlar.reduce((a, k) => a + (k.katilim || 0), 0);
const toplamButce = kayitlar.reduce((a, k) => a + tl(k.butce), 0);
const butceliSay = kayitlar.filter((k) => tl(k.butce)).length;
const bolumListe = (id) => kayitlar.filter((k) => k.bolum === id);
const gezi = F.filter((f) => f.bolum === 'sanayi' && /Gezi|Ziyaret/.test(f.ad));
const okulKatilim = F.filter((f) => f.bolum === 'okullar').reduce((a, f) => a + f.katilim, 0);
const projeKisi = P.reduce((a, p) => a + p.kisi, 0);
const kurumSay = new Set([...data.isbirlikleri, ...kayitlar.flatMap((k) => k.isbirligi || [])]).size;
const A = ach.items;
const dereceSay = A.length;
const birincilik = A.filter((i) => /(^|[^0-9])1\./.test(i.degree)).length;
const final2026 = A.filter((i) => i.year === 2026 && /finalist/i.test(i.degree));
const takimDosyalari = fs.readdirSync(path.join(ROOT, 'src/content/teams')).filter((f) => f.endsWith('.md'));
const aylar = [];
for (let i = 0; i < 10; i++) {
  const d = new Date(2025, 8 + i, 1);
  aylar.push({ key: `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`, ad: AY_KISA[d.getMonth()] });
}
const tarihli = kayitlar.filter((k) => /^\d{4}-\d{2}/.test(k.tarih || '') && k.bolum !== 'teknofest');
for (const a of aylar) a.n = tarihli.filter((x) => x.tarih.startsWith(a.key)).length;
const ayMax = Math.max(...aylar.map((a) => a.n));

// ---------- sayfa altyapısı ----------
const pages = [];
const toc = [];
/**
 * Sayfa ekler. tam: kenar boşluksuz tam sayfa (kapaklar, bölüm açılışları).
 * Tek numaralı sayfalar sağ sayfadır: cilt payı solda, numara sağda.
 */
function page(inner, { cls = '', bolum = '', tam = false, footer = true } = {}) {
  const no = pages.length + 1;
  const taraf = no % 2 ? 'sag' : 'sol';
  const ust = !tam && bolum ? `<div class="ust"><span>${esc(bolum)}</span><span>MATRO · Faaliyet Raporu ${DONEM}</span></div>` : '';
  const alt = footer ? `<div class="alt"><span class="pn">${String(no).padStart(2, '0')}</span></div>` : '';
  pages.push(`<section class="page ${taraf} ${tam ? 'tam' : ''} ${cls}">${ust}<div class="icerik">${inner}</div>${alt}</section>`);
  return no;
}
const eyebrow = (t, cls = '') => `<p class="eyebrow ${cls}">${esc(t)}</p>`;
const baslik = (kicker, h, lead = '') => `<header class="sb">${kicker ? eyebrow(kicker) : ''}<h2>${h}</h2>${lead ? `<p class="lead">${esc(lead)}</p>` : ''}</header>`;

// ---------- 1. Kapak ----------
page(
  `<figure class="kapak-foto">${img('gorseller/turkish-technic-workshop-2000.jpg', 'Turkish Technic Workshop katılımcıları', 'center 40%')}</figure>
  <div class="kapak-ust">
    <div class="logolar"><img src="../../public/logo-matro-beyaz.png" alt="MATRO" /><i></i><img src="../../public/logo-btu-beyaz.png" alt="Bursa Teknik Üniversitesi" /></div>
  </div>
  <div class="kapak-alt">
    <p class="kapak-kurum">Bursa Teknik Üniversitesi<br />Makine Teknolojileri Robot ve Otomasyon Topluluğu</p>
    <h1>Faaliyet<br />Raporu</h1>
    <p class="kapak-donem">${DONEM}</p>
    <ul class="kapak-rakam"><li><b>${toplamFaaliyet}</b>faaliyet</li><li><b>${sayi(toplamKatilim)}</b>katılım</li><li><b>${P.length}</b>TEKNOFEST projesi</li><li><b>${final2026.length}</b>2026 finalisti</li></ul>
  </div>`,
  { cls: 'p-kapak koyu', tam: true, footer: false },
);

// ---------- 2. İç kapak ----------
const kisi = (rol) => site.people.find((p) => p.role === rol)?.name || '';
const adDuzelt = (s) => s.replace(/\b([A-ZÇĞİÖŞÜ])([A-ZÇĞİÖŞÜ]+)\b/g, (_, a, b) => a + b.toLocaleLowerCase('tr'));
page(
  `<div class="ic-logolar"><img src="../../public/logo-matro-mavi.png" alt="MATRO" /><img src="../../public/logo-btu.png" alt="Bursa Teknik Üniversitesi" /></div>
  <div class="ic-baslik">
    ${eyebrow('Bursa Teknik Üniversitesi öğrenci toplulukları')}
    <h1>MATRO<br /><span>${DONEM}</span><br />Faaliyet Raporu</h1>
    <p class="lead">${esc(site.fullName)} (MATRO) tarafından ${DONEM} akademik yılında gerçekleştirilen eğitim, teknik gezi, stant, sosyal sorumluluk, yarışma ve proje faaliyetlerinin raporudur.</p>
  </div>
  <dl class="ic-kunye">
    <dt>Topluluk</dt><dd>${esc(site.fullName)}</dd>
    <dt>Kuruluş</dt><dd>${site.foundedYear}</dd>
    <dt>Topluluk başkanı</dt><dd>${esc(adDuzelt(kisi('Topluluk Başkanı')))}</dd>
    <dt>Akademik danışman</dt><dd>${esc(adDuzelt(kisi('Akademik Danışman')))}</dd>
    <dt>Danışman mühendis</dt><dd>${esc(adDuzelt(kisi('Topluluk Danışman Mühendisi')))}</dd>
    <dt>Hazırlayan</dt><dd>MATRO Yönetim Kurulu</dd>
    <dt>Atölye</dt><dd>${esc(site.contact.workshop)}</dd>
    <dt>İletişim</dt><dd>${esc(site.contact.emails[0])} · btumatro.com</dd>
  </dl>`,
  { cls: 'p-ic-kapak', footer: false },
);

// ---------- 3. Sunuş + içindekiler (sonra doldurulur) ----------
const SUNUS = pages.length;
page('');

// ---------- 4. Biz kimiz ----------
page(
  `${baslik('Topluluk', 'Biz kimiz?')}
  <div class="biz">
    <div class="biz-metin">${about.intro.body.split('\n\n').map((p) => `<p>${esc(p)}</p>`).join('')}</div>
    <figure class="biz-foto">${img('/media/galeri-matrover-arazi-test.jpg', 'LUNA İKA ekibi')}</figure>
  </div>
  <div class="vm">
    <div>${eyebrow('Vizyon', 'volt')}<p class="alinti">${esc(about.vision)}</p></div>
    <div>${eyebrow('Misyon', 'volt')}<p>${esc(about.mission)}</p></div>
  </div>
  <div class="degerler">${about.values.map((v, i) => `<div><span>${String(i + 1).padStart(2, '0')}</span><h3>${esc(v.title)}</h3><p>${esc(v.description)}</p></div>`).join('')}</div>
  <ul class="kunye-serit"><li><b>${site.foundedYear}</b>kuruluş</li><li><b>${takimDosyalari.length}</b>proje takımı</li><li><b>${dereceSay}</b>kayıtlı derece</li><li><b>${birincilik}</b>birincilik</li></ul>`,
  { cls: 'p-biz', bolum: 'Topluluk' },
);
toc.push({ no: '', baslik: 'Biz kimiz?', sayfa: pages.length });

// ---------- 5. Tarihçe ----------
page(
  `${baslik('Topluluk', `${site.foundedYear}'ten bugüne`)}
  <ol class="zaman">${about.timeline.map((t) => `<li><span class="yil">${esc(t.year)}</span><div><h3>${esc(t.title)}</h3><p>${esc(t.description)}</p></div></li>`).join('')}</ol>`,
  { cls: 'p-tarihce', bolum: 'Topluluk' },
);
toc.push({ no: '', baslik: 'Tarihçe', sayfa: pages.length });

// ---------- 6. Yapı ve takımlar ----------
{
  const sira = ['insansiz-hava-araclari', 'insansiz-kara-araci', 'insansiz-deniz-araci', 'insansiz-su-alti-sistemleri', 'su-alti-roket-sistemleri', 'suru-insansiz-hava-araci', 'sanayide-robotik-ve-dijital', 'hava-savunma-sistemleri', 'cevre-enerji-teknolojileri', 'ucan-araba-simulasyonu', 'kablosuz-haberlesme', 'teknoloji-girisimciligi', 'tarim-teknolojileri'];
  const takimlar = sira.map((d) => mdDosya(`src/content/teams/${d}.md`));
  page(
    `${baslik('Topluluk', 'Nasıl çalışıyoruz?', ekip.hero.description)}
    <div class="kurul">${ekip.boardTeams.map((b) => `<div><h3>${esc(b.name)}</h3><p>${esc(b.description)}</p></div>`).join('')}</div>
    ${eyebrow(`${takimlar.length} proje takımı`, 'volt')}
    <div class="takimlar">${takimlar
      .map((t) => `<div class="tk"><figure>${img(t.image, t.title)}</figure><div><h4>${esc(t.title)}</h4><p>${esc(t.subtitle)}</p>${t.badge ? `<span>${esc(t.badge)}</span>` : ''}</div></div>`)
      .join('')}</div>`,
    { cls: 'p-yapi', bolum: 'Topluluk' },
  );
  toc.push({ no: '', baslik: 'Yapımız ve takımlarımız', sayfa: pages.length });
}

// ---------- 7. Sayılarla ----------
page(
  `${baslik('Sezon özeti', `Sayılarla ${DONEM}`)}
  <div class="stat-grid">
    <div class="stat big"><b>${toplamFaaliyet}</b><span>faaliyet</span><em>eğitim, gezi, stant, okul programı, yarışma, proje ve sosyal etkinlik</em></div>
    <div class="stat big"><b>${sayi(toplamKatilim)}</b><span>toplam katılım</span><em>faaliyet başına bildirilen katılımcı sayılarının toplamı</em></div>
    <div class="stat"><b>${P.length}</b><span>TEKNOFEST projesi</span><em>${projeKisi} öğrenci görev aldı</em></div>
    <div class="stat"><b>${gezi.length}</b><span>teknik gezi</span><em>havacılık, savunma, Ar-Ge ve sanayi</em></div>
    <div class="stat"><b>${sayi(okulKatilim)}</b><span>okul öğrencisi</span><em>${bolumListe('okullar').length} okul programında</em></div>
    <div class="stat"><b>${kurumSay}+</b><span>kurumla iş birliği</span><em>sanayi, kamu, okul ve sivil toplum</em></div>
  </div>
  <div class="grafik">
    ${eyebrow('Aylara göre faaliyet sayısı')}
    <div class="bars">${aylar.map((a) => `<div class="bar"><span class="bar-n">${a.n || ''}</span><i style="height:${a.n ? (a.n / ayMax) * 100 : 0}%"></i><span class="bar-a">${a.ad}</span></div>`).join('')}</div>
    <p class="not">Tarihi ay düzeyinde bilinen faaliyetler; sezon boyunca süren TEKNOFEST proje çalışmaları dahil değildir.</p>
  </div>
  <div class="derece-serit">${eyebrow('Sezonun dereceleri')}
    <ul>${data.basarilar.filter((b) => b.derece).map((b) => `<li><b>${esc(b.derece)}</b><span>${esc(b.baslik)}</span></li>`).join('')}<li><b>${final2026.length}</b><span>takım TEKNOFEST 2026 finalinde</span></li></ul>
  </div>`,
  { cls: 'p-sayilar', bolum: 'Sezon özeti' },
);
toc.push({ no: '', baslik: `Sayılarla ${DONEM}`, sayfa: pages.length });

// ---------- 8. Bütçe ----------
{
  const satir = BOLUM_SIRA.map((id) => {
    const l = bolumListe(id);
    return { ad: bolumBul(id).baslik, no: bolumBul(id).no, t: l.reduce((a, k) => a + tl(k.butce), 0), n: l.filter((k) => tl(k.butce)).length, top: l.length };
  });
  const max = Math.max(...satir.map((s) => s.t));
  const ilk = [...kayitlar].sort((a, b) => tl(b.butce) - tl(a.butce)).slice(0, 8);
  page(
    `${baslik('Sezon özeti', 'Bütçe', `Faaliyet raporunda her etkinlik için bildirilen harcamaların bölümlere göre dağılımı. ${toplamFaaliyet} faaliyetin ${butceliSay} tanesinde harcama belirtilmiş; diğerleri kurum desteğiyle veya harcama olmadan gerçekleşti.`)}
    <div class="butce-toplam"><b>${para(toplamButce)}</b><span>toplam harcama</span></div>
    <ul class="butce-bar">${satir.map((s) => `<li><span class="bb-ad"><em>${s.no}</em>${esc(s.ad)}</span><span class="bb-cubuk"><i style="width:${max ? (s.t / max) * 100 : 0}%"></i></span><span class="bb-t">${s.t ? para(s.t) : '–'}</span><span class="bb-n">${s.n}/${s.top}</span></li>`).join('')}</ul>
    ${eyebrow('En yüksek bütçeli faaliyetler')}
    <ol class="butce-ilk">${ilk.map((k) => `<li><span class="no">${k.no}</span><span>${esc(k.ad)}${k.altBaslik ? ` <em>${esc(k.altBaslik.replace('TEKNOFEST ', ''))}</em>` : ''}</span><b>${esc(k.butce)}</b></li>`).join('')}</ol>
    <p class="not">Tutarlar faaliyet raporundaki "Harcanan bütçe" satırlarından alınmıştır. Sponsorların ayni ve nakdi destekleri bu tutarlara dahil olabilir.</p>`,
    { cls: 'p-butce', bolum: 'Sezon özeti' },
  );
  toc.push({ no: '', baslik: 'Bütçe', sayfa: pages.length });
}

// ---------- kart ----------
function kart(k) {
  const d = [
    ['Tarih', k.tarih ? tarih(k.tarih, k.bitis) : `${DONEM} sezonu`],
    ['Katılımcı', k.katilim ? `${sayi(k.katilim)} kişi` : '–'],
    ['Bütçe', k.butce || '–'],
    ['Yer', k.yer || '–'],
    ['Araç gereç', k.arac || '–'],
    ['İş birliği', k.isbirligi?.length ? k.isbirligi.join(', ') : '–'],
  ];
  const bolum = bolumBul(k.bolum);
  // Fotoğraf kendi oranında gösterilir (kırpma yok ya da çok az):
  //  - çok geniş (≥2,1) fotoğraf: kartın üstünde tam genişlik şerit
  //  - diğerleri: solda, en fazla 92 mm yükseklik ve 102 mm genişlikte kendi oranında
  //  - sayfada tek kart varsa: üstte tam genişlik, oranında (en fazla 150 mm)
  const tekKart = k.tek;
  const serit = !tekKart && k.oran >= 2.1;
  let fotoStil = '';
  let tip = 'yan';
  if (tekKart) {
    tip = 'ust';
    fotoStil = `height:${Math.min(150, 174 / k.oran).toFixed(1)}mm`;
  } else if (serit) {
    tip = 'ust';
    fotoStil = `height:${Math.min(70, 174 / k.oran).toFixed(1)}mm`;
  } else {
    const h = Math.min(92, 102 / k.oran);
    fotoStil = `width:${(h * k.oran).toFixed(1)}mm;height:${h.toFixed(1)}mm`;
  }
  const dikey = tip === 'yan';
  return `<article class="kart ${dikey ? 'dikey' : 'genis'}">
    <header class="k-bas"><span class="k-no">${k.no}</span><div>${eyebrow(`${bolum.no} · ${bolum.baslik}${k.altBaslik ? ` · ${k.altBaslik.replace('TEKNOFEST ', 'TEKNOFEST · ')}` : ''}`)}<h3>${esc(k.ad)}</h3></div>${k.derece ? `<span class="k-derece">${esc(k.derece)}</span>` : ''}</header>
    <figure class="k-foto" style="${fotoStil}">${img(k.gorsel, k.ad, k.gorselKonum || 'center 35%')}${k.gorselNotu ? `<figcaption>${esc(k.gorselNotu)}</figcaption>` : ''}</figure>
    <div class="k-govde">
      <div class="k-metin"><p class="k-spot">${esc(k.ozet)}</p><p>${esc(k.metin)}</p></div>
      <dl class="k-kunye">${d.map(([a, v]) => `<div><dt>${a}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>
    </div>
  </article>`;
}

// ---------- bölüm açılışı (iç kapak) ----------
function bolumAcilis(id) {
  const b = bolumBul(id);
  const l = bolumListe(id);
  const katilim = l.reduce((a, k) => a + (k.katilim || 0), 0);
  const butce = l.reduce((a, k) => a + tl(k.butce), 0);
  const no = page(
    `<figure class="ba-foto">${img(b.kapak || l[0].gorsel, b.baslik)}</figure>
    <div class="ba-ust"><span class="ba-etiket">Bölüm</span><span class="ba-no">${b.no}</span></div>
    <div class="ba-alt">
      <h1>${esc(b.baslik)}</h1>
      <p class="ba-lead">${esc(b.ozet)}</p>
      <ul class="ba-rakam"><li><b>${l.length}</b>faaliyet</li><li><b>${sayi(katilim)}</b>katılım</li><li><b>${butce ? para(butce) : '–'}</b>bütçe</li></ul>
      <ol class="ba-liste">${l.map((k) => `<li><span>${k.no}</span>${esc(k.ad)}${k.altBaslik ? ` <em>${esc(k.altBaslik.replace('TEKNOFEST ', ''))}</em>` : ''}</li>`).join('')}</ol>
    </div>`,
    { cls: 'p-bolum koyu', tam: true },
  );
  toc.push({ no: b.no, baslik: b.baslik, sayfa: no });
}
function kartSayfalari(id) {
  const l = bolumListe(id);
  const b = bolumBul(id);
  for (let i = 0; i < l.length; i += 2) {
    const grup = l.slice(i, i + 2);
    grup.forEach((k) => (k.tek = grup.length === 1));
    page(`<div class="kartlar ${grup.length === 1 ? 'tek' : ''}">${grup.map(kart).join('')}</div>`, { cls: 'p-kart', bolum: `${b.no} · ${b.baslik}` });
  }
}

// ---------- bölümler ----------
for (const id of BOLUM_SIRA) {
  bolumAcilis(id);
  if (id === 'teknofest') {
    const bb = `${bolumBul(id).no} · ${bolumBul(id).baslik}`;
    page(
      `${baslik('Özel dosya', 'Bir aracın doğuşu', "Final alanında birkaç dakikalık bir görev. Arkasında on ay, yüzlerce saatlik atölye mesaisi, raporlar ve sayısız test var. Bir MATRO aracının Eylül'den Ağustos'a yolculuğu.")}
      <ol class="dogus">${data.aracinDogusu.map((a, i) => `<li><span class="d-no">${i + 1}</span><div>${eyebrow(a.ay, 'volt')}<h3>${esc(a.baslik)}</h3><p>${esc(a.metin)}</p></div></li>`).join('')}</ol>
      <div class="dogus-foto"><figure>${img('/media/tasarim-iss-auv-mor.jpg', 'İSS tasarımı')}<figcaption>Tasarım</figcaption></figure><figure>${img('/media/galeri-iss-auv-havuz.jpg', 'Havuz testi')}<figcaption>Test</figcaption></figure><figure>${img('/media/galeri-zemheri-final.jpg', 'Final alanı')}<figcaption>Final</figcaption></figure></div>`,
      { cls: 'p-dogus', bolum: bb },
    );
    toc.push({ no: '', baslik: 'Özel dosya: Bir aracın doğuşu', sayfa: pages.length, alt: true });
    page(
      `${baslik('TEKNOFEST 2026', `${final2026.length} takım finalde`, "TEKNOFEST 2026 sezonunda takımlarımız Türkiye'nin dört bir yanındaki final alanlarında üniversitemizi temsil etti. Su Altı Roket kategorisine ilk kez katılan ZEMHERİ, ilk yılında finalist oldu.")}
      <div class="finaller">${final2026.map((f) => `<div><b>${esc(f.team)}</b><span>${esc(f.category)}</span><em>${esc(f.competition.replace('TEKNOFEST — ', ''))}${data.finalYerleri[f.team] ? ` · ${esc(data.finalYerleri[f.team])}` : ''}</em></div>`).join('')}</div>
      <figure class="finaller-foto">${img('/media/mavi-vatan-ekipler.jpg', 'Mavi Vatan')}<figcaption>TEKNOFEST Mavi Vatan: LODOS, PRUSA ve ZEMHERİ ekipleri</figcaption></figure>`,
      { cls: 'p-finaller', bolum: bb },
    );
    toc.push({ no: '', baslik: 'TEKNOFEST 2026 finalleri', sayfa: pages.length, alt: true });
  }
  kartSayfalari(id);
}

// ---------- kapanış sayfaları ----------
const kapanis = [];
kapanis.push(() => {
  const t = [...tarihli].sort((a, b) => a.tarih.localeCompare(b.tarih));
  page(`${baslik('Kronoloji', 'Sezon takvimi')}<ol class="takvim">${t.map((x) => `<li><span class="tk-t">${esc(tarih(x.tarih, x.bitis))}</span><span class="tk-a"><em>${x.no}</em>${esc(x.ad)}</span><span class="tk-y">${esc(x.yer)}</span></li>`).join('')}</ol>`, { cls: 'p-takvim', bolum: 'Kapanış' });
  toc.push({ no: '', baslik: 'Sezon takvimi', sayfa: pages.length });
});
kapanis.push(() => {
  const pk = ['Platin', 'Altın', 'Gümüş', 'Bronz', 'Gönüllü'];
  page(
    `${baslik('Teşekkür', 'Birlikte ürettiklerimiz', sponsors.intro)}
    ${eyebrow('İş birliği yapılan kurumlar', 'volt')}<ul class="kurumlar">${data.isbirlikleri.map((k) => `<li>${esc(k)}</li>`).join('')}</ul>
    ${pk
      .map((k) => {
        const l = sponsors.current.filter((s) => s.package === k);
        return l.length
          ? `<div class="sp ${k.toLocaleLowerCase('tr')}">${eyebrow(`${k} sponsorlar · ${l.length}`)}<div>${l
              .map((s) => (s.logo ? `<figure><img src="../../public${esc(s.logo)}" alt="${esc(s.name)}" /><figcaption>${esc(s.name)}</figcaption></figure>` : `<figure class="yazi"><span>${esc(s.name)}</span></figure>`))
              .join('')}</div></div>`
          : '';
      })
      .join('')}`,
    { cls: 'p-destek', bolum: 'Kapanış' },
  );
  toc.push({ no: '', baslik: 'İş birlikleri ve sponsorlar', sayfa: pages.length });
});
kapanis.push(() => {
  page(
    `${baslik('Gelecek sezon', about.goals2026.title.replace(/^./, (c) => c.toLocaleUpperCase('tr')), about.goals2026.description)}
    <ol class="hedef">${about.goals2026.items.map((g, i) => `<li><span>${String(i + 1).padStart(2, '0')}</span>${esc(g)}</li>`).join('')}</ol>
    <figure class="hedef-foto">${img('/media/galeri-tika-tarimsal-ika.jpg', 'Tarımsal İKA ekibi')}</figure>`,
    { cls: 'p-hedef', bolum: 'Kapanış' },
  );
  toc.push({ no: '', baslik: '2026–2027 hedeflerimiz', sayfa: pages.length });
});
const karelerSayfasi = () => {
  page(
    `${baslik('Fotoğraf', 'Sahadan kareler', 'Takımlarımız atölyede, test alanında ve TEKNOFEST final alanlarında.')}
    <div class="kareler">${data.kareler.map((k, i) => `<figure class="k${i + 1}">${img(k.gorsel, k.not)}<figcaption>${esc(k.not)}</figcaption></figure>`).join('')}</div>`,
    { cls: 'p-kareler', bolum: 'Kapanış' },
  );
  toc.push({ no: '', baslik: 'Sahadan kareler', sayfa: pages.length });
};
const arsivSayfasi = () => {
  page(
    `${baslik('Arşiv', `${site.foundedYear}'ten bugüne ${dereceSay} derece`, ach.intro)}
    <ol class="arsiv">${A.map((i) => `<li class="${i.featured ? 'one' : ''}"><span class="a-yil">${i.year}</span><span class="a-tk">${esc(i.team || '–')}</span><span class="a-kat">${esc(i.category)}<em>${esc(i.competition)}</em></span><span class="a-der ${/(^|[^0-9])1\.|dünya/i.test(i.degree) ? 'altin' : ''}">${esc(i.degree)}</span></li>`).join('')}</ol>`,
    { cls: 'p-arsiv', bolum: 'Kapanış' },
  );
  toc.push({ no: '', baslik: 'Başarı arşivimiz', sayfa: pages.length });
};
const basinSayfasi = () => {
  page(
    `${baslik('Arşiv', 'Basında MATRO', basin.intro)}
    <div class="basin">${basin.items.map((b) => `<article><figure>${img(b.image, b.outlet)}</figure>${eyebrow(`${b.outlet} · ${b.date.slice(0, 4)}`, 'volt')}<h3>${esc(b.headline)}</h3></article>`).join('')}</div>`,
    { cls: 'p-basin', bolum: 'Kapanış' },
  );
  toc.push({ no: '', baslik: 'Basında MATRO', sayfa: pages.length });
};
// Arka kapak dahil toplam sayfa sayısı 4'ün katı olsun: gerekirse sırasıyla
// fotoğraf, başarı arşivi ve basın sayfaları eklenir; kalan açık için not sayfası.
const ekler = [karelerSayfasi, arsivSayfasi, basinSayfasi];
const gereken = (4 - ((pages.length + kapanis.length + 1) % 4)) % 4;
ekler.slice(0, gereken).forEach((f) => f());
for (const f of kapanis) f();
while ((pages.length + 1) % 4) page(`${baslik('', 'Notlar')}<div class="notlar"></div>`, { cls: 'p-not', bolum: 'Kapanış' });

page(
  `<div class="arka">
    <img class="arka-logo" src="../../public/logo-matro-beyaz.png" alt="MATRO" />
    <p class="arka-slogan">Atölyede başlar.<br />Sahada kanıtlanır.</p>
    <div class="arka-alt">
      <div class="qr"><img src="gorseller/qr-btumatro.svg" alt="btumatro.com" /></div>
      <dl><dt>Web</dt><dd>btumatro.com</dd><dt>E-posta</dt><dd>${esc(site.contact.emails[0])}</dd><dt>Atölye</dt><dd>${esc(site.contact.workshop)}</dd><dt>Adres</dt><dd>Mimar Sinan Yerleşkesi, Yıldırım / Bursa</dd></dl>
      <img class="arka-btu" src="../../public/logo-btu-beyaz.png" alt="BTÜ" />
    </div>
  </div>`,
  { cls: 'p-arka koyu', tam: true, footer: false },
);

// ---------- sunuş + içindekiler ----------
{
  const govde = `${baslik('Sunuş', `Bir sezon, ${toplamFaaliyet} faaliyet`)}
  <div class="sunus">
    <div class="sunus-metin">
      <p class="lead">MATRO; Bursa Teknik Üniversitesi'nde insansız hava, kara, deniz ve su altı sistemleri, robotik, haberleşme ve enerji teknolojileri alanlarında proje geliştiren öğrenci topluluğudur.</p>
      <p>${DONEM} döneminde yeni üyelerimizi eğitim kamplarıyla atölyeye hazırladık, sanayinin önde gelen kuruluşlarına teknik geziler düzenledik, fuar ve festivallerde stant açtık, ilkokuldan liseye ${sayi(okulKatilim)} öğrenciyle buluştuk ve ${P.length} farklı TEKNOFEST kategorisinde proje yürüttük. Sezonun sonunda ${final2026.length} takımımız TEKNOFEST finallerinde üniversitemizi temsil etti.</p>
      <p>Bu rapor, topluluğumuzun üniversiteye sunduğu faaliyet raporundan derlenmiştir. ${toplamFaaliyet} faaliyetin her biri numaralı bir kartta; tarih, yer, katılımcı sayısı, bütçe, kullanılan araç gereç ve iş birliği yapılan kurumlarla birlikte yer alıyor.</p>
      <p>Bu sezon kapılarını açan kurumlara, destek veren sponsorlarımıza, bizi ağırlayan okullara ve atölyenin ışığını yakan tüm üyelerimize teşekkür ederiz.</p>
      <p class="imza">MATRO Yönetim Kurulu</p>
    </div>
    <nav class="toc">${eyebrow('İçindekiler')}<ol>${toc
      .sort((a, b) => a.sayfa - b.sayfa)
      .map((t) => `<li class="${t.no ? 'ana' : ''} ${t.alt ? 'ic-alt' : ''}"><span class="t-no">${t.no}</span><span>${esc(t.baslik)}</span><span class="t-p">${String(t.sayfa).padStart(2, '0')}</span></li>`)
      .join('')}</ol></nav>
  </div>`;
  pages[SUNUS] = pages[SUNUS].replace('<div class="icerik"></div>', `<div class="icerik">${govde}</div>`).replace('<section class="page', '<section class="page p-sunus');
}

// ---------- HTML + PDF ----------
const html = `<!doctype html>
<html lang="tr"><head><meta charset="utf-8" />
<title>MATRO Faaliyet Raporu ${DONEM}</title>
<link rel="stylesheet" href="kitapcik.css" />
</head><body>
${pages.join('\n')}
</body></html>`;
fs.writeFileSync(path.join(DIR, 'kitapcik.html'), html);
console.log(`HTML yazıldı: ${pages.length} sayfa, ${toplamFaaliyet} faaliyet, ${toplamKatilim} katılım, ${para(toplamButce)}`);
if (pages.length % 4) console.warn(`Uyarı: sayfa sayısı (${pages.length}) 4'ün katı değil.`);
if (process.argv.includes('--html')) process.exit(0);

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
const tab = await browser.newPage();
await tab.goto(pathToFileURL(path.join(DIR, 'kitapcik.html')).href, { waitUntil: 'networkidle0' });
await tab.evaluate(() => document.fonts.ready);
const kayip = await tab.evaluate(() => [...document.images].filter((i) => !i.naturalWidth).map((i) => i.getAttribute('src')));
if (kayip.length) {
  console.error('Yüklenemeyen görseller:', kayip);
  process.exit(1);
}
// Taşan kartlarda fotoğrafı kademeli küçült; ardından tüm sayfalarda taşma denetimi.
const rapor = await tab.evaluate(() => {
  const mm = 96 / 25.4;
  for (const k of document.querySelectorAll('.kart')) {
    const f = k.querySelector('.k-foto');
    const r = f.getBoundingClientRect();
    const oran = r.width / r.height;
    let h = r.height / mm;
    while (k.scrollHeight > k.clientHeight + 1 && h > 34) {
      h -= 2;
      f.style.height = `${h}mm`;
      if (k.classList.contains('dikey')) f.style.width = `${h * oran}mm`;
    }
  }
  const tasan = [];
  document.querySelectorAll('.page').forEach((p, i) => {
    const ic = p.querySelector('.icerik');
    if (ic.scrollHeight > ic.clientHeight + 1) tasan.push(`sayfa ${i + 1}`);
    p.querySelectorAll('.kart').forEach((k) => k.scrollHeight > k.clientHeight + 1 && tasan.push(`sayfa ${i + 1} kart ${k.querySelector('.k-no').textContent}`));
  });
  return tasan;
});
if (rapor.length) console.warn('Taşma:', rapor.join(', '));
const out = path.join(DIR, 'matro-faaliyet-raporu-2025-2026.pdf');
await tab.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
await browser.close();
console.log('PDF:', path.relative(ROOT, out));
