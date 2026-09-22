# Nasıl Çalışır? Karıştırmaya Karşı Haberleşme

> **Dizgi notu** (basılmaz): Çift sayfa. Ana görsel: zaman-frekans ızgarası üzerinde
> vericinin atladığı kanallar (renkli kareler) ve karıştırıcının kapattığı bant (kırmızı
> şerit). Fotoğraf: cagri-team-cropped. Genel anlatımdır; **ÇAĞRI kaptanı kontrol etmeli.**

## Karıştırıcı varken veri nasıl iletilir?

**Spot:** Bir dron, bir kara aracı ya da bir yer istasyonu; hepsi kablosuz bağlantıya
muhtaç. Birisi o frekansı gürültüyle doldurursa ne olur? Cevap: Kaçmayı bilen bir
haberleşme sistemi.

### Karıştırma (jamming) nedir?

Kablosuz haberleşmede verici ile alıcı belirli bir frekans üzerinden konuşur. Bir
**karıştırıcı (jammer)** aynı frekansa güçlü bir gürültü basarak alıcının asıl sinyali
duymasını engeller. Kalabalık bir odada birinin kulağınıza bağırması gibi.

### Çözüm 1: Frekans atlama

Verici ve alıcı, önceden anlaştıkları bir sıraya göre saniyede birçok kez frekans
değiştirir. Karıştırıcı bir kanalı kapatsa bile iletişim diğer kanallardan sürer.
Bluetooth da günlük hayatta benzer bir yöntem kullanır.

Daha akıllısı **uyarlamalı frekans atlama**: Sistem hangi kanalların gürültülü olduğunu
ölçer ve bu kanalları atlama listesinden çıkarır. Karıştırıcı yer değiştirdikçe liste
de güncellenir.

### Çözüm 2: Hata düzeltme

Kanal ne kadar temiz olursa olsun bazı bitler bozulacaktır. **Hata düzeltme kodları**
veriye hesaplanmış fazlalık ekler; alıcı bu fazlalık sayesinde bozulan bitlerin bir
kısmını geri kurar. Sinyal-gürültü oranı düştükçe daha güçlü (ve daha yavaş) kodlara
geçmek gerekir.

### Donanımı yazılım yapan cihaz: SDR

Eskiden her haberleşme sistemi kendine özel donanımla yapılırdı. **Yazılım tabanlı
radyo (SDR)** ise frekans seçme, modülasyon ve filtreleme gibi işleri yazılımda yapar.
Aynı donanım, yazılım değiştirilerek bambaşka bir haberleşme sistemine dönüşebilir. Bu
esneklik, frekans atlama ve uyarlamalı algoritmaları denemek için idealdir.

> **Kutu — MATRO'da:** ÇAĞRI takımımız 2024 TEKNOFEST Kablosuz Haberleşme Yarışması'nda,
> karıştırma etkisi altındaki frekanslardan kaçarak veriyi eksiksiz iletti ve 397 takım
> arasından Türkiye 6.sı oldu. Takım; SDR mimarileri, karıştırıcıyı tespit edip kaçan
> algoritmalar ve zorlu koşullarda kesintisiz veri iletimi üzerine çalışıyor.

> **Kutu — Neden önemli?** Karıştırmaya dayanıklı haberleşme yalnızca savunma
> sanayiinin konusu değil. Otonom araçlar, endüstriyel kablosuz sensör ağları ve afet
> bölgesinde kurulan acil durum ağları da aynı problemle karşılaşıyor. TEKNOFEST 2026'da
> ilk kez düzenlenen Elektronik Harp Yarışması da bu alana artan ilginin işareti.
