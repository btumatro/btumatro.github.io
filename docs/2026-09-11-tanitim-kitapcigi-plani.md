# MATRO — Tanıtım kitapçığı ve sponsorluk portföyü planı

Durum: tasarım ve içerik hazırlığı. Bu belge, baskıya onay verilmiş bir yayın değildir.

## Amaç ve teslimler

Topluluk Tanıtım Günleri'nde yeni öğrencinin “Burada ne yapabilirim?” sorusunu; sponsor görüşmesinde “Bu ekibe neden ve nasıl destek verebilirim?” sorusunu cevaplayan bir yayın ailesi hazırlıyoruz.

Kullanıcı sayfa sınırı istemiyor; her sayfanın konuyla ilişkili metin, fotoğraf ve tasarım içeriği olmasını istiyor. Başlangıç yapısı **A4 dikey, kapaklar dahil 28 sayfa**. Bu bir üst sınır değil. Özellikle kara araçları veya PUSULA/ANDROMEDA için doğrulanmış içerik artarsa ek sayfalar açılır; görseli zayıf başlıklar boş alanı doldurmak için uzatılmaz.

İlk teslim, başka tasarım programlarına da aktarılabilir **düzenlenebilir içerik ve sanat yönetimi paketi**. Ardından aynı içerikten kitapçık web önizlemesi ve PDF hazırlanır. Yönetim sunumunda web sitesinin ekran görüntüleri ayrı bir bölümde gösterilir.

## Üretim yöntemi

| Yöntem | Güçlü tarafı | Sınırı | Karar |
|---|---|---|---|
| A4'e özel HTML/CSS → kontrollü PDF | Mevcut Astro/JSON içeriğini kullanır; sayfa düzeni ve revizyonlar kodla tekrarlanır; tarayıcı önizlemesi vardır | Matbaa PDF/X, CMYK, taşma/kesim işaretleri için ek hazırlık gerekebilir | **Ana yöntem** |
| InDesign / Affinity Publisher benzeri sayfa tasarımı → PDF | Matbaa hazırlığı ve ayrıntılı tipografi için uygun | Program/lisans ve tasarımcı devri gerekir; site verisiyle senkron ayrıca yönetilir | Matbaa gereksinimi bunu gerektirirse aynı paketle devam |
| A4 boyutlandırılmış PowerPoint / Slides | Yönetim ve ekip üyelerinin metni elle değiştirmesi kolay | Çok sayfalı yayın akışı, kaynak senkronu ve baskı kontrolü daha fazla bakım ister | İsteğe bağlı görüşme sunumu; ana kaynak olmayacak |

HTML ve PDF birbirinin alternatifi olarak ele alınmayacak: HTML düzenlenebilir tasarım, PDF ise sürüm numarası olan teslim dosyası olacak. CSS `@page` ile A4 boyutu ve sayfa kırılımları kontrol edilebilir. [MDN, sayfalı medya](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Paged_media).

Otomatik PDF dışa aktarımı fontların yüklenmesini bekleyecek, CSS sayfa ölçüsünü koruyacak ve arka planları basacak. Bu ayarlar Puppeteer PDF seçeneklerinde mevcut. [Puppeteer PDFOptions](https://pptr.dev/api/puppeteer.pdfoptions).

Standart tarayıcı PDF'si kendiliğinden matbaa PDF/X dosyası sayılmaz. CSS taşma/kesim işaretlerinin tarayıcı desteği sınırlıdır; matbaanın istediği profil alınarak ayrı sonlandırma yapılır. [MDN, destek sınırı](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Paged_media).

## Sanat yönetimi: mühendislik yıllığı

Önerilen yön: **gerçek üretim fotoğrafları + açıklamalı araç çizimleri + sakin, güçlü tipografi**. MATRO bir öğrenci topluluğu olduğu için hem mühendislik ciddiyeti hem insanların birlikte üretme hali görülecek.

- Beyaz veya çok açık sıcak zemin; kömür rengi metin. Siyah MATRO logosu esas; koyu kapak seçilirse kontrastlı beyaz varyant.
- Başlıklarda mevcut Barlow, gövdede Inter. Mono yazı yalnız teknik ölçü, yıl ve görsel numarasında. Türkçe karakterler ve font lisansları teslimle birlikte kontrol edilir.
- Camgöbeği, sınırlı bölüm işareti/ince çizgi vurgusu. Yeni bir marka logosu veya renk kimliği icat edilmez.
- Bir sayfada bir ana fikir. Ana görsel sayfanın yaklaşık %40–60'ını alır; iki küçük ayrıntı fotoğrafı gerektiğinde onu tamamlar.
- 28 sayfa aynı şablonla tekrarlanmaz: fotoğraf açılışı, teknik profil, çalışma süreci, başarı çizelgesi, insan hikâyesi ve destek tablosu olmak üzere altı düzen ailesi.
- Dev sloganlar, neon parlamalar, dekoratif teknoloji ızgaraları ve çok sayıda kutu yerine gerçek araç/üretim ayrıntıları kullanılır. Fotoğraf üzerine uzun paragraf bindirilmez.
- Instagram afişleri kanıt arşivinde korunur. Kitapçığın ana fotoğrafı için mümkün olduğunda afişin arkasındaki orijinal kare seçilir; afişten kırpılmış düşük çözünürlüklü araç görüntüsü büyütülmez.
- Her teknik diyagramın “temsili çalışma şeması” veya “ekibin araç tasarımı” olduğu açık olur. Performans ölçüsü yalnız belgeyle destekleniyorsa yazılır.

Alternatif iki yön: **teknik ürün kataloğu** (daha çok araç çizimi, sponsor görüşmelerine uygun) ve **fotoğraf ağırlıklı topluluk dergisi** (Tanıtım Günleri'nde daha sıcak). Önerilen yıllık bu ikisini dengeler; bütün yayını koyu web ekranlarının çıktısına dönüştürmez.

## A4 düzen kuralları

- Bitmiş sayfa: 210 × 297 mm, dikey. Yan yana çift sayfa önizleme ayrıca olabilir; PDF tek tek okuma sırasındaki sayfalardan oluşur.
- Başlangıç güvenli alanı: üst/alt/dış 15 mm, iç 18 mm; cilt türüne göre revize edilir.
- Altı sütunlu görünmez yerleşim kılavuzu; 4 mm aralık. Ana metin 10,5–11 pt, satır aralığı yaklaşık 1,4; fotoğraf açıklaması en az 8,5–9 pt.
- Tam sayfa fotoğrafta yaklaşık 2480 × 3508 px / 300 ppi hedeflenir. Her görselin kullanılacağı fiziksel boyut ve kırpıma göre etkin ppi hesaplanır. Düşük çözünürlüklü görsel daha küçük yerleştirilir veya orijinali bulunur.
- Logo ve çizimler mümkün olduğunda SVG/PDF vektör olur. Oranları ve logonun boşlukları kontrol edilir; logoların birbirine göre optik boyutları dengelenir.
- Tel dikiş tercih edilirse toplam sayfa sayısı dördün katında tutulur; son sayı matbaa ve içerikle belirlenir. A4 bitmiş boyut, katlanınca A5 olacak bir çıktı ile karıştırılmaz.
- Kenara taşan görsel istenirse başlangıç varsayımı 3 mm taşmadır; matbaa onayı olmadan evrensel standart gibi kullanılmaz. Ofis yazıcısı sürümü beyaz kenarlı olabilir.
- QR kodlar baskıda yaklaşık 25 mm'den başlatılır; açık zemin, boş çevre ve kısa okunabilir URL bulunur. Son basılı örnek gerçek telefonla taranır.
- Üstbilgi/altbilgi, sayfa numarası, sürüm ve yayın dönemi yayının kendi tasarımına aittir. Tarayıcının otomatik tarih/URL başlığı kapatılır.

## Sayfa omurgası

Detaylı metinler, görsel dosyaları, eksikler ve revizyon alanları `kitapcik-hazirlik/yayin-plani.json` dosyasında tutulur. Aynı veriden üretilen `sayfa-icerikleri.md` ve `sayfa-dosya-listesi.csv` tasarımcıya verilir.

| Sayfa | Konu | Görsel / anlatım yaklaşımı |
|---|---|---|
| 1 | Kapak — MATRO, atölyeden sahaya | Bir güçlü gerçek fotoğraf; kısa başlık ve dönem |
| 2 | Biz kimiz? | Topluluk grubu, 2013 kuruluş bilgisi, açık tanım |
| 3 | Bir fikir nasıl projeye dönüşür? | Tasarım–üretim–test–yarışma akışı; gerçek süreç kareleri |
| 4 | Burada hangi işi yapabilirsin? | Mekanik, elektronik, yazılım, tasarım ve organizasyon rolleri |
| 5 | Proje alanları haritası | 13 portföy başlığı; açık alım kategorilerinden ayrı açıklama |
| 6 | ASHİNA | İHA + üretim fotoğrafı + gerçek tasarım çizimi |
| 7 | MATROVER & LUNA / kara araçları | Alt ekipleri sezonlarıyla ayıran araç/ekip profili |
| 8 | İDA / LODOS | Gerçek tekne, gövde/elektronik ayrıntısı, kısa klibe QR |
| 9 | İSS / PRUSA | Sualtı aracı, gerçek CAD görseli, kısa klibe QR |
| 10 | ZEMHERİ / SARA | Araç ve ekip; ilk sezon anlatısı, kısa klibe QR |
| 11 | MATRİS | Birden çok hava aracı ve koordinasyonun temsili şeması |
| 12 | PUSULA / ANDROMEDA | İki farklı çalışma ve yarışma hattını ayıran düzen |
| 13 | GÖKSAV / ASHİNA-H | Doğrulanmış sistem görseli; rapor derecesi açık etiketi |
| 14 | BÜRKÜT | Simülasyon/otonomi anlatısı; Twizy geçmişi teyitten sonra |
| 15 | ÇAĞRI | Haberleşme şeması; gerçek ekip/cihaz fotoğrafı bulunmalı |
| 16 | ALHAZEN | Gerçek laboratuvar görseli + yarışma ekibi; yanlış etiketleri düzelt |
| 17 | ASHİNA İNOVASYON | Araştırma akışı; gerçek görsel bulunmalı, yeni takım bilgisi |
| 18 | Girişimcilik ve inovasyon | INNOSENS, SYNTAX, SCENDERS; belgeli başarılar |
| 19 | Başarılarımız | 6–8 seçilmiş sonuç + doğru dönem ve sonuç türü |
| 20 | 2026 sezonundan | 8 finalist kaydı; dört şehirdeki haberin kapsamı ayrı |
| 21 | Öğrenme ve eğitim | 2025–2026 kampı: 32 saat, 61 belge alan katılımcı; kaynak teyidi |
| 22 | Sanayiyle temas | Turkish Technic / HKTM / diğer doğrulanmış ziyaretlerden seçki |
| 23 | Birlikte yaşanan topluluk | Sosyal sorumluluk, mentorluk ve etkinlik fotoğrafları |
| 24 | Topluluğu birlikte yürütmek | Dört birim; yönetim/üyelik/yarışma ekibi ayrımı |
| 25 | Yanımızda olanlar | Dönemi doğrulanmış sponsorlar; vektör logolar |
| 26 | Üretime katkı | Nakit, malzeme, üretim ve yazılım desteğinin projede karşılığı |
| 27 | Sen de katıl | Üç ayrı katılım yolu ve hedefler; 7 tercih kategorisi |
| 28 | Arka kapak / iletişim | Kurumsal e-posta, web, sosyal hesap, ana QR; sade kapanış |

Sayfa 15 ve 17 için gerçek fotoğraf henüz yok. Şemayla açıklama desteklenebilir; üretilmiş bir ekip veya araç fotoğrafı gerçek faaliyet gibi kullanılamaz. Gerekirse bu sayfalar “araştırma alanları” çift sayfasında birleştirilir; ayrı takım bilgileri korunur.

## Sponsor sürümü

Ortak sayfalardan beslenen ikinci sürümün başlangıç hedefi 32 sayfa. Kapak sponsora göre değişir; öğrenciye dönük sayfa 27–28 yerine altı sayfalık destek modülü gelir:

| Sayfa | Konu | Hazırlanması gereken kanıt |
|---|---|---|
| 27 | Bu dönem neyi üretmek istiyoruz? | Her takımın tarihli hedefi, mevcut aşaması, beklenen çıktı |
| 28 | İhtiyaç ve bütçe | Kalem, adet, nakit/ayni, teklif tarihi, öncelik, sorumlu; rakam uydurulmaz |
| 29 | Desteğiniz nerede görünür? | Araç, forma, stant, etkinlik, dijital paylaşım yerleşimleri; yalnız onaylanabilir haklar |
| 30 | Destek seçenekleri | Yürürlükteki dönem ve resmi hakları teyit edilmiş kademe matrisi |
| 31 | İş birliği ve raporlama | İletişim, ihtiyaç eşleştirme, üniversite süreci, kullanım/çıktı raporu önerisi |
| 32 | İletişim / ortak proje daveti | Kurumsal iletişim, sponsor görüşmesi bağlantısı |

Ziyaret edilen şirketler ve yarışma düzenleyicileri otomatik sponsor sayılmaz. Geçmiş ve güncel sponsorlar ayrı dönem etiketi taşır. İç kayıt tutarları, kişisel telefonlar ve resmi bağış formu bu dosyaya otomatik aktarılmaz. Sponsor görünürlük sözleri, yönetimin/üniversitenin onayladığı kapsamı aşmaz.

## İçerik kayıt sistemi

Ana düzenleme kaynağı `yayin-plani.json`; üretilen Markdown/CSV dosyaları elle farklılaştırılmaz. Tasarım programında değişen metin bu kaynağa geri işlenir.

Her sayfa kaydı şunları taşır: sabit kimlik, sıra, hedef kitle, amaç, başlık, giriş, gövde, maddeler, yerleşim türü, görsel yuvaları, dosya yolu, önerilen açıklama, kaynak referansı, doğrulama durumu, eksikler ve onay durumu.

İddialar `iddia-kayitlari.json` içinde ayrı tutulur: değer, kapsam/sezon, kaynak, doğrulama notu, son kontrol tarihi, sorumlu/onay. “Sitede var” ile “birincil belgeyle doğrulandı” aynı durum değildir. Yönetimin düzeltmesi yeni sürüm olarak işlenir; eski PDF ve manifest korunur.

Medya için web kopyası, yüksek çözünürlüklü orijinal, kırpım/fokal nokta ve açıklama ayrı alanlardır. Fotoğrafın dosya adı değiştiğinde sayfa eşleşmeleri script ile kontrol edilir. Kitapçıkta rakamlar aynı iddia kaydından alınır; elle farklı kopyalar oluşturulmaz.

Kaynak kodu, üretim scripti, kullanılan dosyalar ve SHA-256 listesi teslim paketine girer. Büyük orijinallerin Git'e eklenmesi gerekmez; kaynak paketi yerelde sürümlenebilir. `/varliklar/` erişim korumasız olduğundan doğrulama notları ve taslak sponsor bütçeleri public dizinine konmaz.

## Uygulama sırası ve kabul ölçütleri

1. **Kanıt ve medya düzeltmesi:** denetimdeki yanlış eşleşmeleri çöz; birincil kaynak bulunamayan iddiayı kesin dilde kullanma. Çıktı: tarihli kaynak/iddia listesi.
2. **İçerik dosyası:** her sayfanın metni, görsel listesi, açıklamaları ve eksikleri hazır. Çıktı: JSON, Markdown ve CSV; başka tasarım programında çalışılabilir paket.
3. **Baskı görsel seçkisi:** 28 sayfa için yaklaşık 45–60 birbirinden farklı, konuyla ilişkili fotoğraf/çizim. Her görselin orijinali, ölçüsü ve kullanım nedeni kayıtlı. Bu sayı zorunlu kota değil; tekrar kareler ayıklanır.
4. **Dört gerçek örnek sayfa:** kapak, ASHİNA teknik profili, eğitim/topluluk sayfası ve sponsor iş birliği sayfası. Düzenlenebilir metin, gerçek fotoğraflar ve gerekiyorsa özgün temsili şema. Sayfa başına ayrı PNG + A4 PDF örneği. Örnekler tüm yayının tonunu belirler.
5. **Tam yayın:** onaylanan düzen ailesiyle 28 sayfa ve sponsor modülü. Başlık/gövde/altyazı taşmaları, sayfa numaraları, linkler ve görsel ppi kontrol edilir.
6. **Yönetim değerlendirmesi:** web sitesinin ana sayfa, takımlar, başarılar, katılım ve sponsorluk ekran görüntüleri; kitapçık örnekleri; açık doğrulama listesi. Geri bildirim sayfa/iddia kimliğiyle toplanır.
7. **Son teslim:** sürümlü dijital PDF, matbaa gereksinimine göre baskı PDF'si, HTML/CSS kaynak, manifest, scriptler ve kullanılabilir medya paketi. Fiziksel prova, QR testi ve son içerik kontrolü yapılır.

Tanıtım Günleri tarihi henüz verilmediği için takvim gününe bağlanmış teslim sözü yok. Öncelik sırası sabit: yönetimin içeriği düzeltebileceği kaynak paket → dört örnek sayfa → bütün kitapçık → sponsor modülü → baskı provası.

## Görsel üretimi ne zaman kullanılır?

Önce gerçek içerik ve görsel seçkisi tamamlanır. Gerekirse kapak kompozisyonu için 2–3 konsept veya çalışma prensibini açıklayan temsili çizimler oluşturulur. Üretim promptu, kullanılan referanslar, seçilen çıktı ve düzenleme geçmişi saklanır. Üretilmiş görsel gerçek araç, ekip, ödül veya etkinlik kanıtı olarak gösterilmez. Yazı/logo görselin içine gömülmez; son tasarımda düzenlenebilir kalır.

## Yönetimden içerik aşamasında alınacak bilgiler

Tanıtım Günleri tarihi/stand yeri; 2026–2027 aktif ekip ve açık alım listesi; alt ekiplerin ad ve dönem ilişkileri; tartışmalı başarıların birincil kayıtları; sponsor dönem/kademe teyidi; teknik hedef/ihtiyaç kalemleri; orijinal fotoğraf ve logolar. Bu bilgiler geldikçe ilgili kayıt güncellenir, bütün kitapçık tekrar yazılmaz.
