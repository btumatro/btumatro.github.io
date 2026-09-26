# 8. Radyo paketi: jingle, yataklar ve tema

> MATRO Radyo'nun yayın formatı için (bkz. `docs/podcast/RADYO-YAYIN-PLANI.md`). Yatak ve
> tema parçaları sözsüz üretilmeli (**Instrumental** açık). Üretilen parçalar tam uzunlukta
> gelebilir; kesme ve döngü işini miks betiği yapar.

## 1. İstasyon jingle paketi

**Style of Music**
```
Radio station ident jingle pack, energetic electronic rock, punchy drums, bright synth risers and impacts, short vocoder and choir vocal hooks singing the station name, each ident 5 to 8 seconds long ending on a big final hit, several variations separated by short silences
```
**Exclude Styles**
```
long verses, spoken narration, meta text, sad, lo-fi, trap
```
**Sözler**
```
MATRO Radyo

MATRO Radyo

Atölyeden sahaya, MATRO Radyo

MATRO
```

## 2. DJ yatağı (sözsüz)

**Style of Music**
```
Upbeat electro funk instrumental bed for radio DJ talk, 108 BPM, groovy bassline, clean funky guitar chops, light claps and shakers, minimal melody so a voice can sit on top, steady energy without big drops or breaks, loop friendly, no vocals
```
**Exclude Styles**
```
vocals, singing, rap, choir, lead melody, big drops, dubstep, distortion, sad
```

## 3. Hikâye yatağı (sözsüz)

**Style of Music**
```
Cinematic ambient underscore for a storytelling podcast, 80 BPM, warm soft pads, gentle piano motif, light pulsing synth, very subtle workshop textures, hopeful and understated, no big drums, consistent level from start to end, no vocals
```
**Exclude Styles**
```
vocals, singing, choir, loud drums, epic trailer hits, sad, horror
```

## 4. Bülten yatağı (sözsüz)

**Style of Music**
```
News bulletin bed instrumental, 120 BPM, ticking hi-hat, pulsing synth bass, short bright stabs, urgent but friendly, sparse mid range so speech stays clear, loop friendly, no vocals
```
**Exclude Styles**
```
vocals, singing, choir, heavy guitars, dramatic trailer, sad
```

## 5. Tema müziği (intro/outro, sözsüz)

**Style of Music**
```
Podcast theme song, uplifting indie electronic, catchy synth hook, driving drums, bright plucks, builds quickly and resolves with a clean ending, instrumental, strong first 10 seconds
```
**Exclude Styles**
```
vocals, singing, rap, long intro, fade out ending, sad
```

## Notlar

- Jingle paketinde model istasyon adını yanlış telaffuz ederse ("Matro" yerine "Metro"
  gibi), yalnızca doğru okunan kısımlar kesilir.
- Parçaları `~/Downloads`'a bırakın; kesme, döngü ve miks betikle yapılır.

## Üretim sonucu

| Bölüm | Üretilen dosya | Kullanım |
|---|---|---|
| §1 Jingle paketi | `ses/08-matro-radyo-jingle.mp4` (Saha Bizim, 0:55) | Açılış 0–14,2 sn, kapanış 45,8–53,4 sn |
| §2 DJ yatağı | `ses/09-dj-yatagi-the-hourly-brief.mp4` | DJ bağlantıları |
| §3 Hikâye yatağı | `ses/10-hikaye-yatagi-a-measure-of-intent.mp4` | Hikâye bölümleri |
| §4 Bülten yatağı | `ses/11-bulten-yatagi-unfolding-blueprints.mp4` | Bülten |
| §5 Tema müziği | Üretilmedi | Yerine hikâye yatağının girişi kullanılıyor |
| (ek) | `ses/12-gece-yatagi-the-midnight-invention.mp4` | "Atölyede gece" bağlantısı |

Dosyalar ada göre değil sese göre eşleştirildi (tempo, tiz enerji ve spektrogram
karşılaştırması). Jingle model tarafından tek parça üretildi, ayrı kimlikler hâlinde
değil; kesitler dalga biçimi ve altyazı zamanlarına göre seçildi.

## Sıradaki müzik ihtiyaçları

- **Tema müziği (§5):** Hikâye kuşağının açılış ve kapanışı için hâlâ gerekli.
- **İkinci DJ yatağı:** Tek yatak 8 bağlantıda tekrar ediyor; farklı tempoda ikinci bir
  sözsüz yatak (ör. 96 BPM chill-funk) çeşitlilik sağlar.
