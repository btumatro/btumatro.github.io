# Yapay Zekâ

> **Dizgi notu** (basılmaz): Sayfa 12–16. Fotoğraf yok; büyük rakamlar, ikonlar ve bir
> "ajan döngüsü" diyagramı (Algıla → Planla → Araç kullan → Kontrol et). Kaynakların
> tamamı sayfa altında. Rakamlar Stanford HAI AI Index 2026 raporundan (13 Nisan 2026).

---

## 1. 2026'da yapay zekâ: Stanford raporundan 8 çıkarım

**Spot:** Stanford Üniversitesi'nin her yıl yayımladığı AI Index raporu, yapay zekânın
nerede olduğunu rakamlarla anlatan en kapsamlı kaynaklardan biri. 2026 raporundan
mühendislik öğrencisini en çok ilgilendiren başlıkları seçtik.

**1. Kullanım internetten hızlı yayıldı.** Üretken yapay zekâ üç yılda nüfusun yüzde
53'üne ulaştı. Bu hız, kişisel bilgisayarın ve internetin yayılma hızından daha yüksek.

**2. Öğrenciler zaten kullanıyor, kurallar yetişemiyor.** ABD'de her beş lise ve
üniversite öğrencisinden dördü okul işlerinde yapay zekâ kullanıyor. Buna karşın
öğretmenlerin yalnızca yüzde 6'sı okulunun yapay zekâ politikasını açık buluyor.

**3. Gerçek dünya görevlerinde büyük sıçrama.** Modellerin gerçek dünya görevlerini
tamamlama başarısı bir yılda yüzde 20'den yüzde 77,3'e çıktı. Aynı modeller matematik
olimpiyatı sorularında insan düzeyini aşarken, bir analog saati okumak gibi basit
görünen işlerde hâlâ zorlanabiliyor. Yetenek dengesiz dağılıyor.

**4. Yatırım rekor kırdı.** Küresel kurumsal yapay zekâ yatırımı 2025'te 581,7 milyar
dolara ulaştı; bir önceki yıla göre yüzde 130 artış.

**5. Giriş seviyesi işler değişiyor.** ABD'de 22–25 yaş arası yazılım geliştiricilerin
istihdamı 2024'ten bu yana yaklaşık yüzde 20 düştü. Rapor bunun nedenleri üzerinde
temkinli, ama mesaj açık: Yalnızca kod yazmak değil, problem tanımlamak, sistem
kurmak ve sonucu doğrulamak daha değerli hâle geliyor.

**6. Bilim yapmanın aracı oldu.** Doğa, fizik ve yaşam bilimlerinde yapay zekâ kullanan
yayınlar yüzde 26–28 arttı.

**7. Enerji faturası büyüyor.** Yapay zekâ veri merkezlerinin kapasitesi 29,6 gigavata
ulaştı; bu, New York eyaletinin tüm elektrik ihtiyacına denk.

**8. Şeffaflık azalıyor.** Temel modellerin ne kadar bilgi paylaştığını ölçen şeffaflık
endeksinin ortalaması 58'den 40'a düştü. En güçlü modeller, en az bilgi açıklananlar.

Kaynak: [Stanford HAI, AI Index 2026: 12 çıkarım](https://hai.stanford.edu/news/inside-the-ai-index-12-takeaways-from-the-2026-report)

---

## 2. Ajanlar ve fiziksel yapay zekâ

**Spot:** 2026'nın iki anahtar kavramı: Görev alıp kendi başına bitiren yazılım
"ajanları" ve algıladığı dünyada hareket eden "fiziksel yapay zekâ". İkincisi, robotik
ve otomasyonla uğraşan bizim için doğrudan meslek konusu.

### Sohbetten ajana

İlk üretken yapay zekâ araçları soru-cevap üzerine kuruluydu: Siz sorarsınız, o
yazar. **Yapay zekâ ajanı** ise bir hedef alır, bunu adımlara böler, gerektiğinde başka
araçları (arama motoru, kod çalıştırıcı, takvim, veritabanı) kullanır, sonucu kontrol
eder ve eksikse yeniden dener. Türkiye Yapay Zeka İnisiyatifi'nin 2026 raporu bu
dönüşümü "öneri veren araçtan dijital ekip arkadaşına" geçiş olarak tanımlıyor.

> **Diyagram:** Hedef → Algıla → Planla → Araç kullan → Sonucu kontrol et → (gerekirse
> başa dön) → Teslim et

Bu döngü bir mühendise tanıdık gelmeli: Bir robotun kontrol döngüsü de aynı mantıkla
çalışır. Algıla, karar ver, uygula, hatayı ölç, düzelt.

### Ekrandan sahaya: fiziksel yapay zekâ

Aynı rapor 2026'nın öne çıkan trendleri arasında **fiziksel yapay zekânın
ölçeklenmesini** sayıyor: Otonom araçlar, dronlar, sensör ağları ve dijital ikizler.
Fiziksel yapay zekânın dijital olandan temel farkı, hatanın bedeli. Bir sohbet botunun
yanlış cevabı düzeltilebilir; tarlada ilerleyen bir aracın yanlış kararı bir ürünü
ezebilir, havadaki bir dronun hatası düşüşle biter.

Bu yüzden fiziksel yapay zekâ, klasik mühendislikle iç içe:

- **Algı:** Kamera, LiDAR, sonar, IMU. Görüntü işleme ve sensör füzyonu.
- **Karar:** Rota planlama, görev dağıtımı, öğrenme tabanlı kontrol.
- **Güvenlik:** Arıza durumunda güvenli duruş, insanla ortak çalışma kuralları, test.

MATRO'da bu üç katmanın hepsi var: ASHİNA derin öğrenme tabanlı hedef tespiti yapıyor,
tarımsal kara araçlarımız görüntü işlemeyle bitki sağlığını ayırt ediyor, sürü İHA
takımımız birden fazla aracın ortak karar vermesi üzerine çalışıyor.

Kaynak: [Türkiye Yapay Zeka İnisiyatifi, 2026 Yapay Zeka Trendleri](https://turkiye.ai/yapay-zeka-trendleri-2026/)

---

## 3. Öğrenci olarak yapay zekâyı doğru kullanmak

**Spot:** Yapay zekâ bir hesap makinesi gibi: Doğru kullanana zaman kazandırır, yerine
düşünmesini bekleyene yanlış cevap verir. Atölyede öğrendiğimiz birkaç kural.

**Önce kendin dene.** Bir devre, bir kod parçası ya da bir mukavemet hesabı
üzerinde önce kendin düşün, sonra yapay zekâya sor. Tersini yaparsan öğrenme kısmını
atlamış olursun ve sınavda yapay zekâ yanında olmayacak.

**Kaynak iste, kaynağı aç.** Yapay zekâ var olmayan makale, yanlış formül veya uydurma
datasheet değeri üretebilir. Bir değeri kullanmadan önce üreticinin datasheet'inden,
ders kitabından veya standarttan doğrula.

**Kodu anlamadan çalıştırma.** Özellikle motor sürücüsü, batarya yönetimi veya
yüksek akım içeren sistemlerde anlamadığın kodu donanıma yükleme. Önce simülasyonda,
sonra düşük güçte test et.

**Kişisel ve gizli veriyi paylaşma.** Takımının henüz yarışmaya sunulmamış tasarımını,
sponsor sözleşmesini veya bir arkadaşının kişisel bilgisini yapay zekâ araçlarına yapıştırma.

**Kurallara bak.** Dersin, ödevin ve yarışmanın yapay zekâ kullanımı hakkında kuralı
olabilir. Rapor yazarken yapay zekâdan yardım aldıysan bunu belirtmek çoğu zaman
yeterli ve dürüst olandır.

**Asıl beceri: doğru soruyu sormak.** Problemi net tanımlayan, kısıtları söyleyen ve
çıktıyı kontrol eden öğrenci yapay zekâdan en çok verimi alır. Bu, zaten iyi bir
mühendisin yaptığı şey.
