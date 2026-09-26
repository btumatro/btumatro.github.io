# MATRO Radyo — YouTube tam yayın videosu

Bu üretim, sitenin `src/data/radyo.json` dosyasındaki 14 parçalık sırayı değiştirmeden tek bir yatay YouTube videosuna dönüştürür. Açılış, ara ve kapanış jingle'ları yayın listesindeki yerlerinde kalır. Her parçada gerçek radyo kapak görseli ve başlık değişir; ses dalga biçimi o parçanın sesine tepki verir.

## Çıktılar

- `output/MATRO-Radyo-YouTube.mp4`: H.264/AAC, 1280×720, YouTube'a yüklemeye hazır tam yayın.
- `MATRO-Radyo-YouTube-kapak.jpg`: 16:9 YouTube thumbnail.
- `youtube-aciklama-ve-bolumler.txt`: Başlık, açıklama ve radyo sırasına göre zaman damgalı bölüm listesi.
- `assets/radyo-youtube-arka-plan.png`: Imagegen ile oluşturulmuş, gerçek MATRO/BTÜ logoları ve kapaklarıyla birleştirilen fon.

## Yeniden üretme

Depo kökünden:

```bash
python3 docs/podcast/youtube/create_video.py
```

FFmpeg, ffprobe ve Pillow gerekir. Akış ve kapak eşleşmeleri `src/data/radyo.json` kaynağından okunur. Kısa görsel önizleme için `--limit-seconds 12` seçeneği kullanılabilir. `--skip-video`, yalnızca kapak ve YouTube açıklaması/bölüm listesini üretir.

YouTube video dosyaları `output/` altında yerel tutulur; 30 dakikadan uzun final MP4 repoya eklenmez.
