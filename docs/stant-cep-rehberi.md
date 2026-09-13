# MATRO Stant Cep Rehberi — İçerik Belgesi

**Amaç:** Öğrenci Toplulukları Tanıtım Günleri'nde (15-18 Eylül 2026) standda görevli
arkadaşların telefonundan açıp bakabileceği bir cep rehberi.

**Bu belge tasarım değil, içerik kaynağıdır.** Tasarımı yapacak ajan/kişi bu belgedeki
metinleri kullanarak PDF üretecek.

---

## 0. Tasarımcıya notlar

### Format

- **A4 KULLANMA.** Telefonda okunacak.
- Önerilen sayfa oranı: **3:4 veya 4:5 dikey** (örn. 432×576 pt veya 440×550 pt).
  9:16 gibi uzun oranlar PDF okuyucunun üst/alt araç çubukları yüzünden ekranda
  küçülüyor, okunmuyor.
- Gövde metni sayfa genişliğinin **%3'ünden küçük olmasın** (432 pt genişlikte
  ~13-14 pt). Başlıklar 24-28 pt.
- Her sayfa tek konu. Kaydırmadan, tek bakışta okunmalı.
- Sayfa numarası ve bölüm adı her sayfanın üstünde olsun (hızlı bulmak için).

### Marka

- **Lacivert:** `#152C63` (ana), `#24407E` (açık ton)
- **Sarı:** `#FBD400` (vurgu)
- **Zemin:** `#F7F4EC` krem veya beyaz
- **Metin:** `#1B2231`, ikincil metin `#5C6679`
- Bu renkler topluluğun tanıtım afişindeki (Hoş Geldiniz posteri) renk düzeniyle
  uyumludur.
- Emoji kullanma.

### İçerik kuralları

1. **Uydurma rakam yok.** Bu belgedeki rakamlar `src/data/home.json`,
   `src/data/achievements.json` ve `src/content/` altındaki doğrulanmış site
   verisinden gelir. Belgede olmayan bir rakam eklenmeyecek.
2. **Kişi ismi yok.** Topluluk yapısı anlatılır, isim verilmez — mevcut ekip
   listesi güncel değil.
3. **Telefon numarası ve özel e-posta yok.** Yalnızca topluluğun genel
   e-postaları kullanılır.
4. Takım isimleri ve dereceler birebir bu belgedeki gibi yazılmalı
   ("Türkiye 3.sü", "Türkiye finalisti" vb.).

### QR kodlar

Üç QR kodu üretilecek (tasarımcı qrcode kütüphanesi veya benzeriyle üretebilir):

| Nerede | Hedef URL |
|---|---|
| Sayfa 12 | `https://docs.google.com/forms/d/e/1FAIpQLSfMgCHKihBA7zilbQnI2QfxbMTmjfrU-v7afIGuPeQx6zSUUw/viewform` |
| Sayfa 13 | `https://docs.google.com/forms/d/e/1FAIpQLSeX_98sMFjh5ReuF-zasq5cYje6LOaeFdWoDwVJGaZvd3foyQ/viewform` |
| Sayfa 19 | `https://btumatro.com` |

QR'lar büyük olsun (sayfa genişliğinin en az %35'i) — stantta karşıdakine
telefondan okutulacak.

---

## SAYFA 1 — Kapak

**Üst bilgi:**
BURSA TEKNİK ÜNİVERSİTESİ
Makine Teknolojileri Robot ve Otomasyon Topluluğu

**Ana başlık:**
MATRO
STANT CEP REHBERİ

**Açıklama:**
> Öğrenci Toplulukları Tanıtım Günleri'nde standda görevli arkadaşlarımız için
> hazırlandı. Unuttuğun ya da emin olmadığın bir şey olursa telefonundan açıp
> bakabilirsin.

**Tarih/yer kutusu (vurgulu):**

- **15-16 EYLÜL** — Mimar Sinan Yerleşkesi · B Blok girişi
- **17-18 EYLÜL** — Yıldırım Bayezid Yerleşkesi · A Blok zemin kat

**Alt bilgi:**
btumatro.com · @btumatro
19 sayfa · 2026-2027 sezonu

---

## SAYFA 2 — Standda işimiz ne?

**Başlık:** Standda işimiz ne?

**Giriş:**
> Gelen öğrenciye MATRO'yu tanıtmak, takımları anlatmak ve kayıt formuna
> yönlendirmek. Hepsi bu.

**Numaralı akış (1-4):**

1. **Selam ver, kendini tanıt** — Adını ve hangi takımda ya da ekipte olduğunu söyle.
2. **Kısa anlat** — Sonraki sayfadaki 30 saniyelik anlatımı kullan.
3. **Merakını bul** — Hangi bölüm? Yazılım mı, mekanik mi ilgisini çekiyor?
4. **Yönlendir** — İlgili takımı anlat, kayıt formunun QR'ını göster.

**Uyarı kutusu (sarı vurgulu):**

> **Bilmediğin bir şey sorulursa**
> Uydurma. "Bunu tam bilmiyorum, doğrusunu öğrenip ileteyim" de; Instagram'dan
> yazmasını söyle.

---

## SAYFA 3 — 30 saniyede MATRO

**Başlık:** 30 saniyede MATRO

**Alt metin:** Ezberleme, kendi cümlelerinle söyle. Çatısı bu:

**Alıntı kutusu (lacivert vurgulu):**

> "MATRO, üniversitemizde 2013'ten beri çalışan Makine Teknolojileri Robot ve
> Otomasyon Topluluğu.
>
> 13 Ar-Ge takımımız var: insansız hava aracı, kara aracı, deniz ve sualtı
> araçları, hava savunma, haberleşme, çevre-enerji, girişimcilik.
>
> Bu sezon 8 takımımız TEKNOFEST finaline kaldı.
>
> Bölüm şartı yok, deneyim şartı da yok — eğitim kampımızla sıfırdan
> başlıyorsun. İstersen şimdi kaydolabilirsin."

**Alt bölüm — "Takılırsan bu üç cümle yeter":**

- 2013'ten beri varız, 13 takımımız var.
- Bu sezon 8 takım TEKNOFEST finalinde.
- Bölüm ve deneyim şartı yok.

---

## SAYFA 4 — Biz kimiz?

**Başlık:** Biz kimiz?

**Gövde:**
> Bursa Teknik Üniversitesi bünyesinde 2013'te kurulan Makine Teknolojileri Robot
> ve Otomasyon Topluluğu'yuz. Milli Teknoloji Hamlesi hedefi doğrultusunda çalışan
> bir öğrenci topluluğuyuz.

**Çalıştığımız alanlar:**
İnsansız hava araçları · Sualtı robotları · Kara ve deniz araçları · Hava savunma
sistemleri · Kablosuz haberleşme · Çevre ve enerji teknolojileri · Akıllı sistemler

**Kutu 1 — Atölyemiz:**
> Özdemir Bayraktar TEKNOFEST Atölyesi — Mimar Sinan Yerleşkesi. Tasarım, üretim
> ve test burada yapılır.

**Kutu 2 — Neden varız?:**
> Üyelerimize pratik mühendislik deneyimi kazandırıp onları profesyonel hayata
> hazırlamak; ülkemizin teknolojide dışa bağımlılığını azaltmasına katkı sunmak.

---

## SAYFA 5 — Nasıl işliyoruz? (Topluluk yapısı)

**Başlık:** Nasıl işliyoruz?

**Giriş:**
> Topluluk; yönetim kurulu, ekip yöneticileri ve proje takımı kaptanlarından
> oluşan bir yapıyla yürütülür. Yönetim kurulu işleyişi dört ekip altında
> paylaşır:

**Dört ekip:**

- **Atölye Ekibi** — Atölye düzeni ve denetimi, takımlar arası iletişim ve koordinasyon.
- **Sponsorluk Ekibi** — İş birlikleri kurarak topluluğun ihtiyaçları için sponsorluk süreçlerini yürütür.
- **Organizasyon Ekibi** — Etkinlikleri planlar ve topluluk içi faaliyetleri organize eder.
- **Sosyal Medya Ekibi** — Topluluğun dijital yüzünü oluşturur, görünürlüğü artırır.

**Kutu:**
> **Yönetimde görev almak isteyen olursa**
> Yönetim kurulu başvuru formu da açık; site üzerinden "Bize Katılın" sayfasından
> ulaşabilir.

---

## SAYFA 6 — Rakamlarla MATRO

**Başlık:** Rakamlarla MATRO

**Alt metin:** Sitede yayımlanan doğrulanmış rakamlar. Bunların dışına çıkma.

**Rakam kartları (2 sütun × 3 satır):**

| Rakam | Etiket | Not |
|---|---|---|
| 50 | kayıtlı derece | 2013-2026 |
| 7 | birincilik | Türkiye ve bölge |
| 342 | finalist yarışmacı | 2020-2025 |
| 35 | takım ilk 10'a girdi | 2020-2025 |
| 8 | TEKNOFEST finalisti | 2026 sezonu |
| 13 | aktif Ar-Ge takımı | 2026-2027 |

> **Önemli:** "7 birincilik" ifadesi **"Türkiye ve bölge"** notuyla birlikte
> kullanılmalı — bunlardan biri NASA Space Apps'in bölgesel birinciliğidir,
> "7 ulusal birincilik" denmez.

**Kutu — Bunlar da doğru:**
> Kardeş Okul Projesi'nde 75.000+ TL sosyal sorumluluk desteği sağladık. Eğitim
> kampımızdan 61 üyemiz 32 ders saati sonunda sertifika aldı.

---

## SAYFA 7 — Kilometre taşları

**Başlık:** Kilometre taşları

**Zaman çizelgesi (yıl rozetli liste):**

| Yıl | Metin |
|---|---|
| 2013 | Topluluk kuruldu. LAGARİ ile Future Flight Design'da Dünya 2.si. |
| 2019 | İlk TEKNOFEST dereceleri: Tarım Teknolojileri Türkiye 3.sü. |
| 2020 | TEKNOFEST Baykar Uçan Araba'da Türkiye 1.si. |
| 2021 | Renault Twizy Contest'te Dünya 4.sü ve Türkiye 1.si. |
| 2022 | Singapur SAUVC sualtı yarışmasında dünya finalisti. |
| 2023 | INNOSENS ile TEKNOFEST Girişimcilik Türkiye 1.si. |
| 2024 | NASA Space Apps Bölge 1.si, GDG Yapay Zekâ Türkiye 1.si. |
| 2026 | Sekiz takım TEKNOFEST finalinde; Genç Ticaret Elçileri birinciliği. |

---

## SAYFA 8 — Takımlar (1/3): Hava ve kara

**Başlık:** Hava ve kara

| Takım | Ne yapıyor | Öne çıkan |
|---|---|---|
| **ASHİNA** | İnsansız hava araçları. Kendi motorunu ve atış birimini üretiyor. | 2026 TEKNOFEST finalisti |
| **MATRİS** | Sürü İHA — birden fazla hava aracının koordineli otonom uçuşu. | 2026 finalisti · 2024'te Türkiye 9.su |
| **MATROVER & LUNA** | Otonom kara araçları; tarımsal ekim ve ilaçlama robot kolları. | 2026 finalisti · 2025'te Türkiye 3.sü |
| **GÖKSAV (ASHİNA-H)** | Hava savunma; radar-sensör takibi ve bertaraf mekanizmaları. | 2025 rapor aşamasında Türkiye 3.sü |
| **BÜRKÜT** | Uçan araba simülasyonu, otonom uçuş algoritmaları. | 2020 Türkiye 1.si · 2024 En İyi Takım Ruhu |

---

## SAYFA 9 — Takımlar (2/3): Deniz ve sualtı

**Başlık:** Deniz ve sualtı

| Takım | Ne yapıyor | Öne çıkan |
|---|---|---|
| **İDA / LODOS** | İnsansız deniz aracı; deniz üstü otonom seyir ve keşif. | 2025 ve 2026 TEKNOFEST finalisti |
| **İSS / PRUSA** | Otonom sualtı aracı; sualtı görüntü işleme, sızdırmazlık. | 2026 finalisti · Singapur SAUVC dünya finalisti |
| **ZEMHERİ / SARA** | Su altı roketi; gövde, itki ve atış düzeneği tasarımı. | İlk katılımında 2026 Türkiye finalisti |

**Alt bölüm — "Bunu sorarlarsa":**
> **"Su altı roketi ne demek?"** — TEKNOFEST'in bu yıl ikinci kez düzenlenen
> kategorisi. Roket su altından fırlatılıyor; sızdırmazlık ve basınç dayanımı
> işin en zor kısmı.

---

## SAYFA 10 — Takımlar (3/3): Sanayi, enerji, girişim

**Başlık:** Sanayi, enerji, girişim

| Takım | Ne yapıyor | Öne çıkan |
|---|---|---|
| **SANAYİDE DİJİTAL / PUSULA** | Endüstri 4.0, IoT ve dijital ikiz; üretimi dijitalleştiriyor. | 2026 finalisti · 2021'de Türkiye 3.sü |
| **ÇAĞRI** | Kablosuz haberleşme; karıştırma altında kesintisiz veri iletimi. | 397 takım arasından Türkiye 6.sı |
| **ALHAZEN** | Çevre ve enerji; yenilenebilir enerji, depolama, sıfır atık. | 2025 Türkiye 7.si |
| **GİRİŞİMCİLİK VE İNOVASYON** | Fikri ürüne ve şirkete dönüştürme, hackathonlar. | INNOSENS ile Girişimcilik Türkiye 1.si |
| **ASHİNA İNOVASYON** | Tarım teknolojileri üzerine çalışan yeni araştırma takımımız. | Yeni takım |

---

## SAYFA 11 — Nasıl katılınır?

**Başlık:** Nasıl katılınır?

**Vurgulu kutu (en üstte):**
> **Ön koşul yok.**
> Bölüm şartı yok, deneyim şartı yok. Öğrenmeye istekli olmak yeterli.

**Numaralı adımlar:**

1. **Topluluk kaydı** — Kayıt formunu doldurur, üyeliğini başlatır.
2. **Takım ön başvurusu** — Yarışma takımında yer almak isteyen en fazla 3 takım tercihi yapar.
3. **Tanışma ve mülakat** — Takım sorumlularıyla kısa görüşme; doğru takıma yönlendirme.
4. **Atölye ve proje** — Eğitim programına katılır, aktif projede görev alır.

**Alt not:**
Etkinliğe gelemeyen ama üye olmak isteyenler de aynı formu doldurabilir.

---

## SAYFA 12 — Kayıt formu (QR)

**Başlık:** Kayıt formu

**Alt metin:** Telefonundan bu sayfayı aç, karşındakine okut.

**QR (büyük, sayfanın ortasında):**
`https://docs.google.com/forms/d/e/1FAIpQLSfMgCHKihBA7zilbQnI2QfxbMTmjfrU-v7afIGuPeQx6zSUUw/viewform`

- QR altı etiket: **Topluluk Kayıt Formu**
- QR altı açıklama: İlk adım — herkes bunu doldurur

**Kutu:**
> **Önce bu, sonra takım başvurusu.**
> Takım ön başvurusu ayrı bir form ve üyelikten sonra doldurulur; QR'ı sonraki
> sayfada.

---

## SAYFA 13 — Takım başvurusu (QR)

**Başlık:** Takım başvurusu

**Alt metin:** Yarışma takımlarında görev almak isteyenler için.

**QR (büyük):**
`https://docs.google.com/forms/d/e/1FAIpQLSeX_98sMFjh5ReuF-zasq5cYje6LOaeFdWoDwVJGaZvd3foyQ/viewform`

- QR altı etiket: **Takım Ön Başvuru Formu**
- QR altı açıklama: En fazla 3 takım tercihi yapılır

**Tercih edilebilen takımlar:**
İnsansız Kara Aracı · İnsansız Su Altı · İnsansız Deniz Aracı · Hava Savunma
Sistemleri · Sanayide Dijital Teknolojiler · Sürü İHA · Serbest İHA

---

## SAYFA 14 — Hangi alanda çalışılır?

**Başlık:** Hangi alanda çalışılır?

**Giriş:**
> Başvuruda takım tercihinin yanında bir de çalışma alanı seçiliyor.
> "Ben kod yazmayı bilmiyorum" diyene bunları say:

**Liste:**

- Yazılım
- Mekanik tasarım
- Tasarım analizi
- Malzeme ve üretim yöntemleri
- Elektrik-elektronik
- Sponsorluk ve dış ilişkiler

**Kutu:**
> **Mühendislik dışı bölümden gelen olursa**
> Organizasyon, sponsorluk ve sosyal medya ekiplerinde her bölümden arkadaşımız
> var. Kapımız açık.

---

## SAYFA 15 — Sık gelen sorular (1/2)

**Başlık:** Sık gelen sorular

**S: Hangi bölümden olmalıyım?**
C: Bölüm şartı yok. Makine, mekatronik, elektrik-elektronik, bilgisayar, endüstri,
metalurji ve diğer tüm bölümlerden üyemiz var.

**S: Hiç deneyimim yok, olur mu?**
C: Olur. Her dönem yeni üyeler için eğitim kampı düzenliyoruz. Geçen dönem 32 ders
saatlik kamptan 61 üyemiz sertifika aldı.

**S: Başvurular ne zaman?**
C: Şu anda açık. Başvurular güz döneminin başında açılır; güncel duyurular
Instagram'da (@btumatro).

---

## SAYFA 16 — Sık gelen sorular (2/2)

**Başlık:** Sık gelen sorular

**S: Ne kadar zaman ayırmam gerekir?**
C: Takıma ve yarışma takvimine göre değişir. Dönem başında haftada birkaç saat
atölye çalışması; yarışma yaklaşınca tempo artar.

**S: Nerede çalışıyorsunuz?**
C: Özdemir Bayraktar TEKNOFEST Atölyesi — Mimar Sinan Yerleşkesi.

**S: Ne kazanırım?**
C: Gerçek mühendislik deneyimi, ulusal ve uluslararası yarışmalar, TUSAŞ ve TOGG
gibi kuruluşlara teknik geziler, sertifikalı eğitim ve güçlü bir mühendis ağı.

---

## SAYFA 17 — Eğitim kampı

**Başlık:** Eğitim kampı

**Giriş:**
> Yeni üyeler için her akademik yıl düzenlenen mekanik, elektronik ve yazılım
> programı. Devam şartı %75.

**Mekanik:** SolidWorks, CATIA · 3D baskı · Talaşlı imalat · Atölye kullanımı

**Elektronik:** Devre temelleri · Robotik elektronik · Devre kartı tasarımı ve üretimi

**Yazılım:** Yapay zekâ ve algoritma · Görüntü işleme · Gömülü yazılım · Robotik yazılım

**Kutu — Teknik geziler:**
> TÜBİTAK MAM, TUSAŞ, ERMETAL, ALP Havacılık, Turkish Technic ve HKTM gezilerimiz
> oldu.

---

## SAYFA 18 — Zorlanırsan

**Başlık:** Zorlanırsan

**Dört durum kutusu:**

> **Teknik bir soru geldi, bilmiyorsun**
> "O takımdan bir arkadaşa sorup döneyim" de. Instagram'dan yazmasını söyle;
> kimse sana kızmaz.

> **Firma temsilcisi veya sponsor adayı geldi**
> btumatro.com/sponsorluk sayfasını göster, iletişim bilgisini al ve Sponsorluk
> Ekibi'ne ilet.

> **Aynı anda kalabalık geldi**
> Önce herkese kayıt formu QR'ını göster, sonra tek tek sohbet et.

> **Emin olmadığın rakam**
> Sayfa 6'daki rakamların dışına çıkma; tahmini rakam söyleme.

---

## SAYFA 19 — Site ve iletişim

**Başlık:** Site ve iletişim

**QR:** `https://btumatro.com`
- Etiket: **btumatro.com**
- Açıklama: Takımlar, başarılar, sponsorluk

**Sosyal medya:**

- Instagram · @btumatro
- LinkedIn · linkedin.com/company/btumatro
- YouTube · @btumatro

**E-posta:**
matroiletisim@gmail.com · matrobtu@gmail.com

---

## EK A — Kaynak dosyalar

Bu belgedeki her bilgi aşağıdaki doğrulanmış kaynaklardan alınmıştır:

| İçerik | Kaynak |
|---|---|
| Rakamlar (50/7/342/35/8) | `src/data/home.json` → `stats` |
| Kuruluş, vizyon, misyon, tarihçe | `src/data/about.json` |
| Takım adları, alanları, dereceleri | `src/content/teams/*.md` |
| Başvuru adımları, SSS, çalışma alanları | `src/data/join.json` |
| Form bağlantıları | `src/content/haberler/topluluk-kayitlari-2026-2027.md` |
| Tanıtım günleri tarih/yer | `src/content/haberler/ogrenci-topluluklari-tanitim-gunleri-2026.md` |
| Eğitim kampı içerikleri | `src/content/activities/egitim-kamplari.md` |
| Atölye adı, e-postalar, sosyal medya | `src/data/site.json` |
| Teknik geziler | `docs/sponsorluk-medya-envanteri.md` |

## EK B — Bilinçli olarak dışarıda bırakılanlar

- **Kişi isimleri ve unvanları** — mevcut ekip listesi güncel değil.
- **Telefon numaraları ve kişisel e-postalar.**
- **Takımların teknik spesifikasyonları** (motor modeli, batarya kapasitesi, menzil,
  hız vb.) — bunlar tanıtım kitapçığı taslağında var ama birincil belgeyle
  doğrulanmadı; stant rehberine alınmadı.
- **Üyelik ücreti / aidat bilgisi** — site verisinde yok, uydurulmadı. Sorulursa
  görevli "yönetime sorup dönerim" demeli.
- **Sponsor listesi** — stantta gerekmiyor; sponsor adayı gelirse sponsorluk
  sayfasına yönlendirilecek.
