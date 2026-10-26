# Ekip YZ görselleri: yeniden üretme notu

Bu klasördeki görseller Gemini (`gemini-3-pro-image`, REST `generateContent`) ile üretildi. Siteye konmadı; seçim toplantıda yapılacak.

## Dosyalar

| Klasör | İçerik |
|---|---|
| `stil-ornekleri/<harf>-<slug>.jpg` | Baş-omuz portre. Harfler: a reels sahne, b reels pafta, c 3B animasyon, d vektör, e suluboya, f çizgi roman |
| `stil-ornekleri/tur1/` | Stil denemesinin ilk turu (3 kişi) |
| `referans-sayfasi/{gercek,a}-<slug>.jpg` | 6 baş + 4 tam boy referans sayfası (gerçekçi ve reels stili) |
| `elenen/` | Beğenilmeyen ya da yerine yenisi konan çıktılar; silinmedi |
| `*.istem.json` | Her görselin yanında: model, en-boy oranı, iki turun metinleri ve referans dosyalarının yolları |
| `referans_uret.py` | Güncel üretim betiği (tüm talimatlar içinde) |
| `stil_uret.py` | İlk 3 kişilik stil denemesinin betiği |

`.istem.json` dosyalarının çoğu üretimden sonra betikten yeniden kuruldu (dosyada `not` alanı var). Yeni üretimlerde betik bu kaydı çağrı anında yazar.

## Çalıştırma

Repo kökünden, anahtar ortamdan okunur (dosyaya ya da loga yazılmaz):

```bash
source ~/.zshrc >/dev/null 2>&1
python3 docs/ekip/yz/claude/referans_uret.py sayfa   # yöneticiler: gerçekçi + reels stili referans sayfası
python3 docs/ekip/yz/claude/referans_uret.py stil    # yöneticiler: 6 stil portre
```

Tek kişi ve tek stil:

```bash
python3 -c "import sys; sys.path.insert(0,'docs/ekip/yz/claude'); import referans_uret as r; print(r.portre('ela-ural','e'))"
```

## Talimat kuralları (betikte uygulanıyor)

- **Çok turlu sohbet:** 1. tur kişinin bütün fotoğrafları, model "OK" der, 2. tur stil isteği.
- **1. tur referansları:** `docs/ekip/orijinal/<slug>*` (kesilmemiş orijinaller, `-canva`, `-yuz-N` vb.), grup fotoğraflarında kişi metinle tarif edilir (`GRUP`), `alternatif/<slug>.jpg`, `yz/codex/kadraj/<slug>.jpg`, `yz/codex/gri-fon/<slug>.jpg` (yapay; çelişirse gerçek fotoğraf geçerli). Bilgehan için ek olarak `orijinal/bilgehan-zeki-ozaytac-referans-sayfasi.png` ana referans ve onaylı reels avatarı.
- **Yaş:** istemde sayı yok. "Fotoğraftaki yaşında tut, yaşlı gösterme, kırışık/kilo ekleme." Ataman için yalnız "30 altı". Bilgehan: sakal tamamen koyu, kır yok.
- **Kişi tarifleri:** `KISI` sözlüğü (yöneticiler elle), diğerleri yalnız ad + yaş kuralı; benzemeyenler için ek tarifler `EK` sözlüğünde.
- **Stil örnekleri:** aynı stilde başka kişilerin en çok 2 çizimi, "bunlar başka kişiler, yalnız tarzı al" uyarısıyla. Fazlası kimliği karıştırdı (Bilgehan yerine Irmak çizildi).
- **Stil referansları:** a için `gemini-prompt-arena/kaynak/avatar/morph_07_yakin_plan_mimik.jpg` ve sahne kareleri, b için `KARAKTER_KIMLIK_PAFTASI_v1.jpg`.
- **Kıyafet:** stüdyo portresindeki kıyafet. Aksesuarlar (gözlük, başörtüsü, sakal) fotoğraflardaki gibi.
- **Referans sayfası düzeni:** Bilgehan'ın kendi sayfası örnek alındı: üst sıra önden, 3/4, profil, ciddi, gülümseme, kahkaha; alt sıra tam boy önden, yandan, arkadan, eli cepte 3/4. Açık gri fon, yazı yok, 3:2.

## Kontrol

Benzerlik gri fona göre değil, gerçek fotoğraflara göre kontrol edilir: `docs/ekip/kontrol/suluboya-1.jpg` ve `-2.jpg` (site karesi, orijinal, gri fon, suluboya).
