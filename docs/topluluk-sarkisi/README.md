# MATRO topluluk şarkıları

Yapay zekâ müzik araçlarıyla (Gemini, Suno/Udio promptları) üretilen topluluk şarkıları.
Eylül 2026.

## Klasör

| Yol | İçerik |
|---|---|
| `ses/` | Üretilen şarkılar (MP4, 1024×1024 kapak görseli + ses + gömülü söz altyazısı) |
| `sozler/` | Her şarkının **sesteki gerçek sözleri** (videonun altyazı kanalından çıkarıldı) |
| `prompt-taslaklari/` | Gemini ile hazırlanan üç prompt belgesi: stil, hariç tutulanlar, sözler, notlar |

## Şarkılar

| Dosya | Başlık | Süre | Tür etiketi | Sözlerin kaynağı |
|---|---|---|---|---|
| `ses/01-atolyede-baslar.mp4` | Atölyede Başlar | 2:53 | Anthemic Pop-Rock | Orijinal sözler, "Mavi Vatan" ve "su altı" dahil (bkz. `prompt-taslaklari/v1`) |
| `ses/02-atolyede-baslar-v2.mp4` | Atölyede Başlar (2. sürüm) | 3:02 | Turkish Pop-Rock | Gemini'nin üretimde yeniden yazdığı sözler; "Milli Teknoloji Hamlesi" ve "Mavi Vatan" geçiyor |
| `ses/03-atolyeden-goklere.mp4` | Atölyeden Göklere | 3:03 | Turkish Pop-Rock | Gemini'nin yeniden yazdığı, daha yüksek enerjili sözler; "Milli Teknoloji Hamlesi", "Mavi Vatan", "BTÜ" geçiyor |

**Önemli:** 2. ve 3. şarkının sözleri `prompt-taslaklari/v2` ve `v3` belgelerindeki
sözlerle birebir aynı değildir; model üretim sırasında sözleri değiştirdi. Paylaşırken
veya altyazı hazırlarken her zaman `sozler/` klasöründeki metni kullanın.

## Kullanım önerisi

- **Atölyede Başlar:** Yarışma günü, TEKNOFEST ve tanıtım videoları.
- **Atölyeden Göklere:** Hızlı montaj, Reels ve atölye motivasyon videoları.
- **2. sürüm:** Alternatif; hangi sürümün topluluğun resmî şarkısı olacağına yönetim kurulu karar verir.

## Paylaşmadan önce

- Üretimde kullanılan aracın ticari kullanım ve hak koşullarını kontrol edin; sponsor
  videolarında ve Instagram'da kullanım için bu önemlidir.
- Sözlerde olgu kontrolü: takım adları ve 2013 kuruluş yılı doğru. Sözlerde derece veya
  rakam iddiası varsa (ör. "ilk yılında final") `src/data/achievements.json` ile uyumlu olmalı.
- Emoji içermez; altyazıdaki `♪` işaretleri söz dosyalarından temizlendi.
- MP4 dosyaları 10–11 MB'tır. Siteye gömülecekse `ffmpeg` ile ses (AAC 128k) ayrı çıkarılıp
  kapak görseli poster olarak kullanılabilir (bkz. AGENTS.md video notu).
