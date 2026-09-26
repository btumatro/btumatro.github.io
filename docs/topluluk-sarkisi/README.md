# MATRO topluluk şarkıları ve radyo müzikleri

Yapay zekâ müzik araçlarıyla (Gemini, Suno/Udio promptları) üretilen topluluk şarkıları,
MATRO Radyo jingle'ı ve radyo yatakları. Eylül 2026. Radyonun nasıl birleştirildiği için
`docs/podcast/README.md`.

## Klasör

| Yol | İçerik |
|---|---|
| `ses/` | Üretilen şarkılar (MP4, 1024×1024 kapak görseli + ses + gömülü söz altyazısı) |
| `sozler/` | Her şarkının **sesteki gerçek sözleri** (videonun altyazı kanalından çıkarıldı) |
| `prompt-taslaklari/` | Prompt belgeleri (v1–v8): stil, hariç tutulanlar, sözler, notlar ve üretim sonucu |

## Şarkılar

| Dosya | Başlık | Süre | Tür etiketi | Sözlerin kaynağı |
|---|---|---|---|---|
| `ses/01-atolyede-baslar.mp4` | Atölyede Başlar | 2:53 | Anthemic Pop-Rock | Orijinal sözler, "Mavi Vatan" ve "su altı" dahil (bkz. `prompt-taslaklari/v1`) |
| `ses/02-atolyede-baslar-v2.mp4` | Atölyede Başlar (2. sürüm) | 3:02 | Turkish Pop-Rock | Gemini'nin üretimde yeniden yazdığı sözler; "Milli Teknoloji Hamlesi" ve "Mavi Vatan" geçiyor |
| `ses/03-atolyeden-goklere.mp4` | Atölyeden Göklere | 3:03 | Turkish Pop-Rock | Gemini'nin yeniden yazdığı, daha yüksek enerjili sözler; "Milli Teknoloji Hamlesi", "Mavi Vatan", "BTÜ" geçiyor |
| `ses/04-gece-yarisi-mesaisi.mp4` | Gece Yarısı Mesaisi | 2:57 | Türkçe rap | `v7` sözleri birebir; başa "Bursa Teknik Üniversitesi, MATRO", sona slogan eklenmiş |
| `ses/05-derinden-goklere.mp4` | Derinden Göklere | 2:55 | Pop-rock düet | `v5` (Mavi Vatan) sözleri birebir |
| `ses/06-suru.mp4` | Sürü | 3:00 | Synthwave, sözsüz | `v6` |
| `ses/07-the-bursa-shift.mp4` | The Bursa Shift | 2:57 | Lo-fi, sözsüz | `v4` (Gece Vardiyası) |

## Radyo müzikleri

| Dosya | Başlık | Süre | Radyodaki görevi | Prompt |
|---|---|---|---|---|
| `ses/08-matro-radyo-jingle.mp4` | Saha Bizim | 0:55 | Jingle: 0–14,2 sn açılış, 45,8–53,4 sn kapanış/istasyon kimliği | `v8` §1, sözler `sozler/08-matro-radyo-jingle.md` |
| `ses/09-dj-yatagi-the-hourly-brief.mp4` | The Hourly Brief | 2:48 | DJ bağlantılarının altındaki yatak | `v8` §2 |
| `ses/10-hikaye-yatagi-a-measure-of-intent.mp4` | A Measure of Intent | 2:55 | Hikâye (podcast) bölümlerinin yatağı | `v8` §3 |
| `ses/11-bulten-yatagi-unfolding-blueprints.mp4` | Unfolding Blueprints | 2:53 | Bülten yatağı | `v8` §4/§5 (bkz. not) |
| `ses/12-gece-yatagi-the-midnight-invention.mp4` | The Midnight Invention | 2:56 | "Atölyede gece" bağlantısının yatağı | `v8` §4/§5 (bkz. not) |

Not: Yataklar dosya adına göre değil sese göre eşleştirildi. Unfolding Blueprints
bülten promptundaki ritmik yapıya en yakın parça; The Midnight Invention sakin ve
sinematik çıktığı için bülten yerine gece yatağı oldu. Tema müziği henüz yok.

**Önemli:** 2. ve 3. şarkının sözleri `prompt-taslaklari/v2` ve `v3` belgelerindeki
sözlerle birebir aynı değildir; model üretim sırasında sözleri değiştirdi. Paylaşırken
veya altyazı hazırlarken her zaman `sozler/` klasöründeki metni kullanın.

Şarkıların hepsi MATRO Radyo'da çalar. Sesler tek başına değil, DJ bağlantısıyla birleştirilmiş
bloklar olarak `public/media/ses/blok-*.mp3` altındadır; kapaklar `public/media/ses/0*.jpg`.

## Kullanım önerisi

- **Atölyede Başlar:** Yarışma günü, TEKNOFEST ve tanıtım videoları.
- **Atölyeden Göklere:** Hızlı montaj, Reels ve atölye motivasyon videoları.
- **2. sürüm:** Alternatif; hangi sürümün topluluğun resmî şarkısı olacağına yönetim kurulu karar verir.
- **Gece Yarısı Mesaisi:** Takım tanıtımları, "yoklama" kurgulu videolar (bütün takım adları geçer).
- **Derinden Göklere:** Mavi Vatan, deniz ve su altı takımları içerikleri.
- **Sürü / The Bursa Shift:** Sözsüz; arka plan müziği, atölye timelapse, stant ekranları.

## Paylaşmadan önce

- Üretimde kullanılan aracın ticari kullanım ve hak koşullarını kontrol edin; sponsor
  videolarında ve Instagram'da kullanım için bu önemlidir.
- Sözlerde olgu kontrolü: takım adları ve 2013 kuruluş yılı doğru. Sözlerde derece veya
  rakam iddiası varsa (ör. "ilk yılında final") `src/data/achievements.json` ile uyumlu olmalı.
- Emoji içermez; altyazıdaki `♪` işaretleri söz dosyalarından temizlendi.
- MP4 dosyaları 8–14 MB'tır. Siteye doğrudan konmaz; radyo için ses `scripts/radyo-yayin.mjs`
  ile işlenir.
- Model sözleri değiştirebilir: yeni şarkı gelince altyazı kanalından gerçek sözleri çıkarıp
  `sozler/` klasörüne yazın (`ffmpeg -i sarki.mp4 -map 0:s:0 -f srt -`).
