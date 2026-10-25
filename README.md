# MATRO Web Sitesi

Bursa Teknik Üniversitesi **Makine Teknolojileri Robot ve Otomasyon Topluluğu** resmî web sitesi.

| | |
|---|---|
| **Yayında** | https://btumatro.com |
| **İçerik paneli** | https://app.pagescms.org |
| **Yedek adres** | https://btumatro.github.io |
| **Depo** | https://github.com/btumatro/btumatro.github.io |

Site tamamen statiktir: sunucu, veritabanı ve barındırma ücreti yoktur. Tüm içerik bu deponun içinde metin dosyası olarak durur; içerik panelinden yapılan her düzenleme buraya kaydedilir ve site **1–2 dakika içinde** otomatik güncellenir.

---

## İçeriği nasıl düzenlerim?

> **Kod bilmene gerek yok.** Aşağıdaki panel, Word'de yazı yazmak kadar basit.

### İlk giriş

1. https://app.pagescms.org adresine git.
2. **Sign in with GitHub** ile GitHub hesabınla giriş yap.
3. Karşına çıkan listeden **btumatro.github.io** deposunu seç.
4. Sol menüde sayfaların listelendiğini göreceksin.

> Deponun listede çıkmaması, GitHub hesabının depoya yazma yetkisi olmadığı anlamına gelir. Topluluk sorumlusundan seni depoya **Write** yetkisiyle eklemesini iste.

### Sol menüdeki bölümler

| Bölüm | Ne düzenlenir |
|---|---|
| **Anasayfa** | Giriş yazısı, butonlar, sayaç rakamları, tanıtım videosu |
| **Hakkımızda** | Biz kimiz, vizyon, misyon, değerler, tarihçe |
| **Başarılarımız** | Tüm dereceler ve ödüller tablosu |
| **Faaliyetlerimiz** | Eğitim kampı, teknik gezi, seminer, sosyal sorumluluk |
| **Haberler ve Duyurular** | Yarışma sonuçları, geziler, etkinlikler, başvuru çağrıları |
| **Ekibimiz** | Yönetim kurulu ekipleri ve kişiler (fotoğraflı) |
| **Takımlarımız** | Her takımın kendi sayfası |
| **Sponsorlar** | Güncel ve geçmiş sponsor listesi |
| **Sponsorluk Paketleri** | Platin/Altın/Gümüş/Bronz paket içerikleri |
| **Bize Katılın** | Başvuru formu bağlantısı, adımlar, SSS |
| **Galeri** | Fotoğraflar |
| **Site Ayarları ve İletişim** | E-posta, adres, telefon, sosyal medya |

### Düzenleme yaparken

- Değişiklikten sonra sağ üstteki **Save** düğmesine bas. Site kendiliğinden güncellenir.
- Listelerde (örneğin başarılar, sponsorlar) sağdaki **+** ile yeni satır ekler, sürükleyerek sıralarsın.
- **Sıralama** alanı olan yerlerde küçük sayı üstte görünür (1, 2, 3…).
- Fotoğraf alanlarında **Upload** ile bilgisayarından görsel yükleyebilirsin. Yüklenen görseller `public/media` klasörüne gider.

### Sık yapılan işler

**Yeni bir derece/ödül eklemek**
Başarılarımız → *Dereceler ve Ödüller* listesinde **+** → yıl, yarışma, kategori, derece → Save.
Anasayfada da görünsün istiyorsan **Anasayfada öne çıkar** kutusunu işaretle.

**Yeni takım açmak**
Takımlarımız → sağ üstte **Add entry** → takım adı, alt başlık, kategori, özet ve detay metnini gir → Save.
Takım sayfası otomatik oluşur ve listeye eklenir.

**Bir takımı arşive kaldırmak**
Takımı aç → **Durum** alanını `Arşiv` yap → Save. Takım listeden kalkar ama içerik silinmez.

**Haber yayınlamak**
Haberler ve Duyurular → **Add entry** → başlık, tür, tarih, özet ve içeriği gir → Save.
Yazarken **emoji kullanmayın**; sitenin dili sosyal medyadan farklı, sade ve kurumsaldır.

**Başvuru duyurusu yapmak (ör. yönetim kurulu başvuruları)**
Haberler ve Duyurular → ilgili taslağı aç → **Taslak** kutusunun işaretini kaldır →
**Anasayfada öne çıkar**'ı işaretle → **Son gösterim tarihi**'ne başvuru bitiş tarihini yaz → Save.
Tarih geçince duyuru siteden kendiliğinden düşer; ayrıca bir şey yapmanız gerekmez.
*(Yönetim kurulu başvuru metni taslak olarak hazır bekliyor.)*

**Ekip üyesi eklemek**
Ekibimiz → *Kişiler* listesinde **+** → ad soyad, görev, ekip ve fotoğraf → Save.
Kişiler seçtiğiniz ekibe göre otomatik gruplanır.

**Başvuru formunu bağlamak**
Bize Katılın → *Başvuru formu bağlantısı* alanına Google Forms adresini yapıştır → Save.
(Boş bırakılırsa sitede Instagram butonu gösterilir.)

**Başkan bilgisini güncellemek**
Site Ayarları → *Yetkililer* → ilgili satırı doldur → Save.
Telefon/e-posta boş bırakılırsa sitede hiç gösterilmez.

### Dikkat

- **Sponsor tutarları sitede görünmez.** `Tutar` alanı yalnızca topluluk içi kayıt içindir. Ama bu depo herkese açıksa dosya içeriği de görülebilir — hassas bulunuyorsa alanı boş bırakın.
- **Kişisel telefon/e-posta yayınlarken izin alın.** Site Ayarları → Yetkililer bölümündeki bilgiler herkese açık şekilde sitede görünür.

---

## Alan adı kurulumu (tamamlandı)

btumatro.com Cloudflare'de kayıtlı ve GitHub Pages'e bağlı. Kurulum şu şekilde:

| Type | Name | Content | Proxy |
|---|---|---|---|
| A | `@` | `185.199.108.153` / `.109` / `.110` / `.111` | DNS only |
| AAAA | `@` | `2606:50c0:800{0,1,2,3}::153` | DNS only |
| CNAME | `www` | `btumatro.github.io` | DNS only |

- GitHub → Settings → Pages → *Custom domain*: `btumatro.com`, **Enforce HTTPS** açık.
- `public/CNAME` dosyası alan adını taşır. **Bu dosyayı silmeyin**, silinirse site
  btumatro.github.io adresine geri döner.
- Cloudflare proxy (turuncu bulut) kapalı. Açmak isterseniz **SSL/TLS → Full (strict)**
  seçin; `Flexible` sonsuz yönlendirme döngüsüne yol açar.
- `www.btumatro.com` otomatik olarak `btumatro.com`'a yönlenir.

Alan adı değişirse: `site.config.mjs` içindeki `SITE_URL`, `public/CNAME` ve
`public/robots.txt` güncellenmelidir.

---

## Geliştirici notları

### Kurulum

```bash
npm install
```

### Geliştirme sunucusu

```bash
npm run dev
```

### Yayın derlemesi

```bash
npm run build
```

### Logo ve marka görsellerini yeniden üret

Logo dosyaları değişirse `src/assets/logo-kaynak/` içindekileri güncelle, sonra:

```bash
node scripts/make-brand.mjs && node scripts/make-og.mjs
```

Bu iki betik `public/` altındaki logo, favicon, iOS simgesi ve sosyal medya önizleme
görsellerini kaynak dosyalardan yeniden üretir.

### Teknoloji yığını

- **[Astro](https://astro.build)** — statik site üreteci (SSG)
- **[Tailwind CSS v4](https://tailwindcss.com)** — stil
- **[Pages CMS](https://pagescms.org)** — barındırılan, sunucusuz içerik paneli
- **GitHub Actions + GitHub Pages** — otomatik derleme ve yayın

> **Not:** İlk planda geçen Keystatic, GitHub Pages ile çalışmaz — GitHub mode'u sunucu tarafı API route'u (`prerender: false`) gerektirir, GitHub Pages ise yalnızca statik dosya sunar. Bu yüzden aynı işi sunucusuz yapan Pages CMS tercih edildi.

### Klasör yapısı

```
.pages.yml               İçerik panelinin form şeması
site.config.mjs          Site adresi / alt klasör ayarı
astro.config.mjs         Astro yapılandırması
.github/workflows/       Otomatik yayın (GitHub Actions)
public/
  media/                 Panelden yüklenen görseller
  logo-*.png             Üretilen logolar (elle düzenlemeyin)
  favicon.png            Sekme simgesi (üretilir)
  og.png                 Sosyal medya önizleme görseli (üretilir)
scripts/
  make-brand.mjs         Logo, favicon ve simgeleri üretir
  make-og.mjs            Sosyal medya önizleme görselini üretir
src/
  assets/logo-kaynak/    Orijinal logo dosyaları (kaynak)
  data/*.json            Tekil sayfa içerikleri
  content/teams/*.md     Takım sayfaları
  content/activities/*.md Faaliyetler
  components/            Arayüz bileşenleri
  layouts/               Sayfa iskeleti
  pages/                 Site sayfaları (dosya = URL)
  styles/global.css      Renk paleti ve tipografi
```

### Menü yapısı

Üst menü `src/lib/utils.ts` içindeki `NAV` dizisinde tanımlıdır. Bir öğeye `children` eklerseniz
açılır menü olur. Alt bilgideki düz liste ise aynı dosyadaki `FOOTER_LINKS`'tir.

### Renkleri ve yazı tiplerini değiştirmek

`src/styles/global.css` içindeki `@theme` bloğu tüm paleti ve tipografiyi tanımlar. Oradaki değerleri değiştirmek tüm siteyi etkiler.

### Marka kullanımı

- **MATRO logosu:** Koyu zeminlerde beyaz varyant (`logo-matro-beyaz.png`), açık zeminlerde renkli varyant (`logo-matro.png`) kullanılır. Kaynak dosyaların tamamı `src/assets/logo-kaynak/` altındadır.
- **BTÜ logosu:** [btu.edu.tr kurumsal kimlik sayfasındaki](https://btu.edu.tr/tr/sayfa/detay/3401/kurumsal-kimlik) resmi dosyalardır. Footer'da beyaz yatay sürüm kullanılır.
- **Yazı tipi:** Başlıklarda üniversitenin kurumsal fontu **Barlow**, gövde metinlerinde ekran okunabilirliği için **Inter**, teknik etiket ve sayılarda **JetBrains Mono** kullanılır. Üçü de npm paketi olarak sitede barındırılır; dışarıya font isteği gitmez.

---

## Sorun giderme

**Değişikliğim sitede görünmüyor**
Depo → **Actions** sekmesine bak. Sarı nokta = derleniyor, yeşil tik = yayınlandı, kırmızı çarpı = hata. Kırmızıysa üzerine tıklayıp hatayı oku.

**Panelde depo görünmüyor**
GitHub hesabına depo üzerinde **Write** yetkisi verilmiş olmalı. Ayrıca app.pagescms.org ilk girişte GitHub uygulaması kurulum izni ister; kabul edildiğinden emin ol.

**Görsel yükledim ama çıkmıyor**
Görselin ilgili alana (örn. *Kapak görseli*) seçildiğinden ve **Save** yapıldığından emin ol. Sadece yüklemek yetmez, alana atanması gerekir.

**Site bozuk görünüyor / stiller yok**
`site.config.mjs` içindeki `SITE_URL` ile sitenin gerçek adresi uyuşmuyor olabilir. Depo adı
`btumatro.github.io` olduğu için `BASE_PATH` her zaman `'/'` kalmalıdır.

## Kaynakların durumu ve temizlik

MATRO deposunda bu eğitimin ve genel amaçlı üretim skill'lerinin kopyası tutulmaz; gelecekteki BTÜ MATRO'ya özgü yapay zekâ eğitimi ayrı kapsamda hazırlanır.
