# MATRO Radyo Reels v2

V2, açılış ve radyo yakın planını yeniden üretir; seçilen chibi atölye çizgisini karakter olmadan, MacBook ekranında MATRO ana sayfa görünümüyle kapanış afişine taşır. Site sahnesi MATROVER, MATRIS ve LODOS sticker pack görsellerini tasarım referansı olarak kullanır.

## V2 dosyaları

- `assets/reference/`: sticker pack'ten araç referansları.
- `assets/images/robotik-sahne-kaynagi-v2.png`: Imagegen ile hazırlanan MATRO araçlı site sahnesi.
- `assets/images/chibi-radio-source.png`: açılış videosunda canlandırılan karakterli radyo sahnesi.
- `assets/images/chibi-laptop-site-source-v2.png`: karakteri ve taburesi kaldırılmış, aynı atölye/masa kadrajında küçük MacBook bulunan kapanış sahnesi. Site görünümü ekrandaki gerçek içerik referans alınarak resmedilmiştir; küçük ekranda yazılar okunur olmak üzere tasarlanmamıştır.
- `assets/video/`: Gemini Omni ile yeniden üretilen iki klip.
- `assets/graphics/kapanis-afisi-v2.png`: karakter içermeyen MacBook'lu atölye sahnesi, gerçek MATRO/BTÜ logoları ve CTA.
- `output/MATRO-Radyo-Reels-v2.mp4`: V2 final videosu.
- `prompts.md` ve `scripts/`: üretim promptları ile yeniden render adımları.

Açılış videosu, TTS, jingle, MATRO/BTÜ logoları ve mevcut CTA/başlık katmanları v1 paketinden ortak kullanılır (`../assets/`). Tekrar render için depo kökünden:

```bash
python3 docs/sosyal-medya/matro-radyo-reels/v2/scripts/render_v2.py
```

Yeni Omni sahnelerini yeniden üretmek için `GEMINI_API_KEY` ortam değişkeni gerekir ve Gemini kotası kullanır:

```bash
python3 docs/sosyal-medya/matro-radyo-reels/v2/scripts/generate_omni_v2.py site
python3 docs/sosyal-medya/matro-radyo-reels/v2/scripts/generate_omni_v2.py radio
python3 docs/sosyal-medya/matro-radyo-reels/v2/scripts/generate_omni_v2.py chibi
```

Görselleri yeniden çizmek için `python3 docs/sosyal-medya/matro-radyo-reels/v2/scripts/generate_graphics_v2.py` çalıştır; Pillow ve Arial fontu gerekir. Ardından `render_v2.py` ile MP4'ü üret.

API anahtarı betiklerde veya çıktılarda saklanmaz. İşlenmemiş Gemini API yanıtları depoya eklenmez.
