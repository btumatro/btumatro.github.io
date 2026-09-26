# MATRO Radyo: yayın planı (v2)

Sitedeki radyonun "art arda çalan dosyalar"dan gerçek bir radyo yayınına dönüşmesi için
değerlendirme ve plan. Eylül 2026.

## 1. Mevcut durumun değerlendirmesi

**Ses (düzeltildi, `scripts/radyo-miks.mjs`):**

- Replik arası boşluk ortalama 0,23 sn idi, nefes alınmıyordu. Artık her boşluğa 0,4 sn
  ekleniyor (~0,65 sn).
- Müzik konuşmanın altında sabit seviyedeydi. Artık sidechain ile konuşmada ~14 dB iniyor,
  aralarda geri geliyor; girişte 4 sn, çıkışta 5 sn müzik var.
- Tempo (saniyede 2,1–2,4 kelime) uygun.

**Format (asıl eksik):**

- Radyo değil, "podcast + ayrı anonslar" gibi duruyor. İstasyon kimliği (jingle) yok.
- DJ az önce çalan şarkıyı anmıyor (back-announce), şarkıya konuşarak girmiyor (talk-up).
- Her konuşma ayrı dosya olduğu için parçalar arasında kısa ölü boşluklar oluyor.
- Tüm konuşmalarda aynı lo-fi yatak kullanılıyor; kuşaklar birbirinden ayırt edilmiyor.

**İçerik:**

- Tekrarlar:
  - Lagari hem podcast 2. bölümde hem "Bunu biliyor muydunuz?"da geçiyor.
  - MATROVER'ın 3.'lüğü hem 2. bölümde hem "Karada ve denizde"de var.
  - "Atölyede bir gece" teması hem 1. bölümde hem 07 numaralı arada işleniyor.
  - Başvuru bilgisi hem 3. bölümde hem "Aramıza katıl"da tekrarlanıyor.
- Güncel olmayan bilgiler (podcast 2. bölüm):
  - ZEMHERİ yalnızca "finalist" diye geçiyor; oysa KTR'de 4., finalde 9. oldu.
  - LUNA İKA'nın 9.'luğu yok.
  - ALHAZEN'in nükleer ön rapor 2.'liği yok.

## 2. Hedef format: MATRO Radyo yayın döngüsü (~40 dk)

Yayın "blok"lardan oluşur. Her blok **tek bir dosyadır**:

```
[DJ bağlantısı müzik yatağı üstünde] -> [DJ son cümlesini şarkının girişi üstünde söyler] -> [şarkı]
```

Böylece parçalar arasında boşluk kalmaz ve DJ şarkıya radyodaki gibi "üstünden" girer.

### DJ bağlantısı (link) kuralları

- **Uzunluk:** 20–45 sn. Tek bir bilgi verilir, liste okunmaz.
- **Yapı:**
  1. Back-announce: "Az önce Gece Yarısı Mesaisi'ni dinlediniz..."
  2. Tek bir içerik lokması.
  3. Front-announce: "Sırada Derinden Göklere, deniz takımlarımız için."
- **Talk-up:** Son cümle şarkının enstrümantal girişinin üstünde söylenir; şarkı altta
  kısılıdır, cümle bitince yükselir.
- **İstasyon kimliği:** Her 2–3 blokta bir jingle çalar ("MATRO Radyo, atölyeden sahaya").
- **Sunucular:**
  - Ayşe: akışı yöneten ana DJ, sıcak ve enerjik.
  - Can: teknik tarafı anlatan ikinci ses.
  - İkisi de dinleyiciye "sen" diye hitap eder.

### Kuşaklar (tekrar eden bölümler)

| Kuşak | Süre | İçerik | Yatak |
|---|---|---|---|
| MATRO Hikâyesi | 3 × ~2 dk | Mevcut podcast; 2. bölüm güncel bilgilerle yeniden seslendirilecek | Hikâye yatağı |
| Bunu biliyor muydunuz? | 25 sn | Tek şaşırtıcı bilgi | DJ yatağı |
| Radyo sözlüğü | 30 sn | Tek terim: ÖTR, KTR, otonom, SLAM, sürü İHA | DJ yatağı |
| Takım spotu | 35 sn | Her yayında farklı bir takım | DJ yatağı |
| MATRO bülteni | 40 sn | Sitedeki son 3 haber, sitenin verisinden otomatik yazılır | Bülten yatağı |
| Kapanış | 30 sn | Başvuru ve eğitim çağrısı, istasyon kimliği | Tema müziği |

### Örnek döngü

1. İstasyon jingle
2. MATRO Hikâyesi 1. bölüm, tema müziğiyle açılış
3. Link, ardından Atölyede Başlar
4. Bunu biliyor muydunuz?, ardından Gece Yarısı Mesaisi
5. MATRO bülteni
6. Link, ardından Atölyeden Göklere
7. Jingle, ardından Sürü (enstrümantal; DJ girişte kısa anons)
8. MATRO Hikâyesi 2. bölüm (güncellenmiş)
9. Radyo sözlüğü, ardından Derinden Göklere
10. Takım spotu, ardından Atölyede Başlar (2. sürüm)
11. Jingle, ardından The Bursa Shift
12. MATRO Hikâyesi 3. bölüm ve kapanış, tema müziğiyle bitiş

## 3. Gerekli müzikler (üretilecek)

Promptlar: `docs/topluluk-sarkisi/prompt-taslaklari/v8-radyo-paketi.md`

1. **İstasyon jingle paketi:** "MATRO Radyo" diyen kısa kimlik sesleri. Parçadan 3–4 adet
   5–8 sn'lik jingle kesilecek.
2. **DJ yatağı:** Enerjik, sözsüz, döngüye uygun. Linklerin altında çalacak.
3. **Hikâye yatağı:** Sakin, sinematik, sözsüz. Podcast bölümlerinin altında çalacak.
4. **Bülten yatağı:** Tik-taklı, ritmik, sözsüz. Haber bülteninin altında çalacak.
5. **Tema müziği:** 25–30 sn intro/outro. Hikâye kuşağının açılış ve kapanışı.

## 4. Uygulama adımları

1. Link senaryoları: her geçiş için back-announce, içerik ve front-announce; tekrarların
   ayıklanması; podcast 2. bölümün güncel bilgilerle yeniden yazılması.
2. Bülten üreticisi: `src/content/haberler`'den son 3 yayındaki haberin kısa metni.
3. TTS: Gemini, Can ve Ayşe sesleri (`scripts/podcast-tts.mjs --senaryo`).
4. Blok miksi: `scripts/radyo-miks.mjs` genişletilir. Link yatak üstünde çalar, son cümle
   şarkı girişiyle çakıştırılır (talk-up, sidechain), jingle'lar araya girer, blok başına
   tek MP3 üretilir.
5. Oynatıcı: liste blokları gösterir ("Link + şarkı adı"); ilerleme çubuğu bloğun
   tamamını kapsar.
6. Ölçüm: tüm bloklar -11/-12 LUFS; konuşma altındaki müzik konuşmanın 15–18 dB altında.
