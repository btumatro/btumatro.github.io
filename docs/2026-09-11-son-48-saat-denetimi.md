# Son 48 saat denetimi — 11 Eylül 2026

## Kapsam ve sonuç

İncelenen son commit: `2708626db9c683113531a1ecfae54e9d8f680cd7`.
Denetim sabah yaklaşık 04:40–05:00 Türkiye saatinde yapıldı. `git log --since='48 hours ago'` ile seçilen **30 commit**, ilk commit `820641c` öncesi ile HEAD arasındaki **288 dosyalık net değişiklik** kapsamında incelendi. Başlangıçta çalışma ağacı temizdi.

Sonuç: site çalışıyor ve içerik arşivi ciddi biçimde genişlemiş. Ancak mevcut içerik, doğrudan baskıya aktarılacak kadar tutarlı değil. Öncelik görsellerin doğru takıma ve olaya bağlanması, sayısal ifadelerin kapsamı ve sponsor kaynaklarının uzlaştırılması.

Bu çalışma bir denetim ve kitapçık planıdır. Bulguların tamamı düzeltilmiş sayılmamalı. Site kodu ve yayın içeriği bu denetimde değiştirilmedi.

## Kontroller

| Kontrol | Sonuç | Sınır |
|---|---|---|
| `npm run build` | Başarılı; 26 HTML sayfası, 404 dahil | Astro üretim/şema kontrolü; ayrı bir tam TypeScript denetimi değildir |
| `git diff --check` | Başarılı | İncelenen çalışma ağacı |
| Üretim HTML'lerindeki yerel dosya ve bölüm bağlantıları | Kırık referans bulunmadı | Dış form gönderimi yapılmadı |
| Canlı sayfa/varlık HTTP denetimi | 234 isteğin tamamı 200; 25 normal sayfa dahil | Erişilebilirlik kontrolü, içerik doğruluğu garantisi değil |
| Masaüstü 1440 ve mobil 390 px | 25 sayfa × 2 genişlik: HTTP 200, yatay taşma yok, sayfa başına bir H1 | Otomatik düzen kontrolü; her sayfanın her etkileşiminin elle testi değil |
| Haber görünürlüğü | Taranan sayfalarda opacity:0 olan article yok | Yavaş ağda bütün görsellerin yüklenme süreleri ölçülmedi |
| Görsel inceleme | Varlık listesindeki 201 raster görsel altı temas sayfasında gözden geçirildi; seçilen dosyalar ayrıca incelendi | Drive'daki tüm orijinaller tek tek yeniden doğrulanmadı |
| Raster dosyalar | 202 resim okunabiliyor, hiçbiri 500 KiB üstünde değil; en büyüğü 431.097 bayt | Web sıkıştırması, baskı kalitesi anlamına gelmez |
| Yerel videolar | 4 MP4, tamamı H.264/AAC ve 1280×720 | Klip süreleri aşağıda; tam tanıtım filmi olarak sunulmamalı |
| Dosya tekilleştirme | SHA-256 ile birebir aynı medya dosyası yok | Aynı fotoğrafın farklı kırpım/sıkıştırmaları hâlâ var |
| Başarı bağlantıları | Dolu takım adlarının tamamı bir takım sayfasına çözümleniyor; alias çakışması yok | Eşleşmenin tarihsel/kurumsal doğruluğu ayrıca incelenmeli |
| Pages CMS | Yeni galeri, video, alias, haber bağlantıları ve varlık alanları mevcut; JSON kök alanları panelde karşılık buluyor | Panel üzerinden gerçek kaydetme testi yapılmadı |
| GitHub Pages | Son üç yayın başarılı; son çalıştırma `34551407593` | Denetim sırasında yeni yayın yapılmadı |

## Değişikliklerin özeti

- **Görsel dil:** ana sayfa fotoğraf odaklı yeniden düzenlendi; ortak başlık, sayaç, takım kartı, CTA, header/footer ve renkler sadeleştirildi. Mobil menüye Escape ile kapatma eklendi. Alt sayfalarda aynı başlık sistemi var; kart ağırlıklı bazı gövdeler eski düzeni koruyor.
- **Başvuru:** topluluk kaydı, takım ön başvurusu ve yönetim başvurusu ayrı veriye ve hedeflere bağlandı. İlk başvuru haberinde iki bağımsız düğme var.
- **Başarılar:** kayıt sayısı 39'dan 50'ye çıktı; 2026 finalistleri, SCENDERS ve SYNTAX kayıtları eklendi; takım adları bağlantıya dönüştürüldü. Ana sayfa ve başarılar sayfası ortak sayaç fonksiyonunu kullanıyor.
- **Sponsorlar:** LUNA ROBOTICS platin oldu, TEKYAZ eklendi; ana sayfada kademe grupları oluşturuldu. Sponsorluk haberleri haberler listesinden ayrıldı. Sponsorların geçmiş listesi birden fazla kez değişti; aşağıdaki kaynak uyuşmazlığı önemli.
- **Medya:** kapak + galeri desteği üç koleksiyona yayıldı; 95 galeri kaydı, 205 varlık kaydı, üç takım klibi ve Alper Gezeravcı ziyaret klibi mevcut. Eski sunumdan fotoğraf ve araç çizimleri alındı; medya adları değiştirildi, birebir kopyalar temizlendi.
- **Kurumsal içerik:** 32 kişilik ekip listesi ve dört yönetim birimi, yeni etkinlik/ziyaret içerikleri, alt ekip/araç alias'ları eklendi.
- **İletişim:** kaldırılması istenen danışman e-postası, mühendis telefonu ve sponsor Drive bağlantıları güncel içerikten çıkarıldı. Eski Git geçmişi bu denetimde değiştirilmedi.
- **İç arşiv:** `/varliklar/` eklendi, noindex ve sitemap filtresi var. Bu sayfa erişim korumalı değildir; iç kaynak/onay notları buraya konmamalı.

## Öncelikli bulgular

### 1. Görsel ile açıklama/takım eşleşmesi hataları — baskı öncesi zorunlu düzeltme

| Dosya / kayıt | Görülen kanıt | Yapılacak |
|---|---|---|
| `galeri-matrover-arazi-test.jpg` | Fotoğrafta **LUNA İKA** tabelası ve stantta grup var | MATROVER arazi testi açıklamasını kaldır; LUNA İKA stant fotoğrafı olarak kaynakla eşleştir |
| `galeri-luna-arac-detay.jpg` | Fotoğrafta **MATROVER** tabelası ve grup var | LUNA araç detayı açıklamasını kaldır; MATROVER stant fotoğrafı olarak eşleştir |
| `galeri-matris-dron-filo.jpg` | İki kişinin yarışma alanındaki özçekimi | Dron filosu fotoğrafı diye kullanma |
| `galeri-lodos-deniz-test.jpg` | Kapalı alanda masa üzerinde tekne gövdesi | Deniz testi yerine görülen üretim/atölye bağlamını yaz |
| `galeri-lodos-sahil-ekip.jpg` | Kapalı alanda tekne gövdesi | Sahil ekip fotoğrafı açıklamasını düzelt |
| `galeri-alhazen-laboratuvar.jpg`, `galeri-alhazen-ekipman.jpg`, `galeri-alhazen-analiz.jpg` | Yarışma/stant ekip fotoğrafları | Laboratuvar, ekipman ve analiz isimlerinin ima ettiği bağlamları kaldır |
| `galeri-matrobot-tarla-test.jpg` | Yarışma stantları önünde grup | Tarla testi olarak sunma |
| `galeri-iss-fuar-standi.jpg` | Sualtı aracı ve topluluk sergisi; varlık başlığı Renault Twizy aracından söz ediyor | Başlığı gerçek araçla eşleştir |

Bu adlandırmaların bir kısmı `61b3699` ve `f0663b9` içindeki anlamsal yeniden adlandırma sırasında ortaya çıkmış. Dosya adları doğrulama kaynağı kabul edilmemeli. Site galerisi, takım galerisi, assets başlığı, kaynak manifesti ve kitapçık açıklaması birlikte düzeltilmeli.

### 2. Mobilde TEKNOFEST afişleri kesiliyor

`src/content/haberler/teknofest-2026-finalleri.md` içinde bir kapak + üç galeri görseli, toplam **tam dört** dosya var. Ancak `src/pages/haberler.astro` ana görseli mobilde `aspect-[4/3] object-cover` ile gösteriyor; gerçek görseller 4:5. 390 px ekran görüntüsünde başlık ve alt bant kesiliyor. Kaynak dosyayı doğru seçmek görüntüleme hatasını çözmemiş.

Öneri: afiş ve fotoğraf için ayrı gösterim politikası; afişte oranı koruyan `contain` veya doğal yükseklik. Kitapçıkta afişi tam sayfa süs olarak çoğaltmak yerine orijinal fotoğraf + yeniden dizilmiş, doğrulanmış açıklama kullan; arşiv afişini gösterirken tamamını koru.

### 3. Sponsorluk haber filtresi ana sayfada eksik

`haberler.astro` Sponsorluk türünü eliyor; `index.astro:26–28` ise `publishedNews(...).slice(0,3)` kullanıyor. Yeni bir sponsor haberi yayımlandığında ana haberler bölümüne geri dönebilir ve `/haberler#sponsor-haber-id` bağlantısı hedef bulamayabilir. Şu an ilk üç haber sponsorluk olmadığı için canlı kırık bağlantı yok.

Öneri: ana sayfa haber seçkisinde de aynı ayrımı uygula; sponsorluk haberleri için `/sponsorluk/` altında kararlı bölüm kimlikleri oluştur.

### 4. Baskı envanteri güncel değil

- `assets.json` içindeki **35 resmin en/boy bilgisi** gerçek dosyayla farklı; en/boy veya boyut bilgisinde toplam **37 kayıt** sapması var. Kullanım notlarını yeniden üretmek ölçüleri güncellememiş.
- `docs/web-site-medya-manifest.json` içinde **14 eski dosya yolu** artık yok. Yeniden adlandırılmış/kaldırılmış dosyalar için kaynak → yeni dosya eşlemesi gerekli.
- `galeri-saha-expo-fuar.jpg` diskte mevcut ama varlık listesinde yok. `README.md` medya varlığı sayılmamalı.
- 202 raster resmin hiçbiri A4 dikey sayfayı tam kaplarken 200 ppi seviyesine ulaşmıyor. Bu bir tam sayfa yerleşim hesabıdır; küçük fotoğraflar yeterli olabilir. A4 300 ppi hedefi yaklaşık **2480×3508 px**; yalnız DPI etiketi değiştirmek ayrıntı kazandırmaz.
- Aynı kare farklı kodlamalarla hâlâ tekrarlanıyor: HKTM grup kareleri, özçekimler ve bazı takım görselleri. Editoryal seçimde benzer kareler elenmeli.

### 5. Sponsor geçmişi ve kademeleri uzlaştırılmalı

`6516327` açıklaması **A.NET → A.VET** düzeltmesini belgeliyor; eski sunumun yerel `sponsor-sayfa-16.png` görüntüsünde A.VET logosu okunuyor. Mevcut `sponsors.json` tekrar A.NET yazıyor. Aynı geçmiş listesinde BURGAB/Dijilkart gibi önce kaynaksız diye çıkarıldığı belirtilen adlar yeniden var. Bu adların tamamının yanlış olduğu söylenemez; eklenme kaynağı kaydedilmeden kitapçığa taşınmamalı.

AKKUŞ ENERJİ güncel veride Gümüş, mevcut toplu sponsor afişinde Bronz; iç tutar alanı da yeni kademe aralığıyla uyuşmuyor. LUNA'nın eski altın toplu afişi ile yeni platin duyurusu farklı dönem durumlarını gösteriyor. Güncel sponsor tablosu ile tarihli duyuru görselleri ayrı ele alınmalı; tutardan otomatik kademe tahmini yapılmamalı. KOMAGENE sitede artık mevcut, eski notta hâlâ açık soru görünüyor.

Kitapçık için sponsor adı, destek dönemi, kademe, onaylı vektör logo ve kaynak tarihi birlikte tutulmalı. Kurumsal ziyaretler sponsor ilişkisi olarak gösterilmemeli.

### 6. Sayılar ve başarıların niteliği

- Veride **50 kayıt, 7 birincilik, 8 adet 2026 finalist kaydı** var. “50 ödül” veya “50 ayrı yarışma” denmemeli; finalistlik, rapor derecesi ve özel ödül birlikte sayılıyor.
- `achievementSummary().international` yarışma adındaki “Uluslararası” gibi kelimeleri de sayıyor. Türkiye derecesini “Dünya çapında başarı” diye sunmak yanıltabilir. Bölgesel, ulusal, uluslararası sonuç düzeyleri ayrı alanlarla tanımlanmalı.
- **13 takım sayfası** var: 11 Aktif, 2 Yeni Takım. Başvuruda **7 kategori** sunuluyor. Kitapçıkta portföy ile 2026–2027 alım kapsamı ayrılmalı; 13 başlığa da açık alım var denmemeli.
- **342 finalist yarışmacı / 35 ilk 10 takım kaydı / 22 derece ve özel ödül**, 2020–2025 dönemine ait metinsel veriler. Benzersiz kişi/takım sayısı oldukları bu denetimde doğrulanmadı. “342 aktif üye” şeklinde kullanılmamalı.
- TİKA gövdesinde “altı ayrı derece” yazarken ön bilgilerde sekiz başarı maddesi var; “2019'dan bu yana her yıl” iddiasını listedeki 2020 kaydı desteklemiyor.
- `6516327` notu 2021 Sanayide Dijital Teknolojiler üçüncülüğünün **teknik destek verilen bir ekibe** ait olabileceğini açıkça söylüyor. Kayıt hâlâ PUSULA. Birincil sonuç kaydı/ekip teyidi gelene kadar kitapçığın öne çıkan başarılarına alınmamalı.
- Twizy afişlerinde **EMİZY / MATROBOT ve 2020** ibareleri var; veride başarılar BÜRKÜT / 2021 altında. Yarışmanın sezon adı ile sonuç tarihi ve alt ekip ilişkisi uzlaştırılmalı; afişteki yılı otomatik doğru kabul ederek veriyi değiştirme.

### 7. Alt takım/araç ve dönem ifadeleri

MERGEN ve LUNAROV, devam notunda doğrulanmayı beklerken takım dosyalarında kesin ilişki olarak yer alıyor. MERGEN görselinin varlığı aynı çalışma alanını destekleyebilir; kurumsal olarak GÖKSAV'ın alt ekibi olduğunu tek başına kanıtlamaz. `alias` bir bağlantı kolaylığıdır; tarihsel üst-alt ekip ilişkisiyle aynı veri değildir.

GÖKSAV sayfasının girişindeki isim kökeni ASHİNA-H'yi anlatırken başlığı GÖKSAV. BÜRKÜT “2025'te ... devam etmektedir” diyor. ZEMHERİ “bu yıl” ifadesini kullanıyor. Kalıcı kitapçıkta açık sezon/tarih yazılmalı.

### 8. Başvuru ve dokümantasyon

Üç form ayrılmış ve ilk haberde iki düğme mevcut. Buna karşın bütün takım detayları aynı takım başvuru çağrısını gösteriyor; formun yedi kategorisiyle her takımın ilişkisi belirlenmeli. Kitapçıkta üç katılım yolu açıkça ayrılmalı.

31 Ekim son tarihi önceki notlarda tahmini. Tanıtım Günleri tarihi, stand yeri, baskı adedi ve matbaa gereksinimi henüz belirtilmedi. Bunlar içerik hazırlığını engellemez; baskıya girecek kesin bilgi gibi yazılmaz.

AGENTS.md içindeki “video yok”, “galeriler boş”, “Komagene eklensin mi” maddeleri artık güncel durumu yansıtmıyor. Yeni plan bu eski notların yerine kanıtlı başlangıç noktası olmalı.

### 9. Küçük teknik bulgular

- Haber Markdown başlıkları aynı sayfada tekrarlanan `teşekkür` ve `neler-gördük` id'leri üretiyor. İç başlık bağlantıları için haber kimliği öneki kullanılmalı.
- MediaGaleri küçük resimleri ayrı küçük dosyalar yerine tam boy dosyayı indiriyor; bu yük ve yavaş bağlantı davranışı sonraki iyileştirmede ölçülmeli. Ana resimler için doğal ölçü/yerleşim rezervasyonu ve afiş/fotoğraf ayrımı eklenmeli.
- Başvuru düğmelerinde ve takım detaylarında kalan büyük köşe yuvarlaklıkları yeni ortak tasarımın daha düz çizgileriyle tam tutarlı değil. Kitapçık tasarımı mevcut web gövdesinin doğrudan çıktısı olmamalı.

## Yerel video durumu

| Klip | Süre | Kullanım |
|---|---:|---|
| LODOS | 11,54 sn | Takım sayfası; kısa tanıtım klibi |
| PRUSA | 6,83 sn | Takım sayfası; kısa tanıtım klibi |
| ZEMHERİ | 8,60 sn | Takım sayfası; kısa tanıtım klibi |
| Alper Gezeravcı ziyareti | 14,68 sn | Haber içeriği |

Üç takımın kaynak video yolları yerel Drive'da mevcut. Kitapçıkta videolar QR ve seçilmiş kareyle temsil edilmeli; basılı PDF'nin içinde oynatma beklenmemeli.

## Kanıtlar ve takip

- `docs/kitapcik-hazirlik/denetim-verisi.json`: commit/dosya listesi, referans kontrolleri ve sayımlar.
- `docs/kitapcik-hazirlik/medya-olculeri.json`: gerçek dosya ölçüleri.
- `docs/kitapcik-hazirlik/tarayici-kontrolu.json`: 50 sayfa/genişlik kontrolü.
- `docs/kitapcik-hazirlik/canli-kontrol.json`: canlı HTTP sonuçları.
- `docs/kitapcik-hazirlik/gorsel-eslesme-on-inceleme.jpg`: 24 adayın karşılaştırmalı ön incelemesi; **onaylı baskı seçkisi değildir**.

Önerilen düzeltme sırası: görsel ilişkileri → sponsor/başarı kaynağı → envanter/orijinal dosya eşlemesi → web kırpma ve filtre → kitapçık metni ve tasarımı.
