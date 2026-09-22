# DESIGN.md — MATRO Dergi, Sayı 01

Üniversitenin tüm öğrencilerine yönelik, kuşe kağıda basılacak genel bilim-teknoloji ve
kampüs dergisi. MATRO faaliyetleri omurgadır; gündem, yapay zekâ, "nasıl çalışır",
kampüs/kariyer rehberleri, röportajlar ve keyif sayfaları da vardır.

- Yazılar: bu klasördeki `NN-*.md` dosyaları (içerik planı: `00-icerik-plani.md`)
- Stil: `ornek-baski/dergi.css`
- Üretim betiği: `scripts/build-dergi-sayi-01.mjs`
- Çıktı: `ornek-baski/dergi.html`, `ornek-baski/matro-dergi-sayi-01-ornek.pdf`

```bash
node scripts/build-dergi-sayi-01.mjs
```

Mevcut PDF bir **örnek baskıdır**: röportaj cevapları, künye adları ve foto-röportaj alt
yazıları lorem ipsum ile doldurulur. Ortak marka kuralları kök `DESIGN.md` ve `AGENTS.md`'de.

---

## 1. Yazı dosyası sözleşmesi

Her yazı bir Markdown dosyasıdır. Betik bunları pandoc ile HTML'e çevirir ve aşağıdaki
kalıpları tanır:

| Kalıp | Anlamı | Baskıda |
|---|---|---|
| `# Başlık` | Yazının başlığı ve içindekiler girdisi | Makale başlığı |
| `> **Dizgi notu** ...` | Tasarımcıya not (sayfa, görsel, kaynak) | **Basılmaz** |
| `*Dizgi uyarısı: ...*` | Teyit edilmesi gereken bilgi | **Basılmaz** |
| `> *[Kaptan kontrolü ...]*` | Takıma sorulacak yer | **Basılmaz** |
| `**Spot:** ...` | Giriş paragrafı | Barlow 12 pt, iki sütunu kaplar |
| `> **Kutu — Başlık:** ...` | Kenar kutusu | Açık zemin, volt sol çizgi |
| `> **İnfografik ...:**`, `Diyagram`, `Rakam şeridi`, `Zaman çizelgesi` | Çizilecek grafik | Kesikli çerçeveli yer tutucu |
| `*Görsel: ad1, ad2 (tam sayfa)*` | `public/media` görsel adları | Fotoğraf bloğu; 2–4 görsel yan yana, "tam sayfa" / "yarım sayfa" büyük |
| `Kaynak:` / `Kaynaklar:` | Kaynak satırı | Küçük punto, sayfa altı |
| `[Ad Soyad]` | Henüz belli olmayan kişi | "Lorem Ipsum" |
| `---` | Bölüm ayırıcı | Gündem ve yapay zekâda yeni sayfa |

Yazım kuralları: Rakamlar kaynaklı yazılır ve kaynak satırı eklenir. Kaynaklar arası
tutarsızlıkta her iki kaynağın desteklediği alt sınır kullanılır ve `Dizgi uyarısı`
bırakılır. Röportaj cevapları uydurulmaz. Gündem sayfaları yazıldığı tarihi belirtir
ve baskıdan önce güncellenir. Başka kurumların fotoğrafları kullanılmaz; gündem ve
yapay zekâ sayfaları infografik ve tipografiyle tasarlanır.

## 2. Sayfa ve akış

Diğer iki yayından farklı olarak bu dergi **akışkan** dizilir: metin Chrome'un sayfalı
medya desteğiyle sayfalara kendiliğinden bölünür.

| Özellik | Değer |
|---|---|
| Ebat | 210 × 297 mm |
| Kenar boşluğu | `@page { margin: 16mm 15mm 19mm }` |
| Altbilgi | `@bottom-left` "MATRO DERGİ · SAYI 01 · EKİM 2026", `@bottom-right` `counter(page)` |
| Tam sayfalar | `@page tam` (kenar boşluksuz, altbilgisiz): kapak, bölüm açılışları, kapak dosyası açılışı, ilan, arka kapak |
| Sayfa sonu | Her makale ve tam sayfa öğe yeni sayfada başlar (`break-before: page`) |
| Gövde | İki sütun, 7 mm aralık; editör yazısı tek, sözlük üç sütun |
| Sayfa sayısı | 4'ün katına arka kapaktan önce "Markanız burada" ilan sayfalarıyla tamamlanır |

**İçindekiler iki geçişte hesaplanır:** Her başlığın yanına görünmez bir işaret
(`ZQnnQZ`) konur. İlk PDF'in metninde bu işaretlerin geçtiği sayfa `pdftotext` ile
bulunur, ikinci geçişte numaralar içindekilere yazılır.

## 3. Renk ve tipografi

Faaliyet raporu ve sponsorluk dergisiyle aynı token'lar (`--ink`, `--text`, `--muted`,
`--line`, `--mist`, `--volt`, `--volt-dark`, `--medal`) ve aynı üç font aile.
Türkçe karakter kuralı geçerli; oklar (→) tipografik `›` ile değiştirilir, yıldız (★)
başlıklardan çıkarılır, çünkü font alt kümelerinde yoklar.

| Öğe | Değer |
|---|---|
| Masthead | "MATRO" Barlow 900 118 pt + "DERGİ" 24 pt, 0,3 em, volt |
| Bölüm açılışı | Numara 90 pt + başlık 64 pt, Barlow 900 |
| Makale başlığı (`.m-bas h1`) | Barlow 900 30 pt, altında 0,5 mm siyah çizgi |
| Ara başlık (`h2`) | Barlow 800 20 pt, iki sütunu kaplar |
| Gövde | Inter 8,9 pt / 1,5, heceleme açık |
| Röportaj sorusu | Barlow 800 10,5 pt, volt |
| Çekme alıntı | Barlow 700 20 pt, volt sol çizgi |

## 4. Bölümler

| No | Bölüm | Açılış fotoğrafı | İçerik |
|---|---|---|---|
| — | Açılış | — | Kapak, iç kapak (platin sponsorlar + ilan örneği), içindekiler + künye, editörden, kısa kısa |
| 01 | Gündem | LODOS TEKNOFEST | TEKNOFEST 2026, havacılık ve uzay, dünyada robotlar, uzay kısa haberleri, gezdiğimiz yerler |
| 02 | Yapay Zekâ | (koyu, fotoğrafsız) | Stanford AI Index, ajanlar ve fiziksel yapay zekâ, öğrenci rehberi |
| — | Kapak dosyası | ZEMHERİ | Bir aracın doğuşu + 2026 finalleri |
| 03 | MATRO | LUNA İKA arazi testi | Sezon dosyası, takımlar, kaptan röportajı, atölyede bir gün, başarı arşivi |
| 04 | Nasıl Çalışır? | İSS | AUV, sürü İHA, karıştırmaya karşı haberleşme, PLC |
| 05 | Kampüs ve Kariyer | Tanışma toplantısı | TEKNOFEST dosyası, Bursa ekosistemi, uzay, kampüs rehberi, ilk yıl, yeni üyeler, mezun röportajı |
| 06 | Keyif | Bahar pikniği | Çizgi izleyen robot, öneriler, sözlük, bulmaca |
| — | Kapanış | — | Basında MATRO, sponsor duvarı, sponsor ol, bize katıl (başvuru QR'ları), ilan, arka kapak |

## 5. Özel bileşenler

- **Bulmaca:** `14-bulmaca.md` betikle üretilir; her kelimenin ızgarada tam bir kez
  geçtiği doğrulanır. Izgara JetBrains Mono 15 pt, cevap anahtarı sayfa altında ters.
- **Kod bloğu:** koyu zemin, mono 7 pt, iki sütunu kaplar, bölünmez.
- **Takım kartları:** 72 mm fotoğraf + metin; rozet sol üstte `--medal`.
- **Foto-röportaj (`.gun`):** 4 sütun fotoğraf ızgarası, saat damgalı alt yazı.
- **QR kodlar:** başvuru formları, sponsorluk ve site için `qrcode` paketiyle SVG olarak
  sayfaya gömülür.

## 6. Basıma hazırlık

`00-icerik-plani.md`'deki baskı şartnamesi geçerlidir: 80 sayfa Amerikan cilt (veya
64 sayfa tel dikiş), 130–135 gr mat kuşe iç, 300–350 gr kapak. Örnek PDF ofis
baskısı içindir. Matbaa için: Drive orijinal fotoğrafları (tam sayfa ~2550 × 3550 px),
3 mm taşma, kesim işaretleri, CMYK, PDF/X ve lorem ipsum alanlarının gerçek içerikle
değiştirilmesi gerekir.
