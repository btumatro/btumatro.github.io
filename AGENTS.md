# AGENTS.md — BTÜ MATRO web sitesi

Bu depo Codex, OpenCode, Claude Code veya benzer bir ajan tarafından devralınabilir. Bu dosya
o devir için yazıldı: proje ne, nasıl çalıştırılır, nerede ne var, hangi kurallar sabit,
ve şu an yarım kalan neler var.

## Ne bu proje

Bursa Teknik Üniversitesi **MATRO** (Makine Teknolojileri Robot ve Otomasyon Topluluğu) için
statik bir tanıtım sitesi. **Astro 7** + **Tailwind CSS v4**, **GitHub Pages**'te
(`btumatro.github.io` deposu, `btumatro.com` özel alan adıyla) barındırılıyor. İçerik,
geliştirici olmayan topluluk üyelerinin **Pages CMS** (app.pagescms.org, `.pages.yml` ile
yapılandırılır) üzerinden Türkçe arayüzle düzenleyebileceği şekilde tasarlandı — her yeni alan
hem `src/content.config.ts`/`src/data/*.json` şemasına hem de `.pages.yml`'e eklenmeli.

## Komutlar

```bash
npm install
npm run dev      # localhost:4321
npm run build    # dist/ üretir, aynı zamanda tip/şema hatalarını yakalar — her değişiklikten sonra çalıştır
npm run preview
```

Build hatasız bitmeden commit atma. `.github/workflows/deploy.yml` her `main` push'unda
ve her gün 06:00 TR'de (süresi geçen duyurular düşsün diye) otomatik build+deploy yapar.

## Dizin haritası

- `src/pages/*.astro` — sabit sayfalar (anasayfa, hakkımızda, sponsorluk, iletişim…)
- `src/pages/takimlarimiz/` — `index.astro` (liste) + `[slug].astro` (detay, `getStaticPaths` ile
  `src/content/teams/*.md`'den üretilir)
- `src/content/{teams,activities,haberler}/*.md` — Markdown + frontmatter içerik koleksiyonları;
  şemaları `src/content.config.ts`'de (Zod)
- `src/data/*.json` — sayfa bazlı düz veri (hero metni, sponsorluk paketleri, ekip, vb.)
- `src/components/*.astro` — paylaşılan bileşenler (bkz. DESIGN.md)
- `src/lib/utils.ts` — `url()`, `media()`, `instagramUrl()`, `teamIndex()`/`teamHref()`,
  `publishedNews()`, `packageTone()`/`degreeTone()`, `NAV`
- `public/media/` — tüm görseller (bkz. Görsel kuralları)
- `scripts/*.mjs` — tek seferlik/yeniden çalıştırılabilir üretim betikleri (marka varlıkları,
  OG görseli, sponsor logo kırpma — `node scripts/<isim>.mjs`)
- `.pages.yml` — Pages CMS şeması, Türkçe etiketlerle

## Sabit kurallar (bunları bozma)

- **Site adresi**: `site.config.mjs` → `SITE_URL='https://btumatro.com'`, `BASE_PATH='/'`. Depo adı
  `btumatro.github.io` olduğu için BASE_PATH hep `/` kalmalı — alt sayfa yok.
- **Emoji yasak**: site metninde, duyurularda, commit'lerde hiç emoji kullanılmaz. Kaynak
  materyal (Instagram vb.) emoji içerse bile siteye aktarırken temizlenir.
- **Kişisel veri**: telefon/e-posta gibi bilgiler yalnızca ilgili kişinin açık onayıyla
  yayınlanır. Akademik danışmanın e-postası ve bir mühendisin telefonu bilerek kaldırıldı —
  geri eklenmemeli. Sponsor `logoKaynak` (Drive) bağlantıları da bilerek kaldırıldı.
- **Sponsorluk formu siteye konmaz**: resmî BTÜ sponsorluk formu (PDF) kaldırıldı; süreç artık
  "önce bizimle iletişime geçin" akışı (`sponsorluk.astro` → `sponsorship.json officialForm`).
- **Rakamlar veriden hesaplanır, elle yazılmaz**: `basarilarimiz.astro` başlığı ve sayaçları
  `achievements.json`'dan türetilir (`items.length`, `firstPlaces` regex'i "31.lik" gibi sahte
  eşleşmeleri saymamaya dikkat eder — bkz. dosyadaki yorum).
- **Taslak/süreli içerik**: `haberler` koleksiyonunda `draft: true` hiç yayınlanmaz,
  `expiresOn` geçmişse içerik düşer (`publishedNews()` bunu `src/lib/utils.ts`'de yapar).
- **Görsel/takım/haber ilişkileri**: bir haberin `teams: []` alanı ilgili takım sayfalarına
  bağlanır (dosya adıyla, `tika-ika` gibi); bir takımın `aliases: []` alanı, başarı listesinde
  geçen alt takım adlarını (LODOS, MATROVER…) o takımın sayfasına bağlar (`teamIndex()`/
  `teamHref()`). Yeni alt takım eklerken `aliases`'a eklemeyi unutma.

## Görsel kuralları

- Tüm görseller `public/media/` altında, **sharp** ile optimize edilmiş JPEG (mozjpeg,
  quality 78-84) veya gerekirse PNG (saydam logo rozetleri). Kapak görselleri ~1600px genişlik,
  galeri/ikincil görseller ~1200px yeterli. Örnek komut kalıbı bu oturum boyunca kullanıldı:
  ```js
  const sharp = require('sharp');
  await sharp(kaynak).resize(1200, null, { withoutEnlargement: true })
    .jpeg({ quality: 80, mozjpeg: true }).toFile(hedef);
  ```
- Sponsor logoları: `scripts/crop-sponsor-logos.mjs` duyuru görsellerindeki dairesel rozetleri
  otomatik bulup `public/media/logolar/*.png` üretir (renk maskesi + aşındırma + taşma
  doldurma + yarıçap normalizasyonu). Yeni bir sponsor duyurusu geldiğinde bu betiğe yeni bir
  `jobs` satırı eklenip yeniden çalıştırılır — koordinatları elle tahmin ETME, script'in
  içindeki yöntemi izle (dosyanın başındaki yorum tüm mantığı anlatıyor).
- **Çoklu görsel desteği** (`MediaGaleri.astro`, bkz. DESIGN.md): `teams`, `activities`,
  `haberler` şemalarının hepsinde artık `image` (kapak) yanında `gallery: string[]` var. Bir
  içerik için birden fazla gerçek fotoğraf varsa hepsini `gallery`'e ekle — kapağın altında
  küçük resim şeridi olarak otomatik çıkar, ekstra kod gerekmez.
- **Kaynak doğrulama**: Instagram/Drive'dan görsel çekerken içeriği görmeden (sadece dosya adına
  bakarak) hiçbir şeyi belirli bir takıma/olaya mal etme — görseli aç, kim/ne olduğunu doğrula,
  emin değilsen kullanma. Bu oturumda birkaç kez klasör adı ile fotoğraf içeriği uyuşmadı
  (ör. "TUSAŞ 2025" klasörü aslında MATRO'nun kendi atölyesini gösteriyordu).

## Devam eden / yarım kalan işler

1. **MediaGaleri her yerde bağlandı ama tam doldurulmadı.** Bileşen ve şema hazır
   (`src/components/MediaGaleri.astro`, üç koleksiyonda da `gallery` alanı var, `haberler.astro`/
   `faaliyetlerimiz.astro`/`takimlarimiz/[slug].astro` bağlı). Şu an gerçek çoklu görseli olan
   içerikler: takımlardan `tika-ika`, `insansiz-deniz-araci`, `insansiz-su-alti`, `suru-iha`,
   `su-alti-roketi`, `ashina`; haberlerden `turkish-technic-muhendislik-calistayi`,
   `hktm-teknik-gezisi`, `zemheri-su-alti-roketi-finalist`. **Geri kalan tüm takım/haber/faaliyet
   kayıtlarının `gallery` alanı boş** — kullanıcının paylaştığı Google Drive klasöründe
   (bkz. aşağıdaki link) çok daha fazla ham fotoğraf var, işlenip eklenmeyi bekliyor.
2. **Kullanıcının sohbette doğrudan yapıştırdığı 5 fotoğraf** (Turkish Airlines hangarı,
   Turkish Technic tişörtlü/yelekli grup fotoğrafları) **diske kaydedilemedi** — bu ortamda
   yapıştırılan görseller dosya yolu olarak erişilebilir değil. Kullanıcıdan bu görselleri
   `~/Downloads`'a kaydetmesini veya bir Drive/Instagram bağlantısı paylaşmasını iste; sonra
   indirip `public/media`'ya işle.
3. **Sponsorluk dosyası için görsel/video seçkisi** henüz teslim edilmedi. Kullanıcı sponsorluk
   dosyasını yeniden hazırlayacak, kullanılabilir yüksek çözünürlüklü görsel/video istiyor. Paylaşılan
   Drive klasörü (bağlantı kullanıcının önceki mesajlarında: `SOSYAL MEDYA` ana klasörü, id
   `1Xw1mPE0bEV286Z22K5DxvjbOpXdupjl-`) altında `MATRO TAKIM İÇERİKLERİ`, `MATRO 25/26 ETKİNLİK`,
   `FİNALİSTLER`, `Mavi vatan`, `SIK KULLANILANLAR`, `TAKIM-TANITIM` klasörleri var; çoğu hiç
   açılmadı (TUSAŞ 2025, Turkish Technic Abdullah Aydın, ERMETAL, TÜBİTAK MAM, MEEXX, Robot
   Günleri, Otofest, tanışma toplantıları, halı saha, piknik, eğitim kampları…). Bir sonraki
   ajan bunları tarayıp: (a) siteye uygun olanları `gallery` alanlarına eklemeli, (b) sponsorluk
   dosyası için ayrıca yüksek çözünürlüklü bir seçki hazırlayıp kullanıcıya
   `SendUserFile`/eşdeğeriyle teslim etmeli (bu görseller repoya girmek zorunda değil).
   `TAKIM-TANITIM` altındaki **"Takımlar faaliyet rapaoru" bir klasördür**, belge değildir.
   10 Eylül tarihinde Drive bağlayıcısıyla doğrulandı: id `1awXj2Mu0q30yLAm57uUiIgx7FhjkClsS`,
   içinde 15 görsel var. `/file/d/` yerine `/drive/folders/` ile açılmalı; yeniden kullanıcıdan istenmesine gerek yok.
4. **Video henüz hiç eklenmedi.** Kullanıcı "video resimleri vs gerekli encode/optimizeleri
   yapıp eklemeye çalış" dedi. Drive'da birkaç takımın "Videolar" alt klasörü var (LODOS, Turkish
   Technic Workshop, HKTM, TÜBİTAK, TUSAŞ). Kullanıcının yerelinde (`~/Downloads/v3_60fps.mp4`,
   `v3_takimlogo_reel.mp4`) bulunan iki video **MATRO ile ilgisiz** (PUBG yayın overlay'i,
   "DokunMachine" — kontrol edildi, kullanılmamalı). Web'e video eklenecekse: indir, `ffmpeg`
   ile h264/aac, ~720p, düşük-orta bitrate'e encode et (`ffmpeg -i giris.mp4 -vf scale=-2:720
   -c:v libx264 -crf 23 -preset slow -c:a aac -b:a 128k cikis.mp4`), `public/media/`'ya koy,
   `<video>` etiketiyle (muted/loop/playsinline, poster'lı) uygun sayfaya göm. Henüz hiçbir
   sayfada `<video>` kullanılmıyor — sıfırdan bir yaklaşım gerekecek.
5. **Git geçmişi hâlâ eski PII içeriyor** (iki telefon numarası, bir e-posta, sponsor Drive
   bağlantıları, kaldırılmış sponsorluk PDF'i) — bunlar güncel `main`'de yok ama eski commit'lerde
   duruyor. Kullanıcı "güncel içerikte olmaması yeterli" dedi, geçmişi temizlemeyi istemedi;
   bir daha sorulmadıkça `git filter-repo` ile depo geçmişini yeniden yazma.
6. Küçük açık sorular (kullanıcıya sorulmuş, henüz yanıt yok): **Komagene** sponsor olarak
   eklensin mi (tanışma etkinliğinin "lezzet sponsoru"ymuş); bazı ZEMHERİ haber tarihleri tahmin
   (28 Ağustos), başvuru `expiresOn` tarihi tahmin (31 Ekim) — kesinleşince düzeltilmeli.

## Devir sırasında dikkat

- Bu proje boyunca **Türkçe** yazıldı — commit mesajları, kod yorumları, kullanıcıya yanıtlar
  hep Türkçe. Bunu koru.
- Kullanıcı (Bilgehan Zeki Özaytaç / @WildGenie) hızlı, doğrudan geri bildirim veriyor; iş
  bitince kısa özet + canlı doğrulama (curl ile 200 kontrolü, GitHub Actions run durumu) bekliyor.
  `gh run list` ile deploy'u takip et, `https://btumatro.com` üzerinden gerçek sonucu doğrula.


## 10 Eylül 2026 — Codex devam notu

Kullanıcı medya işinden önce görsel kaliteye öncelik verdi. Ana sayfa, ortak başlık/CTA/
istatistik/takım kartları, renkler ve takım listesi yenilendi; güncel sözleşme DESIGN.md'de.

Medya işinin ön araştırması `/tmp/matro-devralma/` altında korunuyor:
- `claude-text.txt`: yalnızca bu projenin Claude oturumundan çıkarılan konuşma ve araç kayıtları.
- `inventory-complete.json`: Drive klasörleri ve dosyalarının kimlik/MIME/boyut bilgileri.
  100 kayıt dönen büyük klasörlerin listesi kısmi olabilir; tüm arşivin indirildiği anlamına gelmez.
- `original-test.jpg`: doğrudan Drive indirmesiyle alınmış 4032x3024 orijinal fotoğraf;
  yüksek çözünürlüklü indirme çalışıyor. Sponsorluk seçkisi henüz teslim edilmedi.
- `MATRO TAKIM İÇERİKLERİ` altındaki 15 takım klasörü sorgu anında boştu; FİNALİSTLER
  altındaki ASHİNA/LUNA/MATRİS gün klasörleri ve PUSULA da boştu. Boş galerileri doldurmak
  için doğrulanmamış görsel atanmamalı.
- Tanıtım videoları mevcut: LODOS yatay klasörü `178SJFmDtNK7mR4ZB0rL82i20YMJ6V4ET`,
  PRUSA yatay `1KjQMGSuRgDuxireYOokvNbvhKdDha9dk`, sualtı roket yatay
  `1EV5TXipQGJzK66Iz8XRtJTyn3dy7mdDe`. Klipler henüz indirilip görsel olarak incelenmedi.
- Önceki konuşmadaki beş yapıştırılmış fotoğraf yerel Claude JSONL kaydında gömülü bulunamadı.

Astro'nun otomatik arka plan dev sunucusu 4321 portunda eski içeriği gösterebildi.
Üretim çıktısını doğrulamak için `npm run build` ardından
`python3 -m http.server 4341 --bind 127.0.0.1 --directory dist` kullanıldı.
