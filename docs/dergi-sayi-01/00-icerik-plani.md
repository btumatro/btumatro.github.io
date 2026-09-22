# MATRO Dergi — Sayı 01 İçerik ve Yayın Planı

Hazırlanma: 22 Eylül 2026 · Durum: içerik taslağı (dizgi öncesi)

Kuşe kağıda basılacak, **üniversitenin tüm öğrencilerine** hitap eden genel bir
bilim-teknoloji ve kampüs dergisinin ilk sayısı. MATRO'nun tanıtım faaliyetleri
derginin omurgası, ama tek konusu değil: gündem, yapay zekâ, makine-robot-otomasyon
anlatımları, kampüs rehberleri, röportajlar ve eğlence sayfaları da var.

Her yazı ayrı bir dosyada, dizgiye hazır metin olarak duruyor. Dosyaların başındaki
"Dizgi notu" bölümü görsel önerisini, sayfa sayısını ve kaynakları verir; basılmaz.

## 1. Dergi kimliği

**Ad önerileri** (karar yönetim kurulunun):

| Ad | Neden |
|---|---|
| **MATRO Dergi** | En güvenli seçenek; marka zaten tanınıyor. |
| **EKSEN** | Makine ve robotikte temel kavram; "yönümüz" anlamı da taşıyor. |
| **PROTOTİP** | Atölye kültürü: önce yap, sonra iyileştir. |
| **TORK** | Kısa, akılda kalıcı; mekanik ve "itici güç" çağrışımı. |

**Yayın sıklığı:** Yılda iki sayı. Güz sayısı sezon açılışı ve Topluluk Tanıtım
Günleri'ne, bahar sayısı TEKNOFEST finalleri öncesine denk gelir. İlk sayı Ekim 2026.

**Okur:** BTÜ'nün tüm öğrencileri (özellikle birinci sınıflar), aday üyeler,
akademisyenler, sponsor ve iş birliği kurumları, ziyaret edilen okullar, mezunlar.

**Ton:** Popüler bilim dergisi ile kampüs dergisi arası. Rakamı kaynaklı, fotoğrafı
kendi ekiplerimize ait, abartısız.

## 2. Baskı şartnamesi (matbaaya sorulacak başlangıç değerleri)

| Kalem | Öneri | Not |
|---|---|---|
| Ebat | A4 (210 × 297 mm), dikey | Mevcut kitapçık ve dergi şablonlarıyla aynı |
| Sayfa sayısı | **80** (kapaklar dahil), alternatif 64 | 80 sayfa Amerikan cilt; 64 ve altı tel dikiş. Sayfa sayısı 4'ün katı olmalı. |
| İç kağıt | 130–135 gr mat kuşe | 115 gr ekonomik ama ince; 170 gr ağır ve pahalı |
| Kapak | 300–350 gr kuşe, mat selefon; masthead'de isteğe bağlı lokal lak | Amerikan cilt kapağı 300/350 gr |
| Cilt | Amerikan cilt (80 sayfa) veya tel dikiş (64 sayfa) | Amerikan ciltte sırt kalınlığı matbaadan alınıp kapağa eklenir |
| Renk | 4 renk (CMYK) | Koyu zeminli sayfalar için matbaadan zengin siyah değeri istenmeli |
| Taşma payı | 3 mm her kenar | Kesim işaretiyle |
| Güvenli alan | Kenardan 10 mm, cilt tarafında 15 mm | Amerikan ciltte iç kenar açılmaz; çift sayfaya yayılan fotoğrafta yüz ortaya gelmemeli |
| Görsel çözünürlük | Basılı boyutta 300 ppi | Aşağıdaki "Görsel sorunu"na bakın |
| Teslim dosyası | PDF/X-1a veya PDF/X-4, fontlar gömülü | Renk profili matbaaya sorulmalı (genellikle ISO Coated v2 / Fogra39) |

Kaynak: matbaa ürün sayfaları ([istanbulofset.net](https://istanbulofset.net/dergi-basimi.html),
[kitapbastir.com](https://www.kitapbastir.com/dergi/), [bursabaski.net](https://www.bursabaski.net/dergi-baski-fiyatlari)).
Kesin değerler seçilen matbaanın teknik şartnamesiyle doğrulanmalı.

### Görsel sorunu (en önemli ön koşul)

Sitedeki fotoğraflar web için küçültüldü (çoğu 1200–1600 px). Kuşe baskıda:

- **Tam sayfa, taşmalı fotoğraf** için yaklaşık 2550 × 3550 px gerekir.
- **Yarım sayfa** için yaklaşık 2550 × 1750 px.
- **1200 px'lik bir görsel** 300 ppi'de yalnızca ~10 cm genişliğe basılabilir.

Drive'daki orijinaller (ör. 4032 × 3024 test indirmesi) bu ihtiyacı karşılıyor.
**Dizgiden önce her büyük görselin orijinali Drive'dan indirilmeli.** Instagram
afişlerinden kırpılan görseller dergide yalnızca küçük boyutta kullanılmalı.
Gündem ve yapay zekâ sayfaları için başka kurumların fotoğrafları **kullanılmaz**;
bu sayfalar infografik, çizim ve tipografiyle tasarlanır.

## 3. Bölümler ve sayfa planı (80 sayfa)

Faaliyetlerin ayrıntılı işlendiği "Sezon Dosyası" (10 sayfa) eklenince içerik 64 sayfaya
sığmıyor. Öneri **80 sayfa, Amerikan cilt** (sırtlı, daha dergi görünümlü). 64 sayfa tel
dikişte kalınmak istenirse "Kısaltma" sütunundaki sayfalar çıkarılır.

| Sayfa | Bölüm | İçerik | Dosya / durum | Kısaltma |
|---|---|---|---|---|
| 1 | Kapak | Masthead, kapak fotoğrafı, 4 manşet | Orijinal fotoğraf gerekli | |
| 2 | İç kapak | Platin sponsorlar | sponsors.json | |
| 3 | İçindekiler + künye | | Otomatik | |
| 4 | Editörden | Başkanın yazısı | 01-editorden.md (**onay gerekli**) | |
| 5 | Kısa kısa | Topluluktan 8 kısa haber | 02-kisa-kisa.md | |
| **GÜNDEM** | | | | |
| 6–7 | Gündem | TEKNOFEST 2026: Diyarbakır'dan Şanlıurfa'ya | 15-gundem.md §1 | |
| 8–9 | Gündem | Gökyüzü ve uzayda Türkiye: KAAN, HÜRJET, TÜRKSAT 6A | 15-gundem.md §2 | çıkar |
| 10–11 | Gündem | Dünyada robotlar: 10 yılda iki kat | 15-gundem.md §3 | |
| 12 | Gündem | Gezdiğimiz yerlerden haberler (Turkish Technic, Alp Havacılık) | 15-gundem.md §5 | |
| 13 | Gündem | Uzay kısa: TUA Astro Hackathon, NASA Space Apps, GUHEM | 15-gundem.md §4 | |
| **YAPAY ZEKÂ** | | | | |
| 14–15 | Yapay zekâ | 2026'da yapay zekâ: Stanford raporundan 8 çıkarım | 16-yapay-zeka.md §1 | |
| 16–17 | Yapay zekâ | Ajanlar ve fiziksel yapay zekâ | 16-yapay-zeka.md §2 | 1 sayfaya indir |
| 18 | Yapay zekâ | Öğrenci olarak yapay zekâyı doğru kullanmak | 16-yapay-zeka.md §3 | |
| **KAPAK DOSYASI** | | | | |
| 19–24 | Kapak dosyası | Bir aracın doğuşu: fikirden final alanına | 03-kapak-dosyasi.md | 4 sayfaya indir |
| 25 | Harita | 2026 finalleri: 8 takım, 5 final yeri | Sponsorluk dergisinden | |
| **MATRO** | | | | |
| 26–35 | Sezon dosyası | 2025–2026'da neler yaptık? 30 faaliyet, ayrıntılı | 21-sezon-dosyasi.md | 6 sayfaya indir |
| 36–43 | Takımlarımız | 13 takım (4 tam sayfa + 4 çift takım sayfası) | Sponsorluk dergisinden | 6 sayfaya indir |
| 44–45 | Röportaj | Takım kaptanı | 10-roportaj-sablonlari.md (**ekip yapacak**) | |
| 46–47 | Foto-röportaj | Atölyede bir gün | 11-atolyede-bir-gun.md (**çekim gerekli**) | çıkar |
| 48–49 | Başarı arşivi | 13 yılın dereceleri | achievements.json | 1 sayfaya indir |
| **NASIL ÇALIŞIR?** | | | | |
| 50–51 | Nasıl çalışır? | Su altında yön bulmak: AUV | 04-nasil-calisir-auv.md | |
| 52–53 | Nasıl çalışır? | Sürü İHA | 05-nasil-calisir-suru.md | |
| 54–55 | Nasıl çalışır? | Karıştırmaya karşı haberleşme | 06-nasil-calisir-haberlesme.md | çıkar |
| 56–57 | Nasıl çalışır? | PLC: fabrikanın beyni | 20-plc-otomasyon.md | |
| **KAMPÜS VE KARİYER** | | | | |
| 58–59 | Dosya | 20 binden 1,6 milyona TEKNOFEST + başvuru rehberi | 07-teknofest-dosyasi.md | |
| 60–61 | Sektör | Bursa'nın savunma ve havacılık ekosistemi | 08-bursa-ekosistemi.md | |
| 62–63 | Uzay | Gezeravcı'dan GUHEM'e | 09-uzay.md | |
| 64–65 | Kampüs | BTÜ rehberi, staj, ücretsiz yazılımlar | 17-kampus-rehberi.md | |
| 66 | Rehber | MATRO'ya katıldım, şimdi ne olacak? | 12-ilk-yil-rehberi.md | |
| 67 | Röportaj | Yeni üyeler: "İlk dönemim" | 10-roportaj-sablonlari.md §5 | çıkar |
| 68–69 | Röportaj | Mezun: "MATRO'dan sonra" | 10-roportaj-sablonlari.md §2 | |
| **KEYİF** | | | | |
| 70–71 | Kendin yap | İlk robotun: çizgi izleyen araç | 18-evde-robot.md | |
| 72 | Öneriler | İzle, oku, dinle | 19-oneriler.md | |
| 73 | Sözlük | Atölye sözlüğü: 24 terim | 13-sozluk.md | |
| 74 | Bulmaca | Kelime avı + cevaplar | 14-bulmaca.md | sözlükle birleştir |
| **KAPANIŞ** | | | | |
| 75–76 | Basında biz + teşekkür | | basinda-biz.json | |
| 77 | Sponsorlar | Logo duvarı | sponsors.json | |
| 78 | Sponsor ol | Kademeler, süreç, QR | sponsorship.json | |
| 79 | Bize katıl | Başvuru QR'ları, takım listesi | join.json | |
| 80 | Arka kapak | | | |

## 4. Ekipten gelmesi gerekenler (dizgiden önce)

1. **Başkanın editör yazısı** ya da taslağın onayı (01-editorden.md).
2. **İki röportaj**: bir takım kaptanı, bir mezun. Sorular hazır. Kayıt alınmalı,
   yazıya dökülmeli ve son metin konuşan kişiye onaylatılmalı.
3. **Kişisel veri onayı**: Dergide adı, fotoğrafı veya sözü geçen herkesin yazılı onayı.
   Telefon ve kişisel e-posta basılmaz.
4. **"Atölyede bir gün" çekimi**: 12–15 kare, en az 12 MP, çekim listesi hazır.
5. **Orijinal fotoğraflar**: Planda kullanılan her görselin Drive orijinali.
6. **Teknik kontrol**: 04, 05, 06 ve 20 numaralı yazılar genel anlatımlar. İlgili
   takım kaptanları okuyup işaretlesin; araçlarımıza özel ölçü veya performans
   bilgisi yalnızca takım belgesiyle eklensin.
7. **Gündem sayfaları baskıdan bir hafta önce yeniden kontrol edilmeli.** Bu metinler
   22 Eylül 2026 itibarıyla yazıldı; TEKNOFEST Şanlıurfa (30 Eylül – 4 Ekim)
   sonrasında güncellenmesi gerekebilir.

## 5. Kaynaklar (araştırma, 22 Eylül 2026)

- TEKNOFEST 2026: [TÜBİTAK Bilim Genç, 15 Ocak 2026](https://bilimgenc.tubitak.gov.tr/makale/teknofest-2026-teknoloji-yarismalari-basvurulari-basladi),
  [haber.aero yarışma takvimi](https://haber.aero/aero-gundem/teknofest-2026-yarisma-takvimi-aciklandi/),
  [Diyarbakır finalleri, Yeni Birlik](https://www.gazetebirlik.com/teknoloji/teknofest-2026-heyecani-diyarbakirda-basladi-11-yarismada-buyuk-final/1095564),
  [TEKNOFEST 2026 Şanlıurfa duyurusu](https://www.teknofest.org/tr/duyurular/teknofest-2026-yilinda-sanliurfada/)
- TEKNOFEST büyümesi: [Anadolu Ajansı, 19 Ekim 2024](https://www.aa.com.tr/tr/teknofest/turkiyenin-teknoloji-gelecegi-teknofestin-yarismaci-sayisi-1-5-milyonu-asti/3367054),
  [TEKNOFEST etkinlikleri 2018–2025](https://www.teknofest.org/tr/content/teknofest-events/),
  [başvuru adımları](https://teknofest.org/tr/yarismalar/nasil-basvurulur/)
- Havacılık gündemi: [Defence Turkey, Farnborough 2026](https://defenceturkey.com/news/turk-havacilik-ve-uzay-sanayii-farnborough-2026da-kaan-t-70-t-925-ve-hurjet-programlarina-iliskin-son-durumu-paylasti)
- Robotik: [IFR World Robotics 2025 basın bülteni, 25 Eylül 2025](https://ifr.org/ifr-press-releases/news/global-robot-demand-in-factories-doubles-over-10-years)
- Yapay zekâ: [Stanford HAI AI Index 2026, 12 çıkarım, 13 Nisan 2026](https://hai.stanford.edu/news/inside-the-ai-index-12-takeaways-from-the-2026-report),
  [Türkiye Yapay Zeka İnisiyatifi 2026 trendleri](https://turkiye.ai/yapay-zeka-trendleri-2026/)
- Bursa ekosistemi: [Fuar Dergisi, 30 Haziran 2026](https://www.fuardergisi.com.tr/bursa-savunma-sanayiinin-yeni-doneminde-stratejik-rol-ustlenecek)
- Uzay: [TÜBİTAK UZAY](https://uzay.tubitak.gov.tr/en/our-first-astronaut-alper-gezeravci-started-his-space-journey-as-part-of-a-science-mission-on-january-19-2024-00-49/),
  [Axiom Mission 3](https://en.wikipedia.org/wiki/Axiom_Mission_3)
- BTÜ: [Vikipedi](https://tr.wikipedia.org/wiki/Bursa_Teknik_%C3%9Cniversitesi),
  [BTÜ yerleşkeler](https://tercih.btu.edu.tr/tr/sayfa/detay/3044/yerleskeler)
- Staj: [Eskişehir Teknik Üniversitesi SGK bilgilendirmesi](https://mf.eskisehir.edu.tr/tr/Icerik/Detay/sgk-sigorta-islemleri-ile-ilgili-onemli-bilgiler)
- Yazılım lisansları: [SOLIDWORKS öğrenci sürümü](https://www.solidworks.com/product/students/design-standard)
- AUV: [RoboNation, Bumblebee AUV raporu](https://robonation.org/app/uploads/sites/4/2019/10/NSU_RS17_Paper.pdf),
  [Ocean News: RoboSub akustik pinger'lar](https://oceannews.com/news/subsea-and-survey/acoustic-pingers-help-contestants-in-robosub-competition/)
