# DESIGN.md — MATRO Faaliyet Raporu 2025–2026

A4 dikey, kitap düzeninde basılı faaliyet raporu. Üniversiteye sunulan Word raporunun
(`MATRO Faaliyet Raporu 25-26.docx`) tasarlanmış, paylaşılabilir hâli.

- Stil: `kitapcik.css`
- Üretim betiği: `scripts/build-faaliyet-kitapcigi.mjs` (HTML + PDF)
- Çıktı: `kitapcik.html`, `matro-faaliyet-raporu-2025-2026.pdf`

```bash
node scripts/build-faaliyet-kitapcigi.mjs          # HTML + PDF
node scripts/build-faaliyet-kitapcigi.mjs --html   # yalnız HTML (tarayıcıda incelemek için)
```

Ortak marka kuralları (renk anlamları, emoji yasağı, kişisel veri) kök `DESIGN.md` ve
`AGENTS.md`'dedir. Bu dosya yalnızca bu yayına özgü kararları anlatır.

---

## 1. İçerik kaynakları

| Dosya | İçerik | Kim düzenler |
|---|---|---|
| `icerik.json` | Faaliyet künyeleri: ad, bölüm, tarih, yer, katılımcı, bütçe, araç gereç, iş birliği, fotoğraf, kısa özet; bölüm tanımları; projeler; başarılar; "Bir aracın doğuşu"; final yerleri; "Sahadan kareler" | Rapordaki veriye göre |
| `metinler.json` | Her kartın gövde metni. Anahtar: faaliyet `ad`, başarı `baslik` veya proje `takim` | Editör |
| `src/data/*.json` | Topluluk adı, kişiler, tarihçe, vizyon/misyon, başarı arşivi, sponsorlar, basın | Site ile ortak |
| `src/content/teams/*.md` | Takım adı, alt başlık, rozet, kapak fotoğrafı | Site ile ortak |
| `gorseller/` | Rapordaki ama sitede olmayan yüksek çözünürlüklü görseller, QR | — |

Kurallar:

- **Rakam elle yazılmaz.** Faaliyet sayısı, toplam katılım, bütçe toplamları, bölüm
  rakamları, derece/birincilik sayıları ve içindekiler sayfa numaraları betikte hesaplanır.
- **Metin kaynağa dayanır.** `metinler.json`'a yalnızca rapor, sitedeki haber veya takım
  sayfasında geçen bilgi yazılır. Süsleme cümlesi ("kariyer planı netleşti" gibi) eklenmez.
- **Eksik içerik derlemeyi durdurur.** Fotoğrafı veya metni olmayan faaliyet varsa betik hata verir.
- **Bütçe** rapordaki "Harcanan bütçe" satırıdır; raporda "-" olan alan kartta "–" görünür.
- Tahmini tarihler `icerik.json`'da `tarihNotu` alanıyla işaretlidir; kesinleşince düzeltilir.

## 2. Sayfa ve ızgara

| Özellik | Değer |
|---|---|
| Ebat | 210 × 297 mm, `@page { margin: 0 }` (kenar boşlukları sayfa kutusunda) |
| Sağ sayfa (tek numara) | padding 21 / 15 / 21 / **21 mm** (cilt payı solda) |
| Sol sayfa (çift numara) | padding 21 / **21** / 21 / 15 mm (cilt payı sağda) |
| Tam sayfa (`.tam`) | Kenar boşluksuz: kapak, bölüm iç kapakları, arka kapak |
| Üst bilgi (`.ust`) | 10 mm'de; bölüm adı volt, yayın adı gri; dış kenara hizalı |
| Sayfa numarası (`.pn`) | Alt dış köşe, 9 mm; Barlow 800 11 pt + 10 mm volt çizgi |
| Toplam sayfa | 4'ün katı (tel dikiş). Betik gerekirse "Sahadan kareler", "Başarı arşivi", "Basında MATRO" ve en son "Notlar" sayfası ekler |

Sayfa içeriği `.icerik` kutusunda akar ve `overflow: hidden`'dır. PDF basılmadan önce her
sayfa ve kart taşma için ölçülür; taşma varsa betik `Taşma: sayfa N` uyarısı verir.
**Uyarı varken PDF paylaşılmaz.**

## 3. Renk

| Token | Değer | Kullanım |
|---|---|---|
| `--ink` | `#0b1012` | Başlık metni, koyu sayfa zemini, kalın ayırıcılar |
| `--ink-2` | `#1c2427` | Vurgulu gövde, spot cümleler |
| `--text` | `#2c363a` | Gövde metni |
| `--muted` | `#637177` | Etiketler, künye başlıkları, notlar |
| `--line` | `#d9dee0` | İnce ayırıcılar (0,25 mm) |
| `--mist` | `#f3f3ef` | Künye şeridi, açık kutular |
| `--volt` | `#0f8c86` | Marka vurgusu: kart numarası, bölüm numarası, grafik, bağlantı niteliğindeki etiketler |
| `--volt-light` | `#75d5d0` | Koyu zemin üstünde volt |
| `--medal` | `#c0840f` | Yalnızca derece/ödül rozetleri |

Sitedeki anlam korunur: yeni vurgu rengi icat edilmez. Baskıda okunaklılık için sitedeki
açık camgöbeği yerine koyu `--volt` kullanılır; açık ton sadece koyu zeminde.

## 4. Tipografi

Üç aile, `node_modules/@fontsource*` dosyalarından yerel yüklenir (CDN yok):

- **Barlow** (500–900) — başlıklar, büyük rakamlar, kart numaraları
- **Inter** (değişken) — gövde
- **JetBrains Mono** (değişken) — etiketler (`.eyebrow`), künye başlıkları, tarih/yıl

**Türkçe karakter kuralı:** Her aile için hem `latin` hem `latin-ext` dosyası ayrı
`@font-face` olarak ve kendi `unicode-range`'iyle tanımlanır. Yalnızca `latin-ext`
yüklenirse ğ/ş/ı dışındaki harfler yedek fonta düşer ve başlıklarda iki font karışır.
Oklar (U+2190–2199) latin aralığına eklidir. Değişiklikten sonra render edilen fontlar
CDP ile ölçülmeli; `Barlow / Inter / JetBrains Mono` dışında aile görünmemeli.

| Öğe | Değer |
|---|---|
| Gövde | Inter 8,6 pt / 1,5 |
| Kart metni | Inter 8 pt / 1,48 |
| Kart spotu (`.k-spot`) | Barlow 600 10 pt |
| Kart başlığı | Barlow 800 16 pt (fotoğraf yandaysa 14 pt) |
| Sayfa başlığı (`.sb h2`) | Barlow 900 32 pt, −0,025 em |
| Bölüm iç kapak başlığı | Barlow 900 46 pt |
| Kapak | Barlow 900 72 pt + dönem 34 pt |
| Etiket (`.eyebrow`) | JetBrains Mono 600 6,2 pt, 0,18 em, BÜYÜK HARF |
| Künye başlığı (`dt`) | JetBrains Mono 5,3 pt, 0,14 em |

## 5. Sayfa türleri

| Tür | Sınıf | İçerik |
|---|---|---|
| Kapak | `.p-kapak.koyu.tam` | Üst %64 fotoğraf (alta doğru koyuya geçiş), MATRO + BTÜ beyaz logoları, başlık, dönem, 4 rakam |
| İç kapak | `.p-ic-kapak` | Renkli iki logo, volt kenar çizgili başlık bloğu, künye tablosu (başkan, danışmanlar, iletişim) |
| Sunuş + içindekiler | `.p-sunus` | Sol: sunuş metni ve imza; sağ: içindekiler (bölümler kalın, alt başlıklar girintili) |
| Topluluk sayfaları | `.p-biz`, `.p-tarihce`, `.p-yapi` | Biz kimiz, 2013–2026 tarihçe, yönetim ekipleri + 13 takım |
| Sezon özeti | `.p-sayilar`, `.p-butce` | Rakam ızgarası, aylık çubuk grafik, dereceler şeridi; bütçe toplamı, bölüm çubukları, en yüksek 8 |
| Bölüm iç kapağı | `.p-bolum.koyu.tam` | Üst %58 fotoğraf, içi boş (kontur) büyük bölüm numarası, başlık, 3 rakam, numaralı liste |
| Kart sayfası | `.p-kart` | Sayfa başına 2 kart; bölümün son kartı tek kalırsa `.kartlar.tek` |
| Özel sayfalar | `.p-dogus`, `.p-finaller` | TEKNOFEST bölümünde "Bir aracın doğuşu" ve "2026 finalleri" |
| Kapanış | `.p-kareler`, `.p-arsiv`, `.p-basin`, `.p-takvim`, `.p-destek`, `.p-hedef`, `.p-not` | Fotoğraf ızgarası, başarı arşivi, basın, takvim, sponsorlar, hedefler, not sayfası |
| Arka kapak | `.p-arka.koyu.tam` | Beyaz logo, slogan, QR, iletişim, BTÜ logosu |

## 6. Faaliyet kartı

Her faaliyet tek numaralı karttır; numaralar bölüm sırası + bölüm içinde tarih sırasıyla
01'den başlar ve bölüm iç kapağı, takvim, bütçe listesi ve kartlarda aynıdır.

```
[No] BÖLÜM · ALT BAŞLIK                 [derece rozeti]
     Faaliyet adı
[Fotoğraf]  Spot cümle (Barlow)
            Gövde metni (metinler.json)
[Tarih | Katılımcı | Bütçe | Yer | Araç gereç | İş birliği]  ← künye şeridi
```

**Fotoğraf yerleşimi oranına göre betikte seçilir; fotoğraf kırpılmaz:**

| Durum | Sınıf | Yerleşim |
|---|---|---|
| Oran ≥ 2,1 (panorama) | `.kart.genis` | Üstte tam genişlik şerit, yükseklik `174 mm / oran` (en fazla 70 mm) |
| Diğer tüm oranlar | `.kart.dikey` | Solda kendi oranında: yükseklik `min(92, 102 / oran)` mm, genişlik `yükseklik × oran`. Metin sağda, künye altta tam genişlik |
| Sayfada tek kart | `.kart.genis` | Üstte tam genişlik, yükseklik `174 / oran` (en fazla 150 mm) |

Metin sığmazsa betik fotoğrafı **oranını koruyarak** 2 mm adımlarla küçültür (en az 34 mm).
Odak noktası gerekirse `icerik.json`'da `gorselKonum` ile verilir (ör. `"78% center"`).

Derece rozeti (`.k-derece`, `--medal`) yalnızca gerçek derecesi olan kartta görünür.
Fotoğraf bir başka kaynaktan veya temsiliyse `gorselNotu` alt yazı olarak basılır.

## 7. Görsel kuralları

- Önce sitedeki `public/media` görselleri; rapora özgü olanlar `gorseller/` altında.
- Görselin içeriği kontrol edilmeden kullanılmaz (AGENTS.md "Kaynak doğrulama").
  Bilinen açık konular: #19 fotoğraftaki okul tabelası, #26 başka takımın afişi, #40
  robot kolu / altı bacaklı robot uyuşmazlığı.
- Sitedeki görseller 1200–1600 px'tir. Ofis baskısı için yeterli, matbaa baskısı için
  büyük kullanılanların Drive orijinalleri gerekir.
- Kupa ve ödül vitrini fotoğrafları kapak/tarihçe gibi büyük alanlarda kullanılmaz.

## 8. Baskı notları

Chrome'un PDF çıktısı `preferCSSPageSize` ve `printBackground` ile alınır. Bu dosya ofis
baskısı ve dijital paylaşım içindir. Matbaa için ayrıca 3 mm taşma payı, kesim işaretleri,
CMYK dönüşümü ve PDF/X hazırlığı gerekir.
