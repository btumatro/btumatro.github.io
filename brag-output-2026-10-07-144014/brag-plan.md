# Brag Plan: BTÜ MATRO

## What is this project?
Bursa Teknik Üniversitesi Makine Teknolojileri Robot ve Otomasyon Topluluğu için havada, karada ve denizde çalışan robotik sistemleri geliştiren ekipleri tanıtan resmî web sitesi.

## 9 soruluk proje okuması

1. **Ne?** MATRO'nun takımlarını, çalışmalarını, başarılarını ve topluluğa katılım yolunu anlatan statik tanıtım sitesi.
2. **En güçlü iddia?** Ana sayfanın kendi cümlesi: “Atölyede başlar. Sahada kanıtlanır.”
3. **Görsel kanca?** Koyu mürekkep tonları, turkuaz vurgu ve gerçek takım/araç fotoğrafları; başlıklarda Barlow, metinde Inter, teknik etiketlerde JetBrains Mono.
4. **Gösterilecek gerçek içerik?** Ana sayfa başlığı ve CTA'sı; hava aracı, tarım robotu ve insansız deniz aracı fotoğrafları; MATRO ve BTÜ logoları.
5. **En kısa tatmin edici süre?** 21,5 saniye: vaadi kur, üç çalışma alanını kanıtla, ekibi ve katılım davetini göster.
6. **Ton?** `polished`; yaratıcı yön: gerçek fotoğraflarla çekilmiş, teknolojiyi insan emeğine bağlayan kısa belgesel tanıtımı. Dingin açılış, üç net kesme, kısa ekip nefesi, sakin ve okunur kapanış.
7. **Ses nasıl olmalı?** Sözsüz, sıcak ve ritmik bir müzik yatağı; yalnızca iki düşük riskli, yumuşak vurgu. Müzik görüntüyü taşısın, mesajın önüne geçmesin.
8. **Paylaşım metni?** “Atölyede başlar. Sahada kanıtlanır. BTÜ MATRO’da havada, karada ve denizde çalışan robotik projelere göz at.”
9. **Kullanıcı akışı?** Uygulama akışı yok; bu çok sayfalı, statik bir topluluk sitesi. Videoda ana sayfa vaadinden takımların gerçek çalışmalarına ve “Aramıza katıl” çağrısına giden içerik yolu gösterilecek.

## Açı
“Bir öğrenci topluluğu ne üretir?” sorusunu teknik anlatımla değil, aynı cümleyi doğrulayan üç gerçek sahayla yanıtla: hava aracı, tarım robotu, insansız deniz aracı. Sonra görüntüyü ekipte ve katılım davetinde bitir. Siteye ait olmayan araç, sonuç, ödül sayısı veya kurumsal ortaklık ekleme.

## Kanca (ilk 2–3 saniye)
Atölyede çalışan ekip fotoğrafı üzerinde büyük ve yüksek kontrastlı “Atölyede başlar.” Başlık 0,2 saniyelik kısa bir gecikmeyle gelir; fotoğrafın öznesini kapatmaz.

## Orta bölüm
- “Havada.” — hangardaki hava aracı ve ekibi.
- “Karada.” — sahadaki kara robotu ve ekibi.
- “Denizde.” — insansız deniz aracı ve TCG Anadolu.
- “Sahada kanıtlanır.” — Mavi Vatan etkinliğinde bir araya gelen ekipler.

## Kapanış
BTÜ ve MATRO'nun resmî logoları, ardından ana sayfadaki gerçek CTA: “Sıradaki projede sen de ol.” / “Aramıza katıl”. Logolar bozulmadan, oranları korunarak gösterilecek.

## Ton
- **Preset:** polished
- **Yaratıcı yön:** belgesel gerçekliği taşıyan, teknoloji ve ekip emeğini aynı görsel çizgide buluşturan kısa tanıtım filmi.
- **Uygulama:** büyük Barlow başlıkları; Inter ile kısa CTA; ink arka plan ve volt turkuaz vurgu. Kaynak fotoğraflara yapay robot, sahte arayüz, çizim, ek logo veya yoğun filtre ekleme.

## Biçim: yatay — 1920×1080
## Süre: 21,5 saniye

## Görsel kimlik (kaynak dosyalardan)
- **Arka plan:** `#0b1012` (ink-950)
- **Metin:** `#f0f0e9` (mist-100)
- **Vurgu:** `#75d5d0` (volt-400)
- **Başlık:** Barlow; yerel font dosyası kullanılacak.
- **Gövde:** Inter Variable; yerel font dosyası kullanılacak.
- **Teknik etiket:** JetBrains Mono Variable; gerekirse yalnızca ufak meta bilgide.
- **Görsel referanslar:** `src/data/home.json` ve ana sayfa hero'sundaki altı fotoğraf; `public/logo-matro-beyaz.png`; `public/logo-btu-beyaz.png`.

## Paylaşım metni (taslak)
Atölyede başlar. Sahada kanıtlanır. BTÜ MATRO’da havada, karada ve denizde çalışan robotik projelere göz at.

## Ses yönü
- **Rol:** sıcak, hareketli ama ölçülü destek.
- **Müzik:** `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3`; sözsüz ritmik yatak. Parça becerinin yerel varlığında; bu çalışma yayımlanmayacak.
- **Müzik seviyesi/işleme:** düşük-orta seviyede başla; final logosuna doğru hafif yüksel, son 0,7 saniyede yumuşakça kapat.
- **Vuruş ipuçları:** yerel preset 120,19 BPM. Görsel geçişleri yaklaşık 3,52 / 6,03 / 8,52 / 11,52 saniye vuruşlarına; ekipten kapanışa geçişi 16,02 saniye civarına; CTA vurgusunu 20,02 saniyeye yaklaştır. Okunurluk ritimden önce gelir.
- **Ses tepkisi:** mevcut fotoğraf karartma/ışık katmanı, müziğin önceden çıkarılmış Hareket yalnızca fotoğrafa uygulanan yavaş, ölçülü pan/zoom ile verilsin; görselizer ve rastgele parçacık yok.
- **SFX:** az. İlk görsel açılışında ve logoların oturuşunda birer yumuşak vurgu; tekrar eden klik yok.
- **Kaçınılacaklar:** anlatım, aşırı parlama, sert glitch, sürekli zoom, sesin müziğe göre pompalanması.

## Storyboard

| Zaman | Sahne | Ekranda görülen | Sahnenin görevi |
|---|---|---|---|
| 0:00–0:03.7 | Atölye | `galeri-zemheri-sunum-atolye-genis.jpg`; metin: “Atölyede başlar.” | Ana sayfanın kendi vaadiyle merak açar. |
| 0:03.7–0:06.3 | Hava | `galeri-ashina-hangar.jpg`; metin: “Havada.” | Vaat için gerçek bir hava aracı ve ekip gösterir. |
| 0:06.3–0:08.9 | Kara | `galeri-matrover-stand.jpg`; metin: “Karada.” | Kara robotu ve ekibi gerçek saha bağlamında gösterir. |
| 0:08.9–0:11.5 | Deniz | `galeri-lodos-saha.jpg`; metin: “Denizde.” | İnsansız deniz aracını ve ekibini gösterir. |
| 0:11.5–0:16.5 | Ekip | `mavi-vatan-ekipler.jpg`; metin: “Sahada kanıtlanır.” Ardından küçük satır: “Birlikte tasarlıyor, üretiyor ve yarışıyoruz.” | Ana sayfanın vaadini insan emeğiyle tamamlar. |
| 0:16.5–0:21.5 | Davet | Koyu ink zemin; iki resmî logo, CTA: “Sıradaki projede sen de ol.” ve “Aramıza katıl” | Gerçek marka ve ana sayfa çağrısıyla net bitiş sağlar. |

**Ses/müzik:** Müzik ilk kareden itibaren; iki yumuşak SFX yalnızca büyük açılış ve kapanışta. Fotoğraflar arası geçişlerde birer temiz kesme veya kısa dissolve.

**Ritim:** Açılış-hold → üç kısa ve ritmik kanıt → ekipte nefes → logolu CTA'da sabit ve okunur kapanış.
