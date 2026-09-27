# Resmî prompt rehberlerinden uygulama kuralları

Bu dosya 27 Eylül 2026 tarihinde resmî ürün belgelerine bakılarak hazırlandı. Model adları ve teknik sınırlar değişebilir; üretimden önce güncel sayfayı aç.

## Gemini genel prompt tasarımı

Google'ın önerdiği başlangıç: açık ve özgül talimat, yeterli bağlam, örnek ve iterasyon. Karmaşık bir çıktıda istenen biçimi ayrıca belirt; önceki turdaki görselleri ve talimatları bağlam olarak kullan. MATRO işinde kaynak fotoğrafı ekleyip “araç sürümünü ve görülen parçaları say, emin olmadığın ayrıntıyı ayrı belirt” diye başla. Sonraki istemde yalnız değiştirilecek bölgeyi tarif et.

Kaynak: https://ai.google.dev/gemini-api/docs/prompting-strategies

## Gemini görsel üretimi ve düzenleme

Görselde özne, bağlam ve üslubu açıkça yaz. Referansla düzenlemede değişecek nesne veya bölgeyi söyle; geri kalan ışık, perspektif ve kimliği koru. Tek karede çok sayıda çelişen stil isteme. Karakterin yeni açısından üretilecekse önceki kabul edilmiş açıları yeniden referansa kat. Resim içindeki Türkçe yazı ve logo sonuçta görsel olarak okunmadan yayımlanmaz; kritik metni tasarım katmanında yeniden diz.

Kaynak: https://ai.google.dev/gemini-api/docs/image-generation

## Gemini Omni görüntüden video

Omni için başlangıç karesi özne ve kadrajı taşır; promptu tek, kesintisiz sahnede zaman içindeki eylem ve kamera hareketi olarak yaz. Bu örnekte konuşma ve ses üretimini kapalı tuttuk, çünkü klibe şarkının master kaydı eklendi. Modelin güncel süre, en-boy oranı ve API yöntemini üretim öncesi ürün belgesinden yeniden doğrula.

Kaynak: https://ai.google.dev/gemini-api/docs/omni

## Veo video promptu

Google'ın video rehberindeki ayrı alanlar: özne, eylem, stil, kamera yeri/hareketi, kompozisyon, odak/lens etkisi ve atmosfer. Konuşma için konuşan kişi ve cümle; olay sesi ve ortam sesi ayrı tarif edilir. Kaynak görüntü veya ilk/son kare kullanıldığında ikisinin aynı araç sürümü ve sahne yönünde olup olmadığını kontrol et. MATRO planında tek baskın eylem ve tek baskın kamera hareketi seç; araç geometrisini korumayı açıkça yaz.

Kaynak: https://ai.google.dev/gemini-api/docs/veo

## Runway görüntüden video

Başlangıç görüntüsü özne, kompozisyon ve üslubu zaten tanımlar. Metin promptu hareket, kamera ve zaman içindeki değişime odaklanır. İlk denemeyi sade tut; ortaya çıkan kusura göre yalnız bir değişkeni iyileştir. Başlangıç fotoğrafındaki bulanıklık ve bozuk ayrıntı videoya taşınabileceğinden girdi karesini önce incele.

Kaynak: https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide

## Bu rehberlerin sınırı

Resmî sayfalardaki örnekler bir sonucu garanti etmez. Üretilen ilk, orta ve son kareyi, sesi ve kaynak eşleşmesini yine dosya üzerinde denetle. Görüntüdeki olayın gerçekliği model kalitesinden ayrı bir sorudur.
