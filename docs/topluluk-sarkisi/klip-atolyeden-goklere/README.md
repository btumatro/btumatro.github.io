# Atölyeden Göklere — klip storyboard'u

Durum: **tam klip hazır**. Son çıktı: `atolyeden-goklere-final-1080p.mp4` (3:02, 1920×1080, 30 fps, H.264/BT.709 + özgün AAC ses ve CC altyazı). Son kurgu storyboardu `sheets/storyboard-final-cut.png`; 46 planın tam dökümü `final-shotlist.json`. Kaynak parça: `../ses/03-atolyeden-goklere.mp4` (3:02, kare 1024×1024; gömülü altyazının son sözü 3:00'da biter). Söz dökümü: `../sozler/03-atolyeden-goklere.md`. Üç görsel sheet ve birleşik `storyboard-tumu.pdf`, `sheets/` altında; bunlar bitmiş video karesi değil, bölümün ana planlarını gösteren kurgu çıpalarıdır.

## Tam klip — son kurgu

Üretilen üç yeni görsel açılışta kullanılır; geniş atölye karesi aynı görsel diliyle kapanışı taşır. Durgun karelerde yavaşlatılmış 30 fps Ken Burns hareketi ve daha uzun yumuşak geçişler kullanılır. Özgün altyazı CC olarak hem MP4 içine gömülüdür hem de yanındaki SRT dosyasında bulunur; görüntüye yakılmaz.

46 plan ve 45 ritim/geçiş noktası içerir; 23 plan gerçek hareketli kliptir. Kurguda 15 farklı Gemini Omni videosu kullanılır, bazı planlar farklı giriş anlarıyla tekrar edilir. Yeni üretilen sahneler sinematik konsept karelerden türetilmiştir; arşiv fotoğrafları ve ham fotoğrafa dayalı videolar son klibe alınmamıştır. Alt bant yazıları model çıktısı değildir; okunaklı Türkçe için kurgu sırasında eklenir.

Yeniden oluşturmak için depo kökünden:

```sh
python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/assemble_music_video.py
```

Özgün ses akışı değiştirilmeden kopyalanır. Dört ek Omni planı ASHİNA vakum işlemi, PRUSA atölyesi, LODOS kıyı seyri ve MATRİS saha planıdır. Bunlar ile tüm kullanılan video promptları `veo-ornekleri/videolar/*.json` içinde saklanır.

## Sinematik örnek 01

`sheets/storyboard-sinematik-ornek.png` üretilmiş sahne karelerini, çekim bilgisini ve görsel devamlılık kurallarını içeren sheet'tir. Örnek montaj `veo-ornekleri/klip-ornek-01.mp4` dosyasındadır: 20,29 saniye, 1280×720, 24 fps; özgün şarkı 01:30.667'den başlatılmış, beş kısa Omni planı yumuşak geçişlerle birleştirilmiştir.

Profesyonel ana kareler `ana-kareler/` altındadır. Her karenin yanında aynı isimli JSON bulunur; içinde üretim modeli, referans dosyaları ve prompt yer alır. Gerçek takım fotoğrafları araç kimliğini belirler; üretilen kareler yeni kamera açısı/ışık yorumu olduğundan arşiv fotoğrafı diye sunulmaz.

Yeniden üretim:

```sh
python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/ana-kareler/generate_keyframes.py ashina
python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/ana-kareler/generate_keyframes.py lodos
python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/ana-kareler/generate_keyframes.py prusa
python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/ana-kareler/generate_keyframes.py zemheri
python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/ana-kareler/generate_keyframes.py matris
python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/veo-ornekleri/generate_omni.py <sahne>-sinematik
python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/storyboard-sheets-cinematic.py
python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/veo-ornekleri/assemble_sample.py
```

`GEMINI_API_KEY` ortam değişkeninden okunur; betikler anahtarı kaydetmez veya yazdırmaz. Video üretimi sonrasında ilk, orta ve son kareleri görsel olarak incele; geometri değişmişse sahneyi yeniden üret veya montajdan çıkar.

## Ana fikir

Üç dakikalık **belgesel karakterli müzik klibi**: çalışılan nesne, onu yapan insanlar ve gerçek test sahası arasında gidip gelir. Nakarat geniş planlara açılır; ikinci kıta takım adlarını gerçek araçlarla eşleştirir; final tek bir takımın zaferi gibi değil, topluluğun ortak üretimi gibi biter. 16:9 ana kurgu; 9:16 kısa kesit ayrıca tasarlanabilir.

Görsel dil: gerçek çekimin pürüzleri kalır. Doğal ışık ve az miktarda ortak renk düzeni kullanılır. Fotoğraflara 3–5 saniyelik yavaş kadraj hareketi uygulanabilir. Hızlı kesmeler yalnızca müzik vuruşlarına gelir. Kayan yazı, sahte arayüz, parçacık, anlamsız ışık patlaması ve sürekli şarkı sözü bindirmesi kullanılmaz. Şarkıdaki sözcükler zaten işitiliyor; ekranda yalnızca iki güçlü satır ve final logosu yeterli. Kadraj, lens, hareket ve kabul ölçütleri `ARSIV-NOTLARI.md` içinde ayrıntılıdır.

## Kurgu omurgası

| Zaman | Müzik/söz | Görsel çekirdek | Uygulama |
| --- | --- | --- | --- |
| 00:00–00:10 | Giriş, “Başlıyoruz” | Gerçek gece iskelesi, çalışma ışığı | Karanlıkta bekleme, ilk vuruşta kesme. Başka olaya aitmiş gibi sunulmaz. |
| 00:10–00:28 | Gece atölyesi, lehim/vida | ASHİNA prototipi konsept karesi, LODOS kablo/gövde ayrıntıları | Konsept yalnızca görsel köprü. Gerçek fotoğrafla aynı araç biçimi karşılaştırılarak kullanılmalı. |
| 00:28–01:00 | Kuruluş, ilerleme, çizgiden sahaya | Kompozit üretim, gerçek pist ve ekip | “2013” için 2013 tarihliymiş gibi arşiv fotoğrafı gösterilmez. Gerekirse yalnız yalın tarih tipografisi. |
| 01:00–01:32 | İlk nakarat | Üretim → su altı → hava → topluluk | “ATÖLYEDE BAŞLAR / SAHADA KANITLANIR” bir kez, temiz tipografi. |
| 01:32–01:48 | ASHİNA, LODOS, PRUSA, ZEMHERİ, MATRİS | Her takımın kendi aracı veya ekip/araç karesi | Şarkı adları saniye saniye izlenir. Bir fotoğraf diğer takımın aracıymış gibi kullanılmaz. |
| 01:48–02:20 | Yol, test, yeniden deneme, birlik | Gerçek test ve montaj anları | “Kırılan test” için uydurma kaza görüntüsü yok; kontrol ve yeniden çalışma gösterilir. |
| 02:20–02:56 | Son nakarat | Önceki mekânlara daha güçlü ritimle geri dönüş | Deniz/havuz/pist kesmeleri; aynı çekimi tekrar kullanırken farklı kadraj veya yeni an seçilir. |
| 02:56–03:02 | Son “MATRO” ve müzik kuyruğu | Koyu kart + özgün MATRO ve BTÜ logoları | 2 saniye sabit tut; müziğin son kuyruğunu kesme. |

## İncelenen mevcut kaynaklar

- `public/media/galeri-ashina-uretim.jpg`: siyah sabit kanat prototipin atölye fotoğrafı. `assets/konsept-ashina-atolye.png` buradan türetilmiş **AI konseptidir**, arşiv görüntüsü değildir. Yeni açıyı görselleştirir; üretim öncesi pervane, kol, iniş takımı ve kuyruk geometri kontrolü gerekir.
- ASHİNA: `galeri-ashina-kompozit-uretim.jpg`, `galeri-ashina-pist-testi.jpg`, `galeri-ashina-sunum-gece-montaj.jpg`, `galeri-ashina-sunum-elektronik-masa.jpg`. Gece montajı ve masa ayrıntısı takımın kendi sunumundandır.
- LODOS 2026 güncel araç: `takim-lodos.jpg`, `galeri-lodos-saha.jpg`, `galeri-lodos-ekip-sahil.jpg`. Bunlarda **opak gri yükseltilmiş kabin ve üstünde Türk bayrağı** var. Önceki beyaz/bordo açık gövdeli fotoğraflar eski araca ait; klipte güncel LODOS'u temsil etmek için kullanılmaz. `assets/konsept-lodos-guncel-sahil.png`, güncel aracın iki fotoğrafı referans alınarak üretildi.
- PRUSA/su altı: `galeri-prusa-detay.jpg`, `assets/konsept-prusa-atolye.png`; `galeri-iss-auv-havuz.jpg` başka araca aittir ve PRUSA diye etiketlenmez.
- ZEMHERİ: `galeri-zemheri-sunum-gece-su-testi.jpg`, `galeri-zemheri-sunum-roket-inceleme.jpg`, `galeri-zemheri-sunum-govde-montaj.jpg`; bunlar takımın kendi sunumundaki gerçek çalışma ve test fotoğraflarıdır. SARA fotoğrafı ZEMHERİ'nin güncel aracı olarak kullanılmaz.
- MATRİS: `galeri-matris-sunum-yakin-montaj.jpg`, `galeri-matris-sunum-saha-iki-iha.jpg`; ayrıca `assets/konsept-matris-suru-ucus.png` hareket taslağı vardır.
- PUSULA/SIRIUS: `galeri-sirius-sunum-arac-mudahale.jpg` ve `galeri-sirius-sunum-yarisma-parkuru.jpg` atölye ve saha geçişleri için gerçek karelerdir.
- `video-lodos-tanitim.mp4` (11,54 sn), `video-prusa-tanitim.mp4` (6,83 sn), `video-zemheri-tanitim.mp4` (8,60 sn): yerel kare incelemesinde çoğunlukla toplantı/atölye sahneleri var. Araç hareketi veya uçuş görüntüsü olarak kullanılmazlar.

## Yeni çekim / AI kullanımı

En değerli ek çekimler: 1) gerçek atölyede ellerin parça sabitlemesi, 2) pervane/vida/kablo ayrıntısı, 3) gerçek araçta test hazırlığı, 4) ekibin küçük doğal etkileşimleri, 5) geniş saha ve hareketli araç. İnsan yüzleri ve elleri görünürse gerçek çekim tercih edilir. AI gerekirse **nesne veya mekân ara planı** için 2–4 saniyelik birkaç shot ile sınırlanır; gerçek kişi ya da gerçek test belgesi gibi sunulmaz.

Görüntüden videoya promptu, başlangıç görüntüsünü yeniden tarif etmek yerine hareketi tarif etmeli. Örnek (ASHİNA konsept planı için):

> A slow 40 cm dolly-in toward the stationary prototype aircraft. One continuous shot. The aircraft and every rotor, wing, wire and wheel remain physically fixed and unchanged. Only the camera moves; subtle practical workshop light stays constant. Natural documentary footage, no transformation.

Çıktı incelemesi: ilk/son kareyi ve orta kareleri yan yana koy; kanat, pervane, kol, teker ve kuyruk sayısını karşılaştır; insan varsa el/parmak/yüz anatomisini incele; titreyen yazı/logoyu çıkar; bozuk shot'u kurgudan at. Orijinal fotoğrafla hareketli yakınlaşma güvenli yedektir.

Hareket, lens, ışık, karakter ve araç sürekliliği için örnekli üretim sözleşmeleri `ARSIV-NOTLARI.md` içinde bulunur.

## Yeniden üretim

Repo kökünden `python3 docs/topluluk-sarkisi/klip-atolyeden-goklere/storyboard-sheets.py`. Pillow gerekir. Betik `sheets/storyboard-01.png`–`03.png`, `sheets/storyboard-tumu.pdf`, `assets/final-card.png` ve `assets/konsept-takimlar-ucleme.png` üretir; kaynak fotoğrafları değiştirmez. Diğer konsept PNG'ler üretilmiş özgün taslaklardır ve betiğin girdileridir.
