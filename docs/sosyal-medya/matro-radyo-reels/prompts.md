# Görsel ve video üretim promptları

Promptlar, seçilen son kliplerin üretiminde kullanılan metinlerdir. Görselde yazı ve marka işaretleri modelden istenmedi; okunaklı Türkçe metinler ve gerçek logolar sonradan grafik katmanı olarak eklendi.

## Chibi açılış: Gemini Omni Flash 1.1

Girdi: `assets/image/chibi-acilis-kaynagi.png`

Model: `gemini-omni-1.1-flash`

İş: tek plan, 10 sn, dikey 9:16 video.

```text
Animate this exact chibi illustration as one continuous 10-second vertical 9:16 scene. Preserve its clean sticker-like chibi design, teal workshop, warm desk lamp, radio, and character identity. The bald man has black glasses already on his face; glasses stay on throughout and are never removed, adjusted, picked up, or touched. Keep his eyes at their current relaxed size, eyebrows calm, and expression subtle; no wide-eyed surprise, no exaggerated grin, no sudden facial morphing. No dialogue, no speech bubbles, no generated words, captions, logos, or extra props. Motion is gentle and readable: seconds 0-2 the seated character notices the old radio with a small head turn; 2-5 he turns the tuning knob slowly, radio emits soft static and the dial glows; 5-7 the static resolves into a cheerful short station jingle; 7-9 the little robot makes one small rhythmic bob and the character gives a restrained amused smile; 9-10 settle into a clean composition with the man and radio. Subtle camera push-in, no cuts, no dramatic gestures. Audio: only soft playful radio static transitioning to a short upbeat instrumental station jingle, absolutely no speech or gibberish.
```

## Site/robotik sahnesi: Gemini Omni Flash 1.1

Girdi: `assets/image/site-sahne-kaynagi.png`

İş: tek plan, 8 sn, 9:16 image-to-video.

```text
Animate this exact vertical 9:16 robotics illustration into one elegant 8-second cinematic shot. Preserve its exact drone, field rover, underwater ROV and dusk landscape; no morphing or new machinery. Gentle camera push-in with subtle parallax. Drone rotors turn slowly, rover lights glow softly, underwater particles drift. Keep same premium photographic illustration, dark teal and amber grade. Absolutely no text, lettering, logos, UI, subtitles, people or watermarks. No cuts, no flashing.
```

## Radyo sahnesi: Gemini Omni Flash 1.1

Girdi: `assets/image/radyo-sahne-kaynagi.png`

İş: tek plan, 8 sn, 9:16 image-to-video.

```text
Animate this exact vertical 9:16 vintage radio workshop illustration into one elegant 8-second cinematic shot. Preserve the same radio, tuning hand and workshop. The hand turns the frequency knob slightly; the amber dial brightens gently; a few small analog sound waves shimmer near the speaker, subtle dust drifts through the warm light. Keep the same premium illustrated style, dark teal and copper palette. No text, lettering, logos, UI, subtitles, or watermarks. No cuts, no morphs, no new objects, no flashing.
```

## Konuşma metni

Ayşe ve Can replikleri `assets/audio/seslendirme-metni.json` içinde sıralıdır. URL'yi TTS'ye okutmak yerine “Profildeki linke tıklayın” çağrısı ekranda ve Ayşe'nin sesinde verilir. Kullanılan hazır ses dosyası `assets/audio/ayse-can-seslendirme.mp3`.

## Kaydedilmemiş görsel promptu

Site ve radyo için kaynak illüstrasyonlar Gemini Image ile üretildi. Bu iki görselin ilk üretim prompt metni çalışma klasöründe saklanmadığından burada yeniden kurulmuş bir metin varmış gibi sunulmuyor. Girdi görselleri ve ardından kullanılan Omni canlandırma promptları pakette mevcut.
