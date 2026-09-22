# Nasıl Çalışır? PLC: Fabrikanın Beyni

> **Dizgi notu** (basılmaz): Çift sayfa. Ana görsel: basit bir konveyör hattı çizimi
> (sensör → PLC → motor/piston), yanında "tarama döngüsü" diyagramı (Girişleri oku →
> Programı çalıştır → Çıkışları yaz → tekrar). Küçük bir merdiven diyagramı (ladder)
> örneği. Fotoğraf: galeri-pusula-atolye. Makine, mekatronik ve elektrik
> öğrencilerinin hepsine hitap eden genel bir yazı.

## Bir fabrika nasıl karar verir?

**Spot:** Bir otomobil fabrikasında kaynak robotunun ne zaman çalışacağına, bir
şişeleme hattında kapağın ne zaman kapanacağına karar veren şey çoğu zaman aynı cihazdır:
Programlanabilir mantık denetleyicisi, kısaca PLC.

### PLC nedir?

PLC, fabrika koşulları için tasarlanmış endüstriyel bir bilgisayardır. Toza, titreşime,
elektriksel gürültüye ve sıcaklık değişimine dayanır; yıllarca durmadan çalışabilir.
Bir tarafına sensörler (butonlar, sınır anahtarları, yakınlık sensörleri, sıcaklık
ölçerler) bağlanır, diğer tarafına eyleyiciler (motorlar, valfler, pistonlar, lambalar).

### Tarama döngüsü

Bir PLC'nin çalışma mantığı basit ve öngörülebilirdir. Saniyede defalarca şu döngüyü
tekrarlar:

1. **Girişleri oku:** Tüm sensörlerin o anki durumunu belleğe al.
2. **Programı çalıştır:** Bu duruma göre ne yapılacağını hesapla.
3. **Çıkışları yaz:** Motorlara, valflere komutları gönder.

Bu döngünün süresi (tarama süresi) genellikle milisaniyeler mertebesindedir. Öngörülebilir
olması çok önemlidir: Bir acil durdurma butonuna basıldığında sistemin ne kadar sürede
tepki vereceği bilinmelidir.

### Merdiven diyagramı

PLC'ler farklı dillerle programlanabilir. En yaygın olanı **merdiven diyagramı
(ladder)**. Adını, röleli elektrik şemalarına benzeyen görünümünden alır: İki dikey
çizgi arasındaki her "basamak" bir kuraldır. Örneğin:

> *Başlat butonuna basıldıysa VE acil durdurma basılı değilse → konveyör motorunu çalıştır.*

Elektrik şeması okuyabilen bir teknisyenin kolayca anlayabilmesi, bu dilin yıllardır
sahada kalmasının nedeni. Uluslararası IEC 61131-3 standardı merdiven diyagramının yanı
sıra yapılandırılmış metin (ST) ve fonksiyon blok diyagramı (FBD) gibi başka dilleri de
tanımlar.

### Endüstri 4.0 ile değişen ne?

Klasik PLC tek başına çalışan bir kutuydu. Bugün PLC'ler ağa bağlı; ürettikleri veri
fabrika yönetim sistemlerine, bulut platformlarına ve **dijital ikiz** modellerine akıyor.
Dijital ikiz, fiziksel hattın bilgisayardaki eş zamanlı kopyası: Makine arızalanmadan önce
titreşim ve sıcaklık verisinden arızayı tahmin etmek (kestirimci bakım) ya da yeni bir
ürünü hatta almadan simülasyonda denemek mümkün hâle geliyor.

> **Kutu — MATRO'da:** Sanayide Dijital Teknolojiler takımımız Endüstri 4.0, IoT ve
> dijital ikiz uygulamaları üzerine çalışıyor; TEKNOFEST'te 2021'de Türkiye 3.sü, 2025'te
> Türkiye 8.si oldu. 2026'da PUSULA ekibimiz Sanayide Robotik Uygulamalar'da, ANDROMEDA
> ekibimiz ise Akıllı Fabrika Sistemleri Programlama kategorisinde Türkiye finalistiydi.

> **Kutu — Nereden başlamalı?** Pek çok PLC üreticisinin ücretsiz simülasyon ve
> programlama yazılımı var. Bir trafik lambası ya da garaj kapısı otomasyonu, ilk
> merdiven diyagramı için klasik alıştırmalardır.
