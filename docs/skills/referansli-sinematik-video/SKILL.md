---
name: referansli-sinematik-video
description: Gerçek fotoğraf veya araç referansından tutarlı sinematik storyboard kareleri ve kısa video planları üretirken kullan; ürün geometrisini korur, kamera/ışık/hareketi ayrı tanımlar ve çıktıyı görsel olarak denetler.
---

# Referanslı sinematik video

Gerçek bir ekip, araç, ürün veya mekânın yeni açısını üretirken ilk iş kaynak kareyi **açıp** fiziksel öğeleri listele. Dosya adına güvenme; model/yıl karışabilecekse güncel referansı ayrıca doğrula. Eskimiş bir sürümü güncel ürünün görüntüsü olarak üretme.

Her shot için şu kısa sözleşmeyi yaz:

1. **Referans ve rolü:** gerçek fotoğraf, konsept hedefi, ilham görseli ya da kurgu grafiği.
2. **Sabitler:** gövde, kanat, rotor, teker, kabin, logo gibi değişemeyecek gözlenebilir parçalar.
3. **Kamera:** ölçek, açı, yaklaşık lens/odak, kadraj hareketi; bir shot'a tek baskın hareket.
4. **Işık ve ortam:** var olan mekânla uyumlu saat, kaynak, renk ve gölge.
5. **Eylem:** fiziksel olarak mümkün, kısa, sade eylem; insan görünüyorsa gerçek çekimi öncele.
6. **Kurgu işlevi:** şarkı sözü/vuruş, shot süresi ve komşu shot ile eşleşmesi.

7. **Görüntüden videoya prompt:** Şu adımları sırayla uygula:
	1. Başlangıç karesindeki nesneyi 3 ila 5 cümleyle detaylı şekilde tarif et.
	2. Hareketi ve süreyi açıkça belirt.
	3. Mevcut kaynak görüntüye ait olmayan yeni parçaların, yazıların veya kimliklerin eklenmesine ihtiyaç bırakma.
	4. Başlangıç karesinin görünüşünü, eylemi ve kamerayı temel al.
8. **Üretim özellikleri:** Modelin sürüm, çözünürlük ve süre özelliklerini üretim anında geçerli araç arayüzünden kontrol et.

Çıktıyı ilk, orta ve son karede incele. Referansla yan yana koyup parça sayısı, anatomi, yazı, logo, renk ve mekân sürekliliğini denetle. Bir kusuru gizlemek için uzun prompt zinciri kurma; uygun gerçek fotoğraf hareketi veya yeni çekim daha iyi ise ona dön. Üretilmiş kareyi arşiv görüntüsü diye etiketleme.

Storyboard sheet için her panelde zaman, söz/beat, görüntü kaynağı, kamera/lens, hareket ve **ARŞİV / AI KONSEPT / GRAFİK** etiketi bulunsun. Çekim yapmak mümkünse arşiv ve AI yerine gerçek eksik planı tarif et.

Geniş uygulama rehberi: `../../gorsel-video-prompt-uretim-el-kitabi.md`. Genel prompt kurma, fotoğraf düzenleme, karakter paftası, on afiş türü, kamera/ışık/hareket ve MATRO örnekleri bu belgede bulunur. Kullanıcı yalnız bir shot istiyorsa ilgili bölümü oku; tüm belgeyi prompta yapıştırma.

MATRO klip iş akışı ve tekrar üretilebilir örnekler: `../../topluluk-sarkisi/klip-atolyeden-goklere/README.md`. Gerçek araç fotoğrafını önce sinematik ana kareye düzenle; teknik biçim korunmadan videoya geçme. Bir shot'ta tek kamera hareketi seç. Dört veya daha çok noktadan örnek kare al; ilk/orta/son kareleri yan yana denetle. Araç bileşeni/ölçüsü değişmiş, yeni parça türemiş, yazı/logolar kararsızlaşmış veya insan anatomisi bozulmuşsa klibi kabul etme. Geçiş ritmini şarkı sözleri ve altyazı zamanlarıyla eşleştir; modelin ürettiği sesi kullanmayıp gerektiğinde özgün master kaydını kurguya koy.

Model davranışı için resmî ürün rehberlerinden çıkarılmış kurallar: `references/resmi-prompt-rehberleri.md`. Özellikle görüntüden videoda başlangıç görüntüsünü tekrar betimlemek yerine eylem ve kamera hareketini tarif et; metinden videoda özne, eylem, kamera, atmosfer ve sesi ayrı yaz. Üretimden önce modelin güncel özelliklerini resmî sayfada doğrula.

Gemini API komut satırı aracı gerektiğinde kullanılabilir. Güncel durumu, komut örnekleri ve güvenli istek önizlemesi için `references/gemini-api-cli.md` dosyasını oku.
