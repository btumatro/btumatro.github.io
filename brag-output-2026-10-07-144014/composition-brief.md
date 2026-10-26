# Hyperframes Composition Brief: BTÜ MATRO

## Objective
BTÜ MATRO'nun resmî tanıtım sitesini 21,5 saniyelik paylaşılabilir bir videoda gerçek takım ve araç fotoğraflarıyla anlat.

## Output
- Composition directory: `brag-output-2026-10-07-144014/composition/`
- Rendered video: `brag-output-2026-10-07-144014/brag.mp4` (yalnızca son onaydan sonra)
- Format: landscape — 1920×1080
- Duration: 21.5 seconds

## Source Material
- Project root: `/Users/wildgenie/Projects/btu-matro`
- Primary files read: `README.md`, `src/pages/index.astro`, `src/data/home.json`, `src/styles/global.css`, `public/media/`
- Product name: BTÜ MATRO
- Strongest claim: “Atölyede başlar. Sahada kanıtlanır.”
- Key visual moments: gerçek atölye; hava aracı; tarım robotu; insansız deniz aracı; ekip.
- Copy used verbatim: “Atölyede başlar.”, “Sahada kanıtlanır.”, “Birlikte tasarlıyor, üretiyor ve yarışıyoruz.”, “Sıradaki projede sen de ol.”, “Aramıza katıl”.

## Creative Direction
- Tone preset: polished
- Direction: fotoğraf gerçekliğini koruyan, teknoloji ile öğrenci emeğini buluşturan kısa belgesel tanıtımı.
- Interpretation: az ama belirgin hareket; fotoğraflar ana görsel, büyük tipografi kısa mesajı taşır. Hava/karada/denizde sahneleri temiz kesmelerle ritim kurar; kapanış nefes alır.
- Angle: Bir öğrenci topluluğunun ne ürettiğini üç gerçek çalışma alanıyla göster; ekibi ve katılım çağrısını finalle.
- Hook: ana sayfadaki “Atölyede başlar.” sözünü gerçek atölye fotoğrafıyla aç.
- Outro: iki resmî logo ve “Sıradaki projede sen de ol.”
- Avoid: genelleştirilmiş teknoloji ikonları, yapay görsel üretimleri, uydurma ölçüler/ödüller, ağır filtre, grid/karo kolajı, yanlış kesilmiş yüz/araç, okunmayacak küçük yazı.

## Visual Identity
- Background: `#0b1012`
- Text: `#f0f0e9`
- Accent: `#75d5d0`
- Display font: Barlow (local font file)
- Body font: Inter Variable (local font file)
- Visual references: ana sayfa palette, gerçek hero görselleri, BTÜ ve MATRO'nun resmî beyaz logoları.

## Storyboard
1. Atölye — 3.7s — gerçek atölye fotoğrafı ve “Atölyede başlar.”
2. Hava — 2.6s — `galeri-ashina-hangar.jpg`, “Havada.”
3. Kara — 2.6s — `galeri-matrover-stand.jpg`, “Karada.”
4. Deniz — 2.6s — `galeri-lodos-saha.jpg`, “Denizde.”
5. Ekip — 5.0s — `mavi-vatan-ekipler.jpg`, “Sahada kanıtlanır.” ve gerçek ana sayfa açıklaması.
6. Davet — 5.0s — logolar ve gerçek CTA.

## Audio
- Role: sıcak, ritmik destek.
- Music: `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3` (brag skill'in yerel müzik paketi).
- Music treatment: ölçülü seviye; finalde hafif yükseliş ve son 0.7 saniyede yumuşak çıkış.
- Cue guidance: `assets/music/cues/happy-beats-business-moves-vol-1-by-ende-dot-app.music-cues.json`; approx. 120.19 BPM. Güçlü geçiş 16.02–17.02s, kapanış CTA 20.02s; diğer görsel kesmeleri yakındaki yarım saniyelik vuruşlardan seç.
- Audio-reactive: Mevcut fotoğraflara ölçülü, yavaş pan/zoom uygula; kontrastı sabit tut. Görselizer kullanma.
- Audio-coupled: açılıştaki görsel yerleşimi ve logoların finalde oturması.
- SFX guidance: iki yumuşak, düşük frekans riski taşıyan vurgu; ses dosyalarını animasyonla eşleştir.
- SFX analysis: `/Users/wildgenie/.agents/skills/brag/assets/sfx/sfx-analysis.md`
- Exact SFX choice: seçilen dosyaları `composition/assets/` içine kopyala ve ölçülü kullan.

## Hyperframes Instructions
Use Hyperframes-native composition and motion conventions. Show real local photos and the exact sourced copy above. Respect the storyboard, image aspect ratios, original logos and accessibility contrast. Run `npx hyperframes check` before the final preview. The final MP4 render waits for the user's approval in the preview.
