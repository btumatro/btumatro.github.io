# DESIGN.md — MATRO Sponsorluk Dergisi 2026–2027 (Sayı 01)

Sponsor adaylarına verilen, dergi formatında sponsorluk dosyası. A4 dikey, 36 sayfa.
İki bölüm: topluluğu tanıtan dergi kısmı ve sponsorluk kısmı.

- Stil: `dergi.css`
- Üretim betiği: `scripts/build-sponsorluk-dergisi.mjs`
- Çıktı: `dergi.html`, `matro-sponsorluk-dergisi-2026-2027.pdf`

```bash
node scripts/build-sponsorluk-dergisi.mjs          # HTML + PDF
node scripts/build-sponsorluk-dergisi.mjs --html   # yalnız HTML
```

Ortak marka kuralları kök `DESIGN.md` ve `AGENTS.md`'dedir.

---

## 1. İçerik kaynakları

Olgusal içeriğin tamamı sitenin veri dosyalarından okunur; sitede bir bilgi
değiştiğinde dergi yeniden üretilerek güncellenir.

| Kaynak | Sayfalar |
|---|---|
| `src/data/about.json` | Biz kimiz, vizyon/misyon/değerler, tarihçe, 2026–2027 hedefleri |
| `src/data/achievements.json` | Rakamlar, 2026 finalleri, başarı arşivi |
| `src/data/home.json` | Finalist yarışmacı, ilk 10 ve Kardeş Okul rakamları, arka kapak sloganı |
| `src/content/teams/*.md` | 13 takım profili (metin, başarılar, odak alanları, rozet) |
| `src/content/activities/*.md` | Eğitim programı, teknik gezi kurumları |
| `src/data/sponsorship.json` | Destek türleri, kademeler, haklar, resmî süreç |
| `src/data/sponsors.json` | Sponsor logo duvarı, geçmiş sponsorlar |
| `src/data/basinda-biz.json` | Basında MATRO |
| `docs/faaliyet-kitapcigi-2025-26/icerik.json` | 2025–2026 sezon özeti |
| `icerik.json` (bu klasör) | **Yalnızca dergiye özel metin ve seçimler:** kapak, editör yazısı, fotoğraf seçimleri, takım sayfalarının foto/ek görselleri, final yerleri, "neden destek", harcama kalemleri, kapanış |

Kurallar:

- Derece, birincilik, uluslararası başarı ve 2026 finalist sayıları sitedeki
  `achievementSummary()` ile aynı düzenli ifadelerle hesaplanır; iki yerde farklı rakam çıkmaz.
- **Sponsorların bireysel destek tutarları gösterilmez.** Kademe fiyat aralıkları sitede
  yayında olduğu için gösterilir.
- Resmî BTÜ sponsorluk formu konmaz; süreç "önce iletişime geçin" akışıyla anlatılır.
- Editör yazısı kişi adıyla değil "MATRO Yönetim Kurulu" imzasıyla yayımlanır.
- Sponsorluk dosyasında onay izlenimi verebilecek fotoğraflar (ör. ünlü ziyaretçilerle
  özçekimler) ve kupa vitrini fotoğrafları kullanılmaz.

## 2. Sayfa ve ızgara

| Özellik | Değer |
|---|---|
| Ebat | 210 × 297 mm, `@page { margin: 0 }` |
| Kenar boşluğu | Üst 15 mm, yan 16 mm (`--px`), alt 18 mm |
| Taşan öğeler | `.ust-foto`, `.tam-kapak`, `.takim-hero` negatif kenar boşluğuyla sayfa kenarına taşar |
| Altbilgi (`.run`) | 8 mm'de; "MATRO" (Barlow 900) · sayı · dönem · bölüm adı (volt) · sayfa no |
| Sayfa sayısı | 36 (4'ün katı); değişirse betik uyarır |

Betik PDF'ten önce taşma denetimi yapar: altbilgi çizgisinin altına inen öğeyi
`Taşma: sayfa N` olarak raporlar. Uyarı varken PDF paylaşılmaz.

## 3. Renk

Faaliyet raporuyla aynı temel palet, kademe renkleri eklenmiş:

| Token | Değer | Kullanım |
|---|---|---|
| `--ink` / `--ink-2` / `--text` | `#0b1012` / `#1c2427` / `#2a3438` | Başlık, vurgu, gövde |
| `--muted` / `--line` / `--mist` | `#5d6a70` / `#d8dddf` / `#f3f2ec` | Etiket, ayırıcı, açık kutu |
| `--volt` / `--volt-dark` | `#0f8c86` / `#75d5d0` | Marka vurgusu (açık / koyu zemin) |
| `--medal` | `#c0840f` | Derece, Altın kademe |
| `--silver` | `#8a979b` | Gümüş kademe |
| `--bronze` | `#a8643a` | Bronz kademe |

Platin kademe koyu zemin + volt ile gösterilir. Kademe renkleri yalnızca sponsorluk
sayfalarında, kademe ayrımı için kullanılır.

## 4. Tipografi

Barlow (500–900 ve 500 italik), Inter, JetBrains Mono; `latin` + `latin-ext`
çiftleri ayrı `unicode-range` ile (bkz. faaliyet raporu DESIGN.md, Türkçe karakter kuralı).

| Öğe | Değer |
|---|---|
| Masthead "MATRO" | Barlow 900 128 pt, −0,04 em |
| Kapak başlığı | Barlow 800 40 pt |
| Dev başlık (`h2.dev`) | Barlow 900 40 pt / 0,92 |
| Sayfa başlığı (`h2`) | Barlow 800 26 pt |
| Takım adı (`.takim-ad`) | Barlow 900 44 pt (yarım sayfada 28 pt) |
| Büyük rakam | Barlow 900 50–96 pt |
| Alıntı / vizyon | Barlow 600 13,5–16 pt |
| Gövde | Inter 9,2 pt / 1,48 |
| Etiket (`.kicker`) | JetBrains Mono 600 6,6 pt, 0,18 em, BÜYÜK HARF |
| Editör ve "Biz kimiz" açılışı | Barlow 900 volt başharf (drop cap) |

## 5. Sayfa planı

| Sayfa | Tür | Not |
|---|---|---|
| 1 | Kapak | Tam taşmalı fotoğraf, masthead, sayı şeridi, 3 manşet |
| 2 | İçindekiler + editörden | Numaralar betikte hesaplanır |
| 3–4 | Biz kimiz | Metin + tam genişlik fotoğraf; vizyon/misyon, 4 değer, künye şeridi |
| 5–6 | Tarihçe | 5 + 4 madde, ikinci sayfada fotoğraf ve alıntı |
| 7 | Rakamlarla MATRO | Dev derece sayısı + 5 rakam, koyu sezon şeridi |
| 8 | Kapak konusu | 2026 finalleri ve final yerleri |
| 9 | Bölüm 01 açılışı (koyu) | Takım dizini |
| 10–16 | Tam sayfa takım profili ×7 | Hero fotoğraf + rozet, başlık/alt takımlar, metin + başarı kutusu, 2 ek fotoğraf |
| 17–19 | Yarım sayfa takım ×6 | Sayfa başına 2 takım |
| 20–21 | Başarı arşivi | Tüm dereceler tablo hâlinde; birincilik ve dünya dereceleri altın renkte |
| 22–27 | Atölye/eğitim, geçen sezon (2), toplumsal etki, sanayi ağı, basın | |
| 28 | Bölüm 02 açılışı (koyu) | "Neden destek" 5 madde |
| 29–33 | Destek türleri, kademeler, karşılaştırma tablosu + "logonuz nerede görünür", süreç + QR | |
| 34–36 | Sponsor logo duvarı, geçmiş sponsorlar + hedefler, kapanış (koyu), arka kapak | |

## 6. Bileşenler

- **Takım hero (`.takim-hero`):** Tam genişlik 104 mm fotoğraf; rozet sağ üstte `--medal`.
  Odak noktası `icerik.json`'daki `fotoKonum` ile ayarlanır.
- **Başarı listesi (`.takim-basari`):** Derece içeren satırlar (1–3., dünya, "en iyi")
  altın nokta ve kalın yazıyla vurgulanır.
- **Etiketler (`.etiket`):** Odak alanları, mono 6,3 pt, ince çerçeveli kapsül.
- **Kademe kartı (`.paket`):** 2,4 mm üst renk şeridi; Platin koyu zeminli ve öne çıkar.
- **Karşılaştırma tablosu (`.matris`):** Satırlar kademelerdeki hakların birleşimi;
  volt nokta = var, çizgi = yok, "Yılda 2 kez" gibi farklar metinle.
- **Logo duvarı (`.sp-grup`):** Kademe renginde üst çizgi; Platin logolar daha büyük;
  logosu olmayan sponsor kesikli daire içinde adıyla.
- **QR:** `gorseller/qr-sponsorluk.svg` ve `qr-btumatro.svg`, `qrcode` paketiyle üretilir,
  beyaz kutuda en az 25 mm.

## 7. Görsel kuralları

- Fotoğraflar `public/media`'dan; takım sayfaları için en yüksek çözünürlüklü ve
  içeriği doğrulanmış kareler seçilir (`icerik.json` → `takimlar`).
- Gerçek kişi ve kurum fotoğrafı yalnızca kendi etkinliklerimizden. Başka kurumların
  tanıtım görselleri kullanılmaz.
- Matbaaya gitmeden önce büyük kullanılan fotoğrafların Drive orijinalleri alınmalı.
