#!/usr/bin/env node
/**
 * MATRO Sponsorluk Dergisi — A4 dikey, dergi formatında sponsorluk dosyası.
 *
 * Tüm olgusal içerik sitenin kendi kaynaklarından okunur: takımlar
 * (src/content/teams/*.md), başarılar, sponsorlar, paketler, tarihçe, basın,
 * eğitim programı (src/data, src/content/activities) ve 2025–2026 sezon özeti
 * (docs/faaliyet-kitapcigi-2025-26/icerik.json). Dergiye özel editoryal metinler
 * ve fotoğraf seçimleri docs/sponsorluk-dergisi-2026-27/icerik.json'dadır.
 * Rakamlar elle yazılmaz; derece/birincilik sayıları sitedeki
 * achievementSummary() ile aynı kurallarla hesaplanır.
 *
 * Kullanım:
 *   node scripts/build-sponsorluk-dergisi.mjs          # HTML + PDF
 *   node scripts/build-sponsorluk-dergisi.mjs --html   # yalnız HTML
 */
import puppeteer from 'puppeteer-core';
import yaml from 'js-yaml';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'docs/sponsorluk-dergisi-2026-27');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const oku = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));

const D = oku('docs/sponsorluk-dergisi-2026-27/icerik.json');
const sezon = oku('docs/faaliyet-kitapcigi-2025-26/icerik.json');
const site = oku('src/data/site.json');
const about = oku('src/data/about.json');
const home = oku('src/data/home.json');
const ach = oku('src/data/achievements.json');
const sponsors = oku('src/data/sponsors.json');
const paket = oku('src/data/sponsorship.json');
const basin = oku('src/data/basinda-biz.json');

function mdDosya(p) {
  const s = fs.readFileSync(path.join(ROOT, p), 'utf8');
  const m = s.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  return { data: yaml.load(m[1]), body: m[2].trim() };
}

// ---------- yardımcılar ----------
const esc = (s = '') =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const src = (p) => (p.startsWith('/media/') ? `../../public${p}` : p);
const img = (p, alt = '', konum = '') =>
  `<img src="${esc(src(p))}" alt="${esc(alt)}"${konum ? ` style="object-position:${esc(konum)}"` : ''} />`;
const sayi = (n) => n.toLocaleString('tr-TR');
const satir = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
/** Takım dosyalarındaki sade Markdown: ## başlık, - liste, paragraf. */
function md(body) {
  const out = [];
  let liste = null;
  for (const l of body.split('\n')) {
    if (/^- /.test(l)) {
      liste ??= [];
      liste.push(`<li>${satir(l.slice(2))}</li>`);
      continue;
    }
    if (liste) out.push(`<ul>${liste.join('')}</ul>`), (liste = null);
    if (/^## /.test(l)) out.push(`<h4>${satir(l.slice(3))}</h4>`);
    else if (l.trim()) out.push(`<p>${satir(l)}</p>`);
  }
  if (liste) out.push(`<ul>${liste.join('')}</ul>`);
  return out.join('');
}

// ---------- veriden türetilen rakamlar (src/lib/utils.ts achievementSummary ile aynı) ----------
const A = ach.items;
const ozet = {
  kayit: A.length,
  birincilik: A.filter((i) => /(^|[^0-9])1\./.test(i.degree)).length,
  final2026: A.filter((i) => i.year === 2026 && /finalist/i.test(i.degree)).length,
  uluslararasi: A.filter((i) => /dünya|singapore|france|nasa|italian|uluslararası|bölge/i.test(`${i.competition} ${i.degree}`)).length,
  ilkYil: Math.min(...A.map((i) => i.year)),
};
const homeStat = (label) => home.stats.find((s) => s.label === label);
const finalistYarismaci = homeStat('Finalist Yarışmacı');
const ilk10 = homeStat("İlk 10'a Giren Takım");
const kardesOkul = homeStat('Sosyal Sorumluluk Desteği');
const takimDosyalari = fs.readdirSync(path.join(ROOT, 'src/content/teams')).filter((f) => f.endsWith('.md'));
const yas = new Date().getFullYear() - site.foundedYear;
const S = sezon.faaliyetler;
const sezonB = sezon.basarilar.filter((b) => b.katilim);
const sezonFaaliyet = S.length + sezonB.length + sezon.projeler.length;
const sezonKatilim =
  S.reduce((a, f) => a + (f.katilim || 0), 0) + sezonB.reduce((a, b) => a + b.katilim, 0) + sezon.projeler.reduce((a, p) => a + p.kisi, 0);
const okulKatilim = S.filter((f) => f.bolum === 'okullar').reduce((a, f) => a + f.katilim, 0);
const egitim = mdDosya('src/content/activities/egitim-kamplari.md');
const geziler = mdDosya('src/content/activities/teknik-geziler.md');
const kurumlar = geziler.body.split('\n').filter((l) => l.startsWith('- ')).map((l) => l.slice(2));
const aktifSponsor = sponsors.current;
const PK = ['Platin', 'Altın', 'Gümüş', 'Bronz', 'Gönüllü'];

// ---------- sayfa altyapısı ----------
const pages = [];
const toc = [];
let no = 0;
function page(inner, { cls = '', bolum = '', footer = true, tocBaslik = '' } = {}) {
  no += 1;
  if (tocBaslik) toc.push({ baslik: tocBaslik, sayfa: no });
  const n = String(no).padStart(2, '0');
  const foot = footer
    ? `<footer class="run"><span class="run-m">MATRO</span><span>${esc(D.sayi)} · ${esc(D.donem)}</span>${bolum ? `<span class="run-b">${esc(bolum)}</span>` : ''}<span class="pn">${n}</span></footer>`
    : '';
  pages.push(`<section class="page ${cls}">${inner}${foot}</section>`);
  return pages.length - 1;
}
const kicker = (t, cls = '') => `<p class="kicker ${cls}">${esc(t)}</p>`;

// ---------- 1. Kapak ----------
page(
  `<figure class="kapak-foto">${img(D.kapak.foto, 'Mavi Vatan etkinliğinde MATRO takımları', D.kapak.fotoKonum)}</figure>
  <div class="kapak-ust">
    <div class="masthead">MATRO</div>
    <div class="kapak-sayi"><span>${esc(D.sayi)}</span><span>${esc(D.donem)}</span><span>${esc(site.university)}</span></div>
  </div>
  <div class="kapak-alt">
    <p class="kicker volt">${esc(D.kapak.altbaslik)}</p>
    <h1>${esc(D.kapak.baslik)}</h1>
    <ul class="mansetler">${D.kapak.manset.map((m) => `<li>${esc(m)}</li>`).join('')}</ul>
  </div>`,
  { cls: 'p-kapak', footer: false },
);

// ---------- 2. İçindekiler + editörden (sonra doldurulur) ----------
const TOC_YER = page('');

// ---------- 3–4. Biz kimiz ----------
page(
  `<div class="yayilim-sol">
    ${kicker('Biz kimiz')}
    <h2 class="dev">${yas} yıldır<br />atölyedeyiz.</h2>
    <div class="iki-kolon">${about.intro.body.split('\n\n').map((p) => `<p>${esc(p)}</p>`).join('')}</div>
    <figure class="bk-foto">${img(D.fotolar.bizKimiz, 'LUNA İKA arazi testi')}<figcaption>LUNA İKA ekibi TEKNOFEST final alanında</figcaption></figure>
  </div>`,
  { cls: 'p-biz', bolum: 'Biz kimiz', tocBaslik: 'Biz kimiz' },
);
page(
  `<div class="vm">
    <div>${kicker('Vizyon', 'volt')}<p class="alinti">${esc(about.vision)}</p></div>
    <div>${kicker('Misyon', 'volt')}<p>${esc(about.mission)}</p></div>
  </div>
  <div class="degerler">${about.values
    .map((v, i) => `<div><span class="d-no">${String(i + 1).padStart(2, '0')}</span><h3>${esc(v.title)}</h3><p>${esc(v.description)}</p></div>`)
    .join('')}</div>
  <div class="kunye">
    <div><b>${site.foundedYear}</b><span>kuruluş yılı</span></div>
    <div><b>${takimDosyalari.length}</b><span>proje takımı</span></div>
    <div><b>${ozet.kayit}</b><span>kayıtlı derece</span></div>
    <div><b>${ozet.birincilik}</b><span>birincilik</span></div>
  </div>
  <figure class="vm-foto">${img(D.fotolar.bizKimiz2, 'ZEMHERİ ekibi yarışma alanında')}<figcaption>Yarışma alanında ZEMHERİ ekibi; takım kıyafetlerinde sponsor logoları</figcaption></figure>`,
  { cls: 'p-vm', bolum: 'Biz kimiz' },
);

// ---------- 5–6. Tarihçe ----------
{
  const t = about.timeline;
  const yarim = 5;
  const blok = (arr) =>
    arr.map((x) => `<li><span class="yil">${esc(x.year)}</span><div><h3>${esc(x.title)}</h3><p>${esc(x.description)}</p></div></li>`).join('');
  page(
    `${kicker('Tarihçe')}<h2 class="dev">${site.foundedYear}'ten<br />bugüne</h2>
    <ol class="zaman">${blok(t.slice(0, yarim))}</ol>`,
    { cls: 'p-tarihce', bolum: 'Tarihçe', tocBaslik: 'Tarihçe' },
  );
  page(`<ol class="zaman zaman-2">${blok(t.slice(yarim))}</ol>
    <blockquote class="buyuk-alinti">“${esc(ach.intro)}”</blockquote>`, { cls: 'p-tarihce', bolum: 'Tarihçe' });
}

// ---------- 7. Rakamlarla ----------
page(
  `${kicker('Rakamlarla MATRO')}<h2 class="dev">Emeğin<br />karşılığı.</h2>
  <div class="rakam-grid">
    <div class="r r-xl"><b>${ozet.kayit}</b><span>kayıtlı derece</span><em>${ozet.ilkYil}–${Math.max(...A.map((i) => i.year))}</em></div>
    <div class="r"><b>${ozet.birincilik}</b><span>birincilik</span><em>Türkiye ve bölge</em></div>
    <div class="r"><b>${ozet.uluslararasi}</b><span>uluslararası başarı</span><em>dünya ve bölge dereceleri</em></div>
    <div class="r"><b>${finalistYarismaci.value}</b><span>finalist yarışmacı</span><em>${esc(finalistYarismaci.note)}</em></div>
    <div class="r"><b>${ilk10.value}</b><span>ilk 10'a giren takım</span><em>${esc(ilk10.note)}</em></div>
    <div class="r r-volt"><b>${ozet.final2026}</b><span>TEKNOFEST finalisti</span><em>2026 sezonu</em></div>
  </div>
  <div class="sezon-serit">
    ${kicker(`2025–2026 sezonu`, 'volt')}
    <div><b>${sezonFaaliyet}</b><span>faaliyet</span></div>
    <div><b>${sayi(sezonKatilim)}</b><span>toplam katılım</span></div>
    <div><b>${sayi(okulKatilim)}</b><span>okul öğrencisine ulaşıldı</span></div>
    <div><b>${esc(kardesOkul.value + kardesOkul.suffix)}</b><span>Kardeş Okul desteği</span></div>
  </div>`,
  { cls: 'p-rakam', bolum: 'Rakamlarla', tocBaslik: 'Rakamlarla MATRO' },
);

// ---------- 8. 2026 finalleri ----------
{
  const f26 = A.filter((i) => i.year === 2026 && /finalist/i.test(i.degree));
  page(
    `<figure class="ust-foto">${img(D.fotolar.finaller, 'ZEMHERİ final alanında')}</figure>
    <div class="icerik">
      ${kicker('Kapak konusu', 'volt')}<h2 class="dev">2026: ${ozet.final2026} takım finalde</h2>
      <p class="lead">TEKNOFEST 2026 sezonunda ${ozet.final2026} takımımız Türkiye'nin dört bir yanındaki final alanlarında üniversitemizi temsil etti. Su Altı Roket kategorisine ilk kez katılan ZEMHERİ, ilk yılında finalist oldu.</p>
      <div class="final-grid">
        <ol class="final-liste">${f26.map((i) => `<li><b>${esc(i.team)}</b><span>${esc(i.category)}</span><em>${esc(i.competition)}</em></li>`).join('')}</ol>
        <ul class="sehirler">${D.finalSehirleri.map((s) => `<li><span>${esc(s.sehir)}</span>${esc(s.takimlar.join(' · '))}</li>`).join('')}</ul>
      </div>
    </div>`,
    { cls: 'p-final', bolum: 'Kapak konusu', tocBaslik: '2026 TEKNOFEST finalleri' },
  );
}

// ---------- 9. Takımlar açılış ----------
const takimlar = D.takimlar.map((t) => ({ ...t, ...mdDosya(`src/content/teams/${t.dosya}.md`) }));
page(
  `<figure class="tam-kapak">${img(D.fotolar.takimlarAcilis, 'ASHİNA takımı TEKNOFEST sahnesinde')}</figure>
  <div class="bolum-acilis">
    <span class="bolum-no">01</span>
    <div>${kicker('Bölüm', 'volt')}<h2>Takımlarımız</h2>
    <p>${takimlar.length} proje takımı, onlarca alt ekip. Hava, kara, deniz ve su altı araçlarından endüstriyel robotiğe, haberleşmeden enerjiye; hepsi aynı atölyede, Özdemir Bayraktar TEKNOFEST Atölyesi'nde üretiyor.</p>
    <ul class="takim-dizin">${takimlar.map((t) => `<li><b>${esc(t.data.title)}</b><span>${esc(t.data.subtitle)}</span></li>`).join('')}</ul></div>
  </div>`,
  { cls: 'p-bolum dark', footer: false, tocBaslik: 'Takımlarımız' },
);

// ---------- 10–16. Tam sayfa takım profilleri ----------
const dereceVurgu = (s) => /(^|[^0-9])[1-3]\.|dünya|en iyi/i.test(s);
for (const t of takimlar.filter((x) => x.tam)) {
  const d = t.data;
  page(
    `<figure class="takim-hero">${img(t.foto, d.title, t.fotoKonum)}${d.badge ? `<span class="rozet">${esc(d.badge)}</span>` : ''}</figure>
    <header class="takim-bas">
      <div>${kicker(d.category, 'volt')}<h2 class="takim-ad">${esc(d.title)}</h2><p class="takim-alt">${esc(d.subtitle)}</p></div>
      <div class="takim-yan">
        ${d.aliases?.length ? `<p class="kicker">Alt takımlar ve araçlar</p><p class="aliases">${esc(d.aliases.filter((a) => a !== d.title).join(' · '))}</p>` : ''}
        ${d.instagram ? `<p class="kicker">Instagram</p><p class="aliases">@${esc(d.instagram)}</p>` : ''}
      </div>
    </header>
    <div class="takim-govde">
      <div class="takim-metin">${md(t.body)}</div>
      <aside>
        <p class="kicker">Başarılar</p>
        <ul class="takim-basari">${d.achievements.map((a) => `<li class="${dereceVurgu(a) ? 'v' : ''}">${esc(a)}</li>`).join('')}</ul>
        <p class="kicker">Odak alanları</p>
        <ul class="etiket">${d.focus.map((f) => `<li>${esc(f)}</li>`).join('')}</ul>
      </aside>
    </div>
    <div class="takim-ek">${t.ek.map((e) => `<figure>${img(e, d.title)}</figure>`).join('')}</div>`,
    { cls: 'p-takim', bolum: 'Takımlarımız' },
  );
}

// ---------- 17–19. Yarım sayfa takımlar ----------
const kucuk = takimlar.filter((x) => !x.tam);
for (let i = 0; i < kucuk.length; i += 2) {
  page(
    `<div class="yarim-sayfa">${kucuk
      .slice(i, i + 2)
      .map((t) => {
        const d = t.data;
        return `<article class="yarim">
          <figure>${img(t.foto, d.title)}</figure>
          <div>
            ${kicker(d.category, 'volt')}
            <h2 class="takim-ad k">${esc(d.title)}</h2>
            <p class="takim-alt">${esc(d.subtitle)}</p>
            <p class="ozet">${esc(d.summary)}</p>
            ${d.achievements.length ? `<ul class="takim-basari">${d.achievements.slice(0, 5).map((a) => `<li class="${dereceVurgu(a) ? 'v' : ''}">${esc(a)}</li>`).join('')}</ul>` : ''}
            <ul class="etiket">${d.focus.map((f) => `<li>${esc(f)}</li>`).join('')}</ul>
          </div>
        </article>`;
      })
      .join('')}</div>`,
    { cls: 'p-yarim', bolum: 'Takımlarımız' },
  );
}

// ---------- 20–21. Başarı arşivi ----------
{
  const yari = Math.ceil(A.length / 2);
  const tablo = (arr) =>
    `<table class="arsiv"><thead><tr><th>Yıl</th><th>Yarışma</th><th>Kategori</th><th>Derece</th><th>Takım</th></tr></thead><tbody>${arr
      .map(
        (i) =>
          `<tr class="${i.featured ? 'one' : ''}"><td class="m">${i.year}</td><td>${esc(i.competition)}</td><td>${esc(i.category)}</td><td class="der ${/(^|[^0-9])1\.|dünya/i.test(i.degree) ? 'altin' : ''}">${esc(i.degree)}</td><td class="tk">${esc(i.team)}</td></tr>`,
      )
      .join('')}</tbody></table>`;
  page(
    `${kicker('Arşiv')}<h2 class="dev">${ozet.kayit} derece,<br />${ozet.birincilik} birincilik</h2>${tablo(A.slice(0, yari))}`,
    { cls: 'p-arsiv', bolum: 'Başarı arşivi', tocBaslik: 'Başarı arşivi' },
  );
  page(`${tablo(A.slice(yari))}<p class="not">Kaynak: btumatro.com/basarilarimiz. Vurgulu satırlar topluluğun öne çıkan başarılarıdır.</p>`, {
    cls: 'p-arsiv',
    bolum: 'Başarı arşivi',
  });
}

// ---------- 22. Atölye ve eğitim ----------
{
  const bolumler = [...egitim.body.matchAll(/^\*\*([^*]+):\*\*\n\n((?:- .*\n?)+)/gm)].map((m) => ({
    ad: m[1],
    liste: m[2].trim().split('\n').map((l) => l.slice(2)),
  }));
  page(
    `<figure class="ust-foto kisa">${img(D.fotolar.egitim, 'Eğitim kampı')}</figure>
    <div class="icerik">
      ${kicker('Atölye ve eğitim', 'volt')}<h2 class="dev">Her yıl yeniden<br />başlayan okul</h2>
      <p class="lead">${esc(egitim.data.summary)}</p>
      <div class="egitim">
        ${bolumler.map((b) => `<div><h3>${esc(b.ad)}</h3><ul>${b.liste.map((l) => `<li>${esc(l)}</li>`).join('')}</ul></div>`).join('')}
        <div class="egitim-stat">${egitim.data.stats.map((s) => `<p><b>${esc(s.value)}</b><span>${esc(s.label)}</span></p>`).join('')}</div>
      </div>
      <p class="not">Eğitimler ${esc(site.contact.workshop)}'nde verilir; mezunlar sezon içinde proje takımlarına katılır.</p>
      <figure class="alt-foto">${img('/media/galeri-genel-egitim-2025.jpg', 'MATRO genel eğitimi')}<figcaption>MATRO Genel Eğitim, Kasım 2025 · 157 katılımcı</figcaption></figure>
    </div>`,
    { cls: 'p-egitim', bolum: 'Atölye ve eğitim', tocBaslik: 'Atölye ve eğitim' },
  );
}

// ---------- 23–24. 2025–2026 sezon özeti ----------
{
  const one = ['Turkish Technic Workshop', 'Turkish Technic Teknik Gezisi', 'HKTM Teknik Gezisi', 'GUHEM Ziyareti', 'MEEXX Makine Fuarı', 'Tanışma ve Bilgilendirme Toplantısı'];
  const secili = one.map((a) => S.find((f) => f.ad === a)).filter(Boolean);
  page(
    `${kicker('Geçen sezon')}<h2 class="dev">2025–2026'da<br />neler yaptık?</h2>
    <div class="sezon-rakam"><div><b>${sezonFaaliyet}</b><span>faaliyet</span></div><div><b>${sayi(sezonKatilim)}</b><span>katılım</span></div><div><b>${S.filter((f) => f.bolum === 'sanayi' && /Gezi|Ziyaret/.test(f.ad)).length}</b><span>teknik gezi</span></div><div><b>${sezon.projeler.length}</b><span>TEKNOFEST projesi</span></div></div>
    <div class="mozaik">${secili
      .map((f, i) => `<figure class="mz mz${i + 1}">${img(f.gorsel.startsWith('gorseller/') ? `../faaliyet-kitapcigi-2025-26/${f.gorsel}` : f.gorsel, f.ad)}<figcaption><b>${esc(f.ad)}</b> · ${sayi(f.katilim)} katılımcı</figcaption></figure>`)
      .join('')}</div>`,
    { cls: 'p-sezon', bolum: 'Geçen sezon', tocBaslik: '2025–2026 sezonu' },
  );
  const bas = sezon.basarilar.filter((b) => b.derece);
  page(
    `<div class="sezon-2">
      <div>
        ${kicker('Sezonun dereceleri', 'volt')}
        <ul class="sezon-derece">${bas.map((b) => `<li><span class="madalya">${esc(b.derece)}</span><div><h3>${esc(b.baslik)}</h3><p>${esc(b.kurum)}</p></div></li>`).join('')}</ul>
      </div>
      <div>
        ${kicker('Fuarlar ve stantlar', 'volt')}
        <ul class="duz">${S.filter((f) => f.bolum === 'stant').map((f) => `<li><b>${esc(f.ad)}</b><span>${esc(f.yer)}</span></li>`).join('')}</ul>
        ${kicker('Sanayi ile buluşma', 'volt')}
        <ul class="duz">${S.filter((f) => f.bolum === 'sanayi').map((f) => `<li><b>${esc(f.ad)}</b><span>${esc(f.yer)}</span></li>`).join('')}</ul>
      </div>
    </div>
    <figure class="alt-foto">${img('/media/galeri-tanisma-kahvaltisi-salon.jpg', 'Tanışma kahvaltısı')}<figcaption>Tanışma kahvaltısı, Ekim 2025 · 65 katılımcı</figcaption></figure>
    <p class="not">Ayrıntılı döküm: MATRO 2025–2026 Faaliyet Raporu.</p>`,
    { cls: 'p-sezon2', bolum: 'Geçen sezon' },
  );
}

// ---------- 25. Toplumsal etki ----------
{
  const okul = S.filter((f) => f.bolum === 'okullar');
  page(
    `<figure class="ust-foto">${img(D.fotolar.toplum, 'Tugay Ciner İlköğretim Okulu öğrencileri atölyede')}</figure>
    <div class="icerik">
      ${kicker('Toplumsal etki', 'volt')}<h2 class="dev">Yeni nesil mühendisler</h2>
      <div class="toplum">
        <div class="toplum-sayi"><b>${sayi(okulKatilim)}</b><span>öğrenciye 2025–2026'da ulaştık</span><b>${esc(kardesOkul.value + kardesOkul.suffix)}</b><span>Kardeş Okul Projesi kapsamında eğitim ve malzeme desteği</span></div>
        <ul class="duz">${okul.map((f) => `<li><b>${esc(f.ad)}</b><span>${esc(f.yer)} · ${sayi(f.katilim)} öğrenci</span></li>`).join('')}</ul>
      </div>
    </div>`,
    { cls: 'p-toplum', bolum: 'Toplumsal etki', tocBaslik: 'Toplumsal etki' },
  );
}

// ---------- 26. Sanayi ağı ----------
page(
  `<figure class="ust-foto kisa">${img(D.fotolar.sanayi, 'Turkish Technic hangarında MATRO')}</figure>
  <div class="icerik">
    ${kicker('Sanayi ağı', 'volt')}<h2 class="dev">Kapısını açan<br />${kurumlar.length} kurum</h2>
    <p class="lead">${esc(geziler.data.summary)}</p>
    <ul class="kurum-bulut">${kurumlar.map((k) => `<li>${esc(k)}</li>`).join('')}</ul>
    <div class="serit">${D.fotolar.sanayiSerit.map((f) => `<figure>${img(f.foto, f.not)}<figcaption>${esc(f.not)}</figcaption></figure>`).join('')}</div>
  </div>`,
  { cls: 'p-sanayi', bolum: 'Sanayi ağı', tocBaslik: 'Sanayi ağı' },
);

// ---------- 27. Basında biz ----------
page(
  `${kicker('Basında biz')}<h2 class="dev">Haberlerde<br />MATRO</h2>
  <p class="lead">${esc(basin.intro)}</p>
  <div class="basin">${basin.items
    .map((b) => `<article><figure>${img(b.image, b.outlet)}</figure><p class="kicker">${esc(b.outlet)} · ${esc(b.date.slice(0, 4))}</p><h3>${esc(b.headline)}</h3></article>`)
    .join('')}</div>`,
  { cls: 'p-basin', bolum: 'Basında biz', tocBaslik: 'Basında biz' },
);

// ---------- 28. Sponsorluk açılış: neden ----------
page(
  `<figure class="tam-kapak">${img(D.fotolar.sponsorlukAcilis, 'MATROVER ekibi final alanında')}</figure>
  <div class="bolum-acilis">
    <span class="bolum-no">02</span>
    <div>${kicker('Bölüm', 'volt')}<h2>Sponsorluk</h2>
    <p>${esc(paket.hero.description)}</p>
    <ol class="neden">${D.neden.map((n, i) => `<li><span>${String(i + 1).padStart(2, '0')}</span><div><h3>${esc(n.baslik)}</h3><p>${esc(n.metin)}</p></div></li>`).join('')}</ol></div>
  </div>`,
  { cls: 'p-bolum dark', footer: false, tocBaslik: 'Sponsorluk' },
);

// ---------- 29. Desteğiniz nereye gider ----------
page(
  `${kicker('Destek türleri')}<h2 class="dev">Desteğiniz<br />nereye dönüşür?</h2>
  <div class="destek-turleri">${paket.supportTypes.map((s) => `<div><h3>${esc(s.title)}</h3><p>${esc(s.description)}</p></div>`).join('')}</div>
  ${kicker('Harcama kalemleri', 'volt')}
  <div class="harcama">${D.harcama.map((h, i) => `<div><span>${String(i + 1).padStart(2, '0')}</span><h3>${esc(h.baslik)}</h3><p>${esc(h.metin)}</p></div>`).join('')}</div>
  <p class="not">${esc(paket.officialForm.note)}</p>
  <figure class="alt-foto">${img(D.fotolar.atolye, 'MATROBOT ekibi TEKNOFEST alanında')}<figcaption>MATROBOT ekibi TEKNOFEST final alanında</figcaption></figure>`,
  { cls: 'p-destek', bolum: 'Sponsorluk' },
);

// ---------- 30–31. Paketler ----------
{
  const P = paket.packages;
  const norm = (b) => b.replace('yılda iki kez ', '').replace(/^Yarışmayla ilgili b/, 'B');
  const satirlar = [];
  for (const p of P) for (const b of p.benefits) if (!satirlar.includes(norm(b))) satirlar.push(norm(b));
  const hucre = (p, s) => {
    const b = p.benefits.find((x) => norm(x) === s);
    if (!b) return '<td class="yok">–</td>';
    return `<td class="var">${b.includes('yılda iki kez') ? 'Yılda 2 kez' : '<i></i>'}</td>`;
  };
  page(
    `${kicker('Sponsorluk kademeleri')}<h2 class="dev">Dört kademe,<br />tek hedef.</h2>
    <div class="paketler">${P.map(
      (p) => `<article class="paket ${p.name.toLocaleLowerCase('tr')} ${p.highlight ? 'one' : ''}">
        <p class="kicker">${esc(p.name)}</p><h3>${esc(p.range)}</h3>
        <ul>${p.benefits.map((b) => `<li>${esc(b)}</li>`).join('')}</ul>
      </article>`,
    ).join('')}</div>`,
    { cls: 'p-paket', bolum: 'Sponsorluk', tocBaslik: 'Sponsorluk kademeleri' },
  );
  page(
    `${kicker('Karşılaştırma')}<h2>Kademelere göre haklar</h2>
    <table class="matris"><thead><tr><th></th>${P.map((p) => `<th class="${p.name.toLocaleLowerCase('tr')}">${esc(p.name)}<span>${esc(p.range)}</span></th>`).join('')}</tr></thead>
    <tbody>${satirlar.map((s) => `<tr><td>${esc(s)}</td>${P.map((p) => hucre(p, s)).join('')}</tr>`).join('')}</tbody></table>
    <p class="not">${esc(paket.packagesNote)}</p>
    <p class="kicker volt gor-k">Logonuz nerede görünür?</p><div class="gorunurluk">${D.fotolar.gorunurluk.map((g) => `<figure>${img(g.foto, g.not)}<figcaption>${esc(g.not)}</figcaption></figure>`).join('')}</div>`,
    { cls: 'p-matris', bolum: 'Sponsorluk' },
  );
}

// ---------- 32. Süreç ----------
page(
  `${kicker('Süreç')}<h2 class="dev">${esc(paket.officialForm.title)}</h2>
  <p class="lead">${esc(paket.officialForm.description)}</p>
  <ol class="surec">${paket.officialForm.steps.map((s, i) => `<li><span>${i + 1}</span><h3>${esc(s.title)}</h3><p>${esc(s.description)}</p></li>`).join('')}</ol>
  <div class="iletisim-kutu">
    <div>${kicker('Sponsorluk ekibi', 'volt')}<h3>${esc(D.kapanis.eposta)}</h3><p>Sponsorluk ekibimiz destek alanını ve kademeyi sizinle birlikte belirler; resmî form ve bağış bilgilerini görüşmenin ardından iletir.</p></div>
    <div class="qr"><img src="gorseller/qr-sponsorluk.svg" alt="btumatro.com/sponsorluk" /><span>btumatro.com/sponsorluk</span></div>
  </div>`,
  { cls: 'p-surec', bolum: 'Sponsorluk', tocBaslik: 'Sponsorluk süreci' },
);

// ---------- 33–34. Sponsorlar ----------
{
  const grup = PK.map((k) => ({ k, list: aktifSponsor.filter((s) => s.package === k) })).filter((g) => g.list.length);
  page(
    `${kicker('Teşekkür')}<h2 class="dev">${aktifSponsor.length} destekçi,<br />tek atölye.</h2>
    <p class="lead">${esc(sponsors.intro)}</p>
    ${grup
      .map(
        (g) => `<div class="sp-grup ${g.k.toLocaleLowerCase('tr')}"><p class="kicker">${esc(g.k)} · ${g.list.length}</p><div class="sp-logolar">${g.list
          .map((s) => (s.logo ? `<figure><img src="../../public${esc(s.logo)}" alt="${esc(s.name)}" /><figcaption>${esc(s.name)}</figcaption></figure>` : `<figure class="yazi"><span>${esc(s.name)}</span></figure>`))
          .join('')}</div></div>`,
      )
      .join('')}`,
    { cls: 'p-sponsor', bolum: 'Sponsorlarımız', tocBaslik: 'Sponsorlarımız' },
  );
  page(
    `${kicker('Geçmiş dönemler')}<h2>Bugüne kadar yanımızda olanlar</h2>
    <ul class="kurum-bulut">${sponsors.past.map((s) => `<li>${esc(s)}</li>`).join('')}</ul>
    ${kicker('2026–2027 hedeflerimiz', 'volt')}
    <div class="hedef">
      <figure>${img(D.fotolar.hedefler, 'Tarımsal İKA takımı')}</figure>
      <div><h3>${esc(about.goals2026.title)}</h3><p>${esc(about.goals2026.description)}</p>
      <ol>${about.goals2026.items.map((g, i) => `<li><span>${String(i + 1).padStart(2, '0')}</span>${esc(g)}</li>`).join('')}</ol></div>
    </div>`,
    { cls: 'p-hedef', bolum: 'Hedefler', tocBaslik: '2026–2027 hedefleri' },
  );
}

// ---------- 35. Kapanış çağrısı ----------
page(
  `<figure class="kapanis-foto">${img(D.fotolar.kapanis, 'MATROVER ekibi TEKNOFEST alanında')}</figure>
  <div class="kapanis">
    ${kicker('Davet', 'volt')}
    <h2 class="dev">${esc(D.kapanis.baslik)}</h2>
    <p class="lead">${esc(D.kapanis.metin)}</p>
    <dl>
      <dt>Sponsorluk</dt><dd>${esc(D.kapanis.eposta)}</dd>
      <dt>Web</dt><dd>btumatro.com</dd>
      <dt>Sosyal medya</dt><dd>@btumatro · Instagram, LinkedIn, YouTube</dd>
      <dt>Atölye</dt><dd>${esc(site.contact.workshop)}</dd>
      <dt>Adres</dt><dd>${esc(site.contact.address)}</dd>
    </dl>
  </div>`,
  { cls: 'p-kapanis dark', bolum: 'İletişim' },
);

// ---------- 36. Arka kapak ----------
page(
  `<div class="arka">
    <img class="arka-logo" src="../../public/logo-matro-beyaz.png" alt="MATRO" />
    <p class="arka-slogan">${esc(home.hero.title.replace('\n', ' '))}</p>
    <div class="arka-alt">
      <div class="qr"><img src="gorseller/qr-btumatro.svg" alt="btumatro.com" /></div>
      <p>${esc(site.university)}<br />${esc(site.fullName)}<br /><b>btumatro.com</b></p>
    </div>
  </div>`,
  { cls: 'p-arka dark', footer: false },
);

// ---------- İçindekiler + editörden ----------
pages[TOC_YER] = `<section class="page p-toc">
  <div class="toc-ust">
    <div>
      ${kicker('Bu sayıda')}
      <ol class="toc">${toc.map((t) => `<li><span class="toc-p">${String(t.sayfa).padStart(2, '0')}</span><span>${esc(t.baslik)}</span></li>`).join('')}</ol>
    </div>
    <div class="editor">
      ${kicker(D.editor.baslik, 'volt')}
      ${D.editor.paragraflar.map((p, i) => `<p class="${i === 0 ? 'ilk' : ''}">${esc(p)}</p>`).join('')}
      <p class="imza">${esc(D.editor.imza)}</p>
    </div>
  </div>
  <figure class="toc-foto">${img('/media/galeri-turkish-technic-workshop-grup.jpg', 'Turkish Technic Workshop katılımcıları')}<figcaption>Turkish Technic Workshop, BTÜ Mavi Salon, Mart 2026</figcaption></figure>
  <footer class="run"><span class="run-m">MATRO</span><span>${esc(D.sayi)} · ${esc(D.donem)}</span><span class="run-b">İçindekiler</span><span class="pn">02</span></footer>
</section>`;

const html = `<!doctype html>
<html lang="tr"><head><meta charset="utf-8" />
<title>MATRO Sponsorluk Dergisi ${D.donem}</title>
<link rel="stylesheet" href="dergi.css" />
</head><body>
${pages.join('\n')}
</body></html>`;
fs.writeFileSync(path.join(DIR, 'dergi.html'), html);
console.log(`HTML yazıldı: ${pages.length} sayfa`);
if (pages.length % 4) console.warn(`Uyarı: sayfa sayısı (${pages.length}) 4'ün katı değil.`);
if (process.argv.includes('--html')) process.exit(0);

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
const tab = await browser.newPage();
await tab.goto(pathToFileURL(path.join(DIR, 'dergi.html')).href, { waitUntil: 'networkidle0' });
await tab.evaluate(async () => {
  await document.fonts.ready;
});
const eksik = await tab.evaluate(() => [...document.images].filter((i) => !i.naturalWidth).map((i) => i.getAttribute('src')));
if (eksik.length) {
  console.error('Yüklenemeyen görseller:', eksik);
  process.exit(1);
}
// Taşma denetimi: içeriği sayfa kutusundan dışarı çıkan öğeleri raporla.
const tasma = await tab.evaluate(() =>
  [...document.querySelectorAll('.page')].flatMap((p, i) => {
    const pb = p.getBoundingClientRect();
    const foot = p.querySelector('.run');
    const sinir = foot ? foot.getBoundingClientRect().top : pb.bottom;
    return [...p.querySelectorAll('p, li, h2, h3, h4, tr, figure')]
      .filter((e) => !e.closest('.run') && e.getBoundingClientRect().bottom > sinir + 1 && e.getBoundingClientRect().height > 0)
      .slice(0, 2)
      .map((e) => `sayfa ${i + 1}: <${e.tagName.toLowerCase()} class="${e.className}"> ${e.textContent.trim().slice(0, 40)}`);
  }),
);
if (tasma.length) console.warn('Taşma:\n  ' + tasma.join('\n  '));
const out = path.join(DIR, 'matro-sponsorluk-dergisi-2026-2027.pdf');
await tab.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
await browser.close();
console.log('PDF:', path.relative(ROOT, out));
