# Codex görevi: ekip fotoğraflarına YZ ile kadraj düzeltme ve vesikalık

Repo: `/Users/wildgenie/Projects/btu-matro` (Türkçe çalış; emoji yok; commit/push YAPMA).

## Amaç
Sitedeki 26 ekip karesi (`public/media/ekip/<slug>.jpg`, 600×600) için Gemini görsel modeliyle iki çıktı:
1. **Kadraj düzeltmesi** → `docs/ekip/yz/codex/kadraj/<slug>.jpg`: aynı fotoğraf; baş ortada, başın üstünde boşluk, omuzlar görünür. Yüz/kimlik HİÇ değişmemeli.
2. **Standart vesikalık** → `docs/ekip/yz/codex/vesikalik/<slug>.jpg`: beyaz düz fon, önden, baş-omuz, eşit ışık; kişinin kendi kıyafeti/başörtüsü/gözlüğü. Örnek hedef stil: takım kartlarındaki beyaz fonlu stüdyo vesikalıkları.

## Önceki denemede ne bozuldu (Claude)
- Tek seferlik istekle üretilen vesikalıklarda yüzler kişiye **hiç benzemedi** (model yeni yüz çizdi, güzelleştirdi). Kullanıcı reddetti.
- Kadrajda model bazen uzaklaştırdı (Irmak, Rumeysa, Yusuf).
- İşe yarayan kadraj yöntemi: `docs/ekip/yz/kadraj2/` — site karesini 780×780 gri tuvale koyup (üst 150px boşluk) Gemini'ye yalnızca gri kenarları doldurtmak, sonra **orijinal kareyi piksel piksel geri yapıştırmak** (renk eşitleme + yumuşak maske). Betik: `/private/tmp/claude-501/-Users-wildgenie-Projects-btu-matro/c4790c33-2952-44d6-b402-a148a7fb5c92/scratchpad/genislet.py`. Kontrol paftası: `docs/ekip/kontrol/yz-kadraj2.jpg`.

## Kullanıcının isteği
- Vesikalıkları **aynı sohbet bağlamında** üret: her kişi için çok turlu bir Gemini konuşması kur (önce orijinal fotoğraf(lar) + yüzü korunmuş kadraj, sonra aynı konuşmada vesikalık iste; beğenilmezse aynı konuşmada düzeltme iste). Böylece model önceki referanslara bağlı kalsın.
- El/yüz bozulmuşsa kullanma. Benzemeyen sonucu teslim etme; yüz benzerliğini kendin karşılaştırarak kontrol et.

## Kaynaklar
- Orijinaller: `docs/ekip/orijinal/` (kişi adıyla; bazılarında `-canva`, `-kare`, `-yakin`, `-yuz-N` ek fotoğraflar). Alternatif kareler: `docs/ekip/alternatif/`.
- İsim/slug listesi: `src/data/ekibimiz.json` (`people[].photo`).
- Model: `gemini-3-pro-image`, REST `generateContent`, `imageConfig.aspectRatio: "1:1"`. Anahtar: `source ~/.zshrc >/dev/null 2>&1` sonrası `GEMINI_API_KEY` ortam değişkeni. Anahtarı asla yazdırma, dosyaya yazma.
- Önceki tek-tur betik (referans için): scratchpad içindeki `yz_kare.py`.

## Teslim
- Önce 2-3 kişide dene, sonuçları gözle kontrol et, sonra tümü.
- Sonunda `docs/ekip/kontrol/codex-karsilastirma.jpg` paftası: her kişide numara + isim; 1 mevcut | 2 kadraj | 3 vesikalık.
- Kısa Türkçe rapor: hangi kişilerde benzerlik iyi, hangileri kullanılmamalı.

## Ek istek (kullanıcı, sonradan)
Her kişi için **tüm orijinal fotoğraflarını** alternatif referans olarak ver: `docs/ekip/orijinal/<slug>*.jpg` (ek dosyalar dahil: `-canva`, `-kare`, `-yakin`, `-yuz-N`, `-luna-N`), `docs/ekip/alternatif/<slug>.jpg` ve ham Canva indirmeleri `docs/ekip/canva-DAHYwyJ6SQc/`. Grup fotoğraflarını (başka kişiler de olan) referans verirken kişiyi metinle tarif et ya da hiç verme. Sohbetin ilk turunda bu referansların hepsi olsun.

## Ek istek 2 (kullanıcı)
- **Araç seçimi:** Gemini kullanımımız limitsiz; mümkün oldukça Gemini'yi tercih et. Gemini'nin yapamadığı yerlerde (ör. yüzü korumada başarısız olursa) kendi görsel üretim/düzenleme yeteneğini kullan. Hangi görselde hangisini kullandığını raporda belirt.
- **Üçüncü çıktı: doğal gri fonlu portre** → `docs/ekip/yz/codex/gri-fon/<slug>.jpg`. Biyometrik/ID katılığı YOK: kişinin verilen fotoğraflarındaki doğal duruşu, ifadesi, kıyafeti, başörtüsü/gözlüğü korunur; mümkün olduğunca o fotoğraflara uygun kalır. Yalnızca fon, Bilgehan'ın fotoğrafındaki gibi düz orta-gri stüdyo fonu olur (düz beyaz değil; referans: `public/media/ekip/bilgehan-zeki-ozaytac.jpg`) ve kadraj baş-omuz olur. Özetle: profesyonel bir stüdyo çekimi gibi görünmeli (yumuşak stüdyo ışığı, hafif fon degrade/vinyet olabilir, sığ alan derinliği yok, net odak), ama kişi ve duruşu doğal ve kendi fotoğraflarına sadık kalmalı. Aynı kişinin sohbet bağlamında üretilsin.
- Pafta: 1 mevcut | 2 kadraj | 3 vesikalık | 4 gri fon.

## Ek istek 3 (26 Ekim, kullanıcı): eksikleri tamamla
Kontrol sonrası sorunlu çıktılar silindi; `docs/ekip/yz/kadraj`, `kadraj2`, `vesikalik` klasörleri artık yok, onları referans alma.
- **Kadraj yeniden üretilecek (çerçeve izi / kenar dikişi vardı):** adem-baglan, berat-eren-karakas, emine-sultan-gunes, feyza-karabicak, irmak-karaagac, duygu-solak. Yapıştırılan kare ile üretilen kenar arasında görünür dikdörtgen, çizgi, renk/ışık farkı ya da tekrar eden nesne OLMAMALI. Dikiş gizlenemiyorsa o kişi için kadraj teslim etme.
- **Vesikalık yeniden üretilecek:** yusuf-sarsici (takım elbise uydurulmuştu; kendi kıyafeti, gerekirse baret/yelek ya da kendi fotoğraflarındaki kıyafet), irmak-karaagac (başörtüsü siyah olmalı, kahverengi değil), muhammed-ataman (montu/atkısı kendi fotoğrafındaki gibi kalmalı).
- **Referans zorunlu:** her kişinin sohbetinin ilk turunda kesilmemiş orijinallerin hepsini ver: `docs/ekip/orijinal/<slug>*.jpg` (`-canva`, `-yuz-N`, `-bilgehan-N` vb. dahil) ve varsa `docs/ekip/alternatif/<slug>.jpg`. Site karesi (600 px kırpım) tek başına referans olmasın.
- Diğer kişilerin mevcut çıktılarına dokunma. Bitince `docs/ekip/kontrol/agy-eksikler.jpg` paftası: her satırda numara+isim; orijinal | yeni çıktı. Kısa Türkçe rapor yaz.

## Ek istek 4 (26 Ekim, kullanıcı): TÜM kadrajlar yeniden
Kalan 20 kadrajda da ince çerçeve/dikdörtgen izi vardı; `docs/ekip/yz/codex/kadraj/` tamamen boşaltıldı. 26 kişinin hepsi için kadraj yeniden üretilecek (Ek istek 3'teki 3 vesikalık da hâlâ bekliyor).
- İz nedeni: yapıştırılan orijinal kare ile Gemini'nin doldurduğu alan arasındaki parlaklık/renk basamağı, yumuşak alfa maskesiyle bile dikdörtgen olarak görünüyor.
- Yöntem önerisi: yapıştırmayı alfa yerine Poisson karışımıyla yap (`cv2.seamlessClone`, NORMAL_CLONE, maske yalnız yüz+saç+omuz bölgesi — dikdörtgen değil, kişinin silüetine yakın elips/serbest biçim). Ya da Gemini çıktısını doğrudan kullan, yalnız yüz bölgesini Poisson ile geri koy.
- **Zorunlu otomatik kontrol:** her çıktıda `blur(3) - blur(25)` farkı üzerinde uzun düz yatay/dikey kenar ara (ör. satır/sütun boyunca tutarlı basamak, Hough çizgileri); yapıştırma sınırına denk gelen düz çizgi bulunursa o çıktıyı teslim etme, yeniden dene. Ayrıca gözle 2x büyütüp kontrol et.
- Referans: her kişinin kesilmemiş tüm orijinalleri ilk turda (Ek istek 3'teki kural aynen).
- Pafta: `docs/ekip/kontrol/agy-eksikler.jpg` — numara+isim; orijinal | yeni kadraj | (varsa) yeni vesikalık. Teslim edemediğin kişileri raporda açıkça yaz.
