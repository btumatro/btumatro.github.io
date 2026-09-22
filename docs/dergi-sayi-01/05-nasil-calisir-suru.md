# Nasıl Çalışır? Sürü İHA

> **Dizgi notu** (basılmaz): Çift sayfa. Üstten görünüm çizimi: 5 dron, önce "V"
> formasyonunda, sonra bir engelin etrafından ayrılıp yeniden birleşirken. Merkezi ve
> dağıtık mimari için yan yana iki küçük şema. Fotoğraf: webmedya-suru-iha-35 veya
> galeri-matris-test-alani. Genel anlatımdır; **MATRİS kaptanı okuyup kendi
> yaklaşımlarını kutuya eklemeli.**

## Bir filo nasıl tek bir beyin gibi davranır?

**Spot:** Bir dronu uçurmak zor. Beş dronu birbirine çarpmadan, aynı görevi paylaşarak
ve biri düştüğünde görevi yarıda bırakmadan uçurmak bambaşka bir mühendislik problemi.

### Neden sürü?

Tek büyük bir hava aracı yerine birden fazla küçük araç kullanmanın üç avantajı var:
**Dayanıklılık** (biri arızalansa bile görev sürer), **kapsama** (geniş bir alan aynı anda
taranır) ve **maliyet** (küçük araçlar daha ucuz ve kolay değiştirilir). Bu yüzden arama
kurtarma, tarım, haritalama ve gösteri uçuşları gibi alanlarda sürü sistemleri giderek
yaygınlaşıyor.

### İki mimari: merkezi ve dağıtık

**Merkezi mimaride** yer istasyonundaki tek bir bilgisayar her aracın nerede olması
gerektiğini hesaplar ve komut gönderir. Kurması kolaydır, ama merkez ile bağlantı
koptuğunda sürü "kör" kalır.

**Dağıtık mimaride** her araç kendi kararını verir; yalnızca komşularından aldığı
bilgiyle (onların konumu, hızı, görevi) davranışını ayarlar. Doğadaki kuş ve balık
sürüleri buna benzer. Daha dayanıklıdır ama tasarlaması ve test etmesi daha zordur.
Gerçek sistemler çoğu zaman ikisinin karışımıdır.

### Sürünün üç temel problemi

**1. Formasyon koruma.** Araçlar belirli bir şekli (hat, V, kare) korurken birlikte
hareket etmeli. Her araç lidere veya sanal bir merkeze göre kendi hedef konumunu hesaplar
ve rüzgâr gibi bozucu etkilere karşı sürekli düzeltme yapar.

**2. Çakışma önleme.** İki araç aynı noktaya yönelirse hangisi kaçacak? Her araç
çevresinde bir "güvenlik balonu" tanımlanır; başka bir aracın balonuna girmek üzere
olduğunda hız veya yön değiştirir. Bu kararların hızlı ve öngörülebilir olması gerekir.

**3. Görev dağıtımı.** Beş aracın on hedefi ziyaret etmesi gerekiyorsa hangi araç hangi
hedefe gider? Mesafe, batarya durumu ve aracın yükü hesaba katılarak görevler dağıtılır.
Bir araç düştüğünde görevleri kalanlar arasında **yeniden planlanır**.

### Haberleşme: sürünün sinir sistemi

Araçların birbirinin nerede olduğunu bilmesi için sürekli konum paylaşması gerekir.
Haberleşme gecikirse bir aracın bildiği konum, diğerinin gerçek konumundan saniyeler
geride kalabilir. Bu yüzden sürü algoritmaları gecikmeye ve kayıp paketlere dayanıklı
tasarlanır.

> **Kutu — MATRO'da:** MATRİS takımımız TEKNOFEST HAVELSAN Sürü İHA Yarışması'nda
> 2024'te Türkiye 9.su oldu, 2026'da Gaziantep'teki finalde yarıştı. Takım; sürü hâlinde
> otonom uçuş, çoklu araç koordinasyonu ve görev dağıtım algoritmaları üzerine çalışıyor.
> *[Kaptan kontrolü: kullandığınız mimariyi ve bir test anınızı bir-iki cümleyle ekleyin.]*
