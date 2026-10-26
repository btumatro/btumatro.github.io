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

## Ek istek 5 (26 Ekim, kullanıcı): yalnız gri fon ve kadraj, siteye dokunma
- Beyaz fonlu vesikalık ÜRETME (kullanıcı istemiyor). `vesikalik/` klasörü kaldırıldı.
- Mevcut 26 gri fonu silme/üzerine yazma. Yalnız şu üç kişi için yeni gri fon üret, `docs/ekip/yz/codex/gri-fon-yeni/<slug>.jpg` olarak kaydet: gulsiye-begum-gumus (fondan kopuk, küçük, kesilip yapıştırılmış gibi), melek-ozkeser ve nusret-bircan-keser (selfie açısı ve kesik kafa kalmış). Gerçek stüdyo çekimi gibi: kişi kadraja ortalı, baş-omuz, kafa kesilmeden, fonla aynı ışıkta.
- Kadraj: Ek istek 4 aynen (26 kişi, Poisson karışımı, zorunlu dikiş kontrolü).
- Her kişide kesilmemiş tüm orijinaller ilk turda referans.
- `public/media/ekip/` ve site dosyalarına DOKUNMA; seçimi kullanıcı yapacak.
- Pafta: `docs/ekip/kontrol/agy-eksikler.jpg` — numara+isim; orijinal | yeni kadraj | (varsa) yeni gri fon.

## Ek istek 6 (26 Ekim, kullanıcı): stilize karakter denemesi (Ek istek 5 bittikten sonra)
- Önce Ek istek 5'in eksikleri tamam mı kontrol et; gri fonlarda diğerlerine uymayan (ölçek, ortalama, ışık, kesik kafa, kesilip yapıştırılmış görünüm) başka kişi varsa onu da `gri-fon-yeni/`'ye yeniden üret.
- Sonra stilize karakter denemesi: `docs/ekip/yz/codex/stilize/<slug>.jpg`, 1:1. Stil: tek ve tutarlı, yarı gerçekçi dijital illüstrasyon / yumuşak 3B animasyon karakteri havası; düz orta-gri fon (gri fonlarla aynı ton), baş-omuz, kişinin yüz hatları, saç, gözlük, başörtüsü, sakal ve kıyafeti tanınır kalmalı. Karikatür abartısı, büyük göz, güzelleştirme YOK; kişi arkadaşları tarafından hemen tanınmalı.
- Önce 3 kişilik pilot (ör. adem-baglan, irmak-karaagac, muhammed-ataman), pilotu `docs/ekip/kontrol/stilize-pilot.jpg` paftasıyla kaydet (orijinal | gri fon | stilize), sonra 26 kişinin tamamı.
- Referans: kesilmemiş orijinaller + o kişinin gri fon portresi, aynı sohbet bağlamında.
- Pafta: `docs/ekip/kontrol/stilize.jpg` (numara+isim; orijinal | stilize). Site dosyalarına dokunma.

## Ek istek 7 (26 Ekim, kullanıcı): 1-2 örnek karakter sheet (stilize pilottan sonra)
- Stilize pilotundaki 3 kişiden en iyi tutan 1-2 kişi için karakter sheet hazırla: `docs/ekip/yz/codex/karakter-sheet/<slug>.jpg` (yatay, ör. 16:9 ya da 3:2).
- İçerik: önden / üç çeyrek / yandan / arkadan dönüş (turnaround), 3-4 yüz ifadesi (gülümseme, ciddi, şaşkın, konuşurken), renk paleti şeridi (ten, saç, kıyafet, başörtüsü/gözlük), kısa ölçü/oran notu; isim etiketi Türkçe, emoji yok. Arka plan düz açık-gri pafta.
- Tutarlılık: tüm pozlarda aynı kişi, aynı kıyafet ve aksesuar; stilize karakterin kendisi ana referans, kesilmemiş orijinaller yüz benzerliği için yanında. Aynı sohbet bağlamında üret.
- Bu skill'leri OKU ve yöntemlerini uygula (Claude Code eklenti dosyaları, salt okunur):
  - /Users/wildgenie/.claude/plugins/cache/wildgenie-private/yz-medya-atolyesi/1.9.0/skills/karakter-rig-ve-avatar/SKILL.md
  - /Users/wildgenie/.claude/plugins/cache/wildgenie-private/yz-medya-atolyesi/1.9.0/skills/gorsel-video-uretim-cekirdek/references/karakter-urun-tutarliligi.md
  - /Users/wildgenie/.claude/plugins/cache/wildgenie-private/yz-medya-atolyesi/1.9.0/skills/pafta-taslak-sozlugu/SKILL.md
  - /Users/wildgenie/.claude/plugins/cache/wildgenie-private/yz-medya-atolyesi/1.9.0/skills/gorsel-istem-ve-duzenleme/SKILL.md
- Raporda hangi skill'den hangi kuralı uyguladığını kısaca yaz.

## Ek istek 8 (26 Ekim, kullanıcı): stil = Zeki'nin reels karakter tarzı (Ek istek 6 stil tanımının yerine geçer)
Stil referansları (salt okunur, kopyalama): /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/KARAKTER_KIMLIK_PAFTASI_v1.jpg, /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/ANA_REFERANS_SAYFASI_v2.jpg, /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/zeki_kimlik_ve_konusma.jpg ve aynı klasördeki sahne kareleri. Tarz: düz 2B çizgi film, temiz koyu kontur, düz renk + hafif tek ton gölge, sade sıcak gri-bej fon, gerçekçi orantı (büyük göz yok). Karakter sheet düzeni de bu paftadaki gibi: önden + üç çeyrek tam boy, altta 4 yüz ifadesi.
- Önce yalnız STİL PİLOTU: 3 kişi (adem-baglan, irmak-karaagac, muhammed-ataman) baş-omuz portre → `docs/ekip/yz/codex/stilize/`, pafta `docs/ekip/kontrol/stilize-pilot.jpg` (orijinal | gri fon | stilize).
- Sonra 1-2 karakter sheet (Ek istek 7 kuralları + yukarıdaki düzen) → `docs/ekip/yz/codex/karakter-sheet/`.
- 26 kişinin tamamına GEÇME; kullanıcı pilotu görüp karar verecek.

### Ek istek 8 düzeltmesi (kullanıcı): ana stil SAHNE karelerinden alınır
Asıl istenen tarz karakter paftasındaki düz 2B değil, reels sahne karelerindeki tarz. Ana stil referansları:
- /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/morph_07_yakin_plan_mimik.jpg (yakın plan portre — en önemli referans)
- /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/01_sahne_zeki_ve_ani_masada_00_00.jpg, /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/10_sahne_zeki_kisisel_itiraf_cene_elde_05_38.jpg, /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/11_sahne_universiteli_ela_macbook_06_20.jpg, /Users/wildgenie/Projects/gemini-prompt-arena/kaynak/avatar/morph_01_iki_el_acik_anlatim.jpg
- /Users/wildgenie/Downloads/Podcast_Bolum2_Produksiyon_Paketi/source/stills/generated/referans-paftalari/zeki-karakter-devamlilik.jpg
Tarz: çizgi roman / grafik roman illüstrasyonu; ince koyu mürekkep konturu, boyalı yumuşak gölgeleme, sinematik ışık (sıcak lamba ışığı + soğuk lacivert dolgu), gerçekçi orantı, sakin ve doğal ifade. Stilize portrelerde fon: koyu lacivert-gri, sade, hafif sıcak ışık vurgusu (sahnelerdeki gibi). KARAKTER_KIMLIK_PAFTASI yalnız karakter sheet DÜZENİ için (önden + üç çeyrek tam boy + 4 ifade); çizim tarzı yine sahne kareleri gibi olacak.

## Ek istek 9 (26 Ekim, kullanıcı): eksik kadrajları tamamla — BAŞKA HİÇBİR ŞEY YAPMA
Durum: 26 gri fon tamam (Gülsiye/Melek/Nusret yenileri `gri-fon/`'a taşındı). Kadrajda 18 kabul edilen dosya var; onlara DOKUNMA. Stilize/karakter sheet bu turda YOK.
- Yeniden üretilecek kadrajlar (8): adem-baglan, almina-yanar, duygu-solak, ela-ural, zeynep-seher-yolasigmaz, melisa-aydirek, nusret-bircan-keser, eslem-kilic.
- Son turdaki hata: Melisa, Nusret, Eslem ve Zeynep'te arka plan tamamen değişmiş, başka odaya dönmüştü. Bu YASAK. Kadraj = aynı fotoğrafın kenarlarını genişletmek: orijinal karenin tüm pikselleri (yüz + arka plan) korunur, Gemini yalnızca dışarıda kalan şeridi aynı sahnenin devamı olarak doldurur. Önce kesilmemiş orijinal fotoğrafta (`docs/ekip/orijinal/<slug>*.jpg`) zaten kare dışında kalan gerçek alan varsa ÖNCE onu kullan (orijinalden daha geniş kırp), Gemini'yi yalnız gerçek alan yetmezse çağır.
- Kontrol: çıktıyı orijinal kareyle hizalayıp karşılaştır; orijinal karenin içindeki arka plan değişmişse ya da dikiş izi varsa teslim etme. Başarısız kişiyi raporda yaz, uydurma çıktı koyma.
- Pafta: `docs/ekip/kontrol/kadraj-eksikler.jpg` (numara+isim; sitede | yeni kadraj). Site dosyalarına dokunma, commit/push yok.
