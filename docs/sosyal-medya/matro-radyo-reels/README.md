# MATRO Radyo Reels kaynak paketi

Bu klasör, 26 Eylül 2026'da hazırlanan yaklaşık 31 saniyelik dikey MATRO site ve radyo tanıtımının son sürümünü, seçilmiş kaynak medyalarını, Gemini Omni sahne promptlarını ve tekrar render betiğini içerir.

## İçerik

- `output/MATRO-Radyo-Reels-final.mp4`: teslim edilen 720 × 1280, 24 fps, H.264/AAC video.
- `assets/video/`: kullanılan chibi açılışı ve Gemini Omni ile canlandırılan site/radyo klipleri.
- `assets/image/`: Omni sahnelerinin girdileri ve kapanış karesinin kaynağı.
- `assets/graphics/`: Türkçe başlık katmanları ve son afiş. Logolar gerçek MATRO ve BTÜ logo dosyalarından hazırlanmıştır.
- `assets/graphics/alternatif/chibi-final-poster-art-v2.png`: kullanıcının seçtiği alternatif, yazısız kapanış illüstrasyonu; son MP4'ün kapanış görseli değildir.
- `assets/audio/`: Ayşe ve Can seslendirmesi, senaryo ve `Saha Bizim` jingle kaynağı.
- `assets/logos/`: afişte kullanılan resmî logo kaynakları.
- `prompts.md`: kaydedilmiş görsel/video model promptları ve kullanım notları.
- `scripts/render_reel.py`: klipleri, grafik katmanlarını ve sesi birleştirerek MP4'ü yeniden üretir.

## Yeniden render

Depo kökünden:

```bash
python3 docs/sosyal-medya/matro-radyo-reels/scripts/render_reel.py
```

Gerekenler: `ffmpeg` (H.264/AAC kodlayıcılarıyla). Betik geçici sahneleri sistemin geçici dizininde üretir; final dosyayı `output/` altına yazar. Model çağrısı yapmaz ve API anahtarı gerektirmez. Hazır seslendirme ve üretilmiş Omni kliplerini kullanır.

Türkçe metin veya logo katmanlarını yeniden çizmek için önce `python3 docs/sosyal-medya/matro-radyo-reels/scripts/generate_graphics.py` çalıştır. Bu adım Pillow ve sistemde Arial fontu gerektirir.

Model sahnelerini yeniden üretmek için `scripts/generate_omni_scenes.py` dosyasına ve `prompts.md` içindeki promptlara bak. Bu ayrı işlem Gemini API erişimi ve ücret/kota kullanımı gerektirebilir. `GEMINI_API_KEY` yalnızca ortam değişkeninden okunur; anahtar kaynaklara eklenmemelidir.

## Kurgu sırası

1. 10 sn chibi radyo açılışı; ilk 3,5 sn boyunca temiz başlık bandı.
2. 8 sn Omni site/robotik montajı.
3. 8 sn Omni eski radyo sahnesi.
4. 6 sn kapanış afişi. Afiş illüstrasyonu açılış Omni klibinin bir karesinden türetildiği için karakter görünümü girişle eşleşir.

Sahneler arasında 0,35 sn geçiş bulunur. Toplam süre yaklaşık 30,96 sn'dir. Başlangıçta belirgin radyo hışırtısı duyulur; `Saha Bizim` jingle'ı konuşmaların altında devam eder ve konuşma sırasında otomatik kısılır. CTA ekranda ve Ayşe'nin sesinde “Profildeki linke tıklayın.” olarak geçer.

## Alternatif kapanış görseli

`assets/graphics/alternatif/chibi-final-poster-art-v2.png`, daha beğenilen alternatif illüstrasyondur. Kaynak olarak eklendi; üzerinde yazı/logo olmadığı için ana afişin yerine otomatik konmadı. İstenirse `scripts/render_reel.py` içindeki kapanış görseli girdisi bu dosyaya yönlendirilip üzerine MATRO/BTÜ logo ve metinleri yerleştirilebilir.

## Kaynak ve gizlilik

Ses/jingle, kullanıcı tarafından sağlanan `Saha_Bizim.mp4` dosyasından; logolar bu depodaki `public/logo-matro-beyaz.png` ve `public/logo-btu-beyaz.png` kaynaklarından alınmıştır. TTS ve üretilmiş görseller/video, bu çalışma için oluşturulan çıktılardır. Gemini yanıt gövdeleri, geçici ara renderlar ve API anahtarları depoya alınmamıştır. Yeniden dağıtım öncesinde kullanılan müzik ve model hesaplarının güncel lisans/izin koşullarını ayrıca kontrol edin.
