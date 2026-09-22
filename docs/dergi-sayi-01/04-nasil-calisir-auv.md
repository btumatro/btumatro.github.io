# Nasıl Çalışır? Su Altında Yön Bulmak

> **Dizgi notu** (basılmaz): Çift sayfa. Sol sayfada büyük bir AUV kesit çizimi
> (kendi CAD görselimiz tasarim-iss-auv-izometrik temel alınarak çizilebilir), sensörler
> numaralı etiketlerle. Sağ sayfada metin ve "Neden GPS çalışmaz?" kutusu. Genel
> anlatımdır; **İSS/PRUSA kaptanı okuyup kendi araçlarında olmayan sensörleri
> işaretlemeli**, kendi araçlarına özel bir bilgi varsa kutuya eklenmeli.

## Bir otonom su altı aracı nasıl görür?

**Spot:** Suyun altında GPS yok, radyo dalgaları birkaç metrede sönüyor, kamera
bulanık suda birkaç metreden ötesini göremiyor. Yine de otonom bir su altı aracı (AUV)
kapıdan geçmeli, hedefe ulaşmalı ve eve dönmeli. Peki nasıl?

### Önce sorun: Su her şeyi zorlaştırır

Karada bir robotun nerede olduğunu bulmanın en kolay yolu GPS'tir. Ama GPS sinyalleri
suya girdiği anda sönümlenir. Wi-Fi ve radyo da aynı durumda. Işık ise hızla zayıflar ve
dağılır; havuzda iyi çalışan bir kamera denizde birkaç metreden sonra işe yaramayabilir.
Bu yüzden bir AUV tek bir sensöre değil, birbirinin eksiğini kapatan bir sensör ailesine
güvenir.

### Sensör ailesi

**1. IMU (Ataletsel ölçüm birimi).** Üç eksenli ivmeölçer ve üç eksenli jiroskoptan
oluşur. Aracın nasıl döndüğünü ve ivmelendiğini çok hızlı ölçer. Tek başına kullanılırsa
küçük hatalar zamanla birikir ve araç "nerede olduğunu" yavaş yavaş kaybeder. Buna
kayma (drift) denir.

**2. Derinlik sensörü.** Su basıncını ölçer. Basınç her 10 metrede yaklaşık 1 atmosfer
arttığı için derinliği çok doğru verir. Aracın dikey konumu için en güvenilir kaynaktır.

**3. DVL (Doppler hız ölçer).** Tabana doğru, genellikle çapraz yerleştirilmiş dört
akustik ışın gönderir ve yankının frekans kaymasından aracın tabana göre hızını
hesaplar. IMU'nun biriktirdiği hatayı düzeltmenin en etkili yoludur, ancak pahalıdır.

**4. Hidrofon dizisi.** Suyun altındaki "kulak". Yarışmalarda hedefler çoğu zaman
belirli frekansta ses yayan akustik vericilerle (pinger) işaretlenir. Birkaç hidrofona
sesin ulaşma zaman farkı ölçülerek sesin yönü bulunur.

**5. Kameralar.** Biri ileriye, biri aşağıya bakar. Kapı, şamandıra, yerdeki yön
işaretleri gibi görsel hedefler görüntü işlemeyle tanınır. Bulanık suda renk düzeltme
ve kontrast artırma gibi ön işlemler şarttır.

**6. Sonar (isteğe bağlı).** Ses dalgalarıyla görüntü oluşturur, karanlık ve bulanık suda
kameranın göremediği engelleri görür.

### Hepsini birleştirmek: sensör füzyonu

Hiçbir sensör tek başına yeterli değil. IMU hızlı ama kayıyor; DVL doğru ama yavaş;
kamera anlamlı ama menzili kısa. **Sensör füzyonu**, bu ölçümleri her birinin güvenilirliğine
göre ağırlıklandırarak tek bir konum ve yön tahmininde birleştirir. Bu iş için en sık
kullanılan yöntem Kalman filtresi ve türevleridir.

Sonuç: Araç, "şu an kapıdan 2 metre uzaktayım, 1,5 metre derinlikteyim ve 10 derece
sola dönmem gerekiyor" diyebilir. Buradan sonrası kontrol algoritmasının işidir:
İticilere hangi gücün verileceğini hesaplamak.

> **Kutu — Neden GPS çalışmaz?** GPS uydularının yayını, suyun içinde çok kısa
> mesafede sönümlenir. Bazı araçlar yüzeye çıkıp GPS ile konum düzeltmesi alır, sonra
> yeniden dalar. Yarışma havuzlarında bu mümkün olmadığı için araç tamamen kendi
> sensörlerine güvenir.

> **Kutu — MATRO'da:** İSS takımımız 2022'de Singapur'daki SAUVC'de (Singapore AUV
> Challenge) dünya finaline kaldı; 2026'da PRUSA ekibiyle TEKNOFEST İnsansız Su Altı
> Aracı finalindeydi. Aracın otonom kontrol kartı, batarya sistemi ve kontrol yazılımı
> takım tarafından geliştiriliyor.
> *[Kaptan kontrolü: aracınızda hangi sensörler var? Buraya bir cümle ekleyin.]*

Kaynaklar: [RoboNation, Bumblebee AUV tasarım raporu](https://robonation.org/app/uploads/sites/4/2019/10/NSU_RS17_Paper.pdf),
[Ocean News: RoboSub akustik pinger'lar](https://oceannews.com/news/subsea-and-survey/acoustic-pingers-help-contestants-in-robosub-competition/),
[BeamsNet: DVL ölçümleri üzerine (arXiv)](https://arxiv.org/pdf/2206.13603)
