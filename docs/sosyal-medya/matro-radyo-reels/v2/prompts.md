# MATRO Radyo Reels v2 — üretim promptları

V2, açılış ve radyo yakın planını Gemini Omni ile yeniden üretir; v1'in seslendirmesini, jingle'ını ve CTA metnini kullanır. Yeni site karesi sticker pack'teki güncel araçlara göre üretildi. Kapanışta karakter kaldırıldı; aynı atölye sahnesindeki MacBook ekranına gerçek btumatro.com ana sayfası yerleştirildi.

## Site sahnesi kaynak görseli

Model: OpenAI Imagegen. Referanslar `assets/reference/` içindedir: MATROVER, MATRIS ve LODOS sticker görselleri. Metin görseli sonradan kodla eklenir.

```text
Use case: cinematic social reel scene background for Bursa Technical University MATRO. Portrait 9:16, no text. Reference Image 1 is the exact MATROVER six-wheel field rover design: retain black boxy chassis, six rugged wheels, exposed upper frame and sensor proportions. Reference Image 2 is the exact MATRIS quadcopter design: retain the red X-shaped four-arm frame, four motors and propellers, central electronics. Reference Image 3 is the exact LODOS unmanned surface vessel: retain its low angular gray deckhouse, dark hull, compact antenna/sensor details and single boat silhouette. Create one polished cinematic illustrated scene featuring each recognizable machine in a distinct setting within a unified vertical composition: MATRIS quadcopter hovering in the upper sky, MATROVER rover on a rocky outdoor test track in the middle, LODOS vessel crossing water in the lower foreground. Keep every machine faithful to its own corresponding reference; do not merge parts or invent extra wheels, rotors, arms or hulls. Refined engineering illustration, dark teal dusk shadows, restrained warm amber highlights, believable practical robotics, clear silhouettes, natural scale, high-end editorial animation background for a social Reels ad. Keep top and bottom edges dark and uncluttered for later title overlays. No people, no lettering, no fake text, no logos, no flags, no badges, no user interface, no watermark, no collage panels, no duplicate vehicles.
```

Imagegen ilk denemede LODOS'u çift gövdeli çizdi. Düzenleme promptunda yalnızca tekne, sticker referansına göre tek gövdeli olacak şekilde düzeltildi:

```text
Edit Image 1 only where the boat appears at the very bottom of the portrait scene. Replace that vessel with a single-hull LODOS unmanned surface boat faithful to Image 2: one compact low angular gray upper deckhouse, one dark single central hull, small antenna/sensor details, no side pontoons and no catamaran/twin hull. Preserve the upper red quadcopter, the middle black six-wheel MATROVER exactly as they are in Image 1, and keep the sunset, rocky landscape, water, lighting, crop and illustration style unchanged. The boat should read as one clear monohull profile, with only its own reflection and surrounding water. No text, no logos, no added vehicles.
```

## Site video: Gemini Omni Flash 1.1

Girdi: `assets/images/robotik-sahne-kaynagi-v2.png`. Kare başına yeni araç tasarlatmamak ve teker/rotor/gövde sayısının değişmesini önlemek için prompt şekilleri ve sınırları açıkça sabitler. Tam prompt `scripts/generate_omni_v2.py` içindedir.

## Radyo video: Gemini Omni Flash 1.1

Girdi: `assets/images/radio-closeup-source-v2.png`. Gözlük, yüz, el/nesne teması, metin ve yeni uzuv oluşumu promptta özellikle kısıtlandı. Açılış girdisi `assets/images/chibi-radio-source.png` dosyasıdır. Tam promptlar `scripts/generate_omni_v2.py` içindedir.

## Sonraki düzenleme

Son afiş girdisi `assets/images/chibi-laptop-site-source-v2.png` dosyasıdır. Karakter ve tabure kaldırılmış, atölye/masa kadrajı korunup küçük MacBook eklenmiştir. Edge'deki MATRO ana sayfası laptop ekranında görsel referans olarak kullanılmıştır; minik ekranda yazılar birebir okunur değildir. Logo ve Türkçe başlıklar sonradan gerçek MATRO/BTÜ logo dosyalarıyla çizilir. CTA “btumatro.com” olarak kalır.
